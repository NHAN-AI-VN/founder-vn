"""`founder-vn install`: copy packaged skills into the host folder, idempotently."""

import json
import tomllib
from pathlib import Path

import pytest

from founder_vn import install

SRC = Path(__file__).parent / "fixtures" / "skills_src"

FOLDERS = {
    "kiro": ".kiro/skills",
    "kirocrew": ".kiro/skills",
    "grok": ".grok/skills",
    "claude": ".claude/skills",
    "codex": ".agents/skills",
}


@pytest.mark.parametrize("host", sorted(FOLDERS))
def test_install_copies_skills_into_the_host_folder(host: str, project_root: Path) -> None:
    text = install.run(project_root, host, print_only=False, skills_dir=SRC)
    base = project_root / FOLDERS[host] / "founder-demo"
    assert (base / "SKILL.md").read_text(encoding="utf-8").startswith("---\nname: founder-demo")
    assert (base / "refs" / "a.md").read_text(encoding="utf-8") == "ref\n"
    assert f"create     {FOLDERS[host]}/founder-demo/SKILL.md" in text


def test_install_with_no_skills_says_so_and_does_not_crash(
    project_root: Path, tmp_path: Path
) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    text = install.run(project_root, "kiro", print_only=False, skills_dir=empty)
    assert "no skills found" in text
    assert not (project_root / ".kiro" / "skills").exists()


