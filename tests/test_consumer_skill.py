"""founder-consumer: the skill text and its golden case (design §3, issue #16)."""

import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-consumer" / "SKILL.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_customer_json_is_shown_to_the_owner_before_dealing() -> None:
    text = _skill()
    assert "customer.json" in text
    for field in ("segments", "behaviours", "objections", "habits", "monthly VND income"):
        assert field in text, field
    assert "before dealing" in text
    assert "Do not call `panel_init` until the Owner has confirmed" in text
    assert "competitors.md" in text and "If `founder/competitors.md` exists" in text
    assert "guess" in text


def test_pitch_rules() -> None:
    text = _skill()
    assert "pitch.md" in text
    assert "three to six" in text
    assert "superlative" in text
    assert "cannot deliver" in text


def test_panel_size_and_tool_order() -> None:
    text = _skill()
    assert "`n = 20`" in text
    assert "Use 100 only when the Owner asks" in text
    assert "cost and time" in text
    order = [text.index(t) for t in ("panel_init", "panel_run", "job_status", "panel_tally")]
    assert order == sorted(order)
    assert "Poll" in text


def test_never_answers_for_a_buyer_and_reports_excluded() -> None:
    text = _skill()
    assert "Never answer for a buyer" in text
    assert "excluded" in text
    assert "do not write an answer yourself" in text


def test_five_point_read_back_and_caveat_once() -> None:
    text = _skill()
    for needle in (
        "Headline",
        "differ most",
        "Top three reasons",
        "one quote each",
        "What would flip a no",
        "one sentence",
    ):
        assert needle in text, needle
    assert "mô phỏng, cận trên, không phải khách hàng thật" in text
    assert "once" in text


def test_names_carry_no_gender_so_segments_name_it() -> None:
    text = _skill()
    assert "gender" in text
    assert "segment name" in text


def test_no_dollar_next_to_a_digit() -> None:
    assert not DOLLAR.search(_skill())


def test_skill_lint_passes_on_the_repo() -> None:
    done = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "skill_lint.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert done.returncode == 0, done.stdout + done.stderr


def test_installer_ships_the_skill(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=ROOT / "skills")
    assert (project_root / ".kiro/skills/founder-consumer/SKILL.md").is_file()
