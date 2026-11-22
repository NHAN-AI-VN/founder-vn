"""CFO slice: unit economics for a Vietnamese household business, with revenue tax.

One pure function (``analyse``) behind both ``founder-vn cfo`` and the MCP tool ``cfo_analyse``.
Every numeric input is required: a missing field is an error naming it, never a default. The tax
rate and the tax-free threshold are inputs from the Owner, not constants of this module.
"""

import json
import math
from collections.abc import Mapping
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path
from typing import Any

from founder_vn import files
from founder_vn.vnd import format_vnd, parse_vn_number

MONTHS = 12
NUMERIC_FIELDS = (
    "price",
    "days_per_month",
    "capacity_per_day",
    "plan_per_day",
    "tax_rate_on_revenue",
    "tax_free_threshold",
)
LIST_FIELDS = ("variable", "fixed_monthly", "startup")


class NumbersError(ValueError):
    """``numbers.json`` is incomplete or malformed; the message names the field."""


def _number(value: Any, field: str) -> float:
    """Read a number given as a JSON number or as Vietnamese text (``35k``, ``1,2 triệu``)."""
    if isinstance(value, bool) or value is None:
        raise NumbersError(f"'{field}' không phải số: {value!r}")
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        try:
            return float(parse_vn_number(text))
        except ValueError:
            pass
        try:
            return float(Decimal(text))
        except ArithmeticError:
            pass
    raise NumbersError(f"'{field}' không phải số: {value!r}")


def _required(spec: Mapping[str, Any], field: str) -> Any:
    if field not in spec or spec[field] is None:
        raise NumbersError(f"thiếu trường '{field}'")
    return spec[field]


def _items(spec: Mapping[str, Any], field: str) -> list[dict[str, Any]]:
    raw = _required(spec, field)
    if not isinstance(raw, list):
        raise NumbersError(f"'{field}' phải là danh sách")
    items = []
    for i, item in enumerate(raw):
        if not isinstance(item, dict) or "cost" not in item:
            raise NumbersError(f"thiếu trường '{field}[{i}].cost'")
        items.append({"label": str(item.get("label", "chi phí")), "cost": item["cost"]})
    return items


def _cost(items: list[dict[str, Any]], field: str, factor: float = 1.0) -> list[dict[str, Any]]:
    return [
        {"label": it["label"], "cost": _number(it["cost"], f"{field}[{i}].cost") * factor}
        for i, it in enumerate(items)
    ]


