"""Parity: the CLI and the MCP server wrap one function and print byte-identical text."""

import anyio
import pytest
from mcp import Client

from founder_vn import __version__, info
from founder_vn.server import mcp as server


def mcp_tool_text(name: str) -> str:
    async def call() -> str:
        async with Client(server) as client:
            result = await client.call_tool(name, {})
            assert not result.is_error
            assert len(result.content) == 1
            return result.content[0].text

    return anyio.run(call)


def test_version_text_names_the_package_version() -> None:
    assert info.version_text() == f"founder-vn {__version__}"


def test_cli_version_equals_mcp_server_info(capsys: pytest.CaptureFixture[str]) -> None:
    from founder_vn.cli import main

    assert main(["version"]) == 0
    cli_text = capsys.readouterr().out
    assert cli_text == info.version_text() + "\n"
    assert mcp_tool_text("server_info") == cli_text.removesuffix("\n")


def test_cli_dash_dash_version_equals_version_command(capsys: pytest.CaptureFixture[str]) -> None:
    from founder_vn.cli import main

    assert main(["version"]) == 0
    expected = capsys.readouterr().out
    assert main(["--version"]) == 0
    assert capsys.readouterr().out == expected
