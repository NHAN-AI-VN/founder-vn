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
def founder(project_root: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """founder/ with the synthetic customer.json and pitch.md; the cwd is the project root."""
    monkeypatch.chdir(project_root)
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


def _fail(founder: Path, capsys: pytest.CaptureFixture[str], change: Callable[[dict], None]) -> str:
    """Apply ``change`` to customer.json, run `panel init`, expect exit 2; return stderr."""
    from founder_vn.cli import main

    customer = json.loads((founder / "customer.json").read_text(encoding="utf-8"))
    change(customer)
    (founder / "customer.json").write_text(json.dumps(customer), encoding="utf-8")
    capsys.readouterr()
    assert main(["panel", "init", "--n", "7", "--seed", "7"]) == 2
    return capsys.readouterr().err


@pytest.mark.parametrize(
    ("change", "field"),
    [
        pytest.param(lambda c: c.pop("business"), "business", id="business"),
        pytest.param(lambda c: c.update(objections=[]), "objections", id="objections"),
        pytest.param(lambda c: c["segments"][1].pop("name"), "segments[1].name", id="seg-name"),
        pytest.param(
            lambda c: c["segments"][1].update(income=[30000000]), "segments[1].income", id="income"
        ),
        pytest.param(
            lambda c: c["segments"][0].update(income=["a", "b"]),
            "segments[0].income",
            id="income-nan",
        ),
        pytest.param(
            lambda c: c["segments"][2].update(income=[60000000, 30000000]),
            "segments[2].income",
            id="income-order",
        ),
        pytest.param(lambda c: c["segments"][2].pop("share"), "segments[2].share", id="seg-share"),
        pytest.param(lambda c: c["behaviours"][0].pop("name"), "behaviours[0].name", id="beh-name"),
        pytest.param(
            lambda c: c["behaviours"][1].update(share=-1), "behaviours[1].share", id="beh-share"
        ),
        pytest.param(lambda c: c.pop("age"), "age", id="age"),
    ],
)
def test_customer_error_names_the_field(
    founder: Path,
    capsys: pytest.CaptureFixture[str],
    change: Callable[[dict], None],
    field: str,
) -> None:
    err = _fail(founder, capsys, change)
    assert err.startswith("lỗi: ")
    assert f"'{field}'" in err


def test_empty_or_missing_pitch_and_bad_n_are_errors(
    founder: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from founder_vn.cli import main

    (founder / "pitch.md").write_text("  \n", encoding="utf-8")
    assert main(["panel", "init", "--seed", "7"]) == 2
    assert "pitch.md" in capsys.readouterr().err
    (founder / "pitch.md").unlink()
    assert main(["panel", "init", "--seed", "7"]) == 2
    assert "pitch.md" in capsys.readouterr().err
    assert main(["panel", "init", "--n", "0", "--seed", "7"]) == 2
    assert "'--n'" in capsys.readouterr().err


def test_init_writes_only_panel_json_and_personas_under_founder_panel(
    founder: Path, run_cli: RunCli
) -> None:
    run = run_cli("panel", "init", "--n", "7", "--seed", "7")
    assert sorted(run.files) == [
        "customer.json",
        "panel/panel.json",
        "panel/personas.json",
        "pitch.md",
    ]
    panel = json.loads(run.files["panel/panel.json"])
    assert (panel["n"], panel["seed"]) == (7, 7)
    assert panel["pitch"] == (FIXTURES / "panel_pitch.md").read_text(encoding="utf-8").strip()
    assert panel["customer"] == json.loads(run.files["customer.json"])
    assert run.stdout == "Đã chia 7 người mua (seed 7) vào founder/panel/\n"


def test_customer_outside_founder_is_refused(
    founder: Path, project_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from founder_vn.cli import main

    shutil.copy(FIXTURES / "panel_customer.json", project_root / "customer.json")
    assert main(["panel", "init", "--customer", "../customer.json", "--seed", "7"]) == 2
    assert "path refused" in capsys.readouterr().err
    assert not (founder / "panel").exists()
