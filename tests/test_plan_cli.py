"""`founder-vn plan`: the verdict is computed from CFO numbers only (design §3, issue #10)."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from conftest import CliRun
from founder_vn.cli import main

FIXTURES = Path(__file__).parent / "fixtures"
RunCli = Callable[..., CliRun]


def _numbers(project_root: Path, **changes: Any) -> None:
    spec = json.loads((FIXTURES / "cfo_numbers.json").read_text(encoding="utf-8"))
    spec.update(changes)
    target = project_root / "founder" / "numbers.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(spec, ensure_ascii=False), encoding="utf-8")


def _verdict(run: CliRun) -> str:
    return run.stdout.splitlines()[0]


def test_no_numbers_is_incomplete(project_root: Path, run_cli: RunCli) -> None:
    run = run_cli("plan")
    assert run.exit_code == 0
    assert _verdict(run).startswith("Kết luận: Incomplete")
    assert "Chưa có số của CFO" in run.files["business-plan.md"]


def test_all_three_checks_pass_is_profitable(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    run = run_cli("plan")
    assert _verdict(run).startswith("Kết luận: Profitable")


@pytest.mark.parametrize(
    ("changes", "failed"),
    [
        pytest.param({"price": "10k"}, "Đóng góp mỗi ly lớn hơn 0", id="contribution"),
        pytest.param(
            {"price": "17k", "ramp_per_day": [5] * 12, "plan_per_day": 5},
            "Lợi nhuận hoạt động năm 1 sau thuế lớn hơn 0",
            id="year1-profit",
        ),
        pytest.param(
            {"capacity_per_day": 10}, "Hòa vốn không vượt công suất", id="break-even-capacity"
        ),
    ],
)
def test_each_failed_check_is_not_yet_and_named(
    changes: dict[str, Any], failed: str, project_root: Path, run_cli: RunCli
) -> None:
    _numbers(project_root, **changes)
    run = run_cli("plan")
    assert _verdict(run).startswith("Kết luận: Not yet")
    assert f"| {failed} | Không đạt |" in run.files["business-plan.md"]


def test_missing_numeric_field_is_an_error_naming_it(
    project_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _numbers(project_root)
    path = project_root / "founder" / "numbers.json"
    spec = json.loads(path.read_text(encoding="utf-8"))
    del spec["tax_rate_on_revenue"]
    path.write_text(json.dumps(spec), encoding="utf-8")
    monkeypatch.chdir(project_root)
    assert main(["plan"]) == 2
    assert "tax_rate_on_revenue" in capsys.readouterr().err
    assert not (project_root / "founder" / "business-plan.md").exists()
