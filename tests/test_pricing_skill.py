"""founder-pricing: the skill text (design §3, issue #17)."""

import json
import re
import subprocess
import sys
from pathlib import Path

from founder_vn import cfo, install, pricing
from founder_vn.vnd import format_vnd

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


EXAMPLE = ROOT / "examples" / "barbershop"
GOLDEN = EXAMPLE / "founder" / "pricing.md"


def _tool(source: str = "pricing_input.json") -> dict:
    return json.loads(pricing.run(EXAMPLE, source, as_json=True))


def test_golden_pricing_md_has_the_five_sections_in_order() -> None:
    text = GOLDEN.read_text(encoding="utf-8")
    heads = re.findall(r"^## (.+)$", text, flags=re.M)
    assert heads[:5] == [
        "Khoảng giá chấp nhận được",
        "Giá đề xuất",
        "Bậc giá",
        "Ưu đãi mở đầu để thử",
        "Theo dõi sau khi mở bán",
    ]


def test_golden_figures_are_the_tool_output() -> None:
    text = GOLDEN.read_text(encoding="utf-8")
    a = _tool()
    for key in ("pmc", "ipp", "pme"):
        assert format_vnd(a["points"][key]) in text, key
    for value in a["medians"].values():
        assert format_vnd(value) in text, value
    assert a["answers"] == {"valid": 20, "dropped": 0}
    assert a["warnings"] == []
    assert "thin_data" not in text and "Dữ liệu mỏng" not in text


def test_golden_uses_only_competitor_prices_from_competitors_md() -> None:
    comp = (GOLDEN.parent / "competitors.md").read_text(encoding="utf-8")
    spec = json.loads((GOLDEN.parent / "pricing_input.json").read_text(encoding="utf-8"))
    for price in spec["competitor_prices"]:
        assert format_vnd(price) in comp, price
    text = GOLDEN.read_text(encoding="utf-8")
    inside = _tool()["competitors"]["prices"]
    assert f"{len(inside)}" in text
    assert "Le Barbier de Saigon" in text and "chưa có số liệu" in text


def test_golden_flags_every_price_below_the_cfo_break_even() -> None:
    text = GOLDEN.read_text(encoding="utf-8")
    numbers = "numbers.json"
    plan_per_day = json.loads((GOLDEN.parent / numbers).read_text(encoding="utf-8"))["plan_per_day"]
    below = []
    for price in (199000, 279000, 389000):
        out = json.loads(cfo.run(EXAMPLE, numbers, price=str(price), as_json=True))
        assert format_vnd(price) in text
        if out["margin_at_plan"] <= 0 or out["breakeven_per_day"] > plan_per_day:
            below.append(price)
            assert format_vnd(price) + ": thấp hơn mức hòa vốn của CFO" in text
    assert below == [199000]
    assert text.count("thấp hơn mức hòa vốn của CFO") == len(below)


def test_golden_caveat_once_disclaimer_and_vietnamese() -> None:
    text = GOLDEN.read_text(encoding="utf-8")
    assert text.count("mô phỏng, cận trên, không phải khách hàng thật") == 1
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text
    assert "anh/chị" in text
    assert not DOLLAR.search(text)
