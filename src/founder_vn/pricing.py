"""Pricing slice: Van Westendorp price sensitivity on VND.

One function (``run``) behind both ``founder-vn pricing`` and the MCP tool ``pricing_psm``.
Prices come from the panel's four answers and from competitor prices, in Vietnamese formats.
Nothing is invented: an answer that cannot be read is dropped and counted.
"""

import json
import statistics
from collections.abc import Mapping
from pathlib import Path
from typing import Any

from founder_vn import files
from founder_vn.vnd import format_vnd, parse_vn_number

MIN_VALID_ANSWERS = 8
QUESTIONS = ("too_cheap", "bargain", "getting_expensive", "too_expensive")


class PricingInputError(ValueError):
    """The pricing input file is missing or malformed; the message names the problem."""


def _price(value: Any) -> int | None:
    """Return whole đồng above zero, or None when the value cannot be read or is not positive."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        parsed = parse_vn_number(value)
    except (ValueError, TypeError):
        return None
    return parsed if parsed > 0 else None


def _answers(raw: Any) -> tuple[list[dict[str, int]], int]:
    if not isinstance(raw, list):
        raise PricingInputError("'answers' phải là danh sách")
    valid: list[dict[str, int]] = []
    for item in raw:
        row = {q: _price(item.get(q)) for q in QUESTIONS} if isinstance(item, Mapping) else {}
        if row and all(v is not None for v in row.values()):
            valid.append({q: int(v) for q, v in row.items() if v is not None})
    return valid, len(raw) - len(valid)


def _competitors(raw: Any) -> list[int | None]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise PricingInputError("'competitor_prices' phải là danh sách")
    return [_price(v) for v in raw]


def _share(values: list[int], test: Any) -> Any:
    return lambda p: sum(1 for v in values if test(v, p)) / len(values)


def _curves(valid: list[dict[str, int]]) -> dict[str, Any]:
    col = {q: [row[q] for row in valid] for q in QUESTIONS}
    return {
        "too_cheap": _share(col["too_cheap"], lambda v, p: v >= p),
        "not_cheap": _share(col["bargain"], lambda v, p: v < p),
        "bargain": _share(col["bargain"], lambda v, p: v >= p),
        "getting_expensive": _share(col["getting_expensive"], lambda v, p: v <= p),
        "not_expensive": _share(col["getting_expensive"], lambda v, p: v > p),
        "too_expensive": _share(col["too_expensive"], lambda v, p: v <= p),
    }


def _cross(grid: list[int], f: Any, g: Any) -> int | None:
    """Price where curves ``f`` and ``g`` meet: the first grid price where they are equal, else a
    linear interpolation across the first sign change; None when they never meet."""
    diffs = [f(p) - g(p) for p in grid]
    for i, d in enumerate(diffs):
        if d == 0:
            return grid[i]
        if i + 1 < len(grid) and d * diffs[i + 1] < 0:
            share = d / (d - diffs[i + 1])
            return round(grid[i] + share * (grid[i + 1] - grid[i]))
    return None


def _points(valid: list[dict[str, int]]) -> dict[str, int | None]:
    if not valid:
        return {"pmc": None, "ipp": None, "pme": None}
    c = _curves(valid)
    grid = sorted({v for row in valid for v in row.values()})
    return {
        "pmc": _cross(grid, c["too_cheap"], c["not_cheap"]),
        "ipp": _cross(grid, c["bargain"], c["getting_expensive"]),
        "pme": _cross(grid, c["too_expensive"], c["not_expensive"]),
    }


def analyse(spec: Mapping[str, Any]) -> dict[str, Any]:
    """Return every number in the report."""
    if "answers" not in spec:
        raise PricingInputError("thiếu trường 'answers'")
    valid, dropped = _answers(spec["answers"])
    rivals = _competitors(spec.get("competitor_prices"))
    kept = sorted(p for p in rivals if p is not None)
    return {
        "answers": {"valid": len(valid), "dropped": dropped},
        "warnings": ["thin_data"] if len(valid) < MIN_VALID_ANSWERS else [],
        "points": _points(valid),
        "medians": {
            q: round(statistics.median(row[q] for row in valid)) if valid else None
            for q in QUESTIONS
        },
        "competitors": {"prices": kept, "dropped": len(rivals) - len(kept)},
    }


def _money(value: int | None) -> str:
    return "không xác định được" if value is None else format_vnd(value)


QUESTION_LABELS = {
    "too_cheap": "Rẻ đến mức nghi ngờ chất lượng",
    "bargain": "Rẻ, đáng mua",
    "getting_expensive": "Bắt đầu thấy đắt",
    "too_expensive": "Đắt đến mức không mua",
}


def report(a: dict[str, Any]) -> str:
    """The Vietnamese price-sensitivity report."""
    n, dropped = a["answers"]["valid"], a["answers"]["dropped"]
    pts, rivals = a["points"], a["competitors"]
    lines = [
        "# Độ nhạy giá (Van Westendorp)",
        "",
        f"Số câu trả lời hợp lệ: {n}. Số câu bị loại: {dropped} "
        "(không đọc được thành số hoặc không lớn hơn 0).",
        "",
    ]
    if "thin_data" in a["warnings"]:
        lines += [
            f"**Dữ liệu mỏng: chỉ có {n} câu trả lời hợp lệ, dưới mức tối thiểu "
            f"{MIN_VALID_ANSWERS}.** Các mốc giá bên dưới chỉ để tham khảo, anh/chị chưa nên "
            "chốt giá từ đây.",
            "",
        ]
    if n == 0:
        lines += ["Chưa có câu trả lời hợp lệ nên không tính được mốc giá nào.", ""]
    else:
        lines += [
            "## Bốn câu hỏi về giá (trung vị)",
            "",
            "| câu hỏi | trung vị |",
            "| --- | ---: |",
        ]
        lines += [f"| {QUESTION_LABELS[q]} | {_money(a['medians'][q])} |" for q in QUESTIONS]
        lines += [
            "",
            "## Khoảng giá chấp nhận được",
            "",
            f"- Giá thấp nhất còn chấp nhận được (điểm rẻ cận biên): **{_money(pts['pmc'])}**.",
            f"- Giá cao nhất còn chấp nhận được (điểm đắt cận biên): **{_money(pts['pme'])}**.",
            f"- Điểm cân bằng (rẻ và đắt có số người chọn bằng nhau): **{_money(pts['ipp'])}**.",
            "",
        ]
    if rivals["prices"]:
        prices = rivals["prices"]
        low, high = pts["pmc"], pts["pme"]
        inside = (
            sum(1 for p in prices if low <= p <= high)
            if low is not None and high is not None
            else None
        )
        lines += [
            "## Giá đối thủ",
            "",
            f"- Số giá đối thủ đọc được: {len(prices)}; bị loại: {rivals['dropped']}.",
            f"- Thấp nhất {format_vnd(prices[0])}, trung vị "
            f"{format_vnd(statistics.median(prices))}, cao nhất {format_vnd(prices[-1])}.",
        ]
        if inside is not None:
            lines.append(
                f"- {inside} trên {len(prices)} giá đối thủ nằm trong khoảng chấp nhận được."
            )
        lines.append("")
    else:
        lines += [
            "## Giá đối thủ",
            "",
            "Chưa có giá đối thủ đọc được. Báo cáo không dùng mốc giá nào ngoài số anh/chị nhập.",
            "",
        ]
    lines += [
        "## Lưu ý",
        "",
        "Các câu trả lời đến từ panel mô phỏng hoặc khảo sát nhỏ, không thay cho khách thật. "
        "Đây là khoảng giá để anh/chị thử ngoài thực tế, không phải giá chắc chắn bán được.",
    ]
    return "\n".join(lines) + "\n"


def _load(project: Path, source: str) -> dict[str, Any]:
    rel = source.removeprefix(f"{files.ROOT_NAME}/")
    try:
        raw = files.read_text(project, rel)
    except FileNotFoundError:
        raise PricingInputError(f"không thấy file: {source}") from None
    try:
        spec = json.loads(raw)
    except json.JSONDecodeError as e:
        raise PricingInputError(f"{source} không phải JSON hợp lệ: {e}") from None
    if not isinstance(spec, dict):
        raise PricingInputError(f"{source} phải là một đối tượng JSON")
    return spec


def run(project: Path, source: str, as_json: bool = False, out: str | None = None) -> str:
    """Behind ``founder-vn pricing`` and MCP ``pricing_psm``: return the exact stdout text.

    ``source`` is read under ``<project>/founder/``; with ``out`` the report is written there
    through the path-locked layer and a one-line confirmation is returned instead.
    """
    a = analyse(_load(project, source))
    text = json.dumps(a, ensure_ascii=False, indent=2) + "\n" if as_json else report(a)
    if out is None:
        return text
    target = files.write_text(project, out, text)
    return f"Đã ghi {target.relative_to(project).as_posix()}\n"
