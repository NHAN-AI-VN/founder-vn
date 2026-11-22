"""Each shared fixture works, and none of them reaches the network."""

import socket
from pathlib import Path

import httpx
import pytest

from founder_vn import info


def test_project_root_is_an_empty_temporary_directory(project_root: Path) -> None:
    assert project_root.is_dir()
    assert list(project_root.iterdir()) == []


def test_cli_golden_runner_matches_stdout_and_files(run_cli, assert_golden) -> None:
    run = run_cli("version")
    assert run.exit_code == 0
    assert run.files == {}
    assert_golden("version", run)


def test_cli_golden_runner_detects_a_changed_output(run_cli, assert_golden) -> None:
    run = run_cli("version")
    run.stdout += "extra\n"
    with pytest.raises(AssertionError):
        assert_golden("version", run)


def test_cli_golden_runner_reports_files_written_under_root(run_cli, project_root: Path) -> None:
    from founder_vn import files

    files.write_text(project_root, "a/b.md", "nội dung")
    assert run_cli("version").files == {"a/b.md": "nội dung"}


def test_mcp_stdio_client_calls_server_info(mcp_call) -> None:
    assert mcp_call("server_info", None) == info.version_text()


def test_fake_provider_answers_chat_completions_on_loopback(fake_provider) -> None:
    assert fake_provider.base_url.startswith("http://127.0.0.1:")
    response = httpx.post(
        f"{fake_provider.base_url}/chat/completions",
        json={"model": "m", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert response.status_code == 200
    assert response.json()["choices"][0]["message"]["content"] == "xin chào"
    assert fake_provider.requests[0]["model"] == "m"


def test_network_guard_refuses_a_non_loopback_connection() -> None:
    with pytest.raises(RuntimeError, match="network"):
        socket.socket().connect(("93.184.216.34", 80))
