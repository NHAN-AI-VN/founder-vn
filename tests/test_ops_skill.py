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
