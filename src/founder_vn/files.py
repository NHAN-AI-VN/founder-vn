"""Path-locked file layer: the only place the package reads or writes project state.

Root is ``<project>/founder/``. Refused: ``..`` segments, absolute paths outside the root,
symlinks resolving outside the root. Only ``.md`` and ``.json`` are written. Nothing is deleted,
and this module exposes no way to delete.
"""

from pathlib import Path

ROOT_NAME = "founder"
ALLOWED_SUFFIXES = (".md", ".json")


class PathRefused(ValueError):
    """The requested path is outside what the path-locked layer allows."""


def root_of(project: Path) -> Path:
    """Return the state root ``<project>/founder/`` (not created)."""
    return Path(project) / ROOT_NAME


def resolve(project: Path, path: str | Path) -> Path:
    """Validate ``path`` against the root and return the absolute target path."""
    root = root_of(project)
    candidate = Path(path)
    if ".." in candidate.parts:
        raise PathRefused(f"path refused: '..' is not allowed ({path})")
    if candidate.is_absolute():
        if not candidate.is_relative_to(root):
            raise PathRefused(f"path refused: absolute path outside {ROOT_NAME}/ ({path})")
        target = candidate
    else:
        target = root / candidate
    real_root = root.resolve()
    if not target.resolve().is_relative_to(real_root):
        raise PathRefused(f"path refused: symlink resolves outside {ROOT_NAME}/ ({path})")
    return target


def write_text(project: Path, path: str | Path, text: str) -> Path:
    """Write ``text`` to ``path`` under the root; only ``.md`` and ``.json`` are accepted."""
    target = resolve(project, path)
    if target.suffix not in ALLOWED_SUFFIXES:
        raise PathRefused(f"path refused: extension must be .md or .json ({path})")
    target.parent.mkdir(parents=True, exist_ok=True)
    resolve(project, target)  # re-check after creating directories
    target.write_text(text, encoding="utf-8")
    return target


def read_text(project: Path, path: str | Path) -> str:
    """Read a file under the root, applying the same path checks as writes."""
    return resolve(project, path).read_text(encoding="utf-8")
