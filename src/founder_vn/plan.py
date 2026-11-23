"""Plan compiler: ``business-plan.md`` from whatever exists under ``founder/``.

The verdict (``Profitable`` / ``Not yet`` / ``Incomplete``) is computed from CFO numbers only.
Nothing from the simulated panel is an input of :func:`verdict`.
"""

from pathlib import Path
from typing import Any

from founder_vn import cfo, files
from founder_vn.vnd import format_vnd

PLAN_FILE = "business-plan.md"
NUMBERS_FILE = "numbers.json"

PROFITABLE = "Profitable"
NOT_YET = "Not yet"
INCOMPLETE = "Incomplete"
VERDICT_LABELS = {
    PROFITABLE: "Profitable (có lãi)",
    NOT_YET: "Not yet (chưa lãi)",
    INCOMPLETE: "Incomplete (chưa đủ số)",
}


def verdict(analysis: dict[str, Any] | None) -> tuple[str, list[tuple[str, bool]]]:
    """Return the verdict and the three checks from ``cfo.analyse`` output only.

    ``None`` means there are no numbers: ``Incomplete`` with no checks.
    """
    if analysis is None:
        return INCOMPLETE, []
    v = analysis["verdict_inputs"]
    unit = analysis["unit"]
    checks = [
        (f"Đóng góp mỗi {unit} lớn hơn 0", v["contribution"] > 0),
        ("Lợi nhuận hoạt động năm 1 sau thuế lớn hơn 0", v["year1_operating_profit_after_tax"] > 0),
        ("Hòa vốn không vượt công suất", v["breakeven_within_capacity"]),
    ]
    return (PROFITABLE if all(ok for _, ok in checks) else NOT_YET), checks


def _analysis(project: Path) -> dict[str, Any] | None:
    if not files.resolve(project, NUMBERS_FILE).exists():
        return None
    return cfo.analyse(cfo._load(project, NUMBERS_FILE))


def compile_plan(project: Path) -> tuple[str, str]:
    """Return the verdict and the text of ``business-plan.md``."""
    analysis = _analysis(project)
    result, checks = verdict(analysis)
    lines = [
        "# Kế hoạch kinh doanh",
        "",
        "## Kết luận",
        "",
        f"**Kết luận: {VERDICT_LABELS[result]}.** Tính từ số của CFO thôi.",
        "",
    ]
    if analysis is None:
        lines += ["Chưa có số của CFO (founder/numbers.json), nên chưa kết luận được.", ""]
    else:
        lines += ["| Kiểm tra | Kết quả |", "| --- | --- |"]
        lines += [f"| {name} | {'Đạt' if ok else 'Không đạt'} |" for name, ok in checks]
        lines.append("")
    return result, "\n".join(lines)


def run(project: Path) -> str:
    """Behind ``founder-vn plan`` and MCP ``plan_compile``: write the plan, return the stdout."""
    result, text = compile_plan(project)
    files.write_text(project, PLAN_FILE, text)
    return f"Kết luận: {VERDICT_LABELS[result]}. Đã ghi founder/{PLAN_FILE}\n"
