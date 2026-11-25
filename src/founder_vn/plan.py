"""Plan compiler: ``business-plan.md`` from whatever exists under ``founder/``.

The verdict (``Profitable`` / ``Not yet`` / ``Incomplete``) is computed from CFO numbers only.
Nothing from the simulated panel is an input of :func:`verdict`.
"""

import json
import math
from pathlib import Path
from typing import Any

from founder_vn import cfo, files, panel
from founder_vn.vnd import format_vnd

PLAN_FILE = "business-plan.md"
NUMBERS_FILE = "numbers.json"

PROFITABLE = "Profitable"
NOT_YET = "Not yet"
INCOMPLETE = "Incomplete"
PANEL_RESULTS = "panel/results.json"
DISCLAIMER = (
    "Kế hoạch này là bản tổng hợp từ các file anh/chị đã tạo và các con số anh/chị nhập, "
    "không phải tư vấn tài chính, tư vấn thuế hay tư vấn pháp lý. Thuế suất, ngưỡng miễn thuế "
    "và thủ tục pháp lý cần đối chiếu với quy định hiện hành (hoặc hỏi cơ quan thuế, kế toán, "
    "UBND cấp xã) trước khi quyết định bỏ vốn. Tín hiệu từ panel là mô phỏng, không phải "
    "khách hàng thật."
)
# Pipeline order (spec #1 pipeline sentence, design §7, Q55): (skill, file under founder/ or None, section title).
SECTIONS = (
    ("board", "board.md", "Hội đồng cố vấn"),
    ("competitors", "competitors.md", "Đối thủ"),
    ("consumer", "panel/results.md", "Khách hàng (panel mô phỏng)"),
    ("pricing", "pricing.md", "Giá"),
    ("offer", "offer.md", "Đề xuất giá trị"),
    ("cfo", "cfo.md", "Kinh tế đơn vị"),
    ("permits", "permits.md", "Giấy phép và thuế"),
    ("marketing", "marketing.md", "Tiếp thị"),
    ("brand", "brand.md", "Thương hiệu"),
    ("ops", "ops.md", "Vận hành"),
    ("launch", "launch.md", "Khai trương"),
)
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


def panel_line(project: Path) -> str:
    """The demand-signal line from ``panel/results.json``; never an input of :func:`verdict`."""
    head = "Tín hiệu cầu (mô phỏng, cận trên)"
    target = files.resolve(project, PANEL_RESULTS)
    if not target.exists():
        return f"{head}: chưa chạy panel."
    try:
        res = json.loads(files.read_text(project, PANEL_RESULTS))
    except json.JSONDecodeError as e:
        raise panel.PanelError(f"{PANEL_RESULTS} không phải JSON hợp lệ: {e}") from None
    for field in ("buys", "passes"):
        if not isinstance(res, dict) or not isinstance(res.get(field), int):
            raise panel.PanelError(f"{PANEL_RESULTS}: thiếu số '{field}'")
    return (
        f"{head}: {res['buys']} mua, {res['passes']} không mua; "
        f"chế độ {res.get('mode', 'manual')}; mô hình {res.get('model') or 'không có'}."
    )


def _key_numbers(a: dict[str, Any]) -> list[str]:
    u = a["unit"]
    be = a["breakeven_per_day"]
    breakeven = "không bao giờ" if be == float("inf") else f"{math.ceil(be):,}".replace(",", ".")
    payback = f"tháng {a['payback_month']}" if a["payback_month"] else "chưa trong năm 1"
    rows = [
        ("Giá bán (khách trả)", format_vnd(a["price"])),
        (f"Chi phí biến đổi mỗi {u}", format_vnd(a["variable_per_unit"])),
        (f"Đóng góp mỗi {u}", format_vnd(a["contribution"])),
        ("Chi phí cố định mỗi tháng", format_vnd(a["fixed_monthly"])),
        ("Vốn khởi đầu", format_vnd(a["startup"])),
        (f"Hòa vốn ({u} mỗi ngày)", breakeven),
        (f"Công suất tối đa ({u} mỗi ngày)", f"{a['capacity_per_day']:,.0f}".replace(",", ".")),
        ("Doanh thu năm 1", format_vnd(a["year1_revenue"])),
        ("Thuế doanh thu năm 1", format_vnd(a["year1_tax"])),
        ("Lợi nhuận hoạt động năm 1 sau thuế", format_vnd(a["year1_profit_after_tax"])),
        ("Thu hồi vốn khởi đầu", payback),
        ("Vốn cần có trước khi tự nuôi được mình", format_vnd(a["cash_needed"])),
    ]
    return ["| Khoản | Số |", "| --- | ---: |"] + [f"| {k} | {v} |" for k, v in rows]


def _demote(text: str) -> list[str]:
    """Push a file's headings two levels down so they sit under the section's ``##``."""
    return [f"##{line}" if line.startswith("#") else line for line in text.strip().splitlines()]


def compile_plan(project: Path) -> tuple[str, str]:
    """Return the verdict and the text of ``business-plan.md``."""
    analysis = _analysis(project)
    result, checks = verdict(analysis)
    title = "# Kế hoạch kinh doanh"
    if analysis is not None and analysis["business"]:
        title += f": {analysis['business']}"
    lines = [
        title,
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
    lines += [panel_line(project), ""]
    if analysis is not None:
        lines += ["## Số chính", "", *_key_numbers(analysis), ""]
    todo = []
    for skill, name, heading in SECTIONS:
        path = files.resolve(project, name)
        if skill == "cfo" and analysis is not None and not path.exists():
            continue
        if not path.exists():
            todo.append(f"- {heading}: chạy skill `founder-{skill}` (tạo founder/{name}).")
            continue
        lines += [f"## {heading}", "", *_demote(files.read_text(project, name)), ""]
    if todo:
        lines += ["## Chưa làm", "", *todo, ""]
    lines += ["## Lưu ý", "", DISCLAIMER]
    return result, "\n".join(lines) + "\n"


def run(project: Path, check: bool = False) -> tuple[str, int]:
    """Behind ``founder-vn plan`` and MCP ``plan_compile``: return the stdout text and exit code.

    Without ``check`` the plan is written. With it nothing is written: the code is 0 when
    ``business-plan.md`` equals what would be compiled now, 1 when it is missing or stale.
    """
    result, text = compile_plan(project)
    if not check:
        files.write_text(project, PLAN_FILE, text)
        return f"Kết luận: {VERDICT_LABELS[result]}. Đã ghi founder/{PLAN_FILE}\n", 0
    if not files.resolve(project, PLAN_FILE).exists():
        return f"{PLAN_FILE} chưa có: chạy `founder-vn plan`\n", 1
    if files.read_text(project, PLAN_FILE) != text:
        return f"{PLAN_FILE} đã cũ so với các file hiện có: chạy `founder-vn plan`\n", 1
    return f"{PLAN_FILE} khớp với các file hiện có\n", 0
