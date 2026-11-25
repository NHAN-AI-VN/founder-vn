"""Golden tests of `founder-vn install --print-only` per host, and the CLI contract."""

from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import CliRun

from founder_vn import install

SRC = Path(__file__).parent / "fixtures" / "skills_src"
RunCli = Callable[..., CliRun]


@pytest.fixture(autouse=True)
def synthetic_package_skills(monkeypatch: pytest.MonkeyPatch) -> None:
    """The CLI has no source flag; point the packaged-skills lookup at the synthetic fixture."""
    monkeypatch.setattr(install, "packaged_skills_dir", lambda: SRC)


Golden = Callable[[str, CliRun], None]


@pytest.mark.parametrize("host", ["kiro", "claude", "codex", "grok", "kirocrew"])
def test_print_only_golden(
    host: str, project_root: Path, run_cli: RunCli, assert_golden: Golden
) -> None:
    run = run_cli("install", "--host", host, "--print-only")
    assert run.exit_code == 0
    assert "$" not in run.stdout
    assert str(SRC) not in run.stdout
    assert list(project_root.iterdir()) == []
    assert_golden(f"install_{host}", run)


def test_codex_snippet_carries_the_timeout_note(run_cli: RunCli) -> None:
    run = run_cli("install", "--host", "codex", "--print-only")
    assert "60 seconds" in run.stdout and "tool_timeout_sec" in run.stdout


def test_kirocrew_snippet_names_dashboard_and_trust(run_cli: RunCli) -> None:
    run = run_cli("install", "--host", "kirocrew", "--print-only")
    assert "dashboard" in run.stdout and "Trust the project" in run.stdout


def test_snippets_name_env_variables_without_values(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "synthetic-secret-value")
    for host in install.HOSTS:
        text = install.run(Path("."), host, print_only=True, skills_dir=SRC)
        assert "FOUNDER_LLM_API_KEY" in text
        assert "synthetic-secret-value" not in text


def test_gemini_is_not_a_host_value(run_cli: RunCli, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        run_cli("install", "--host", "gemini")


def test_cli_refusal_exits_2(
    project_root: Path, tmp_path_factory: pytest.TempPathFactory, run_cli: RunCli
) -> None:
    (project_root / ".kiro").mkdir()
    (project_root / ".kiro" / "skills").symlink_to(
        tmp_path_factory.mktemp("out"), target_is_directory=True
    )
    assert run_cli("install", "--host", "kiro").exit_code == 2


def test_cli_install_writes_the_registration_file_on_a_clean_project(
    project_root: Path, run_cli: RunCli
) -> None:
    assert run_cli("install", "--host", "kiro").exit_code == 0
    assert (project_root / ".kiro/settings/mcp.json").is_file()
