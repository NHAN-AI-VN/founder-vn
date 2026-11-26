"""founder-launch: the skill text (design §3, issue #116)."""

import re
from pathlib import Path

from founder_vn import __version__

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-launch" / "SKILL.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")

HEADINGS = (
    "## 1. Thử nghiệm thật trước",
    "## 2. Đếm ngược",
    "## 3. Run sheet ngày khai trương",
    "## 4. 30 ngày đầu",
    "## 5. Người mua thật ghi đè panel",
    "## 6. Lưu ý",
)


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _protocol_block() -> str:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    return conventions.split("````markdown\n", 1)[1].split("````", 1)[0].strip()


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    assert _protocol_block() in _skill()
    assert _skill().count("## Protocol") == 1


def test_frontmatter_matches_the_lint_and_the_package_version() -> None:
    head = _skill().split("---", 2)[1]
    assert "name: founder-launch" in head
    assert "license: MIT" in head
    for trigger in ("khai trương thế nào", "khi nào mở được", "bán trước", "danh sách chờ"):
        assert trigger in head, trigger
    assert f'version: "{__version__}"' in head


def test_output_is_the_six_part_structure_in_order() -> None:
    text = _skill()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)


def test_real_test_is_one_of_three_at_the_listed_price_with_an_owner_chosen_stop_rule() -> None:
    text = _skill()
    for needle in ("pre-sale", "waitlist with a deposit", "pop-up", "exactly one test"):
        assert needle in text, needle
    assert "listed price" in text and "not a discount" in text
    assert "idea.md" in text and "pricing.md" in text
    assert "fewer than N real buyers in M days" in text
    assert "anh/chị chọn" in text
    assert "never invent N or M" in text


def test_countdown_runs_d_minus_30_to_d_0_with_owner_role_and_dependency() -> None:
    text = _skill()
    assert "D-30" in text and "D-0" in text
    for needle in ("permits.md", "ops.md", "marketing.md", "a role that exists in `ops.md`"):
        assert needle in text, needle


def test_run_sheet_is_hour_by_hour_with_an_owner_per_line() -> None:
    text = _skill()
    assert "hour by hour" in text
    assert "one owner per line" in text


def test_first_thirty_days_measure_the_three_sources_and_say_what_to_change() -> None:
    text = _skill()
    for needle in ("stop conditions", "break-even", "cfo.md", "metrics of `marketing.md`"):
        assert needle in text, needle
    assert "what to change" in text


def test_real_buyers_override_the_panel_with_the_caveat() -> None:
    text = _skill()
    assert "Real buyers override the panel" in text
    assert "chưa có" in text
    assert "Panel là mô phỏng, cận trên, không phải khách hàng thật" in text


def test_never_writes_a_date_a_real_buyer_number_or_a_name() -> None:
    text = _skill()
    assert "Never write a calendar date" in text
    assert "Never write a real-buyer number" in text
    assert "Never name a person" in text


def test_disclaimer_and_no_dollar() -> None:
    text = _skill()
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text
    assert not DOLLAR.search(text)
