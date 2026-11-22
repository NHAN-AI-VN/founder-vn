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
    assert f"{FOLDERS[host]}/founder-demo/SKILL.md" in text


def test_install_with_no_skills_says_so_and_does_not_crash(
    project_root: Path, tmp_path: Path
) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()
    text = install.run(project_root, "kiro", print_only=False, skills_dir=empty)
    assert "no skills found" in text
    assert not (project_root / ".kiro" / "skills").exists()
