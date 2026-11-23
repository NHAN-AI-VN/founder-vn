"""Parity: `founder-vn panel init|tally` and MCP `panel_init|panel_tally` give identical text and files."""

import json
import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

from conftest import CliRun

FIXTURES = Path(__file__).parent / "fixtures"
McpCall = Callable[[str, dict[str, Any] | None], str]


def _restore(project_root: Path, state: dict[str, str]) -> None:
    """Replace founder/ with exactly the files in ``state``."""
    root = project_root / "founder"
    shutil.rmtree(root, ignore_errors=True)
    for name, text in state.items():
        target = root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


def _files(project_root: Path) -> dict[str, str]:
    root = project_root / "founder"
    return {
        p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def _inputs() -> dict[str, str]:
    return {
        "customer.json": (FIXTURES / "panel_customer.json").read_text(encoding="utf-8"),
        "pitch.md": (FIXTURES / "panel_pitch.md").read_text(encoding="utf-8"),
    }


def test_panel_init_cli_equals_mcp_seed_7(
    project_root: Path, run_cli: Callable[..., CliRun], mcp_call: McpCall
) -> None:
    _restore(project_root, _inputs())
    cli = run_cli("panel", "init", "--n", "7", "--seed", "7")
    assert cli.exit_code == 0
    _restore(project_root, _inputs())
    text = mcp_call("panel_init", {"n": 7, "seed": 7})
    assert text == cli.stdout
    assert _files(project_root) == cli.files


def test_panel_tally_cli_equals_mcp_seed_7(
    project_root: Path, run_cli: Callable[..., CliRun], mcp_call: McpCall
) -> None:
    _restore(project_root, _inputs())
    run_cli("panel", "init", "--n", "7", "--seed", "7")
    answers = json.loads((FIXTURES / "panel_answers.json").read_text(encoding="utf-8"))
    for pid, answer in answers.items():
        target = project_root / "founder" / "panel" / "answers" / f"{pid}.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(answer, ensure_ascii=False), encoding="utf-8")
    before = _files(project_root)
    cli = run_cli("panel", "tally")
    assert cli.exit_code == 0
    _restore(project_root, before)
    text = mcp_call("panel_tally", None)
    assert text == cli.stdout
    assert _files(project_root) == cli.files


def test_panel_init_default_n_is_twenty_on_cli_and_mcp(
    project_root: Path, run_cli: Callable[..., CliRun], mcp_call: McpCall
) -> None:
    _restore(project_root, _inputs())
    cli = run_cli("panel", "init", "--seed", "7")
    assert len(json.loads(cli.files["panel/personas.json"])) == 20
    _restore(project_root, _inputs())
    text = mcp_call("panel_init", {"seed": 7})
    assert text == cli.stdout
    assert _files(project_root) == cli.files
