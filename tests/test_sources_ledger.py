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


def _entries() -> dict[str, str]:
    text = LEDGER.read_text(encoding="utf-8")
    parts = re.split(r"^## ", text, flags=re.M)[1:]
    return {p.split(":", 1)[0].strip(): p for p in parts if p.split(":", 1)[0].strip() in KEYS}


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


def test_ledger_lists_the_seven_documents_with_official_links() -> None:
    text = LEDGER.read_text(encoding="utf-8")
    for number in ("48/2024/QH15", "149/2025/QH15", "109/2025/QH15", "09/2026/QH16"):
        assert number in text, number
    for number in ("68/2026/NĐ-CP", "141/2026/NĐ-CP", "253/2026/NĐ-CP"):
        assert number in text, number
    assert len(set(OFFICIAL_LINK.findall(text))) == 7


def test_ledger_has_no_dollar_sign() -> None:
    assert not DOLLAR.search(LEDGER.read_text(encoding="utf-8"))
