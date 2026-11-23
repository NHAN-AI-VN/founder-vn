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
