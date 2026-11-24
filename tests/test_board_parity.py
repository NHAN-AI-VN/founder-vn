"""Parity: `founder-vn board run` and MCP `board_run` give identical text, files and job status."""

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

BRIEF = "# Brief\n\nTiệm cắt tóc nam, 4 ghế, giá trọn gói 199.000 đ, Quận 7 cũ.\n"


def _restore(project_root: Path) -> None:
    root = project_root / "founder"
    shutil.rmtree(root, ignore_errors=True)
    (root / "board").mkdir(parents=True)
    (root / "board" / "brief.md").write_text(BRIEF, encoding="utf-8")


def _files(project_root: Path) -> dict[str, str]:
    root = project_root / "founder"
    return {
        p.relative_to(root).as_posix(): p.read_text(encoding="utf-8")
        for p in sorted(root.rglob("*"))
        if p.is_file() and "/jobs/" not in p.as_posix()
    }


def _poll(call: Callable[[], str]) -> str:
    text = call()
    for _ in range(100):
        if json.loads(text)["state"] != "running":
            break
        time.sleep(0.1)
        text = call()
    return text


def _mcp_run_and_poll(project_root: Path) -> tuple[str, str, str]:
    """One MCP session (the job lives in the server process): `board_run`, then `job_status`."""
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

            started = await call("board_run", {})
            job_id = json.loads(started)["job_id"]
            text = await call("job_status", {"job_id": job_id})
            for _ in range(100):
                if json.loads(text)["state"] != "running":
                    break
                await anyio.sleep(0.1)
                text = await call("job_status", {"job_id": job_id})
            return started, job_id, text

    return anyio.run(session)


def test_board_run_and_job_status_cli_equals_mcp(
    project_root: Path,
    run_cli: Callable[..., CliRun],
    monkeypatch: pytest.MonkeyPatch,
    fake_provider: FakeProvider,
) -> None:
    monkeypatch.setenv("FOUNDER_LLM_BASE_URL", fake_provider.base_url)
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "khoa-gia")
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")

    def script(body: dict, n: int) -> tuple[int, str, float]:
        lens = re.search(r"Mã lens: (\w+)", body["messages"][0]["content"]).group(1)  # type: ignore[union-attr]
        memo = {
            "score": 6,
            "vote": "conditional",
            "strong": [f"{lens} mạnh"],
            "would_kill": [f"{lens} yếu"],
            "questions": [],
            "conditions": [f"{lens} điều kiện"],
        }
        return 200, json.dumps(memo, ensure_ascii=False), 0.0

    fake_provider.script = script

    def settled(text: str, job_id: str) -> str:
        return text.replace(job_id, "J-xxxxxxxx")

    _restore(project_root)
    cli_run = run_cli("board", "run")
    assert cli_run.exit_code == 0
    cli_id = json.loads(cli_run.stdout)["job_id"]
    cli_status = _poll(lambda: run_cli("panel", "status", cli_id).stdout)
    cli_files = _files(project_root)

    _restore(project_root)
    mcp_run, mcp_id, mcp_status = _mcp_run_and_poll(project_root)

    assert settled(mcp_run, mcp_id) == settled(cli_run.stdout, cli_id)
    assert settled(mcp_status, mcp_id) == settled(cli_status, cli_id)
    assert json.loads(cli_status)["done"] == 3
    assert sorted(cli_files) == [
        "board/board.json",
        "board/brief.md",
        "board/offers.json",
        "board/offers.md",
        "board/product.json",
        "board/product.md",
        "board/systems.json",
        "board/systems.md",
    ]
    assert _files(project_root) == cli_files


def test_board_run_without_a_brief_exits_2_naming_the_file(
    project_root: Path, run_cli: Callable[..., CliRun], capsys: pytest.CaptureFixture[str]
) -> None:
    from founder_vn.cli import main

    assert main(["board", "run"]) == 2
    assert "board/brief.md" in capsys.readouterr().err
