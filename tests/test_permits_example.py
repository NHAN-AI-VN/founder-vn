"""Golden case: examples/barbershop/founder/permits.md (design §3, Q55, issue #112)."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
FOUNDER = ROOT / "examples" / "barbershop" / "founder"
LEDGER = ROOT / "permits" / "sources.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
LINK = re.compile(r"https://congbao\.chinhphu\.vn/van-ban/[a-z0-9-]+\.htm")
HEADINGS = (
    "## 1. Đăng ký hộ kinh doanh",
    "## 2. Đăng ký thuế và cách kê khai",
    "## 3. Sau khi mở cửa",
    "## 4. Ngành có điều kiện",
    "## 5. Nguồn và ngày kiểm chứng",
    "## 6. Lưu ý và khi nào hỏi kế toán",
)


def _text() -> str:
    return (FOUNDER / "permits.md").read_text(encoding="utf-8")


def test_has_the_six_parts_in_order() -> None:
    text = _text()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)


def test_every_link_is_a_ledger_link_and_dated() -> None:
    text = _text()
    ledger_links = set(LINK.findall(LEDGER.read_text(encoding="utf-8")))
    links = set(LINK.findall(text))
    assert links and links <= ledger_links
    assert "26/11/2026" in text and "23/11/2026" in text
    assert "kiểm chứng ngày" in text


def test_the_ledger_figures_are_on_the_page_and_the_fee_is_unsourced() -> None:
    text = _text()
    for needle in ("1.000.000.000 đ", "03 ngày làm việc", "31 tháng 01", "5%", "2%"):
        assert needle in text, needle
    assert (
        "mức lệ phí: chưa có nguồn đã kiểm chứng; hỏi Cơ quan đăng ký kinh doanh cấp xã khi nộp"
    ) in text
    assert "UBND cấp xã" in text and "anh/chị" in text


def test_conditional_sector_line_points_to_the_law_and_the_portal() -> None:
    text = _text()
    assert "ngành có điều kiện: tra tại đây" in text
    assert "https://congbao.chinhphu.vn/van-ban/luat-so-143-2025-qh15-468703.htm" in text
    assert "www.dangkykinhdoanh.gov.vn" in text


def test_ends_with_the_disclaimer_and_has_no_dollar() -> None:
    text = _text()
    assert "không phải tư vấn pháp lý" in text
    assert "hỏi kế toán" in text.lower()
    assert not DOLLAR.search(text)
    assert "\u2014" not in text
