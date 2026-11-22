"""Shared fixtures: temporary project root, CLI golden runner, MCP stdio client, fake provider."""

import json
import socket
import sys
import threading
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

import anyio
import pytest
from mcp import Client, StdioServerParameters

GOLDEN_DIR = Path(__file__).parent / "golden"
LOOPBACK = {"127.0.0.1", "::1", "localhost"}


@pytest.fixture(autouse=True)
def no_external_network(monkeypatch: pytest.MonkeyPatch) -> None:
    """Refuse any socket connection from the test process that is not loopback."""
    real_connect = socket.socket.connect

    def guarded(self: socket.socket, address: Any) -> None:
        if self.family in (socket.AF_INET, socket.AF_INET6) and address[0] not in LOOPBACK:
            raise RuntimeError(f"tests must not use the network: {address[0]}")
        real_connect(self, address)

    monkeypatch.setattr(socket.socket, "connect", guarded)


@pytest.fixture
def project_root(tmp_path: Path) -> Path:
    """A temporary project root; the path-locked layer works under <root>/founder/."""
    return tmp_path


@dataclass
class CliRun:
    exit_code: int
    stdout: str
    files: dict[str, str] = field(default_factory=dict)


@pytest.fixture
def run_cli(
    project_root: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> Callable[..., CliRun]:
    """Run the CLI inside the project root; return exit code, stdout and files under founder/."""
    from founder_vn.cli import main

    monkeypatch.chdir(project_root)

    def run(*args: str) -> CliRun:
        code = main(list(args))
        out = capsys.readouterr().out
        root = project_root / "founder"
        written = {}
        if root.is_dir():
            for path in sorted(p for p in root.rglob("*") if p.is_file()):
                written[path.relative_to(root).as_posix()] = path.read_text(encoding="utf-8")
        return CliRun(code, out, written)

    return run


@pytest.fixture
def assert_golden() -> Callable[[str, CliRun], None]:
    """Compare a CLI run (stdout and written files) with tests/golden/<name>.json."""

    def check(name: str, run: CliRun) -> None:
        expected = json.loads((GOLDEN_DIR / f"{name}.json").read_text(encoding="utf-8"))
        assert {"stdout": run.stdout, "files": run.files} == expected

    return check


@pytest.fixture
def mcp_call(project_root: Path) -> Callable[[str, dict[str, Any] | None], str]:
    """Call a tool of `founder-vn-mcp` over real stdio (subprocess), return its text."""
    params = StdioServerParameters(
        command=sys.executable, args=["-m", "founder_vn.server"], cwd=project_root
    )

    def call(name: str, arguments: dict[str, Any] | None = None) -> str:
        async def run() -> str:
            async with Client(params) as client:
                result = await client.call_tool(name, arguments or {})
                assert not result.is_error
                return "".join(block.text for block in result.content)

        return anyio.run(run)

    return call


@dataclass
class FakeProvider:
    base_url: str
    requests: list[dict[str, Any]] = field(default_factory=list)
    reply: str = "xin chào"


@pytest.fixture
def fake_provider() -> Iterator[FakeProvider]:
    """OpenAI-compatible provider on 127.0.0.1 answering /v1/chat/completions; no network."""
    state = FakeProvider(base_url="")

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self) -> None:
            body = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            if self.path != "/v1/chat/completions":
                self.send_error(404)
                return
            state.requests.append(body)
            payload = json.dumps(
                {
                    "id": "fake-1",
                    "object": "chat.completion",
                    "model": body.get("model", "fake-model"),
                    "choices": [
                        {
                            "index": 0,
                            "message": {"role": "assistant", "content": state.reply},
                            "finish_reason": "stop",
                        }
                    ],
                }
            ).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def log_message(self, format: str, *args: Any) -> None:
            pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    state.base_url = f"http://127.0.0.1:{server.server_address[1]}/v1"
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield state
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
