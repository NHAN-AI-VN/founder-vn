"""Tests of the fan-out in `founder_vn.panel`: brief, prompt hash, answer extraction, jobs."""

import json
import re
import shutil
from pathlib import Path

import pytest
from conftest import FakeProvider

from founder_vn import panel

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def dealt(project_root: Path) -> Path:
    """A project with seed-7, n=7 cards dealt from the synthetic customer and pitch."""
    root = project_root / "founder"
    root.mkdir()
    shutil.copy(FIXTURES / "panel_customer.json", root / "customer.json")
    shutil.copy(FIXTURES / "panel_pitch.md", root / "pitch.md")
    panel.init(project_root, "customer.json", "pitch.md", 7, 7)
    return project_root


def _cards(project: Path) -> list[dict]:
    return json.loads((project / "founder/panel/personas.json").read_text(encoding="utf-8"))


def test_brief_is_vietnamese_and_carries_persona_pitch_and_answer_shape(dealt: Path) -> None:
    card = _cards(dealt)[0]
    pitch = (dealt / "founder/pitch.md").read_text(encoding="utf-8").strip()
    text = panel.brief(card, pitch)
    assert card["id"] in text
    assert card["name"] in text
    assert card["objection"] in text
    assert pitch in text
    assert "Bạn là" in text
    assert "reason_code" in text and "buys" in text
    assert "$" not in text


def test_prompt_hash_covers_template_personas_and_pitch(
    dealt: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    cards = _cards(dealt)
    base = panel.prompt_hash(cards, "bán cà phê")
    assert base == panel.prompt_hash(cards, "bán cà phê")
    assert len(base) == 64
    assert base != panel.prompt_hash(cards, "bán trà")
    assert base != panel.prompt_hash(cards[:-1], "bán cà phê")
    monkeypatch.setattr(panel, "BRIEF_TEMPLATE", panel.BRIEF_TEMPLATE + " ")
    assert base != panel.prompt_hash(cards, "bán cà phê")


VALID = {"id": "P001", "buys": True, "reason_code": "need", "reason": "Cần ly cà phê buổi sáng."}


def test_extract_takes_the_first_json_object_in_prose() -> None:
    reply = "Dạ, câu trả lời của tôi:\n" + json.dumps(VALID, ensure_ascii=False) + "\nCảm ơn {anh}."
    assert panel.extract_answer(reply, "P001") == (VALID, None)


def test_extract_reports_the_problem_instead_of_guessing() -> None:
    assert panel.extract_answer("không có gì", "P001") == (None, "không có đối tượng JSON")
    answer, problem = panel.extract_answer('{"id": "P001", "buys": tr', "P001")
    assert answer is None and problem is not None and "không đọc được" in problem
    answer, problem = panel.extract_answer(json.dumps({**VALID, "id": "P002"}), "P001")
    assert answer is None and problem == "id là 'P002', cần P001"


def _setenv(monkeypatch: pytest.MonkeyPatch, provider: FakeProvider) -> None:
    monkeypatch.setenv("FOUNDER_LLM_BASE_URL", provider.base_url)
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "khoa-gia")
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")


def _buyer(body: dict) -> str:
    """The buyer id the brief in a request is addressed to."""
    match = re.search(r'"id": "(P\d+)"', body["messages"][0]["content"])
    assert match
    return match.group(1)


def _answer(pid: str, buys: bool = True) -> str:
    return json.dumps(
        {"id": pid, "buys": buys, "reason_code": "need", "reason": f"{pid} nói vậy."},
        ensure_ascii=False,
    )


def _status(project: Path, job_id: str) -> dict:
    return json.loads(panel.job_status(project, job_id))


def _start(project: Path) -> str:
    """Start a job without launching a worker; return its id."""
    return json.loads(panel.start_job(project, lambda project, job_id: None))["job_id"]


