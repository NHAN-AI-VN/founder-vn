"""Tests of `founder-vn pricing` through the CLI."""

import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import CliRun

FIXTURE = Path(__file__).parent / "fixtures" / "pricing_input.json"
RunCli = Callable[..., CliRun]
Golden = Callable[[str, CliRun], None]


@pytest.fixture
def prices(project_root: Path) -> Path:
    target = project_root / "founder" / "pricing_input.json"
    target.parent.mkdir()
    shutil.copy(FIXTURE, target)
    return target


def test_parses_vietnamese_formats_and_reports_dropped(prices: Path, run_cli: RunCli) -> None:
    run = run_cli("pricing", "pricing_input.json", "--json")
    assert run.exit_code == 0
    data = json.loads(run.stdout)
    assert data["answers"] == {"valid": 10, "dropped": 3}
    assert data["competitors"]["dropped"] == 2
    assert data["competitors"]["prices"] == [35000, 39000, 42000, 45000]


def _spread(project_root: Path) -> None:
    """Ten respondents; question q answers 10k+i, 20k+i, 30k+i, 40k+i for i in 0..9 (in nghìn)."""
    answers = [
        {"too_cheap": f"{10 + i}k", "bargain": f"{20 + i}k", "getting_expensive": f"{30 + i}k"}
        | {"too_expensive": f"{40 + i}k"}
        for i in range(10)
    ]
    target = project_root / "founder" / "spread.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps({"answers": answers}), encoding="utf-8")


def test_van_westendorp_points_on_a_hand_checked_spread(
    project_root: Path, run_cli: RunCli
) -> None:
    # Hand check: too cheap meets "not cheap" at 20.000 (share of too-cheap answers hits 0 as the
    # share of bargain answers below the price is still 0); bargain meets getting-expensive between
    # 29.000 (0,1 vs 0) and 30.000 (0 vs 0,1), so 29.500; too expensive meets "not expensive" at 39.000.
    _spread(project_root)
    run = run_cli("pricing", "spread.json", "--json")
    assert run.exit_code == 0
    data = json.loads(run.stdout)
    assert data["points"] == {"pmc": 20000, "ipp": 29500, "pme": 39000}
    assert data["medians"] == {
        "too_cheap": 14500,
        "bargain": 24500,
        "getting_expensive": 34500,
        "too_expensive": 44500,
    }
