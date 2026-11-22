"""Shared locale utilities: VND formatting and the Vietnamese number parser."""

import re
from decimal import ROUND_HALF_UP, Decimal


def format_vnd(value: float | int | Decimal) -> str:
    """Format as whole đồng: dot thousands, trailing ``đ``, no decimals (``35.000 đ``)."""
    whole = int(Decimal(str(value)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    sign = "-" if whole < 0 else ""
    return f"{sign}{abs(whole):,}".replace(",", ".") + " đ"


_UNITS = {
    "k": 1_000,
    "nghìn": 1_000,
    "ngàn": 1_000,
    "tr": 1_000_000,
    "triệu": 1_000_000,
    "tỷ": 1_000_000_000,
    "tỉ": 1_000_000_000,
}
_NUMBER = re.compile(
    r"(?P<int>\d+(?:[.,]\d+)*)(?:\s*(?P<unit>[^\W\d_]+)(?P<tail>\d+)?)?",
)
_THOUSANDS = re.compile(r"\d{1,3}([.,]\d{3})+")


def _fail(text: object) -> ValueError:
    return ValueError(f"không hiểu số: {text!r}")


def parse_vn_number(text: str | int | float) -> int:
    """Parse Vietnamese money text into whole đồng.

    Accepts ``35.000``, ``35k``, ``35 nghìn``, ``1,2 triệu``, ``1tr2`` and ``1.200.000 đ``.
    Without a unit, ``.`` and ``,`` are thousands separators. With a unit, a single ``.`` or
    ``,`` is the decimal mark, and digits right after the unit (``1tr2``) are the decimals.
    """
    if isinstance(text, bool):
        raise _fail(text)
    if isinstance(text, (int, float)):
        value = Decimal(str(text))
    else:
        raw = text.strip().lower()
        for suffix in ("vnđ", "vnd", "đ", "₫"):
            if raw.endswith(suffix):
                raw = raw.removesuffix(suffix).strip()
                break
        match = _NUMBER.fullmatch(raw)
        if match is None:
            raise _fail(text)
        digits, unit, tail = match["int"], match["unit"], match["tail"]
        if unit is None:
            if not re.fullmatch(r"\d+", digits) and not _THOUSANDS.fullmatch(digits):
                raise _fail(text)
            value = Decimal(re.sub(r"[.,]", "", digits))
        else:
            if unit not in _UNITS or len(re.findall(r"[.,]", digits)) > 1:
                raise _fail(text)
            if tail is not None and re.search(r"[.,]", digits):
                raise _fail(text)
            value = Decimal(digits.replace(",", ".") + (f".{tail}" if tail else ""))
            value *= _UNITS[unit]
    if value != value.to_integral_value():
        raise _fail(text)
    return int(value)