def test_start_job_unconfigured_is_an_error_with_setup_and_writes_no_job(
    dealt: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("FOUNDER_LLM_BASE_URL", "FOUNDER_LLM_API_KEY", "FOUNDER_LLM_MODEL"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(panel.PanelError, match="FOUNDER_LLM_BASE_URL"):
        _start(dealt)
    assert not (dealt / "founder/panel/jobs").exists()


def test_job_lifecycle_answers_land_and_model_and_hash_reach_results(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, _answer(_buyer(body)), 0.0)
    launched: list[str] = []
    started = json.loads(panel.start_job(dealt, lambda project, job_id: launched.append(job_id)))
    job_id = started["job_id"]
    assert launched == [job_id]
    assert started == {"job_id": job_id, "state": "running", "buyers": 7}
    assert _status(dealt, job_id) == {
        "job_id": job_id,
        "state": "running",
        "total": 7,
        "done": 0,
        "pending": 7,
        "failed": 0,
        "excluded": 0,
        "last_error": None,
    }
    panel.execute(dealt, job_id)
    status = _status(dealt, job_id)
    assert (status["state"], status["done"], status["pending"]) == ("done", 7, 0)
    for card in _cards(dealt):
        written = json.loads(
            (dealt / f"founder/panel/answers/{card['id']}.json").read_text(encoding="utf-8")
        )
        assert written["reason"] == f"{card['id']} nói vậy."
    meta = json.loads((dealt / "founder/panel/panel.json").read_text(encoding="utf-8"))
    pitch = meta["pitch"]
    assert meta["mode"] == "model" and meta["model"] == "mo-hinh-gia"
    assert meta["prompt_hash"] == panel.prompt_hash(_cards(dealt), pitch)
    assert sorted(_buyer(r) for r in fake_provider.requests) == [c["id"] for c in _cards(dealt)]
    panel.run_tally(dealt)
    results = json.loads((dealt / "founder/panel/results.json").read_text(encoding="utf-8"))
    assert (results["mode"], results["model"]) == ("model", "mo-hinh-gia")
    assert results["prompt_hash"] == meta["prompt_hash"]
    assert results["answered"] == 7


def test_job_status_refuses_an_unknown_or_malformed_job_id(dealt: Path) -> None:
    with pytest.raises(panel.PanelError, match="job"):
        panel.job_status(dealt, "../panel")
    with pytest.raises(panel.PanelError, match="J-00000000"):
        panel.job_status(dealt, "J-00000000")


def _answer_file(project: Path, pid: str) -> Path:
    return project / f"founder/panel/answers/{pid}.json"


def _run(project: Path, **kwargs: float) -> dict:
    job_id = _start(project)
    panel.execute(project, job_id, **kwargs)
    return _status(project, job_id)


def test_prose_wrapped_json_is_filed(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (
        200,
        f"Dạ em xin trả lời:\n{_answer(_buyer(body))}\nChúc anh/chị bán đắt.",
        0.0,
    )
    status = _run(dealt)
    assert (status["done"], status["excluded"], status["failed"]) == (7, 0, 0)


def test_buyer_invalid_twice_is_excluded_and_nothing_is_written_for_them(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def script(body: dict, n: int) -> tuple[int, str, float]:
        pid = _buyer(body)
        return 200, ("không phải JSON" if pid == "P003" else _answer(pid)), 0.0

    fake_provider.script = script
    status = _run(dealt)
    assert (status["done"], status["excluded"], status["failed"], status["pending"]) == (6, 1, 0, 0)
    assert status["state"] == "done"
    assert status["last_error"] is not None and status["last_error"].startswith("P003")
    assert not _answer_file(dealt, "P003").exists()
    assert [_buyer(r) for r in fake_provider.requests].count("P003") == 2
    panel.run_tally(dealt)
    results = json.loads((dealt / "founder/panel/results.json").read_text(encoding="utf-8"))
    assert results["excluded"] == 1 and results["excluded_buyers"][0]["id"] == "P003"


def test_buyer_invalid_once_then_valid_is_kept(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    seen: list[str] = []

    def script(body: dict, n: int) -> tuple[int, str, float]:
        pid = _buyer(body)
        first = pid == "P002" and pid not in seen
        seen.append(pid)
        return 200, ("{hỏng" if first else _answer(pid)), 0.0

    fake_provider.script = script
    status = _run(dealt)
    assert (status["done"], status["excluded"]) == (7, 0)


def test_5xx_is_retried_with_backoff_then_succeeds(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    failures: dict[str, int] = {}

    def script(body: dict, n: int) -> tuple[int, str, float]:
        pid = _buyer(body)
        if pid == "P004" and failures.get(pid, 0) < 2:
            failures[pid] = failures.get(pid, 0) + 1
            return 503, "", 0.0
        return 200, _answer(pid), 0.0

    fake_provider.script = script
    slept: list[float] = []
    monkeypatch.setattr(panel.time, "sleep", slept.append)
    status = _run(dealt)
    assert (status["done"], status["failed"]) == (7, 0)
    assert [_buyer(r) for r in fake_provider.requests].count("P004") == 3
    assert [s for s in slept if s >= 1] == [panel.BACKOFF, panel.BACKOFF * 2]


def test_5xx_for_good_is_failed_with_the_last_error_and_no_answer(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def script(body: dict, n: int) -> tuple[int, str, float]:
        pid = _buyer(body)
        return (500, "", 0.0) if pid == "P005" else (200, _answer(pid), 0.0)

    fake_provider.script = script
    status = _run(dealt, backoff=0.0)
    assert (status["done"], status["failed"], status["excluded"]) == (6, 1, 0)
    assert status["last_error"] == "P005: máy chủ mô hình trả mã 500"
    assert not _answer_file(dealt, "P005").exists()
    assert [_buyer(r) for r in fake_provider.requests].count("P005") == panel.ATTEMPTS


def test_timeout_is_a_failed_buyer_not_a_hang(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def script(body: dict, n: int) -> tuple[int, str, float]:
        pid = _buyer(body)
        return (200, _answer(pid), 0.6 if pid == "P001" else 0.0)

    fake_provider.script = script
    status = _run(dealt, timeout=0.2, backoff=0.0)
    assert (status["done"], status["failed"]) == (6, 1)
    assert status["last_error"] == "P001: quá thời gian chờ 0.2 giây"
    assert not _answer_file(dealt, "P001").exists()


def test_rerun_asks_only_buyers_with_a_missing_or_invalid_answer(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, _answer(_buyer(body)), 0.0)
    _run(dealt)
    _answer_file(dealt, "P002").unlink()
    _answer_file(dealt, "P006").write_text('{"id": "P006"}', encoding="utf-8")
    fake_provider.requests.clear()
    status = _run(dealt)
    assert sorted(_buyer(r) for r in fake_provider.requests) == ["P002", "P006"]
    assert (status["total"], status["done"]) == (2, 2)
    fake_provider.requests.clear()
    assert json.loads(panel.start_job(dealt, lambda p, j: None))["buyers"] == 0
    assert fake_provider.requests == []


def test_buyers_are_asked_in_waves_of_ten_concurrent_calls(
    project_root: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    root = project_root / "founder"
    root.mkdir()
    shutil.copy(FIXTURES / "panel_customer.json", root / "customer.json")
    shutil.copy(FIXTURES / "panel_pitch.md", root / "pitch.md")
    panel.init(project_root, "customer.json", "pitch.md", 25, 7)
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, _answer(_buyer(body)), 0.15)
    status = _run(project_root)
    assert (status["total"], status["done"]) == (25, 25)
    assert fake_provider.max_active == panel.WAVE == 10


def test_a_worker_crash_is_written_into_the_job(
    dealt: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    job_id = _start(dealt)

    def boom(project: Path, job_id: str) -> None:
        raise RuntimeError("hỏng giữa chừng")

    monkeypatch.setattr(panel, "execute", boom)
    panel.work(dealt, job_id)
    status = _status(dealt, job_id)
    assert status["state"] == "error"
    assert status["last_error"] == "RuntimeError: hỏng giữa chừng"
