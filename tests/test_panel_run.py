"""Tests of the fan-out in `founder_vn.panel`: brief, prompt hash, answer extraction, jobs."""

import json
import shutil
from pathlib import Path

import pytest

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
