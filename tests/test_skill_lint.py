"""skill-lint holds a skill's metadata.version to the package version, also when it is dynamic,
and its ``## Protocol`` block to the Vietnamese step-1 stop template (#148, Q60)."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
SCRIPT = ROOT / "scripts" / "skill_lint.py"
# The template of docs/skill-conventions.md, "Shared protocol", step 1 (placeholders included).
PROTOCOL_STOP = (
    "Dừng ở bước 1 của Protocol: gói founder-vn <phiên bản gói> và skill <tên skill> "
    "<phiên bản skill> lệch số major; anh/chị cập nhật gói hoặc skill rồi chạy lại."
)
PROTOCOL = f"""## Protocol

1. Check the version. On a major mismatch, stop and tell the Facilitator. The stop message is in
   Vietnamese and has this shape:
   `{PROTOCOL_STOP}`
2. Prefer MCP tools.
"""
PROTOCOL_WITHOUT_TEMPLATE = """## Protocol

1. Check the version. On a major mismatch, stop and tell the Facilitator to update the package or
   the skill.
2. Prefer MCP tools.
"""
SKILL = """---
name: demo
description: Dùng khi Facilitator cần một ví dụ.
license: MIT
metadata:
  version: "{version}"
---

# demo

{protocol}
Nội dung.
"""


def lint(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root)], capture_output=True, text=True
    )


def make_project(root: Path, skill_version: str, protocol: str = PROTOCOL) -> Path:
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
    skill = root / "skills" / "demo" / "SKILL.md"
    skill.write_text(SKILL.format(version=skill_version, protocol=protocol), encoding="utf-8")
    return skill


def test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version(
    tmp_path: Path,
) -> None:
    make_project(tmp_path, "9.9.9")
    result = lint(tmp_path)
    assert result.returncode == 1
    assert "differs from pyproject" in result.stderr
    assert result.stderr.count("\n") == 1, "one finding, the version"


def test_skill_lint_accepts_a_skill_version_equal_to_a_dynamic_package_version(
    tmp_path: Path,
) -> None:
    import founder_vn

    make_project(tmp_path, founder_vn.__version__)
    result = lint(tmp_path)
    assert result.returncode == 0, result.stderr
    assert f"package version {founder_vn.__version__}" in result.stdout


def test_skill_lint_reports_a_protocol_block_that_lacks_the_vietnamese_stop_template(
    tmp_path: Path,
) -> None:
    import founder_vn

    skill = make_project(tmp_path, founder_vn.__version__, protocol=PROTOCOL_WITHOUT_TEMPLATE)
    heading_line = skill.read_text(encoding="utf-8").splitlines().index("## Protocol") + 1
    result = lint(tmp_path)
    assert result.returncode == 1
    findings = result.stderr.splitlines()
    assert len(findings) == 1, findings
    assert findings[0].startswith(f"{skill.as_posix()}:{heading_line}: ")
    assert "Dừng ở bước 1 của Protocol" in findings[0]
    assert "1 finding(s)" in result.stdout


def test_skill_lint_finds_the_template_in_the_ten_shipped_skills() -> None:
    result = lint(ROOT)
    assert result.returncode == 0, result.stderr
    assert "10 skills checked" in result.stdout and "0 finding(s)" in result.stdout
    for skill in sorted((ROOT / "skills").glob("*/SKILL.md")):
        assert PROTOCOL_STOP in skill.read_text(encoding="utf-8"), skill
