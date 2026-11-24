"""Wave A example completeness and the review checklist walk (docs/review-checklist.md, issue #18)."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
FOUNDER = ROOT / "examples" / "barbershop" / "founder"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
ENGLISH = re.compile(
    r"\b(the|and|is|are|with|for|that|this|from|your|you|will|can|should|which|but)\b"
)
LEGAL = re.compile(r"Luật|Nghị định|thuế suất")
DATE = re.compile(r"\d{2}/\d{2}/\d{4}")
REPORTS = ("cfo.md", "pricing.md", "summary.md", "business-plan.md")
CAVEAT_PARTS = ("mô phỏng", "cận trên", "không phải khách hàng thật")
WAVE_A_FILES = (
    "idea.md",
    "board.md",
    "competitors.md",
    "customer.json",
    "pitch.md",
    "consumer.md",
    "panel/results.md",
    "pricing.md",
    "numbers.json",
    "cfo.md",
    "summary.md",
    "business-plan.md",
)


def _markdown() -> list[Path]:
    return sorted(FOUNDER.rglob("*.md"))


def test_example_holds_every_wave_a_artifact() -> None:
    for name in WAVE_A_FILES:
        assert (FOUNDER / name).is_file(), name


def test_readme_references_the_complete_wave_a_example() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "examples/barbershop/founder/" in text
    assert "business-plan.md" in text and "summary.md" in text
    assert "`founder-plan`" in text


def test_no_dollar_in_any_example_or_skill_text() -> None:
    paths = _markdown() + sorted((ROOT / "skills").glob("*/SKILL.md"))
    for path in paths:
        assert not DOLLAR.search(path.read_text(encoding="utf-8")), path


def test_no_english_leaks_into_owner_facing_text() -> None:
    for path in _markdown():
        for line in path.read_text(encoding="utf-8").splitlines():
            if "http" in line:
                continue
            assert not ENGLISH.search(line), (path.name, line[:100])


def test_every_legal_claim_file_carries_an_official_link_and_a_date() -> None:
    legal = [p for p in _markdown() if LEGAL.search(p.read_text(encoding="utf-8"))]
    assert {p.name for p in legal} >= {"cfo.md", "summary.md", "business-plan.md"}
    for path in legal:
        text = path.read_text(encoding="utf-8")
        assert "https://congbao.chinhphu.vn/" in text, path
        assert DATE.search(text), path


def test_every_report_carries_the_disclaimer() -> None:
    for name in REPORTS:
        assert "không phải tư vấn" in (FOUNDER / name).read_text(encoding="utf-8"), name


def test_every_file_showing_a_panel_result_carries_the_caveat() -> None:
    shown = ("panel/results.md", "consumer.md", "pricing.md", "summary.md", "business-plan.md")
    for name in shown:
        text = (FOUNDER / name).read_text(encoding="utf-8")
        for part in CAVEAT_PARTS:
            assert part in text, (name, part)
    assert "mô phỏng, cận trên, không phải khách hàng thật" in (FOUNDER / "summary.md").read_text(
        encoding="utf-8"
    )