def test_install_is_idempotent_and_reports_unchanged(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    target = project_root / ".kiro/skills/founder-demo/SKILL.md"
    before = target.stat().st_mtime_ns
    text = install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert "unchanged  .kiro/skills/founder-demo/SKILL.md" in text
    assert target.stat().st_mtime_ns == before


def test_install_updates_a_changed_file_and_keeps_unrelated_files(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    skill = project_root / ".kiro/skills/founder-demo/SKILL.md"
    skill.write_text("old", encoding="utf-8")
    keep = project_root / ".kiro/skills/mine/SKILL.md"
    keep.parent.mkdir(parents=True)
    keep.write_text("mine", encoding="utf-8")
    text = install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert "update     .kiro/skills/founder-demo/SKILL.md" in text
    assert skill.read_text(encoding="utf-8").startswith("---")
    assert keep.read_text(encoding="utf-8") == "mine"


def test_print_only_plans_without_writing(project_root: Path) -> None:
    text = install.run(project_root, "codex", print_only=True, skills_dir=SRC)
    assert "create     .agents/skills/founder-demo/SKILL.md" in text
    assert list(project_root.iterdir()) == []


def test_install_refuses_a_symlink_that_escapes_the_project(
    project_root: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    outside = tmp_path_factory.mktemp("outside")
    (project_root / ".kiro").mkdir()
    (project_root / ".kiro" / "skills").symlink_to(outside, target_is_directory=True)
    with pytest.raises(install.InstallRefused):
        install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert list(outside.iterdir()) == []


def test_default_source_is_the_packaged_skills_folder() -> None:
    assert install.packaged_skills_dir().name == "skills"


def test_pyproject_ships_skills_in_the_wheel() -> None:
    import tomllib

    root = Path(__file__).parent.parent
    wheel = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["hatch"][
        "build"
    ]["targets"]["wheel"]
    assert wheel["force-include"]["skills"] == "founder_vn/skills"


def test_kiro_writes_the_registration_file_when_absent(project_root: Path) -> None:
    text = install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    written = project_root / ".kiro/settings/mcp.json"
    entry = json.loads(written.read_text(encoding="utf-8"))["mcpServers"]["founder-vn"]
    assert entry == {"command": "uvx", "args": ["--from", "founder-vn", "founder-vn-mcp"]}
    assert "create     .kiro/settings/mcp.json" in text


def test_kiro_leaves_an_existing_registration_file_byte_unchanged(project_root: Path) -> None:
    existing = project_root / ".kiro/settings/mcp.json"
    existing.parent.mkdir(parents=True)
    existing.write_bytes(b'{"mcpServers": {"mine": {}}}')
    text = install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert existing.read_bytes() == b'{"mcpServers": {"mine": {}}}'
    assert "exists     .kiro/settings/mcp.json (not modified)" in text
    assert '"founder-vn"' in text


def test_print_only_writes_no_registration_file(project_root: Path) -> None:
    text = install.run(project_root, "kiro", print_only=True, skills_dir=SRC)
    assert "create     .kiro/settings/mcp.json" in text
    assert list(project_root.iterdir()) == []


def test_kirocrew_has_no_registration_file(project_root: Path) -> None:
    text = install.run(project_root, "kirocrew", print_only=False, skills_dir=SRC)
    assert not (project_root / ".kiro/settings").exists()
    assert "mcp.json (" not in text and "create     .kiro/settings" not in text


def test_registration_file_through_an_escaping_symlink_is_refused(
    project_root: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    outside = tmp_path_factory.mktemp("outside")
    (project_root / ".kiro").mkdir()
    (project_root / ".kiro" / "settings").symlink_to(outside, target_is_directory=True)
    with pytest.raises(install.InstallRefused):
        install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert list(outside.iterdir()) == []


@pytest.mark.parametrize(
    ("host", "rel"),
    [("claude", ".mcp.json"), ("codex", ".codex/config.toml"), ("grok", ".grok/config.toml")],
)
def test_project_file_hosts_write_when_absent_and_print_when_present(
    host: str, rel: str, project_root: Path
) -> None:
    text = install.run(project_root, host, print_only=False, skills_dir=SRC)
    target = project_root / rel
    assert f"create     {rel}" in text
    body = target.read_text(encoding="utf-8")
    parsed = json.loads(body) if rel.endswith(".json") else tomllib.loads(body)
    servers = parsed["mcpServers" if rel.endswith(".json") else "mcp_servers"]
    assert servers["founder-vn"]["args"] == ["--from", "founder-vn", "founder-vn-mcp"]
    if host == "codex":
        assert servers["founder-vn"]["tool_timeout_sec"] == 300
    target.write_bytes(b"mine")
    again = install.run(project_root, host, print_only=False, skills_dir=SRC)
    assert target.read_bytes() == b"mine"
    assert f"exists     {rel} (not modified)" in again and "founder-vn" in again
    assert "~/" not in again.split("MCP registration", 1)[1].splitlines()[0]


LEDGER = Path(__file__).parent.parent / "permits" / "sources.md"


def test_pyproject_ships_the_ledger_in_the_wheel() -> None:
    root = Path(__file__).parent.parent
    wheel = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))["tool"]["hatch"][
        "build"
    ]["targets"]["wheel"]
    assert wheel["force-include"]["permits/sources.md"] == "founder_vn/permits/sources.md"


def test_default_ledger_is_the_repository_ledger_when_not_packaged() -> None:
    assert install.packaged_ledger().read_bytes() == LEDGER.read_bytes()


@pytest.mark.parametrize("host", sorted(FOLDERS))
def test_every_host_writes_the_ledger_on_an_empty_project(host: str, project_root: Path) -> None:
    text = install.run(project_root, host, print_only=False, skills_dir=SRC)
    assert (project_root / "permits/sources.md").read_bytes() == LEDGER.read_bytes()
    assert "create     permits/sources.md" in text


def test_second_run_reports_the_ledger_unchanged(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    text = install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert "unchanged  permits/sources.md" in text


def test_a_differing_ledger_is_updated_and_other_permits_files_are_kept(
    project_root: Path,
) -> None:
    target = project_root / "permits/sources.md"
    target.parent.mkdir()
    target.write_text("local edit", encoding="utf-8")
    other = project_root / "permits/notes.md"
    other.write_text("mine", encoding="utf-8")
    text = install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert "update     permits/sources.md" in text
    assert target.read_bytes() == LEDGER.read_bytes()
    assert other.read_text(encoding="utf-8") == "mine"


def test_print_only_plans_the_ledger_and_writes_nothing(project_root: Path) -> None:
    text = install.run(project_root, "kirocrew", print_only=True, skills_dir=SRC)
    assert "create     permits/sources.md" in text
    assert list(project_root.iterdir()) == []


def test_ledger_through_an_escaping_symlink_is_refused(
    project_root: Path, tmp_path_factory: pytest.TempPathFactory
) -> None:
    outside = tmp_path_factory.mktemp("outside")
    (project_root / "permits").symlink_to(outside, target_is_directory=True)
    with pytest.raises(install.InstallRefused):
        install.run(project_root, "kiro", print_only=False, skills_dir=SRC)
    assert list(outside.iterdir()) == []
    assert not (project_root / ".kiro").exists()


def test_design_and_standards_record_q57() -> None:
    root = Path(__file__).parent.parent
    design = (root / "docs" / "founder-vn-design.md").read_text(encoding="utf-8")
    assert "(Q1–Q57)" in design and "\n- Q57 (2026-11-27" in design
    assert "ghi sổ nguồn `permits/sources.md` của gói vào dự án (Q57)" in design
    standards = (root / "docs" / "agents" / "standards.md").read_text(encoding="utf-8")
    assert "`<project>/permits/sources.md`" in standards and "(Q57, #142.)" in standards
