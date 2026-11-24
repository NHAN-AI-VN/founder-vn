"""Tests of `founder_vn.board`: lens prompts, memo shape, the job on the shared runner."""

import json
import re
from pathlib import Path

import pytest
from conftest import FakeProvider

from founder_vn import board, panel

BRIEF = "# Brief\n\nTiệm cắt tóc nam, 4 ghế, giá trọn gói 199.000 đ, Quận 7 cũ.\n"
LENSES = ("offers", "product", "systems")


@pytest.fixture
def briefed(project_root: Path) -> Path:
    """A project with a standalone brief at founder/board/brief.md."""
    target = project_root / "founder/board/brief.md"
    target.parent.mkdir(parents=True)
    target.write_text(BRIEF, encoding="utf-8")
    return project_root


def _setenv(monkeypatch: pytest.MonkeyPatch, provider: FakeProvider) -> None:
    monkeypatch.setenv("FOUNDER_LLM_BASE_URL", provider.base_url)
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "khoa-gia")
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")


def _lens(body: dict) -> str:
    match = re.search(r"Mã lens: (\w+)", body["messages"][0]["content"])
    assert match
    return match.group(1)


def _memo(lens: str, **changes: object) -> str:
    memo = {
        "score": 7,
        "vote": "conditional",
        "strong": [f"{lens}: lời hứa rõ ràng"],
        "would_kill": [f"{lens}: vốn lưu động mỏng"],
        "questions": [f"{lens}: ai là khách lặp lại?"],
        "conditions": [f"{lens}: chốt giá thuê dưới 15% doanh thu"],
    }
    return json.dumps(memo | changes, ensure_ascii=False)


def _status(project: Path, job_id: str) -> dict:
    return json.loads(panel.job_status(project, job_id))


def _start(project: Path) -> str:
    return json.loads(board.start_job(project, lambda project, job_id: None))["job_id"]


def _read_memo(project: Path, lens: str) -> str:
    return (project / f"founder/board/{lens}.md").read_text(encoding="utf-8")


