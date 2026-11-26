"""permits/sources.md: the first sources-ledger entries (CONTRIBUTING hard rule, issue #12)."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEDGER = ROOT / "permits" / "sources.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
VERIFIED = "kiểm chứng ngày 23/11/2026 bởi operator trên bản PDF Công báo"
OFFICIAL_LINK = re.compile(r"https://congbao\.chinhphu\.vn/van-ban/[a-z0-9-]+\.htm")
ISSUE_DATE = re.compile(r"Công báo (?:số )?[\d+ ]+, \d{2}/\d{2}/\d{4}")
KEYS = ("tax_rate_on_revenue", "tax_free_threshold")
# Entries added for issue #112, verified by the operator on 26/11/2026.
PERMITS_KEYS = (
    "household_registration",
    "tax_registration_declaration",
    "einvoice_obligation",
    "conditional_sectors",
)
VERIFIED_LINE = re.compile(
    r"^- Xác nhận: kiểm chứng ngày \d{2}/\d{2}/\d{4} bởi operator trên bản PDF Công báo$",
    flags=re.M,
)


def _entries(keys: tuple[str, ...] = KEYS) -> dict[str, str]:
    text = LEDGER.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    return {p.split(":", 1)[0].strip(): p for p in parts if p.split(":", 1)[0].strip() in keys}


def test_ledger_has_the_two_first_entries_in_order() -> None:
    assert list(_entries()) == list(KEYS)


def test_entry_for_the_rate_names_the_sector_and_the_value() -> None:
    entry = _entries()["tax_rate_on_revenue"]
    assert "cắt tóc, làm đầu, gội đầu" in entry
    assert "7" in entry and "GTGT 5%" in entry and "TNCN 2%" in entry


def test_entry_for_the_threshold_names_the_value() -> None:
    assert "1.000.000.000 đ" in _entries()["tax_free_threshold"]


def test_every_entry_has_link_issue_article_excerpt_and_verification() -> None:
    for key, entry in _entries().items():
        assert OFFICIAL_LINK.search(entry), key
        assert ISSUE_DATE.search(entry), key
        assert "Điều" in entry, key
        assert re.search(r"^> .{20,}", entry, flags=re.M), key
        assert VERIFIED in entry, key


def test_ledger_has_the_four_permits_entries_with_link_issue_article_excerpt_and_one_status() -> (
    None
):
    entries = _entries(PERMITS_KEYS)
    assert list(entries) == list(PERMITS_KEYS)
    for key, entry in entries.items():
        assert OFFICIAL_LINK.search(entry), key
        assert ISSUE_DATE.search(entry), key
        assert "Điều" in entry, key
        assert re.search(r"^> .{20,}", entry, flags=re.M), key
        assert len(re.findall(r"^- Xác nhận: ", entry, flags=re.M)) == 1, key
        assert "kiểm chứng ngày 26/11/2026 bởi operator trên bản PDF Công báo" in entry, key


def test_every_entry_has_a_verification_line_and_none_is_unverified() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    assert "chưa kiểm chứng" not in text
    entries = _entries(KEYS + PERMITS_KEYS)
    assert list(entries) == list(KEYS + PERMITS_KEYS)
    for key, entry in entries.items():
        assert len(VERIFIED_LINE.findall(entry)) == 1, key


def test_conditional_sectors_entry_points_to_the_portal_and_quotes_no_fee() -> None:
    entry = _entries(PERMITS_KEYS)["conditional_sectors"]
    assert "www.dangkykinhdoanh.gov.vn" in entry
    assert "Phụ lục IV" in entry
    assert "luat-so-143-2025-qh15-468703.htm" in entry


def test_household_registration_carries_the_168_2025_excerpts() -> None:
    entry = _entries(PERMITS_KEYS)["household_registration"]
    for needle in ("Điều 99", "Điều 94", "Điều 88", "Điều 85", "Điều 91", "Điều 97", "Điều 116"):
        assert needle in entry, needle
    assert "không phải là giấy phép kinh doanh" in entry
    assert "03 ngày làm việc" in entry


def test_ledger_lists_the_ten_documents_with_official_links() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for number in ("48/2024/QH15", "149/2025/QH15", "109/2025/QH15", "09/2026/QH16"):
        assert number in text, number
    for number in ("68/2026/NĐ-CP", "141/2026/NĐ-CP", "253/2026/NĐ-CP", "296/2026/NĐ-CP"):
        assert number in text, number
    for number in ("168/2025/NĐ-CP", "143/2025/QH15"):
        assert number in text, number
    assert len(set(OFFICIAL_LINK.findall(text))) == 10


def test_ledger_has_no_dollar_sign() -> None:
    assert not DOLLAR.search(LEDGER.read_text(encoding="utf-8"))