def analyse(
    spec: Mapping[str, Any],
    price: float | None = None,
    volume: float = 1.0,
    unit_cost_factor: float = 1.0,
) -> dict[str, Any]:
    """Return every number in the report. ``price`` and ``volume`` are the what-ifs."""
    for field in (*NUMERIC_FIELDS, "ramp_per_day", *LIST_FIELDS):
        if field == "price" and price is not None:
            continue
        _required(spec, field)
    p = price if price is not None else _number(spec["price"], "price")
    if p <= 0:
        raise NumbersError("'price' phải lớn hơn 0")
    days = _number(spec["days_per_month"], "days_per_month")
    if days <= 0:
        raise NumbersError("'days_per_month' phải lớn hơn 0")
    capacity = _number(spec["capacity_per_day"], "capacity_per_day")
    plan = _number(spec["plan_per_day"], "plan_per_day") * volume
    if plan <= 0:
        raise NumbersError("'plan_per_day' phải lớn hơn 0")
    rate = _number(spec["tax_rate_on_revenue"], "tax_rate_on_revenue")
    threshold = _number(spec["tax_free_threshold"], "tax_free_threshold")
    if rate < 0:
        raise NumbersError("'tax_rate_on_revenue' không được âm")
    ramp_raw = spec["ramp_per_day"]
    if not isinstance(ramp_raw, list) or len(ramp_raw) != MONTHS:
        raise NumbersError(f"'ramp_per_day' cần đúng {MONTHS} số, mỗi tháng một số")
    ramp = [_number(v, f"ramp_per_day[{i}]") * volume for i, v in enumerate(ramp_raw)]

    variable_items = _cost(_items(spec, "variable"), "variable", unit_cost_factor)
    fixed_items = _cost(_items(spec, "fixed_monthly"), "fixed_monthly")
    startup_items = _cost(_items(spec, "startup"), "startup")
    var = sum(it["cost"] for it in variable_items)
    fixed = sum(it["cost"] for it in fixed_items)
    startup = sum(it["cost"] for it in startup_items)

    contribution = p - var
    breakeven_day = math.inf if contribution <= 0 else fixed / (contribution * days)
    margin_at_plan = (contribution - fixed / (plan * days)) / p

    year_revenue = sum(per_day * days * p for per_day in ramp)
    crosses = year_revenue > threshold
    months = []
    cumulative = -startup
    payback_month = None
    for m, per_day in enumerate(ramp, start=1):
        units = per_day * days
        revenue = units * p
        variable_cost = units * var
        tax = revenue * rate / 100 if crosses else 0.0
        profit = revenue - variable_cost - fixed - tax
        cumulative += profit
        if payback_month is None and cumulative >= 0:
            payback_month = m
        months.append(
            {
                "month": m,
                "per_day": per_day,
                "units": units,
                "revenue": revenue,
                "variable": variable_cost,
                "fixed": fixed,
                "tax": tax,
                "profit": profit,
                "cumulative": cumulative,
            }
        )
    year_profit = sum(m["profit"] for m in months)
    year_tax = sum(m["tax"] for m in months)
    cash_needed = -min([-startup] + [m["cumulative"] for m in months])

    flags = []
    if contribution <= 0:
        flags.append(
            "Mỗi đơn vị bán ra đã lỗ trước khi trả chi phí cố định: giá thấp hơn chi phí biến đổi."
        )
    if breakeven_day > capacity:
        flags.append("Hòa vốn cần bán số lượng vượt công suất tối đa mỗi ngày.")
    if plan > capacity:
        flags.append("Kế hoạch bán mỗi ngày vượt công suất tối đa.")
    if crosses:
        flags.append(
            "Doanh thu năm 1 vượt ngưỡng miễn thuế: thuế doanh thu tính trên toàn bộ doanh thu năm."
        )
    if year_profit < 0:
        flags.append("Năm 1 lỗ hoạt động sau thuế.")
    if payback_month is None:
        flags.append("Vốn khởi đầu chưa thu hồi được trong năm 1.")

    return {
        "business": str(spec.get("business", "")),
        "unit": str(spec.get("unit", "đơn vị")),
        "price": p,
        "variable_per_unit": var,
        "contribution": contribution,
        "contribution_pct": contribution / p,
        "fixed_monthly": fixed,
        "startup": startup,
        "days_per_month": days,
        "plan_per_day": plan,
        "capacity_per_day": capacity,
        "margin_at_plan": margin_at_plan,
        "breakeven_per_day": breakeven_day,
        "tax_rate_on_revenue": rate,
        "tax_free_threshold": threshold,
        "tax_threshold_crossed": crosses,
        "year1_revenue": year_revenue,
        "year1_tax": year_tax,
        "year1_profit_after_tax": year_profit,
        "year1_after_startup": year_profit - startup,
        "payback_month": payback_month,
        "cash_needed": cash_needed,
        "months": months,
        "flags": flags,
        "variable_items": variable_items,
        "fixed_items": fixed_items,
        "startup_items": startup_items,
        "verdict_inputs": {
            "contribution": contribution,
            "year1_operating_profit_after_tax": year_profit,
            "breakeven_per_day": None if math.isinf(breakeven_day) else breakeven_day,
            "capacity_per_day": capacity,
            "breakeven_within_capacity": breakeven_day <= capacity,
        },
    }


