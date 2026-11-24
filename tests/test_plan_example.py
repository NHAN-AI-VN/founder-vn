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
