"""Shared locale utilities: VND formatting and the Vietnamese number parser."""

from decimal import ROUND_HALF_UP, Decimal


def format_vnd(value: float | int | Decimal) -> str:
    """Format as whole đồng: dot thousands, trailing ``đ``, no decimals (``35.000 đ``)."""
    whole = int(Decimal(str(value)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    sign = "-" if whole < 0 else ""
    return f"{sign}{abs(whole):,}".replace(",", ".") + " đ"
