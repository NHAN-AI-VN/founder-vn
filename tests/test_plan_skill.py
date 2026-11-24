"""founder-plan: the skill text (design §3, issue #18)."""

import json
import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install, plan

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


def _table_labels() -> set[str]:
    section = _skill().split("## Step 3", 1)[1].split("## Step 4", 1)[0]
    rows = [line for line in section.splitlines() if line.startswith("| ") and "---" not in line]
    return {row.split("|")[1].strip() for row in rows[1:]}


def test_failing_check_table_matches_the_labels_the_compiler_prints(tmp_path: Path) -> None:
    spec = json.loads((ROOT / "tests" / "fixtures" / "cfo_numbers.json").read_text("utf-8"))
    cases = (
        {"price": "10k"},
        {"price": "17k", "ramp_per_day": [5] * 12, "plan_per_day": 5},
        {"capacity_per_day": 10},
    )
    printed: set[str] = set()
    for i, changes in enumerate(cases):
        project = tmp_path / str(i)
        (project / "founder").mkdir(parents=True)
        numbers = json.dumps({**spec, **changes}, ensure_ascii=False)
        (project / "founder" / "numbers.json").write_text(numbers, encoding="utf-8")
        result, text = plan.compile_plan(project)
        assert result == plan.NOT_YET
        failed = [
            line.split("|")[1].strip() for line in text.splitlines() if "| Không đạt |" in line
        ]
        assert failed
        printed |= {f.replace(f"mỗi {spec['unit']} ", "mỗi (đơn vị bán) ") for f in failed}
    assert printed == _table_labels()


def test_incomplete_verdict_names_the_missing_file_and_its_skill(tmp_path: Path) -> None:
    result, text = plan.compile_plan(tmp_path)
    assert result == plan.INCOMPLETE
    assert "## Chưa làm" in text
    assert "chạy skill `founder-cfo`" in text or "Chưa có số của CFO" in text
    assert "Chưa làm" in _skill()
