"""Golden case: summary.md and the compiled business-plan.md (design §3, issue #18)."""

import re
from pathlib import Path

from founder_vn import cfo, plan

ROOT = Path(__file__).parent.parent
EXAMPLE = ROOT / "examples" / "barbershop"
FOUNDER = EXAMPLE / "founder"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
CAVEAT = "mô phỏng, cận trên, không phải khách hàng thật"
DISCLAIMER = "không phải tư vấn tài chính, thuế hay pháp lý"
VND = re.compile(r"\d{1,3}(?:\.\d{3})+ đ")


def _read(name: str) -> str:
    return (FOUNDER / name).read_text(encoding="utf-8")


def test_business_plan_is_the_compiler_output_and_check_passes() -> None:
    verdict, text = plan.compile_plan(EXAMPLE)
    assert _read("business-plan.md") == text
    out, code = plan.run(EXAMPLE, check=True)
    assert code == 0, out


def test_verdict_line_in_plan_and_summary_equals_the_computed_verdict() -> None:
    verdict, _ = plan.compile_plan(EXAMPLE)
    label = plan.VERDICT_LABELS[verdict]
    assert f"**Kết luận: {label}.**" in _read("business-plan.md")
    assert f"**Kết luận của công cụ: {label}.**" in _read("summary.md")


def test_summary_has_both_parts_in_order() -> None:
    text = _read("summary.md")
    first = text.index("## Tóm tắt điều hành")
    second = text.index("## Bản một trang cho đối tác hoặc bên cho vay")
    assert first < second


def test_every_amount_in_the_summary_is_printed_by_a_tool() -> None:
    sources = _read("business-plan.md") + _read("cfo.md") + cfo.run(EXAMPLE, "founder/numbers.json")
    for amount in set(VND.findall(_read("summary.md"))):
        assert amount in sources, amount


def test_summary_carries_caveat_disclaimer_and_dated_links() -> None:
    text = _read("summary.md")
    assert CAVEAT in text
    assert DISCLAIMER in text
    assert "https://congbao.chinhphu.vn/" in text
    assert "23/11/2026" in text
    assert "permits/sources.md" in text
    assert not DOLLAR.search(text)


def _parts() -> tuple[str, str]:
    text = _read("summary.md")
    marker = "## Bản một trang cho đối tác hoặc bên cho vay"
    first, rest = text.split(marker)
    # Cut the one-page version at the next "## " heading so the closing "## Lưu ý"
    # section cannot supply the caveat and disclaimer on its behalf.
    return first, marker + rest.split("\n## ")[0]


def test_one_page_version_stands_alone_with_caveat_disclaimer_and_sources() -> None:
    for part in _parts():
        assert CAVEAT in part
        assert DISCLAIMER in part
    page = _parts()[1]
    for link in ("luat-so-48-2024-qh15", "luat-so-109-2025-qh15", "nghi-dinh-so-253-2026-nd-cp"):
        assert link in page, link
    assert "23/11/2026" in page


def test_summary_closes_with_the_caveat_then_the_disclaimer() -> None:
    tail = _read("summary.md").strip().splitlines()[-1]
    assert tail.index(CAVEAT) < tail.index(DISCLAIMER)


def test_business_plan_lists_only_offer_and_brand_as_not_done() -> None:
    # #116: after founder-launch the compiled plan misses only the two after-pilot skills (Q12, Q55).
    plan_text = _read("business-plan.md")
    todo = plan_text[plan_text.index("## Chưa làm") :].split("\n\n## ", 1)[0].splitlines()[2:]
    assert todo == [
        "- Đề xuất giá trị: để sau pilot, chưa có trong bản này (skill `founder-offer` sẽ tạo founder/offer.md).",
        "- Thương hiệu: để sau pilot, chưa có trong bản này (skill `founder-brand` sẽ tạo founder/brand.md).",
    ]
    assert "## Khai trương" in plan_text
