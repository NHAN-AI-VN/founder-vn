"""`founder-vn plan`: the verdict is computed from CFO numbers only (design §3, issue #10)."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from conftest import CliRun

from founder_vn.cli import main

FIXTURES = Path(__file__).parent / "fixtures"
GOLDEN = Path(__file__).parent / "golden"
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


def _panel(project_root: Path, **changes: Any) -> dict[str, Any]:
    """File the `panel/results.json` of the T07 golden run, with ``changes`` applied."""
    golden = json.loads((GOLDEN / "panel_tally.json").read_text(encoding="utf-8"))
    results = {**json.loads(golden["files"]["panel/results.json"]), **changes}
    target = project_root / "founder" / "panel" / "results.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    (target.parent / "results.md").write_text(golden["files"]["panel/results.md"], encoding="utf-8")
    return results


def test_panel_line_shows_buys_passes_mode_and_model(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    _panel(project_root, mode="llm", model="mo-hinh-gia")
    plan = run_cli("plan").files["business-plan.md"]
    assert (
        "Tín hiệu cầu (mô phỏng, cận trên): 3 mua, 2 không mua; chế độ llm; mô hình mo-hinh-gia."
        in plan
    )


@pytest.mark.parametrize("buys", [0, 5], ids=["nobody-buys", "everybody-buys"])
def test_panel_never_changes_the_verdict(buys: int, project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    without = _verdict(run_cli("plan"))
    _panel(project_root, buys=buys, passes=5 - buys, buy_rate=buys / 5)
    assert _verdict(run_cli("plan")) == without
    _numbers(project_root, price="10k")
    assert _verdict(run_cli("plan")).startswith("Kết luận: Not yet")


def test_panel_line_without_panel_says_not_run(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    assert (
        "Tín hiệu cầu (mô phỏng, cận trên): chưa chạy panel."
        in (run_cli("plan").files["business-plan.md"])
    )


def test_panel_results_without_buys_is_an_error_naming_it(
    project_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _numbers(project_root)
    results = _panel(project_root)
    del results["buys"]
    (project_root / "founder" / "panel" / "results.json").write_text(json.dumps(results))
    monkeypatch.chdir(project_root)
    assert main(["plan"]) == 2
    assert "buys" in capsys.readouterr().err


def test_key_numbers_table_is_in_vnd(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    plan = run_cli("plan").files["business-plan.md"]
    assert "| Giá bán (khách trả) | 45.000 đ |" in plan
    assert "| Đóng góp mỗi ly | 28.500 đ |" in plan
    assert "| Lợi nhuận hoạt động năm 1 sau thuế | 342.761.250 đ |" in plan
    assert "$" not in plan


def test_sections_follow_pipeline_order_and_missing_ones_name_their_skill(
    project_root: Path, run_cli: RunCli
) -> None:
    _numbers(project_root)
    (project_root / "founder" / "pricing.md").write_text("# Giá\n\nGiá hợp lý.\n", encoding="utf-8")
    (project_root / "founder" / "board.md").write_text("# Hội đồng\n\nÝ kiến.\n", encoding="utf-8")
    plan = run_cli("plan").files["business-plan.md"]
    assert plan.index("## Hội đồng cố vấn") < plan.index("## Giá")
    assert "### Hội đồng\n" in plan
    todo = plan[plan.index("## Chưa làm") :]
    assert "`founder-competitors`" in todo and "`founder-marketing`" in todo
    assert "`founder-board`" not in todo and "`founder-pricing`" not in todo
    assert plan.rstrip().endswith("không phải khách hàng thật.")


def test_plan_golden_full_state(
    project_root: Path, run_cli: RunCli, assert_golden: Callable[[str, CliRun], None]
) -> None:
    _numbers(project_root)
    _panel(project_root)
    run_cli("cfo", "numbers.json", "--out", "cfo.md")
    assert_golden("plan_full", run_cli("plan"))


def test_plan_golden_numbers_only(
    project_root: Path, run_cli: RunCli, assert_golden: Callable[[str, CliRun], None]
) -> None:
    _numbers(project_root)
    assert_golden("plan_numbers_only", run_cli("plan"))


def test_check_is_0_when_current_and_writes_nothing(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    run_cli("plan")
    before = (project_root / "founder" / "business-plan.md").stat().st_mtime_ns
    run = run_cli("plan", "--check")
    assert run.exit_code == 0
    assert run.stdout == "business-plan.md khớp với các file hiện có\n"
    assert (project_root / "founder" / "business-plan.md").stat().st_mtime_ns == before


def test_check_is_1_when_missing_and_creates_nothing(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    run = run_cli("plan", "--check")
    assert run.exit_code == 1
    assert run.stdout == "business-plan.md chưa có: chạy `founder-vn plan`\n"
    assert "business-plan.md" not in run.files


def test_check_is_1_when_a_source_changed_since(project_root: Path, run_cli: RunCli) -> None:
    _numbers(project_root)
    run_cli("plan")
    _numbers(project_root, price="10k")
    run = run_cli("plan", "--check")
    assert run.exit_code == 1
    assert run.stdout == "business-plan.md đã cũ so với các file hiện có: chạy `founder-vn plan`\n"
