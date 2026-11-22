"""Golden tables for the shared VND formatter and Vietnamese number parser."""

import pytest

from founder_vn.vnd import format_vnd, parse_vn_number

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


PARSE_TABLE = [
    ("35.000", 35000),
    ("35k", 35000),
    ("35 nghìn", 35000),
    ("1,2 triệu", 1200000),
    ("1tr2", 1200000),
    ("1.200.000 đ", 1200000),
    ("35000", 35000),
    ("  2 TRIỆU ", 2000000),
    ("1tr25", 1250000),
    ("1,5k", 1500),
    ("2 tỷ", 2000000000),
    ("0", 0),
]


@pytest.mark.parametrize(("text", "expected"), PARSE_TABLE)
def test_parse_vn_number_table(text: str, expected: int) -> None:
    assert parse_vn_number(text) == expected


@pytest.mark.parametrize("text", ["", "abc", "1,2,3 triệu", "12,34", "1tr2x", "$5"])
def test_parse_vn_number_rejects_and_names_the_input(text: str) -> None:
    with pytest.raises(ValueError, match="không hiểu số"):
        parse_vn_number(text)
