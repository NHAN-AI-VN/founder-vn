"""Golden-file tests of `founder-vn cfo` through the CLI."""

import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import CliRun

from founder_vn.cli import main

FIXTURE = Path(__file__).parent / "fixtures" / "cfo_numbers.json"
RunCli = Callable[..., CliRun]
Golden = Callable[[str, CliRun], None]


@pytest.fixture
def numbers(project_root: Path) -> Path:
    target = project_root / "founder" / "numbers.json"
    target.parent.mkdir()
    shutil.copy(FIXTURE, target)
    return target


def test_report_golden(numbers: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    run = run_cli("cfo", "numbers.json")
    assert run.exit_code == 0
    assert "$" not in run.stdout
    assert_golden("cfo_report", run)


def test_json_golden(numbers: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    run = run_cli("cfo", "founder/numbers.json", "--json")
    assert run.exit_code == 0
    data = json.loads(run.stdout)
    assert set(data["verdict_inputs"]) >= {
        "contribution",
        "year1_operating_profit_after_tax",
        "breakeven_per_day",
        "capacity_per_day",
    }
    assert [row["scenario"] for row in data["sensitivity"]] == [
        "Kế hoạch gốc",
        "Giá giảm 10%",
        "Sản lượng giảm 20%",
        "Chi phí mỗi đơn vị tăng 15%",
    ]
    assert_golden("cfo_json", run)


def test_price_what_if_golden(numbers: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    run = run_cli("cfo", "numbers.json", "--price", "40k")
    assert run.exit_code == 0
    assert_golden("cfo_price", run)


def test_volume_what_if_golden(numbers: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    run = run_cli("cfo", "numbers.json", "--volume", "0.5")
    assert run.exit_code == 0
    assert_golden("cfo_volume", run)


def test_below_threshold_has_no_tax(numbers: Path, run_cli: RunCli, assert_golden: Golden) -> None:
    spec = json.loads(numbers.read_text(encoding="utf-8"))
    spec["tax_free_threshold"] = "5 tỷ"
    numbers.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")
    run = run_cli("cfo", "numbers.json")
    assert run.exit_code == 0
    assert "Ngưỡng miễn thuế: 5.000.000.000 đ" in run.stdout
    assert "Thuế doanh thu năm 1: 0 đ" in run.stdout
    assert_golden("cfo_below_threshold", run)


def test_out_writes_cfo_md_under_founder(numbers: Path, run_cli: RunCli) -> None:
    run = run_cli("cfo", "numbers.json", "--out", "cfo.md")
    assert run.exit_code == 0
    assert run.stdout == "Đã ghi founder/cfo.md\n"
    assert run.files["cfo.md"].startswith("# Kinh tế đơn vị:")


def test_out_outside_root_is_refused(
    numbers: Path,
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.chdir(project_root)
    assert main(["cfo", "numbers.json", "--out", "../cfo.md"]) == 2
    assert "path refused" in capsys.readouterr().err
    assert not (project_root / "cfo.md").exists()


def test_missing_field_exits_2_naming_it(
    numbers: Path,
    project_root: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    spec = json.loads(numbers.read_text(encoding="utf-8"))
    del spec["tax_rate_on_revenue"]
    numbers.write_text(json.dumps(spec), encoding="utf-8")
    monkeypatch.chdir(project_root)
    assert main(["cfo", "numbers.json"]) == 2
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "lỗi: thiếu trường 'tax_rate_on_revenue'\n"
