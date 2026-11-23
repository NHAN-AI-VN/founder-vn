"""Tests of `founder-vn pricing` through the CLI."""

import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import CliRun

from founder_vn.cli import main

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


def _rows(project_root: Path, n: int) -> None:
    answers = [
        {"too_cheap": "10k", "bargain": "20k", "getting_expensive": "30k", "too_expensive": "40k"}
    ] * n
    target = project_root / "founder" / "rows.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps({"answers": answers}), encoding="utf-8")


def test_thin_data_warning_below_eight_valid_answers(project_root: Path, run_cli: RunCli) -> None:
    _rows(project_root, 7)
    thin = run_cli("pricing", "rows.json")
    assert thin.exit_code == 0
    assert "Dữ liệu mỏng: chỉ có 7 câu trả lời hợp lệ" in thin.stdout
    assert json.loads(run_cli("pricing", "rows.json", "--json").stdout)["warnings"] == ["thin_data"]
    _rows(project_root, 8)
    enough = run_cli("pricing", "rows.json")
    assert "Dữ liệu mỏng" not in enough.stdout
    assert json.loads(run_cli("pricing", "rows.json", "--json").stdout)["warnings"] == []


def test_report_golden(prices: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    run = run_cli("pricing", "pricing_input.json")
    assert run.exit_code == 0
    assert "$" not in run.stdout
    assert "anh/chị" in run.stdout
    assert "panel mô phỏng" in run.stdout
    assert "mô phỏng, cận trên" in run.stdout
    assert "không phải tư vấn tài chính hay định giá" in run.stdout
    assert_golden("pricing_report", run)


def test_json_golden(prices: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    run = run_cli("pricing", "pricing_input.json", "--json")
    assert run.exit_code == 0
    assert_golden("pricing_json", run)


def test_out_writes_pricing_md_under_founder(prices: Path, run_cli: RunCli) -> None:
    run = run_cli("pricing", "pricing_input.json", "--out", "pricing.md")
    assert run.exit_code == 0
    assert run.stdout == "Đã ghi founder/pricing.md\n"
    assert run.files["pricing.md"].startswith("# Độ nhạy giá (Van Westendorp)")


def test_out_outside_root_is_refused(
    prices: Path,
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(project_root)
    assert main(["pricing", "pricing_input.json", "--out", "../pricing.md"]) == 2
    assert "path refused" in capsys.readouterr().err
    assert not (project_root / "pricing.md").exists()


def test_missing_answers_exits_2_naming_the_field(
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    (project_root / "founder").mkdir()
    (project_root / "founder" / "empty.json").write_text("{}", encoding="utf-8")
    monkeypatch.chdir(project_root)
    assert main(["pricing", "empty.json"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "lỗi: thiếu trường 'answers'\n"
