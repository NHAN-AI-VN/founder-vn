"""Parity: `founder-vn cfo` and MCP `cfo_analyse` print identical text and write identical files."""

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from conftest import CliRun

FIXTURE = Path(__file__).parent / "fixtures" / "cfo_numbers.json"

CASES = [
    pytest.param(["numbers.json"], {"numbers": "numbers.json"}, id="report"),
    pytest.param(
        ["numbers.json", "--json"], {"numbers": "numbers.json", "as_json": True}, id="json"
    ),
    pytest.param(
        ["numbers.json", "--price", "40k", "--volume", "0.8"],
        {"numbers": "numbers.json", "price": "40k", "volume": 0.8},
        id="what-if",
    ),
    pytest.param(
        ["numbers.json", "--out", "cfo.md"], {"numbers": "numbers.json", "out": "cfo.md"}, id="out"
    ),
]


@pytest.mark.parametrize(("cli_args", "tool_args"), CASES)
def test_cfo_cli_equals_mcp(
    cli_args: list[str],
    tool_args: dict[str, Any],
    project_root: Path,
    run_cli: Callable[..., CliRun],
    mcp_call: Callable[[str, dict[str, Any] | None], str],
) -> None:
    numbers = project_root / "founder" / "numbers.json"
    numbers.parent.mkdir()
    shutil.copy(FIXTURE, numbers)

    cli = run_cli("cfo", *cli_args)
    assert cli.exit_code == 0
    cli_files = dict(cli.files)

    shutil.rmtree(project_root / "founder")
    numbers.parent.mkdir()
    shutil.copy(FIXTURE, numbers)
    mcp_text = mcp_call("cfo_analyse", tool_args)
    mcp_files = {
        p.relative_to(project_root / "founder").as_posix(): p.read_text(encoding="utf-8")
        for p in sorted((project_root / "founder").rglob("*"))
        if p.is_file()
    }

    assert mcp_text == cli.stdout
    assert mcp_files == cli_files
