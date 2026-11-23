"""Content checks for the golden case under examples/barbershop/ (issue #5)."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXAMPLE = ROOT / "examples" / "barbershop"
IDEA = EXAMPLE / "founder" / "idea.md"

DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
VND = re.compile(r"\b\d{1,3}(?:\.\d{3})+ đ\b")
PHONE = re.compile(r"\b0\d{9}\b|\+84")
STREET_ADDRESS = re.compile(r"\b[Ss]ố \d+[A-Za-z/]*,? (?:đường|Đường|phố|Phố) ")

SUB_DISTRICT_NAMES = ("Phú Mỹ Hưng",)
LEGAL_CLAIMS = ("thuế thuê nhà 10%", "bảo hiểm xã hội", "48 giờ/tuần")

UPSTREAM_BULLETS = (
    "- Là gì:",
    "- Cho ai:",
    "- Bán gì, giá bao nhiêu:",
    "- Ở đâu và bằng cách nào:",
    "- Ngân sách và ràng buộc:",
)


def test_idea_file_sits_in_the_example_project_root() -> None:
    assert IDEA.is_file(), IDEA


def test_idea_file_has_the_upstream_shape_in_vietnamese() -> None:
    text = IDEA.read_text(encoding="utf-8")
    assert text.startswith("# "), text[:40]
    for bullet in UPSTREAM_BULLETS:
        assert bullet in text, bullet


def test_idea_file_prices_are_vnd_in_vietnamese_format() -> None:
    text = IDEA.read_text(encoding="utf-8")
    assert not DOLLAR.search(text)
    assert VND.search(text), "no price shaped like 199.000 đ"


def test_example_is_anonymised() -> None:
    paths = sorted(EXAMPLE.rglob("*.md"))
    assert paths, EXAMPLE
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert not DOLLAR.search(text), path
        assert not PHONE.search(text), path
        assert "@" not in text, path
        assert not STREET_ADDRESS.search(text), path
        for name in SUB_DISTRICT_NAMES:
            assert name not in text, (path, name)


def test_readme_names_the_example_directory_as_the_golden_case() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "examples/barbershop/" in text
    assert "golden case" in text.lower()



def test_idea_file_carries_no_unsourced_legal_or_tax_claim() -> None:
    text = IDEA.read_text(encoding="utf-8")
    for claim in LEGAL_CLAIMS:
        assert claim not in text, claim
