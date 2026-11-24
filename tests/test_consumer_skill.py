"""founder-consumer: the skill text and its golden case (design §3, issue #16)."""

import json
import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install, panel

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-consumer" / "SKILL.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_customer_json_is_shown_to_the_owner_before_dealing() -> None:
    text = _skill()
    assert "customer.json" in text
    for field in ("segments", "behaviours", "objections", "habits", "monthly VND income"):
        assert field in text, field
    assert "before dealing" in text
    assert "Do not call `panel_init` until the Owner has confirmed" in text
    assert "competitors.md" in text and "If `founder/competitors.md` exists" in text
    assert "guess" in text


def test_pitch_rules() -> None:
    text = _skill()
    assert "pitch.md" in text
    assert "three to six" in text
    assert "superlative" in text
    assert "cannot deliver" in text


def test_panel_size_and_tool_order() -> None:
    text = _skill()
    assert "`n = 20`" in text
    assert "Use 100 only when the Owner asks" in text
    assert "cost and time" in text
    order = [text.index(t) for t in ("panel_init", "panel_run", "job_status", "panel_tally")]
    assert order == sorted(order)
    assert "Poll" in text


def test_never_answers_for_a_buyer_and_reports_excluded() -> None:
    text = _skill()
    assert "Never answer for a buyer" in text
    assert "excluded" in text
    assert "do not write an answer yourself" in text


def test_five_point_read_back_and_caveat_once() -> None:
    text = _skill()
    for needle in (
        "Headline",
        "differ most",
        "Top three reasons",
        "one quote each",
        "What would flip a no",
        "one sentence",
    ):
        assert needle in text, needle
    assert "mô phỏng, cận trên, không phải khách hàng thật" in text
    assert "once" in text


def test_names_carry_no_gender_so_segments_name_it() -> None:
    text = _skill()
    assert "gender" in text
    assert "segment name" in text


def test_no_dollar_next_to_a_digit() -> None:
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
    assert (project_root / ".kiro/skills/founder-consumer/SKILL.md").is_file()


EXAMPLE_DIR = ROOT / "examples" / "barbershop" / "founder"
SUPERLATIVES = ("nhất", "số một", "số 1", "hoàn hảo", "tuyệt vời")


def test_golden_customer_json_passes_the_panel_validation_and_is_gender_explicit() -> None:
    spec = json.loads((EXAMPLE_DIR / "customer.json").read_text(encoding="utf-8"))
    panel.validate_customer(spec)
    for segment in spec["segments"]:
        assert segment["name"].startswith("Nam"), segment["name"]
    assert spec["habits"] and len(spec["objections"]) >= 3


def test_golden_pitch_is_three_to_six_plain_lines_without_superlatives() -> None:
    text = (EXAMPLE_DIR / "pitch.md").read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if ln.strip()]
    assert 3 <= len(lines) <= 6
    lowered = text.lower()
    for word in SUPERLATIVES:
        assert word not in lowered, word
    assert not DOLLAR.search(text)


def test_golden_panel_has_twenty_buyers_and_matches_its_results() -> None:
    base = EXAMPLE_DIR / "panel"
    meta = json.loads((base / "panel.json").read_text(encoding="utf-8"))
    res = json.loads((base / "results.json").read_text(encoding="utf-8"))
    assert meta["n"] == 20
    assert len(list((base / "answers").glob("P*.json"))) == 20
    assert res["n"] == 20 and res["excluded"] == 0
    assert res["buys"] + res["passes"] == res["answered"] == 20
    assert meta["model"] and meta["prompt_hash"]
    assert not any(k in meta for k in ("api_key", "base_url"))
    assert (base / "results.md").is_file()


def test_golden_readback_has_five_points_and_the_caveat_once() -> None:
    text = (EXAMPLE_DIR / "consumer.md").read_text(encoding="utf-8")
    res = json.loads((EXAMPLE_DIR / "panel" / "results.json").read_text(encoding="utf-8"))
    points = re.findall(r"^[1-5]\. \*\*", text, flags=re.M)
    assert len(points) == 5
    assert text.count("mô phỏng, cận trên, không phải khách hàng thật") == 1
    assert f"{res['buys']} mua, {res['passes']} không mua" in text
    assert res["model"] in text
    assert "anh/chị" in text
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text
    assert not DOLLAR.search(text)
