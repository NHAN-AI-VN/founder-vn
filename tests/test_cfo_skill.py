"""founder-cfo: the skill text and the sources it relies on (design §3, issue #12)."""

import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-cfo" / "SKILL.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _protocol_block() -> str:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    block = conventions.split("````markdown\n", 1)[1].split("````", 1)[0]
    return block.strip()


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    assert _protocol_block() in _skill()


def test_frontmatter_names_the_skill_and_carries_vietnamese_triggers() -> None:
    head = _skill().split("---", 2)[1]
    assert "name: founder-cfo" in head
    assert "license: MIT" in head
    assert "kinh tế đơn vị" in head


def test_asks_for_costs_in_the_owner_terms() -> None:
    text = _skill()
    for term in (
        "nguyên liệu",
        "bao bì",
        "phí app giao hàng",
        "thuê mặt bằng",
        "lương",
        "điện nước",
    ):
        assert term in text, term


def test_looks_up_the_two_legal_figures_in_the_ledger_and_never_guesses() -> None:
    text = _skill()
    assert "permits/sources.md" in text
    assert "tax_rate_on_revenue" in text and "tax_free_threshold" in text
    assert "official link" in text and "verification date" in text
    assert "never from memory" in text


def test_calls_the_tool_on_either_transport() -> None:
    text = _skill()
    assert "cfo_analyse" in text
    assert "founder-vn cfo" in text
    assert "--out cfo.md" in text


def test_reads_flags_back_in_plain_vietnamese_and_never_computes() -> None:
    text = _skill()
    assert "plain Vietnamese" in text
    assert "flags" in text
    assert "Never compute" in text


def test_states_the_two_tax_model_limits_and_the_temporary_relief_line() -> None:
    text = _skill()
    assert "20 triệu đồng" in text
    assert "3 tỷ đồng" in text
    assert "17%" in text
    assert "có ưu đãi tạm thời, chưa tính" in text


def test_ends_with_the_disclaimer() -> None:
    assert "không phải tư vấn tài chính hay thuế" in _skill()


def test_no_dollar_sign_next_to_a_number() -> None:
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
    assert (project_root / ".kiro/skills/founder-cfo/SKILL.md").is_file()
