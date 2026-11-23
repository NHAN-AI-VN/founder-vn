"""Parity: `founder-vn pricing` and MCP `pricing_psm` print identical text and write identical files."""

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest
from conftest import CliRun

FIXTURE = Path(__file__).parent / "fixtures" / "pricing_input.json"

CASES = [
    pytest.param(["pricing_input.json"], {"source": "pricing_input.json"}, id="report"),
    pytest.param(
        ["pricing_input.json", "--json"],
        {"source": "pricing_input.json", "as_json": True},
        id="json",
    ),
    pytest.param(
        ["pricing_input.json", "--out", "pricing.md"],
        {"source": "pricing_input.json", "out": "pricing.md"},
        id="out",
    ),
]


@pytest.mark.parametrize(("cli_args", "tool_args"), CASES)
def test_pricing_cli_equals_mcp(
    cli_args: list[str],
    tool_args: dict[str, Any],
    project_root: Path,
    run_cli: Callable[..., CliRun],
    mcp_call: Callable[[str, dict[str, Any] | None], str],
) -> None:
    source = project_root / "founder" / "pricing_input.json"
    source.parent.mkdir()
    shutil.copy(FIXTURE, source)

    cli = run_cli("pricing", *cli_args)
    assert cli.exit_code == 0
    cli_files = dict(cli.files)

    shutil.rmtree(project_root / "founder")
    source.parent.mkdir()
    shutil.copy(FIXTURE, source)
    mcp_text = mcp_call("pricing_psm", tool_args)
    mcp_files = {
        p.relative_to(project_root / "founder").as_posix(): p.read_text(encoding="utf-8")
        for p in sorted((project_root / "founder").rglob("*"))
        if p.is_file()
    }

    assert mcp_text == cli.stdout
    assert mcp_files == cli_files
