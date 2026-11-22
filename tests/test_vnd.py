"""Golden tables for the shared VND formatter and Vietnamese number parser."""

import pytest

from founder_vn.vnd import format_vnd

FORMAT_TABLE = [
    (35000, "35.000 đ"),
    (1200000, "1.200.000 đ"),
    (0, "0 đ"),
    (999, "999 đ"),
    (-35000, "-35.000 đ"),
    (1234.4, "1.234 đ"),
    (1234.6, "1.235 đ"),
    (1000000000, "1.000.000.000 đ"),
]


@pytest.mark.parametrize(("value", "expected"), FORMAT_TABLE)
def test_format_vnd_table(value: float, expected: str) -> None:
    assert format_vnd(value) == expected
