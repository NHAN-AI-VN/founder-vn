"""Tests of `founder-vn panel` through the CLI."""

import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import CliRun

FIXTURES = Path(__file__).parent / "fixtures"
RunCli = Callable[..., CliRun]


@pytest.fixture
def founder(project_root: Path) -> Path:
    """founder/ with the synthetic customer.json and pitch.md."""
    root = project_root / "founder"
    root.mkdir()
    shutil.copy(FIXTURES / "panel_customer.json", root / "customer.json")
    shutil.copy(FIXTURES / "panel_pitch.md", root / "pitch.md")
    return root


def _cards(run: CliRun) -> list[dict[str, object]]:
    return json.loads(run.files["panel/personas.json"])


def test_init_deals_vietnamese_cards_by_quota_seed_7(founder: Path, run_cli: RunCli) -> None:
    """Seed 7, n=7. Quotas by largest remainder, worked by hand: segments 0.5/0.3/0.2 give raw
    3.5/2.1/1.4, floors 3/2/1, the one spare seat goes to the largest remainder (0.5): 4/2/1;
    behaviours 0.5/0.3/0.2 give the same 4/2/1."""
    run = run_cli("panel", "init", "--n", "7", "--seed", "7")
    assert run.exit_code == 0
    cards = _cards(run)
    assert [c["id"] for c in cards] == [f"P00{i}" for i in range(1, 8)]
    by_segment = [c["segment"] for c in cards]
    assert by_segment.count("Nhân viên mới đi làm") == 4
    assert by_segment.count("Nhân viên lâu năm") == 2
    assert by_segment.count("Thu nhập cao") == 1
    by_behaviour = [c["behaviour"] for c in cards]
    assert by_behaviour.count("Quen quán") == 4
    assert by_behaviour.count("Mua theo hội nhóm") == 2
    assert by_behaviour.count("Săn voucher app") == 1
    ranges = {
        "Nhân viên mới đi làm": (8_000_000, 15_000_000),
        "Nhân viên lâu năm": (15_000_000, 30_000_000),
        "Thu nhập cao": (30_000_000, 60_000_000),
    }
    for c in cards:
        low, high = ranges[str(c["segment"])]
        assert isinstance(c["income"], int)
        assert c["income"] % 100_000 == 0
        assert low <= c["income"] <= high
        assert isinstance(c["age"], int) and 24 <= c["age"] <= 38
        assert c["objection"] in json.loads(run.files["customer.json"])["objections"]
    assert len({c["name"] for c in cards}) == 7


def test_same_seed_same_cards_other_seed_other_cards(
    founder: Path, run_cli: RunCli, project_root: Path
) -> None:
    first = _cards(run_cli("panel", "init", "--n", "20", "--seed", "7"))
    again = _cards(run_cli("panel", "init", "--n", "20", "--seed", "7"))
    other = _cards(run_cli("panel", "init", "--n", "20", "--seed", "8"))
    assert first == again
    assert first != other
