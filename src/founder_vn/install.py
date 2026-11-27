"""Installer: copy the packaged skills into a host's project-level skills folder.

Writes only inside the project: the host's skills folder, the packaged source ledger
``permits/sources.md`` (Q57; created or updated like a skill file) and, for hosts whose MCP
registration is a project file, that file when it is absent (Q54). Never merges into an
existing file; never deletes.
"""

import os
from pathlib import Path

SKILL_FOLDERS = {
    "kiro": ".kiro/skills",
    "kirocrew": ".kiro/skills",
    "grok": ".grok/skills",
    "claude": ".claude/skills",
    "codex": ".agents/skills",
}
HOSTS = tuple(SKILL_FOLDERS)
LEDGER_PATH = "permits/sources.md"


class InstallRefused(ValueError):
    """A target resolves outside the project (``..`` or a symlink escape)."""


_ENV_NOTE = (
    "Model calls read FOUNDER_LLM_BASE_URL, FOUNDER_LLM_API_KEY and FOUNDER_LLM_MODEL from the\n"
    "host environment. Set them there; never write their values into a config file or the repository.\n"
)

_JSON_SERVER = """{
  "mcpServers": {
    "founder-vn": {
      "command": "uvx",
      "args": ["--from", "founder-vn", "founder-vn-mcp"]
    }
  }
}
"""

_TOML_SERVER = """[mcp_servers.founder-vn]
command = "uvx"
args = ["--from", "founder-vn", "founder-vn-mcp"]
"""

REGISTRATION_FILES = {
    "kiro": (".kiro/settings/mcp.json", _JSON_SERVER),
    "claude": (".mcp.json", _JSON_SERVER),
    "codex": (".codex/config.toml", _TOML_SERVER + "tool_timeout_sec = 300\n"),
    "grok": (".grok/config.toml", _TOML_SERVER),
}

SNIPPETS = {
    "kiro": (
        "MCP registration: .kiro/settings/mcp.json (workspace; written when absent, never merged):\n\n"
        + _JSON_SERVER
    ),
    "claude": (
        "MCP registration: .mcp.json at the project root (written when absent, never merged):\n\n"
        + _JSON_SERVER
        + "\nor run: claude mcp add --scope project founder-vn -- uvx --from founder-vn founder-vn-mcp\n"
    ),
    "codex": (
        "MCP registration: .codex/config.toml at the project root (Codex loads it for a trusted project):\n\n"
        + _TOML_SERVER
        + "tool_timeout_sec = 300\n\n"
        "Codex stops a tool call after 60 seconds by default; tool_timeout_sec raises that limit\n"
        "for long panel jobs.\n"
    ),
    "grok": ("MCP registration: .grok/config.toml at the project root:\n\n" + _TOML_SERVER),
    "kirocrew": (
        "MCP registration (dashboard, no file to edit):\n"
        "  1. Open the KiroCrew dashboard, MCP Servers page, and add a server.\n"
        "  2. Name: founder-vn. Command: uvx. Arguments: --from founder-vn founder-vn-mcp.\n"
        "  3. Trust the project in KiroCrew; it loads skills and servers only for a trusted project.\n"
        "KiroCrew does not read the workspace .kiro/settings/mcp.json.\n"
    ),
}


def packaged_skills_dir() -> Path:
    """Skills shipped in the wheel (founder_vn/skills), else the repository ``skills/``."""
    here = Path(__file__).parent
    shipped = here / "skills"
    return shipped if shipped.is_dir() else here.parent.parent / "skills"


def packaged_ledger() -> Path:
    """Ledger shipped in the wheel (founder_vn/permits/sources.md), else the repository's."""
    here = Path(__file__).parent
    shipped = here / "permits" / "sources.md"
    return shipped if shipped.is_file() else here.parent.parent / "permits" / "sources.md"


def _skill_files(skills_dir: Path) -> list[Path]:
    if not skills_dir.is_dir():
        return []
    found = []
    for skill in sorted(p for p in skills_dir.iterdir() if (p / "SKILL.md").is_file()):
        found.extend(sorted(f for f in skill.rglob("*") if f.is_file()))
    return found


def run(project: Path, host: str, print_only: bool, skills_dir: Path | None = None) -> str:
    """Install (or plan) the skills for ``host``; return the text for the Facilitator."""
    registration = _plan_registration(project, host)
    _check_inside(project, LEDGER_PATH)
    return (
        _copy_skills(project, host, print_only, skills_dir)
        + _write_ledger(project, print_only)
        + _write_registration(project, registration, print_only)
        + "\n"
        + SNIPPETS[host]
        + "\n"
        + _ENV_NOTE
    )


def _copy_skills(project: Path, host: str, print_only: bool, skills_dir: Path | None) -> str:
    source = Path(skills_dir) if skills_dir is not None else packaged_skills_dir()
    files = _skill_files(source)
    lines = [f"founder-vn install: host {host}"]
    if not files:
        lines.append("no skills found in the package; nothing to copy")
        return "\n".join(lines) + "\n"
    folder = SKILL_FOLDERS[host]
    real_project = Path(project).resolve()
    for f in files:
        rel = f.relative_to(source)
        target = Path(project) / folder / rel
        if not target.resolve().is_relative_to(real_project):
            raise InstallRefused(f"refused: {folder}/{rel.as_posix()} resolves outside the project")
        data = f.read_bytes()
        if not target.exists():
            state = "create"
        elif target.read_bytes() == data:
            state = "unchanged"
        else:
            state = "update"
        if state != "unchanged" and not print_only:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        lines.append(f"{state:<10} {folder}/{rel.as_posix()}")
    return "\n".join(lines) + "\n"


def _check_inside(project: Path, rel: str) -> None:
    if not (Path(project) / rel).resolve().is_relative_to(Path(project).resolve()):
        raise InstallRefused(f"refused: {rel} resolves outside the project")


def _write_ledger(project: Path, print_only: bool) -> str:
    """Create or update ``permits/sources.md`` from the package; the packaged content wins."""
    data = packaged_ledger().read_bytes()
    target = Path(project) / LEDGER_PATH
    if not target.exists():
        state = "create"
    elif target.read_bytes() == data:
        state = "unchanged"
    else:
        state = "update"
    if state != "unchanged" and not print_only:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return f"{state:<10} {LEDGER_PATH}\n"


def _plan_registration(project: Path, host: str) -> tuple[str, str] | None:
    """Return (relative path, content) when ``host`` registers through a project file."""
    entry = REGISTRATION_FILES.get(host)
    if entry is None:
        return None
    rel, _content = entry
    if not (Path(project) / rel).resolve().is_relative_to(Path(project).resolve()):
        raise InstallRefused(f"refused: {rel} resolves outside the project")
    return entry


def _write_registration(
    project: Path, registration: tuple[str, str] | None, print_only: bool
) -> str:
    """Write the registration file when absent; leave an existing one untouched."""
    if registration is None:
        return ""
    rel, content = registration
    target = Path(project) / rel
    if os.path.lexists(target):
        return f"{'exists':<10} {rel} (not modified)\n"
    if not print_only:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return f"{'create':<10} {rel}\n"
