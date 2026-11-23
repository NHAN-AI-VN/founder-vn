"""Parity: `founder-vn panel init|tally` and MCP `panel_init|panel_tally` give identical text and files."""

import json
import os
import re
import shutil
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any

import anyio
import pytest
from conftest import CliRun, FakeProvider
from mcp import Client, StdioServerParameters

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


def _poll(call: Callable[[], str]) -> str:
    """Call until the job leaves `running`; return the last status text."""
    text = call()
    for _ in range(100):
        if json.loads(text)["state"] != "running":
            break
        time.sleep(0.1)
        text = call()
    return text


def _mcp_run_and_poll(project_root: Path) -> tuple[str, str, str]:
    """One MCP session (the job lives in the server process): `panel_run`, then `job_status`
    until the job is no longer running. Returns the run text, the job id and the last status."""
    env = {k: v for k, v in os.environ.items() if k.startswith("FOUNDER_LLM_")}
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "founder_vn.server"], cwd=project_root, env=env
    )

    async def session() -> tuple[str, str, str]:
        async with Client(params) as client:

            async def call(name: str, arguments: dict[str, Any]) -> str:
                result = await client.call_tool(name, arguments)
                assert not result.is_error
                return "".join(block.text for block in result.content)

            started = await call("panel_run", {})
            job_id = json.loads(started)["job_id"]
            text = await call("job_status", {"job_id": job_id})
            for _ in range(100):
                if json.loads(text)["state"] != "running":
                    break
                await anyio.sleep(0.1)
                text = await call("job_status", {"job_id": job_id})
            return started, job_id, text

    return anyio.run(session)


def test_panel_run_and_job_status_cli_equals_mcp_seed_7(
    project_root: Path,
    run_cli: Callable[..., CliRun],
    monkeypatch: pytest.MonkeyPatch,
    fake_provider: FakeProvider,
) -> None:
    monkeypatch.setenv("FOUNDER_LLM_BASE_URL", fake_provider.base_url)
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "khoa-gia")
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")

    def script(body: dict, n: int) -> tuple[int, str, float]:
        pid = re.search(r'"id": "(P\d+)"', body["messages"][0]["content"]).group(1)  # type: ignore[union-attr]
        answer = {"id": pid, "buys": pid != "P003", "reason_code": "need", "reason": "Vậy."}
        return 200, json.dumps(answer, ensure_ascii=False), 0.0

    fake_provider.script = script

    def settled(text: str, job_id: str) -> str:
        return text.replace(job_id, "J-xxxxxxxx")

    def stable_files() -> dict[str, str]:
        return {k: v for k, v in _files(project_root).items() if not k.startswith("panel/jobs/")}

    _restore(project_root, _inputs())
    run_cli("panel", "init", "--n", "7", "--seed", "7")
    cli_run = run_cli("panel", "run")
    cli_id = json.loads(cli_run.stdout)["job_id"]
    cli_status = _poll(lambda: run_cli("panel", "status", cli_id).stdout)
    cli_files = stable_files()

    _restore(project_root, _inputs())
    run_cli("panel", "init", "--n", "7", "--seed", "7")
    mcp_run, mcp_id, mcp_status = _mcp_run_and_poll(project_root)

    assert settled(mcp_run, mcp_id) == settled(cli_run.stdout, cli_id)
    assert settled(mcp_status, mcp_id) == settled(cli_status, cli_id)
    assert json.loads(cli_status)["done"] == 7
    assert stable_files() == cli_files
