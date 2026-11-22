"""Installer: copy the packaged skills into a host's project-level skills folder.

Writes only under the host's skills folder inside the project; never deletes.
"""

from pathlib import Path

SKILL_FOLDERS = {
    "kiro": ".kiro/skills",
    "kirocrew": ".kiro/skills",
    "grok": ".grok/skills",
    "claude": ".claude/skills",
    "codex": ".agents/skills",
}
HOSTS = tuple(SKILL_FOLDERS)


def packaged_skills_dir() -> Path:
    """Skills shipped in the wheel (founder_vn/skills), else the repository ``skills/``."""
    here = Path(__file__).parent
    shipped = here / "skills"
    return shipped if shipped.is_dir() else here.parent.parent / "skills"


def _skill_files(skills_dir: Path) -> list[Path]:
    if not skills_dir.is_dir():
        return []
    found = []
    for skill in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()):
        found.extend(sorted(f for f in skill.rglob("*") if f.is_file()))
    return found


def run(project: Path, host: str, print_only: bool, skills_dir: Path | None = None) -> str:
    """Install (or plan) the skills for ``host``; return the text for the Facilitator."""
    source = Path(skills_dir) if skills_dir is not None else packaged_skills_dir()
    files = _skill_files(source)
    lines = [f"founder-vn install: host {host}"]
    if not files:
        lines.append("no skills found in the package; nothing to copy")
        return "\n".join(lines) + "\n"
    folder = SKILL_FOLDERS[host]
    for f in files:
        rel = f.relative_to(source)
        target = Path(project) / folder / rel
        if not print_only:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(f.read_bytes())
        lines.append(f"{folder}/{rel.as_posix()}")
    return "\n".join(lines) + "\n"
