"""founder-permits: the skill text (design §3, Q55, Q56, issue #112)."""

import re
from pathlib import Path

from founder_vn import __version__

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-permits" / "SKILL.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
DIGIT_FIGURE = re.compile(r"\d[\d.,]*\s?(%|đ|triệu|tỷ|ngày)")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _protocol_block() -> str:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    return conventions.split("````markdown\n", 1)[1].split("````", 1)[0].strip()


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    assert _protocol_block() in _skill()


def test_frontmatter_matches_the_lint_and_the_package_version() -> None:
    head = _skill().split("---", 2)[1]
    assert "name: founder-permits" in head
    assert "license: MIT" in head
    for trigger in (
        "cần giấy phép gì",
        "đăng ký hộ kinh doanh",
        "thuế hộ kinh doanh",
        "hóa đơn điện tử",
    ):
        assert trigger in head, trigger
    assert f'version: "{__version__}"' in head


def test_states_the_never_guess_rule_and_the_unsourced_wording() -> None:
    text = _skill()
    assert "never guess a number" in text.lower()
    assert "chưa có nguồn đã kiểm chứng" in text


def test_output_is_the_static_six_part_structure_in_order() -> None:
    text = _skill()
    headings = [
        "## 1. Đăng ký hộ kinh doanh",
        "## 2. Đăng ký thuế và cách kê khai",
        "## 3. Sau khi mở cửa",
        "## 4. Ngành có điều kiện",
        "## 5. Nguồn và ngày kiểm chứng",
        "## 6. Lưu ý và khi nào hỏi kế toán",
    ]
    positions = [text.index(h) for h in headings]
    assert positions == sorted(positions)
    assert "step, authority, documents, when" in text
    assert "UBND cấp xã" in text


def test_reuses_the_cfo_tax_entries_and_names_the_ledger_keys() -> None:
    text = _skill()
    for key in ("tax_rate_on_revenue", "tax_free_threshold"):
        assert key in text, key
    assert "founder-cfo" in text and "Q52" in text
    assert "hóa đơn điện tử" in text and "ngành có điều kiện: tra tại đây" in text


def test_run_time_recheck_falls_back_to_the_ledger_copy_with_dated_wording() -> None:
    text = _skill()
    assert "kiểm chứng ngày X, chưa xác nhận lại hôm nay" in text
    assert "never drop" in text.lower()
    assert "unofficial" in text.lower()


def test_fee_amount_is_written_as_unsourced_with_the_ask_the_office_wording() -> None:
    text = _skill()
    assert (
        "mức lệ phí: chưa có nguồn đã kiểm chứng; hỏi Cơ quan đăng ký kinh doanh cấp xã khi nộp"
    ) in text


def test_conditional_sectors_line_points_to_the_investment_law_and_the_portal() -> None:
    text = _skill()
    assert "https://congbao.chinhphu.vn/van-ban/luat-so-143-2025-qh15-468703.htm" in text
    assert "Cổng thông tin quốc gia về đăng ký doanh nghiệp" in text
    assert "conditional_sectors" in text
    assert "household_registration" in text


def test_run_time_recheck_names_the_congbao_search_endpoint() -> None:
    text = _skill()
    assert "POST https://api-searchcongbao.chinhphu.vn/search/all" in text
    assert '{"filters":{},"page":1,"page_size":10,"query":"<số ký hiệu>"}' in text
    assert "id_van_ban" in text and "/van-ban/<slug>-<id>.htm" in text
    assert "User-Agent" in text


def test_names_the_missing_fb_path_in_one_sentence() -> None:
    text = _skill()
    assert "Q56" in text
    assert "chứng nhận an toàn thực phẩm" in text


def test_ends_with_the_disclaimer_and_the_accountant_line() -> None:
    text = _skill()
    assert "không phải tư vấn pháp lý" in text
    assert "hỏi kế toán" in text.lower()


def test_no_dollar_and_no_legal_figure_is_typed_into_the_skill() -> None:
    text = _skill()
    assert not DOLLAR.search(text)
    body = text.split("---", 2)[2]
    body = re.sub(r"`[^`]*`", "", body)
    assert not DIGIT_FIGURE.search(body), DIGIT_FIGURE.search(body)


LEDGER_SENTENCE = (
    "When `permits/sources.md` is absent from the project, the ledger is written by "
    "`founder-vn install --host <host>` from the installed package: run it, and do not fill "
    "the figure from memory or from a website."
)


def test_says_how_to_get_an_absent_ledger_and_not_to_guess() -> None:
    assert LEDGER_SENTENCE in _skill()
