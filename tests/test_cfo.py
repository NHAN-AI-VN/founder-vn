"""CFO slice: analyse() numbers, tax threshold, required fields."""

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from founder_vn.cfo import NumbersError, analyse

FIXTURE = Path(__file__).parent / "fixtures" / "cfo_numbers.json"


def spec() -> dict[str, Any]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_one_unit_and_break_even() -> None:
    a = analyse(spec())
    assert a["price"] == 45000
    assert a["variable_per_unit"] == 16500
    assert a["contribution"] == 28500
    assert a["fixed_monthly"] == 17_000_000
    assert a["breakeven_per_day"] == pytest.approx(17_000_000 / (28500 * 30))
    assert a["startup"] == 85_000_000


def test_tax_applies_to_full_year_revenue_above_threshold() -> None:
    a = analyse(spec())
    assert a["tax_threshold_crossed"] is True
    revenue = sum(m["revenue"] for m in a["months"])
    assert a["year1_tax"] == pytest.approx(revenue * 0.015)
    for m in a["months"]:
        assert m["tax"] == pytest.approx(m["revenue"] * 0.015)
        assert m["profit"] == pytest.approx(m["revenue"] - m["variable"] - m["fixed"] - m["tax"])
    assert any("ngưỡng miễn thuế" in f for f in a["flags"])


def test_no_tax_at_or_below_threshold() -> None:
    s = spec()
    a = analyse(s)
    s["tax_free_threshold"] = a["year1_revenue"]
    below = analyse(s)
    assert below["tax_threshold_crossed"] is False
    assert below["year1_tax"] == 0
    assert all(m["tax"] == 0 for m in below["months"])
    assert not any("ngưỡng miễn thuế" in f for f in below["flags"])


def test_verdict_inputs_are_exposed_not_decided() -> None:
    a = analyse(spec())
    v = a["verdict_inputs"]
    assert v["contribution"] == a["contribution"]
    assert v["year1_operating_profit_after_tax"] == a["year1_profit_after_tax"]
    assert v["breakeven_per_day"] == a["breakeven_per_day"]
    assert v["capacity_per_day"] == 120
    assert v["breakeven_within_capacity"] is True
    assert "verdict" not in a


@pytest.mark.parametrize(
    "field",
    [
        "price",
        "days_per_month",
        "capacity_per_day",
        "plan_per_day",
        "ramp_per_day",
        "tax_rate_on_revenue",
        "tax_free_threshold",
        "variable",
        "fixed_monthly",
        "startup",
    ],
)
def test_missing_field_is_an_error_naming_it(field: str) -> None:
    s = spec()
    del s[field]
    with pytest.raises(NumbersError, match=f"'{field}'"):
        analyse(s)


def test_bad_cost_names_the_field() -> None:
    s = copy.deepcopy(spec())
    s["variable"][1]["cost"] = "nhiều"
    with pytest.raises(NumbersError, match=r"variable\[1\]\.cost"):
        analyse(s)
