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


FOUNDER = ROOT / "examples" / "barbershop" / "founder"
ROLES = ("quản lý", "lễ tân", "thợ", "phụ tá", "anh/chị")
DEPENDENCIES = ("permits.md", "ops.md", "marketing.md", "idea.md", "pricing.md")
CALENDAR_DATE = re.compile(r"\d{1,2}/\d{1,2}/20\d\d|\b20\d\d-\d\d-\d\d\b")


def _golden() -> str:
    return (FOUNDER / "launch.md").read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    start = text.index(heading) + len(heading)
    rest = text[start:]
    nxt = re.search(r"^## ", rest, flags=re.M)
    return rest[: nxt.start()] if nxt else rest


def _table_rows(section: str) -> list[list[str]]:
    rows = [
        [c.strip() for c in ln.strip().strip("|").split("|")]
        for ln in section.splitlines()
        if ln.startswith("|") and not ln.startswith("|---")
    ]
    return rows[1:]  # drop the header


def test_golden_has_the_six_sections_in_order() -> None:
    text = _golden()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)


def test_golden_real_test_is_one_waitlist_at_the_listed_price_with_the_owners_stop_rule() -> None:
    section = _section(_golden(), HEADINGS[0])
    assert "danh sách chờ" in section and "50.000 đ" in section and "199.000 đ" in section
    assert "không phải giá giảm" in section
    assert re.search(
        r"nếu dưới [^.|]*anh/chị chọn[^.|]* người mua thật trong [^.|]*anh/chị chọn", section
    )
    assert "Kết quả thật: chưa có" in section
    assert not re.search(r"\d+ (người|ngày)", section)


def test_golden_countdown_runs_d_30_to_d_0_each_row_with_a_role_and_a_file() -> None:
    rows = _table_rows(_section(_golden(), HEADINGS[1]))
    days = [int(r[0].removeprefix("D-")) for r in rows]
    assert days[0] == 30 and days[-1] == 0 and days == sorted(days, reverse=True)
    assert len(set(days)) == len(days)
    for row in rows:
        assert len(row) == 4, row
        assert any(role in row[2].lower() for role in ROLES), row
        assert "thợ trưởng" not in row[2].lower(), row
        assert any(dep in row[3] for dep in DEPENDENCIES), row
    files = " ".join(r[3] for r in rows)
    for dep in ("permits.md", "ops.md", "marketing.md"):
        assert dep in files, dep


def test_golden_owners_are_roles_that_exist_in_ops_md() -> None:
    ops = (FOUNDER / "ops.md").read_text(encoding="utf-8").lower()
    for role in ROLES[:-1]:
        assert role in ops, role
    text = _golden()
    rows = _table_rows(_section(text, HEADINGS[1])) + _table_rows(_section(text, HEADINGS[2]))
    for row in rows:
        assert any(role in row[2].lower() for role in ROLES), row


def test_golden_run_sheet_is_hour_by_hour_over_the_opening_hours() -> None:
    rows = _table_rows(_section(_golden(), HEADINGS[2]))
    starts = [r[0][:5] for r in rows]
    assert all(re.fullmatch(r"\d\d:\d\d", s) for s in starts), starts
    assert starts == sorted(starts)
    assert "10:00" in starts and "21:00" in starts and starts[0] < "10:00"
    for row in rows:
        assert len(row) == 3, row


def test_golden_first_thirty_days_quote_the_three_sources() -> None:
    section = _section(_golden(), HEADINGS[3])
    for needle in ("9 lượt/ghế/ngày", "55%", "265.000 đ", "28 lượt", "70%"):
        assert needle in section, needle
    assert "idea.md" in section and "cfo.md" in section and "marketing.md" in section
    rows = _table_rows(section)
    assert len(rows) >= 5
    for row in rows:
        assert len(row) == 4 and row[3], row


def test_golden_real_buyers_override_the_panel_with_one_caveat() -> None:
    text = _golden()
    section = _section(text, HEADINGS[4])
    assert "chưa có" in section and "40%" in section
    assert text.count("Panel là mô phỏng, cận trên, không phải khách hàng thật") == 1
    assert "Panel là mô phỏng, cận trên, không phải khách hàng thật" in section
    assert len([p for p in section.strip().split("\n\n") if p.strip()]) == 1


def test_golden_no_date_no_dollar_and_the_disclaimer_closes_the_file() -> None:
    text = _golden()
    assert not CALENDAR_DATE.search(text)
    assert "anh/chị" in text
    assert not DOLLAR.search(text) and "$" not in text
    assert text.rstrip().splitlines()[-1].endswith("không phải tư vấn tài chính, thuế hay pháp lý.")
