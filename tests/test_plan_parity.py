"""Parity: `founder-vn plan` and MCP `plan_compile` print identical text and write identical files."""

import json
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from conftest import CliRun

FIXTURES = Path(__file__).parent / "fixtures"
GOLDEN = Path(__file__).parent / "golden"
McpCall = Callable[[str, dict[str, Any] | None], str]


def _state(project_root: Path, *, panel: bool) -> dict[str, str]:
    root = project_root / "founder"
    shutil.rmtree(root, ignore_errors=True)
    root.mkdir()
    state = {"numbers.json": (FIXTURES / "cfo_numbers.json").read_text(encoding="utf-8")}
    if panel:
        golden = json.loads((GOLDEN / "panel_tally.json").read_text(encoding="utf-8"))
        state["panel/results.json"] = golden["files"]["panel/results.json"]
        state["panel/results.md"] = golden["files"]["panel/results.md"]
    for name, text in state.items():
        (root / name).parent.mkdir(parents=True, exist_ok=True)
        (root / name).write_text(text, encoding="utf-8")
    return state


def _files(project_root: Path) -> dict[str, str]:
    root = project_root / "founder"
    return {
        p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


@pytest.mark.parametrize("panel", [False, True], ids=["numbers-only", "with-panel"])
def test_plan_cli_equals_mcp(
    panel: bool, project_root: Path, run_cli: Callable[..., CliRun], mcp_call: McpCall
) -> None:
    _state(project_root, panel=panel)
    cli = run_cli("plan")
    assert cli.exit_code == 0
    _state(project_root, panel=panel)
    text = mcp_call("plan_compile", None)
    assert text == cli.stdout
    assert _files(project_root) == cli.files


def test_plan_check_cli_equals_mcp(
    project_root: Path, run_cli: Callable[..., CliRun], mcp_call: McpCall
) -> None:
    _state(project_root, panel=True)
    run_cli("plan")
    before = _files(project_root)
    cli = run_cli("plan", "--check")
    assert cli.exit_code == 0
    text = mcp_call("plan_compile", {"check": True})
    assert text == cli.stdout
    assert _files(project_root) == before


def test_plan_with_permits_section_cli_equals_mcp(
    project_root: Path, run_cli: Callable[..., CliRun], mcp_call: McpCall
) -> None:
    permits = "# Thuế\n\nHộ kinh doanh.\n"

    def prepare() -> None:
        _state(project_root, panel=False)
        (project_root / "founder" / "permits.md").write_text(permits, encoding="utf-8")

    prepare()
    cli = run_cli("plan")
    assert "## Giấy phép và thuế\n\n### Thuế\n" in cli.files["business-plan.md"]
    prepare()
    assert mcp_call("plan_compile", None) == cli.stdout
    assert _files(project_root) == cli.files
