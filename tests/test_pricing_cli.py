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
