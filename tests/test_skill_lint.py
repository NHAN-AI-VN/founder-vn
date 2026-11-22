"""skill-lint holds a skill's metadata.version to the package version, also when it is dynamic."""

import subprocess
import sys
from pathlib import Path

SCRIPT = Path(__file__).parent.parent / "scripts" / "skill_lint.py"
SKILL = """---
name: demo
description: Dùng khi Facilitator cần một ví dụ.
license: MIT
metadata:
  version: "{version}"
---

Nội dung.
"""


def lint(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)], capture_output=True, text=True
    )


def make_project(root: Path, skill_version: str) -> None:
    import founder_vn

    (root / "pyproject.toml").write_text(
        '[project]\nname = "demo"\ndynamic = ["version"]\n\n'
        '[tool.hatch.version]\npath = "src/demo/__init__.py"\n',
        encoding="utf-8",
    )
    (root / "src" / "demo").mkdir(parents=True)
    (root / "src" / "demo" / "__init__.py").write_text(
        f'__version__ = "{founder_vn.__version__}"\n', encoding="utf-8"
    )
    (root / "skills" / "demo").mkdir(parents=True)
    (root / "skills" / "demo" / "SKILL.md").write_text(
        SKILL.format(version=skill_version), encoding="utf-8"
    )


def test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version(
    tmp_path: Path,
) -> None:
    make_project(tmp_path, "9.9.9")
    result = lint(tmp_path)
    assert result.returncode == 1
    assert "differs from pyproject" in result.stderr


def test_skill_lint_accepts_a_skill_version_equal_to_a_dynamic_package_version(
    tmp_path: Path,
) -> None:
    import founder_vn

    make_project(tmp_path, founder_vn.__version__)
    result = lint(tmp_path)
    assert result.returncode == 0, result.stderr
    assert f"package version {founder_vn.__version__}" in result.stdout
