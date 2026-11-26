"""founder-ops: the skill text (design §3, issue #114)."""

import re
from pathlib import Path

from founder_vn import __version__

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-ops" / "SKILL.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")

HEADINGS = (
    "## 1. Nhà cung cấp",
    "## 2. Nhân sự và ca làm",
    "## 3. Quy trình mở cửa, phục vụ, đóng cửa",
    "## 4. Bộ công cụ tối thiểu",
    "## 5. Sổ rủi ro",
    "## 6. Giấy phép và nghĩa vụ",
    "## 7. Lưu ý",
)


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _protocol_block() -> str:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    return conventions.split("````markdown\n", 1)[1].split("````", 1)[0].strip()


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    assert _protocol_block() in _skill()


def test_frontmatter_matches_the_lint_and_the_package_version() -> None:
    head = _skill().split("---", 2)[1]
    assert "name: founder-ops" in head
    assert "license: MIT" in head
    for trigger in ("ngày đầu vận hành", "nhà cung cấp", "ca làm", "sổ rủi ro"):
        assert trigger in head, trigger
    assert f'version: "{__version__}"' in head


def test_output_is_the_seven_part_structure_in_order() -> None:
    text = _skill()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)
    assert "exactly ten rows" in text
    assert "risk, early sign, what to do, who" in text


def test_never_invents_a_supplier_a_quote_or_a_price() -> None:
    text = _skill()
    assert "Never invent a supplier, a quote or a price" in text
    assert "chưa có báo giá" in text and "chưa chọn" in text
    assert "no data is not data" in text


def test_numbers_json_belongs_to_founder_cfo() -> None:
    text = _skill()
    assert "numbers.json" in text and "founder-cfo" in text
    assert "founder-pricing" in text and "founder-plan" in text
    assert "writes no `numbers.json`" in text
    assert "cập nhật" in text


def test_permits_section_points_and_restates_no_figure() -> None:
    text = _skill()
    assert "founder/permits.md" in text and "founder-permits" in text
    assert "restate no legal figure" in text


def test_tool_stack_names_categories_not_vendors() -> None:
    text = _skill()
    for category in ("đặt lịch", "thanh toán QR", "hóa đơn điện tử", "chấm công"):
        assert category in text, category
    assert "no vendor" in text


def test_no_dollar_in_the_skill() -> None:
    assert not DOLLAR.search(_skill())


FOUNDER = ROOT / "examples" / "barbershop" / "founder"


def _golden() -> str:
    return (FOUNDER / "ops.md").read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    start = text.index(heading) + len(heading)
    rest = text[start:]
    nxt = re.search(r"^## ", rest, flags=re.M)
    return rest[: nxt.start()] if nxt else rest


def test_golden_has_the_seven_sections_in_order() -> None:
    text = _golden()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)


def test_golden_risk_register_has_exactly_ten_rows() -> None:
    register = _section(_golden(), "## 5. Sổ rủi ro")
    rows = [ln for ln in register.splitlines() if ln.startswith("|")]
    assert rows[0].count("|") == 5
    assert [c.strip() for c in rows[0].strip("|").split("|")] == [
        "Rủi ro",
        "Dấu hiệu sớm",
        "Việc cần làm",
        "Ai làm",
    ]
    assert len(rows) - 2 == 10


def test_golden_every_supplier_quote_is_unquoted_and_no_supplier_is_named() -> None:
    table = _section(_golden(), "## 1. Nhà cung cấp")
    rows = [ln for ln in table.splitlines() if ln.startswith("|")][2:]
    assert len(rows) >= 5
    for row in rows:
        cells = [c.strip() for c in row.strip("|").split("|")]
        assert cells[1] == "chưa chọn", row
        assert cells[2] == "chưa có báo giá", row
        assert cells[3] == "chưa có", row
    assert not re.search(r"\d", "".join(rows))


def test_golden_feedback_loop_sentence_and_staffing() -> None:
    text = _golden()
    assert "`founder/numbers.json` là file của `founder-cfo`" in text
    assert "`founder-pricing`" in text and "`founder-plan`" in text
    staffing = _section(text, "## 2. Nhân sự và ca làm")
    for needle in ("Thợ cắt", "Phụ tá", "Lễ tân", "Quản lý", "Thứ Hai", "nghỉ"):
        assert needle in staffing, needle


def test_golden_points_to_permits_and_holds_no_legal_figure() -> None:
    text = _golden()
    section = _section(text, "## 6. Giấy phép và nghĩa vụ")
    assert "founder/permits.md" in section and "founder-permits" in section
    assert not re.search(r"\d", section)
    assert "%" not in text and "Nghị định" not in text and "Luật" not in text


def test_golden_is_vietnamese_with_disclaimer_and_no_dollar() -> None:
    text = _golden()
    assert "anh/chị" in text
    assert not DOLLAR.search(text) and "$" not in text
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text
    assert text.rstrip().splitlines()[-1].startswith("Tài liệu vận hành này")


def test_business_plan_carries_the_ops_section() -> None:
    plan = (FOUNDER / "business-plan.md").read_text(encoding="utf-8")
    assert "## Vận hành" in plan
    assert "### 1. Nhà cung cấp" in plan and "### 5. Sổ rủi ro" in plan