def test_start_without_a_brief_names_the_file_and_writes_no_job(
    project_root: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    with pytest.raises(board.BoardError, match=r"board/brief\.md"):
        _start(project_root)
    assert not (project_root / "founder/board/jobs").exists()


def test_start_unconfigured_is_an_error_with_setup_and_writes_no_job(
    briefed: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    for name in ("FOUNDER_LLM_BASE_URL", "FOUNDER_LLM_API_KEY", "FOUNDER_LLM_MODEL"):
        monkeypatch.delenv(name, raising=False)
    with pytest.raises(board.BoardError, match="FOUNDER_LLM_BASE_URL"):
        _start(briefed)
    assert not (briefed / "founder/board/jobs").exists()


def test_job_lifecycle_three_independent_memos_model_and_hash_recorded(
    briefed: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, _memo(_lens(body)), 0.0)
    launched: list[str] = []
    started = json.loads(board.start_job(briefed, lambda project, job_id: launched.append(job_id)))
    job_id = started["job_id"]
    assert launched == [job_id]
    assert started == {"job_id": job_id, "state": "running", "lenses": 3}
    assert _status(briefed, job_id) == {
        "job_id": job_id,
        "state": "running",
        "total": 3,
        "done": 0,
        "pending": 3,
        "failed": 0,
        "excluded": 0,
        "last_error": None,
    }
    board.execute(briefed, job_id)
    status = _status(briefed, job_id)
    assert (status["state"], status["done"], status["pending"]) == ("done", 3, 0)
    # three independent completions: one request per lens, each with only its own lens text
    assert sorted(_lens(r) for r in fake_provider.requests) == sorted(LENSES)
    for request in fake_provider.requests:
        prompt = request["messages"][0]["content"]
        assert len(request["messages"]) == 1
        assert BRIEF.strip() in prompt
        for other in set(LENSES) - {_lens(request)}:
            assert f"Mã lens: {other}" not in prompt
        assert "$" not in prompt
    meta = json.loads((briefed / "founder/board/board.json").read_text(encoding="utf-8"))
    assert meta["mode"] == "model" and meta["model"] == "mo-hinh-gia"
    assert meta["prompt_hash"] == board.prompt_hash(BRIEF.strip())
    assert len(meta["prompt_hash"]) == 64


def test_memo_has_the_fixed_vietnamese_shape(
    briefed: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, _memo(_lens(body)), 0.0)
    board.execute(briefed, _start(briefed))
    text = _read_memo(briefed, "offers")
    order = [
        "# Lens Offers",
        "**Điểm: 7/10**",
        "**Phiếu: làm có điều kiện**",
        "## Điểm mạnh",
        "## Điều có thể giết ý tưởng này",
        "## Câu hỏi còn mở",
        "## Điều kiện",
    ]
    positions = [text.index(h) for h in order]
    assert positions == sorted(positions)
    assert "- offers: lời hứa rõ ràng" in text
    assert "- offers: chốt giá thuê dưới 15% doanh thu" in text
    assert "mô phỏng" in text and "không nói thay tác giả" in text
    assert "$" not in text
    stored = json.loads((briefed / "founder/board/offers.json").read_text(encoding="utf-8"))
    assert stored["score"] == 7 and stored["vote"] == "conditional"


def test_each_lens_prompt_carries_its_framework_and_the_never_speak_as_the_author_rule() -> None:
    assert set(board.LENSES) == set(LENSES)
    assert "100M Offers" in board.LENSES["offers"]["source"]
    assert "Isaacson" in board.LENSES["product"]["source"]
    assert "E-Myth" in board.LENSES["systems"]["source"]
    for lens in LENSES:
        prompt = board.prompt(lens, BRIEF.strip())
        assert board.LENSES[lens]["source"] in prompt
        assert "không bao giờ nói thay tác giả" in prompt
        assert "tiếng Việt" in prompt
        assert "anh/chị" in prompt


def test_prose_wrapped_json_is_filed(
    briefed: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, f"Dạ:\n{_memo(_lens(body))}\nXong.", 0.0)
    job_id = _start(briefed)
    board.execute(briefed, job_id)
    assert _status(briefed, job_id)["done"] == 3


def test_a_lens_invalid_twice_is_excluded_and_nothing_is_written_for_it(
    briefed: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def script(body: dict, n: int) -> tuple[int, str, float]:
        lens = _lens(body)
        return 200, (_memo(lens, vote="maybe") if lens == "product" else _memo(lens)), 0.0

    fake_provider.script = script
    job_id = _start(briefed)
    board.execute(briefed, job_id)
    status = _status(briefed, job_id)
    assert (status["done"], status["excluded"], status["failed"], status["pending"]) == (2, 1, 0, 0)
    assert status["state"] == "done"
    assert status["last_error"] is not None and status["last_error"].startswith("product")
    assert not (briefed / "founder/board/product.md").exists()
    assert not (briefed / "founder/board/product.json").exists()
    assert [_lens(r) for r in fake_provider.requests].count("product") == 2


def test_a_call_that_keeps_failing_is_failed_after_three_attempts_and_rerun_resumes(
    briefed: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def broken(body: dict, n: int) -> tuple[int, str, float]:
        lens = _lens(body)
        return (500, "", 0.0) if lens == "systems" else (200, _memo(lens), 0.0)

    fake_provider.script = broken
    job_id = _start(briefed)
    board.execute(briefed, job_id, backoff=0.0)
    status = _status(briefed, job_id)
    assert (status["done"], status["failed"], status["state"]) == (2, 1, "done")
    assert "systems" in status["last_error"]
    assert [_lens(r) for r in fake_provider.requests].count("systems") == board.ATTEMPTS
    # a second run asks only the lens without a valid memo
    fake_provider.requests.clear()
    fake_provider.script = lambda body, n: (200, _memo(_lens(body)), 0.0)
    second = json.loads(board.start_job(briefed, lambda project, job_id: None))
    assert second["lenses"] == 1
    board.execute(briefed, second["job_id"])
    assert [_lens(r) for r in fake_provider.requests] == ["systems"]
    assert _status(briefed, second["job_id"])["done"] == 1


def test_memo_problem_names_the_first_offending_field() -> None:
    good = json.loads(_memo("offers"))
    assert board.memo_problem(good) is None
    assert "score" in (board.memo_problem({**good, "score": 11}) or "")
    assert "score" in (board.memo_problem({**good, "score": True}) or "")
    assert "vote" in (board.memo_problem({**good, "vote": "maybe"}) or "")
    assert "strong" in (board.memo_problem({**good, "strong": []}) or "")
    assert "conditions" in (board.memo_problem({**good, "conditions": "một"}) or "")
    assert "questions" in (
        board.memo_problem({k: v for k, v in good.items() if k != "questions"}) or ""
    )


def test_work_writes_a_crash_into_the_job(
    briefed: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)
    job_id = _start(briefed)
    monkeypatch.delenv("FOUNDER_LLM_MODEL")
    board.work(briefed, job_id)
    status = _status(briefed, job_id)
    assert status["state"] == "error" and "FOUNDER_LLM_MODEL" in status["last_error"]