def sensitivity(
    spec: Mapping[str, Any], price: float | None = None, volume: float = 1.0
) -> list[tuple[str, dict[str, Any]]]:
    """Base plus the three what-ifs every plan should survive, relative to the base."""
    base = analyse(spec, price=price, volume=volume)
    return [
        ("Kế hoạch gốc", base),
        ("Giá giảm 10%", analyse(spec, price=base["price"] * 0.9, volume=volume)),
        ("Sản lượng giảm 20%", analyse(spec, price=price, volume=volume * 0.8)),
        (
            "Chi phí mỗi đơn vị tăng 15%",
            analyse(spec, price=price, volume=volume, unit_cost_factor=1.15),
        ),
    ]


def _per_day(value: float, up: bool = False) -> str:
    whole = math.ceil(value) if up else int(Decimal(str(value)).quantize(Decimal(1), ROUND_HALF_UP))
    return f"{whole:,}".replace(",", ".")


def _break_even(value: float) -> str:
    return "không bao giờ" if math.isinf(value) else _per_day(value, up=True)


def _pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def report(
    spec: Mapping[str, Any], a: dict[str, Any], price: float | None = None, volume: float = 1.0
) -> str:
    """The Vietnamese unit-economics report (markdown)."""
    u = a["unit"]
    lines = [
        f"# Kinh tế đơn vị: {a['business'] or 'doanh nghiệp của anh/chị'}",
        "",
        "Mọi con số dưới đây lấy từ file numbers.json của anh/chị. Không số nào được tra cứu hay đoán.",
        "",
        f"## Một {u}",
        "",
        f"| khoản | mỗi {u} |",
        "| --- | ---: |",
        f"| Giá bán (khách trả) | {format_vnd(a['price'])} |",
    ]
    lines += [f"| {it['label']} | -{format_vnd(it['cost'])} |" for it in a["variable_items"]]
    lines += [
        f"| **Đóng góp** (phần mỗi {u} còn lại để trả chi phí cố định) "
        f"| **{format_vnd(a['contribution'])}** ({_pct(a['contribution_pct'])}) |",
        "",
        "## Hòa vốn và biên lợi nhuận",
        "",
        f"Chi phí cố định: {format_vnd(a['fixed_monthly'])} mỗi tháng ("
        + ", ".join(f"{it['label']} {format_vnd(it['cost'])}" for it in a["fixed_items"])
        + ").",
        "",
        f"- **Hòa vốn: {_break_even(a['breakeven_per_day'])} {u} mỗi ngày.** "
        "Bán dưới mức đó thì tháng nào cũng lỗ (chưa tính thuế doanh thu).",
        f"- **Biên lợi nhuận theo kế hoạch** ({_per_day(a['plan_per_day'])} {u} mỗi ngày): "
        f"**{_pct(a['margin_at_plan'])}** trên mỗi đồng bán ra, trước thuế doanh thu.",
        f"- Công suất tối đa: {_per_day(a['capacity_per_day'])} {u} mỗi ngày.",
        "",
        "## Năm 1 theo từng tháng",
        "",
        f"| tháng | {u} mỗi ngày | doanh thu | thuế doanh thu | lợi nhuận | "
        f"lũy kế (sau vốn khởi đầu {format_vnd(a['startup'])}) |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    lines += [
        f"| {m['month']} | {_per_day(m['per_day'])} | {format_vnd(m['revenue'])} "
        f"| {format_vnd(m['tax'])} | {format_vnd(m['profit'])} | {format_vnd(m['cumulative'])} |"
        for m in a["months"]
    ]
    payback = f"tháng {a['payback_month']}" if a["payback_month"] else "chưa trong năm 1"
    lines += [
        "",
        f"- Doanh thu năm 1: {format_vnd(a['year1_revenue'])}. Ngưỡng miễn thuế: "
        f"{format_vnd(a['tax_free_threshold'])}; thuế suất trên doanh thu: {str(round(a['tax_rate_on_revenue'], 2)).removesuffix('.0').replace('.', ',')}%.",
        f"- Thuế doanh thu năm 1: {format_vnd(a['year1_tax'])}.",
        f"- **Lợi nhuận hoạt động năm 1 sau thuế: {format_vnd(a['year1_profit_after_tax'])}.**",
        f"- Sau vốn khởi đầu {format_vnd(a['startup'])}: {format_vnd(a['year1_after_startup'])}.",
        f"- Thu hồi vốn khởi đầu: {payback}.",
        f"- Vốn cần có trước khi tự nuôi được mình: **{format_vnd(a['cash_needed'])}**.",
        "",
        "## Nếu thay đổi",
        "",
        "| kịch bản | biên lợi nhuận | hòa vốn mỗi ngày | lợi nhuận năm 1 sau thuế |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, s in sensitivity(spec, price, volume):
        lines.append(
            f"| {name} | {_pct(s['margin_at_plan'])} | {_break_even(s['breakeven_per_day'])} "
            f"| {format_vnd(s['year1_profit_after_tax'])} |"
        )
    lines.append("")
    if a["flags"]:
        lines += ["## Cảnh báo", ""] + [f"- {f}" for f in a["flags"]]
    else:
        lines.append(
            "Không có cảnh báo trong các con số này. Chúng chỉ đúng bằng dữ liệu đầu vào: "
            "anh/chị hãy đối chiếu từng khoản chi với báo giá thật."
        )
    return "\n".join(lines) + "\n"


def _round(value: Any) -> Any:
    if isinstance(value, float):
        return None if math.isinf(value) else round(value, 2)
    if isinstance(value, dict):
        return {k: _round(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_round(v) for v in value]
    return value


def report_json(
    spec: Mapping[str, Any], a: dict[str, Any], price: float | None = None, volume: float = 1.0
) -> str:
    """The same numbers as JSON; ``verdict_inputs`` carries the three inputs of the verdict."""
    out = {k: v for k, v in a.items() if not k.endswith("_items")}
    out["sensitivity"] = [
        {
            "scenario": name,
            "margin_at_plan": s["margin_at_plan"],
            "breakeven_per_day": s["breakeven_per_day"],
            "year1_profit_after_tax": s["year1_profit_after_tax"],
        }
        for name, s in sensitivity(spec, price, volume)
    ]
    return json.dumps(_round(out), ensure_ascii=False, indent=2) + "\n"


def _load(project: Path, numbers: str) -> dict[str, Any]:
    rel = numbers.removeprefix(f"{files.ROOT_NAME}/")
    try:
        raw = files.read_text(project, rel)
    except FileNotFoundError:
        raise NumbersError(f"không thấy file: {numbers}") from None
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError as e:
        raise NumbersError(f"{numbers} không phải JSON hợp lệ: {e}") from None
    if not isinstance(spec, dict):
        raise NumbersError(f"{numbers} phải là một đối tượng JSON")
    return spec


def run(
    project: Path,
    numbers: str,
    price: str | None = None,
    volume: float = 1.0,
    as_json: bool = False,
    out: str | None = None,
) -> str:
    """Behind ``founder-vn cfo`` and MCP ``cfo_analyse``: return the exact stdout text.

    ``numbers`` is read under ``<project>/founder/``; with ``out`` the report is written there
    through the path-locked layer and a one-line confirmation is returned instead.
    """
    spec = _load(project, numbers)
    what_if_price = None if price is None else float(parse_vn_number(price))
    if volume <= 0:
        raise NumbersError("'volume' phải lớn hơn 0")
    a = analyse(spec, price=what_if_price, volume=volume)
    text = (report_json if as_json else report)(spec, a, what_if_price, volume)
    if out is None:
        return text
    target = files.write_text(project, out, text)
    return f"Đã ghi {target.relative_to(project).as_posix()}\n"
