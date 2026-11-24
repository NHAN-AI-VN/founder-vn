"""founder-board: the skill text, the lens reference and the golden case (design §3, issue #14)."""

import json
import re
import subprocess
import sys
from pathlib import Path

from founder_vn import board, install

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "founder-board"
SKILL = SKILL_DIR / "SKILL.md"
LENSES = SKILL_DIR / "lenses.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
EXAMPLE_DIR = ROOT / "examples" / "barbershop" / "founder"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    block = conventions.split("````markdown\n", 1)[1].split("````", 1)[0].strip()
    assert block in _skill()


def test_step_0_writes_or_reuses_idea_md() -> None:
    text = _skill()
    step0 = text.split("## Step 0", 1)[1].split("## Step 1", 1)[0]
    assert "founder/idea.md" in step0
    assert "reuse" in step0 and "write" in step0


def test_brief_stands_alone_and_is_written_to_board_brief() -> None:
    text = _skill()
    assert "founder/board/brief.md" in text
    assert "cannot see the conversation" in text
    assert "stand alone" in text


def test_run_polls_job_status_and_names_both_transports() -> None:
    text = _skill()
    for needle in ("board_run", "founder-vn board run", "job_status", "founder-vn panel status"):
        assert needle in text, needle


def test_chair_summary_keeps_disagreements_merges_conditions_and_routes_open_numbers() -> None:
    text = _skill()
    assert "board.md" in text
    assert "disagreement" in text and "never average" in text
    assert "checklist" in text and "conditions" in text
    for name in ("founder-cfo", "founder-competitors", "founder-consumer", "founder-pricing"):
        assert name in text, name
    assert "Never write the verdict" in text or "never write the verdict" in text.lower()


def test_lens_reference_names_the_three_books_and_the_author_rule() -> None:
    text = LENSES.read_text(encoding="utf-8")
    assert "100M Offers" in text and "Isaacson" in text and "The E-Myth Revisited" in text
    assert "never speak as the author" in text
    for lens in board.LENSES.values():
        assert lens["title"] in text
    assert not DOLLAR.search(text)
    assert "Thiel" in text and "Monopoly" in text  # why the old lens is gone


def test_skill_lint_passes_on_the_repo() -> None:
    done = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "skill_lint.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert done.returncode == 0, done.stdout + done.stderr


def test_installer_ships_the_skill_with_its_lens_reference(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=ROOT / "skills")
    base = project_root / ".kiro/skills/founder-board"
    assert (base / "SKILL.md").is_file()
    assert (base / "lenses.md").is_file()


def test_golden_brief_stands_alone_from_idea_md() -> None:
    brief = (EXAMPLE_DIR / "board" / "brief.md").read_text(encoding="utf-8")
    idea = (EXAMPLE_DIR / "idea.md").read_text(encoding="utf-8")
    assert brief.split("\n")[0] == idea.split("\n")[0]
    for figure in ("199.000 đ", "279.000 đ", "1.990.000 đ", "265.000 đ", "Quận 7 cũ"):
        assert figure in brief, figure
    assert "tự đứng một mình" in brief
    assert "idea.md" not in brief and "competitors.md" not in brief
    assert not DOLLAR.search(brief)


# #14 criterion 4: the golden case is a real model run of `founder-vn board run` on Kiro CLI
# (examples/barbershop/founder/board/{offers,product,systems}.{json,md}, board.json and board.md).
# The memo text is non-deterministic, so these tests pin the fixed shape, the package renderer and
# the chair's-summary structure, not the model's words.

BOARD_DIR = EXAMPLE_DIR / "board"
BOARD_MD = EXAMPLE_DIR / "board.md"


def _memo(lens: str) -> dict:
    return json.loads((BOARD_DIR / f"{lens}.json").read_text(encoding="utf-8"))


def test_golden_board_json_records_the_model_and_prompt_hash() -> None:
    meta = json.loads((BOARD_DIR / "board.json").read_text(encoding="utf-8"))
    assert meta["mode"] == "model"
    assert isinstance(meta["model"], str) and meta["model"].strip()
    assert re.fullmatch(r"[0-9a-f]{64}", meta["prompt_hash"])
    assert meta["lenses"] == list(board.LENSES)


def test_golden_memos_have_the_fixed_shape_and_match_the_package_renderer() -> None:
    for lens in board.LENSES:
        memo = _memo(lens)
        assert board.memo_problem(memo) is None, lens
        rendered = (BOARD_DIR / f"{lens}.md").read_text(encoding="utf-8")
        assert rendered == board.memo_md(lens, memo), lens
        assert not DOLLAR.search(rendered), lens


def test_golden_board_md_is_the_chair_summary_over_the_real_memos() -> None:
    md = BOARD_MD.read_text(encoding="utf-8")
    for heading in (
        "## Ba lens, ba cách đọc",
        "## Chỗ các lens không đồng ý",
        "## Danh sách điều kiện",
        "## Số còn mở và skill trả lời",
    ):
        assert heading in md, heading
    # every lens, with its score and vote exactly as its own memo prints them
    for lens, spec in board.LENSES.items():
        memo = _memo(lens)
        assert spec["title"] in md, lens
        line = f"**Điểm: {memo['score']}/10** · **Phiếu: {board.VOTES[memo['vote']]}**"
        assert line in md, line
    # conditions merged into a checklist that keeps the lens names
    assert md.count("- [ ]") >= 3
    for tag in ("[Offers]", "[Product]", "[Systems]"):
        assert tag in md, tag
    # open numbers routed to the skill that answers each; none answered here
    for skill in ("founder-cfo", "founder-competitors", "founder-consumer", "founder-pricing"):
        assert skill in md, skill
    assert "ngoài bộ công cụ" in md
    # the two closing lines, verbatim; no verdict; no dollar sign
    assert (
        "Ba bản đọc này là mô phỏng từ ba khung đã xuất bản, không nói thay tác giả của chúng, "
        "và không thay thế khách hàng thật." in md
    )
    assert "Đây không phải tư vấn tài chính, thuế hay pháp lý." in md
    for verdict in ("Profitable", "Not yet", "Incomplete"):
        assert verdict not in md, verdict
    assert not DOLLAR.search(md)
