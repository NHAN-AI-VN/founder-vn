"""Content checks for the pilot kit under pilot/ (issue #4)."""

import re
from pathlib import Path

PILOT = Path(__file__).resolve().parent.parent / "pilot"


def read(name: str) -> str:
    return (PILOT / name).read_text(encoding="utf-8")


def test_consent_names_api_publication_deletion_withdrawal_and_law() -> None:
    text = read("consent.md")
    for needle in ("91/2025/QH15", "API", "bên thứ ba", "ẩn danh", "90 ngày", "rút lại"):
        assert needle in text, needle
    assert "đồng ý giữ" in text
    assert "[LIÊN HỆ RÚT LẠI" in text


def test_baseline_has_four_fields_date_and_acknowledgement() -> None:
    text = read("baseline.md")
    for needle in ("Giá dự định", "Địa điểm", "Vốn", "Mở hay không mở", "Ngày ghi", "xác nhận"):
        assert needle in text, needle


def test_follow_up_questions_are_three_preregistered_and_sent_by_someone_else() -> None:
    text = read("follow-up-questions.md")
    assert "một trong bốn mục baseline khác đi so với văn bản intake" in text
    assert len(re.findall(r"^[123]\. ", text, re.M)) == 3
    assert "+14 ngày" in text
    assert "không phải Người hỗ trợ" in text


def test_results_template_has_columns_and_descriptive_caveat() -> None:
    text = read("results-template.md")
    for col in (
        "Mã người tham gia",
        "Ngành",
        "Giá",
        "Địa điểm",
        "Vốn",
        "Mở/không mở",
        "Câu 1",
        "Câu 2",
        "Câu 3",
        "Đổi quyết định",
        "Ghi chú",
    ):
        assert col in text, col
    assert "n = 20" in text
    assert "mô tả" in text


def test_runbook_covers_two_sessions_offline_run_pdf_root_and_deletion() -> None:
    text = read("runbook.md")
    for needle in (
        "30 phút",
        "45–60 phút",
        "đợt A",
        "ngoại tuyến",
        "PDF",
        "Zalo",
        "ngoài git",
        "90 ngày",
        "xóa",
    ):
        assert needle in text, needle


def test_pilot_kit_has_no_dollar_and_no_phone_numbers() -> None:
    paths = sorted(PILOT.glob("*.md"))
    assert len(paths) == 5
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "$" not in text, path.name
        assert not re.search(r"\b0\d{9}\b", text), path.name
