"""`founder-vn install`: copy packaged skills into the host folder, idempotently."""

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
