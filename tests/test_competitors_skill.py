"""founder-competitors: the survey form and the skill text (design §3, issue #13)."""

import re
import subprocess
import sys
from pathlib import Path

from founder_vn import install

ROOT = Path(__file__).parent.parent
SKILL_DIR = ROOT / "skills" / "founder-competitors"
SKILL = SKILL_DIR / "SKILL.md"
FORM = SKILL_DIR / "survey-form.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")

FORM_FIELDS = (
    "Tên đối thủ",
    "Địa chỉ",
    "Giá",
    "Lượng khách giờ cao điểm",
    "Ảnh menu",
    "Phàn nàn",
    "Khoảng cách",
)


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _form() -> str:
    return FORM.read_text(encoding="utf-8")


def test_form_has_the_six_required_fields_in_vietnamese() -> None:
    text = _form()
    for field in FORM_FIELDS:
        assert field in text, field
    assert "anh/chị" in text
    assert not DOLLAR.search(text)


def test_skill_requires_the_filled_form_before_analysing() -> None:
    text = _skill()
    assert "survey-form.md" in text
    assert "Do not analyse" in text
    assert "no filled form" in text


def test_web_results_are_supplementary_and_linked() -> None:
    text = _skill()
    assert "supplementary" in text
    assert "Bổ trợ từ web" in text
    assert "link" in text


def test_no_fabrication_rule() -> None:
    text = _skill().lower()
    assert "never invent" in text
    assert "competitor" in text and "number" in text


def test_output_shape() -> None:
    text = _skill()
    for needle in (
        "5 to 10 competitors",
        "Google Maps",
        "Facebook",
        "ShopeeFood",
        "GrabFood",
        "positioning map",
        "the gap",
        "competitors.md",
    ):
        assert needle in text, needle


def test_thin_data_warning_below_three_reviews() -> None:
    text = _skill()
    assert "fewer than three reviews" in text
    assert "Dữ liệu mỏng" in text


def test_skill_lint_passes_on_the_repo() -> None:
    done = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "skill_lint.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert "founder-competitors" in done.stdout or "skill" in done.stdout


def test_installer_ships_the_skill_with_its_form(project_root: Path) -> None:
    install.run(project_root, "kiro", print_only=False, skills_dir=ROOT / "skills")
    base = project_root / ".kiro/skills/founder-competitors"
    assert (base / "SKILL.md").is_file()
    assert (base / "survey-form.md").is_file()


def test_skill_copies_the_survey_method_and_sets_the_source_by_method() -> None:
    text = _skill()
    assert "Cách khảo sát" in text
    assert "verbatim" in text
    assert "khảo sát bàn giấy từ nguồn công khai, ngày" in text
    assert "Never write `khảo sát thực địa` for a desk survey" in text
    assert "source (set by the survey method" in text
    assert "source (`khảo sát thực địa`)" not in text


def test_disclaimer_varies_by_method() -> None:
    text = _skill()
    assert "varies by method" in text
    assert "Field survey:" in text and "Desk survey:" in text
    desk = text.split("Desk survey:")[-1]
    assert "bàn giấy" in desk.split("\n")[0]
    assert "thực địa" not in desk.split("\n")[0]


def test_empty_review_count_is_not_thin_data() -> None:
    text = _skill()
    assert "An empty review-count cell is not a number" in text
    assert "never the thin-data warning" in text
    assert "including a 0 written explicitly" in text


def test_desk_survey_states_small_sample_in_map_and_gap() -> None:
    text = _skill()
    assert "small sample" in text
    assert "the positioning map and the gap must also say" in text
    assert "desk survey from public sources" in text


EXAMPLE_DIR = ROOT / "examples" / "barbershop" / "founder"


def test_golden_competitors_follows_the_skill_on_the_desk_survey_form() -> None:
    out = (EXAMPLE_DIR / "competitors.md").read_text(encoding="utf-8")
    form = (EXAMPLE_DIR / "survey-form.md").read_text(encoding="utf-8")
    declaration = next(ln for ln in form.splitlines() if ln.startswith("**Cách khảo sát**"))
    assert declaration in out
    assert out.index(declaration) < out.index("## 1. Bảng đối thủ")
    table = out.split("## 1. Bảng đối thủ")[1].split("## 2.")[0]
    rows = re.findall(r"^\| \d+ \| .*\| khảo sát .*$", table, flags=re.M)
    assert 5 <= len(rows) <= 10
    for row in rows:
        source = row.rsplit("|", 2)[-2]
        assert "khảo sát bàn giấy từ nguồn công khai, ngày 23/11/2026" in source
        assert "khảo sát thực địa" not in source
        assert "http" in source
    for section in ("Chủ đề đánh giá", "Dữ liệu mỏng", "Bổ trợ từ web"):
        assert section in out
    assert "Bản đồ định vị" in out and "Khoảng trống" in out
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in out
    assert "chưa có số liệu" in out
    assert "Dữ liệu mỏng: chỉ có" not in out
    assert not DOLLAR.search(out)
