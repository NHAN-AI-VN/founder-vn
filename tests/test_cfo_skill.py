"""founder-cfo: the skill text and the sources it relies on (design §3, issue #12)."""

import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-cfo" / "SKILL.md"
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
    assert "name: founder-cfo" in head
    assert "license: MIT" in head
    assert "kinh tế đơn vị" in head


def test_asks_for_costs_in_the_owner_terms() -> None:
    text = _skill()
    for term in (
        "nguyên liệu",
        "bao bì",
        "phí app giao hàng",
        "thuê mặt bằng",
        "lương",
        "điện nước",
    ):
        assert term in text, term


def test_looks_up_the_two_legal_figures_in_the_ledger_and_never_guesses() -> None:
    text = _skill()
    assert "permits/sources.md" in text
    assert "tax_rate_on_revenue" in text and "tax_free_threshold" in text
    assert "official link" in text and "verification date" in text
    assert "never from memory" in text


def test_calls_the_tool_on_either_transport() -> None:
    text = _skill()
    assert "cfo_analyse" in text
    assert "founder-vn cfo" in text
    assert "--out cfo.md" in text


def test_reads_flags_back_in_plain_vietnamese_and_never_computes() -> None:
    text = _skill()
    assert "plain Vietnamese" in text
    assert "flags" in text
    assert "Never compute" in text


def test_states_the_two_tax_model_limits_and_the_temporary_relief_line() -> None:
    text = _skill()
    assert "20 triệu đồng" in text
    assert "3 tỷ đồng" in text
    assert "17%" in text
    assert "có ưu đãi tạm thời, chưa tính" in text


def test_ends_with_the_disclaimer() -> None:
    assert "không phải tư vấn tài chính hay thuế" in _skill()


def test_step_6_copies_the_ledger_sources_and_verification_into_the_report() -> None:
    """SPEC-1 (reviews/issue-12/spec.md): the Owner reads cfo.md, not the ledger, so the appended
    section carries the documents, links and verification date copied from the ledger entries."""
    step6 = _skill().split("## Step 6", 1)[1].split("## Rules", 1)[0]
    assert "permits/sources.md" in step6
    assert "never from memory" in step6
    assert "Link" in step6 and "Xác nhận" in step6
    assert 'Đính chính mục "Lưu ý"' in step6
    assert "không phải số anh/chị nhập" in step6


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
    assert (project_root / ".kiro/skills/founder-cfo/SKILL.md").is_file()


EXAMPLE = ROOT / "examples" / "barbershop"
LIMITS_HEADING = "## Giới hạn của phần thuế"


def test_golden_numbers_json_holds_the_ledger_values_for_the_sector() -> None:
    import json

    spec = json.loads((EXAMPLE / "founder" / "numbers.json").read_text(encoding="utf-8"))
    assert spec["tax_rate_on_revenue"] == 7
    assert spec["tax_free_threshold"] == 1_000_000_000
    assert len(spec["ramp_per_day"]) == 12
    assert spec["variable"] and spec["fixed_monthly"] and spec["startup"]


def test_golden_cfo_md_is_the_tool_output_plus_the_limits_section() -> None:
    from founder_vn import cfo

    out = (EXAMPLE / "founder" / "cfo.md").read_text(encoding="utf-8")
    tool_text = cfo.run(EXAMPLE, "founder/numbers.json")
    assert out.startswith(tool_text)
    limits = out[len(tool_text) :]
    assert limits.lstrip().startswith(LIMITS_HEADING)
    assert "20 triệu đồng mỗi năm" in limits
    assert "3 tỷ đồng" in limits and "17%" in limits
    assert limits.count("có ưu đãi tạm thời, chưa tính") == 1
    assert "không phải tư vấn tài chính hay thuế" in limits
    assert not DOLLAR.search(out)


LEDGER = ROOT / "permits" / "sources.md"
CONG_BAO_LINK = re.compile(r"https://congbao\.chinhphu\.vn/\S+?\.htm")
VERIFICATION = re.compile(r"kiểm chứng ngày \d{2}/\d{2}/\d{4}[^\n]*")


def _ledger_entry(key: str) -> str:
    text = LEDGER.read_text(encoding="utf-8")
    body = text.split(f"\n## {key}", 1)[1]
    return body.split("\n## ", 1)[0]


def test_golden_cfo_md_limits_section_cites_every_ledger_link_and_the_verification_line() -> None:
    """SPEC-1: each legal figure in the Owner's report carries its official link and verification
    date, copied from the ledger entry, and the tool's "Lưu ý" wording is corrected."""
    from founder_vn import cfo

    out = (EXAMPLE / "founder" / "cfo.md").read_text(encoding="utf-8")
    limits = out[len(cfo.run(EXAMPLE, "founder/numbers.json")) :]
    for key in ("tax_rate_on_revenue", "tax_free_threshold"):
        entry = _ledger_entry(key)
        links = CONG_BAO_LINK.findall(entry)
        assert len(links) >= 3, key
        for link in links:
            assert link in limits, link
        verification = VERIFICATION.search(entry)
        assert verification is not None, key
        assert verification.group(0) in limits
    assert "không phải số anh/chị nhập" in limits
    assert "permits/sources.md" in limits
