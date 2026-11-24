"""founder-plan: the skill text (design §3, issue #18)."""

import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-plan" / "SKILL.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _protocol_block() -> str:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    block = conventions.split("````markdown\n", 1)[1].split("````", 1)[0]
    return block.strip()


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    assert _protocol_block() in _skill()


def test_frontmatter_names_the_skill_and_carries_vietnamese_triggers() -> None:
    head = _skill().split("---", 2)[1]
    assert "name: founder-plan" in head
    assert "license: MIT" in head
    assert "kế hoạch kinh doanh" in head


def test_writes_summary_with_both_parts() -> None:
    text = _skill()
    assert "founder/summary.md" in text
    assert "Tóm tắt điều hành" in text
    assert "Bản một trang cho đối tác hoặc bên cho vay" in text


def test_calls_the_compiler_on_either_transport() -> None:
    text = _skill()
    assert "plan_compile" in text
    assert "founder-vn plan" in text
    assert "--check" in text


def test_never_writes_the_verdict_and_never_edits_the_plan_by_hand() -> None:
    text = _skill()
    assert "Never write the verdict" in text
    assert "never edit `founder/business-plan.md`" in text


def test_explains_each_failing_check_with_the_skill_that_fixes_it() -> None:
    text = _skill()
    for check in (
        "Đóng góp mỗi",
        "Lợi nhuận hoạt động năm 1 sau thuế",
        "Hòa vốn không vượt công suất",
    ):
        assert check in text, check
    for fixer in ("founder-pricing", "founder-cfo", "founder-board"):
        assert fixer in text, fixer
    assert "Không đạt" in text


def test_keeps_the_caveat_the_disclaimer_and_the_legal_source_rule() -> None:
    text = _skill()
    assert "mô phỏng, cận trên, không phải khách hàng thật" in text
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text
    assert "permits/sources.md" in text
    assert "never from memory" in text


def test_no_dollar_sign_next_to_a_number() -> None:
    assert not DOLLAR.search(_skill())


def test_skill_lint_passes_on_the_repo() -> None:
    done = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "skill_lint.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert done.returncode == 0, done.stdout + done.stderr


def test_installer_ships_the_skill(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=ROOT / "skills")
    assert (project_root / ".kiro/skills/founder-plan/SKILL.md").is_file()
