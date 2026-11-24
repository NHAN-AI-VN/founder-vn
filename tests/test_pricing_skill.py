"""founder-pricing: the skill text (design §3, issue #17)."""

import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-pricing" / "SKILL.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_calls_the_pricing_tool_on_the_panels_four_price_answers() -> None:
    text = _skill()
    assert "`pricing_psm`" in text
    assert "founder-vn pricing" in text
    assert "founder/panel/pricing_input.json" in text
    for key in ("too_cheap", "bargain", "getting_expensive", "too_expensive"):
        assert key in text, key
    assert "Never compute a number yourself" in text


def test_cross_checks_competitors_and_cfo() -> None:
    text = _skill()
    assert "founder/competitors.md" in text and "competitor_prices" in text
    assert "founder/cfo.md" in text and "founder/numbers.json" in text
    assert "founder-vn cfo" in text and "--price" in text
    assert "chưa có số liệu" in text


def test_flags_a_price_below_the_cfo_break_even() -> None:
    text = _skill()
    assert "break-even" in text
    assert "margin_at_plan" in text and "breakeven_per_day" in text
    assert "below the CFO break-even" in text
    assert "Never hide" in text


def test_pricing_md_contract() -> None:
    text = _skill()
    assert "founder/pricing.md" in text
    for section in (
        "Khoảng giá chấp nhận được",
        "Giá đề xuất",
        "Bậc giá",
        "Ưu đãi mở đầu để thử",
        "Theo dõi sau khi mở bán",
    ):
        assert section in text, section
    for rung in ("good", "better", "best"):
        assert rung in text, rung


def test_no_fabricated_anchors_and_thin_data_passed_through() -> None:
    text = _skill()
    assert "No fabricated anchors" in text
    assert "thin_data" in text and "Dữ liệu mỏng" in text
    assert "mô phỏng, cận trên, không phải khách hàng thật" in text
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text
    assert "anh/chị" in text


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
    assert (project_root / ".kiro/skills/founder-pricing/SKILL.md").is_file()
