"""founder-marketing: the skill text (design §3, issue #115)."""

import re
from pathlib import Path

from founder_vn import __version__

ROOT = Path(__file__).parent.parent
SKILL = ROOT / "skills" / "founder-marketing" / "SKILL.md"
CONVENTIONS = ROOT / "docs" / "skill-conventions.md"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")

HEADINGS = (
    "## 1. Định vị",
    "## 2. Kênh",
    "## 3. Chiến dịch 30 ngày",
    "## 4. Hook đầu tiên",
    "## 5. Chia ngân sách",
    "## 6. Số đo",
    "## 7. Lưu ý",
)
CHANNELS = ("Biển hiệu", "Google Maps", "Zalo OA", "Facebook", "ShopeeFood", "người sáng tạo")


def _skill() -> str:
    return SKILL.read_text(encoding="utf-8")


def _protocol_block() -> str:
    conventions = CONVENTIONS.read_text(encoding="utf-8")
    return conventions.split("````markdown\n", 1)[1].split("````", 1)[0].strip()


def test_skill_carries_the_shared_protocol_block_verbatim() -> None:
    assert _protocol_block() in _skill()


def test_frontmatter_matches_the_lint_and_the_package_version() -> None:
    head = _skill().split("---", 2)[1]
    assert "name: founder-marketing" in head
    assert "license: MIT" in head
    for trigger in ("làm sao để có khách", "kênh quảng cáo", "chiến dịch", "hook"):
        assert trigger in head, trigger
    assert f'version: "{__version__}"' in head


def test_output_is_the_seven_part_structure_in_order() -> None:
    text = _skill()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)


def test_positioning_clauses_are_traced_to_a_quoted_source() -> None:
    text = _skill()
    for needle in ("panel/results.md", "consumer.md", "competitors.md", "objection", "quoted"):
        assert needle in text, needle
    assert "one statement" in text


def test_channel_list_is_the_specs_and_food_channels_can_be_not_applicable() -> None:
    text = _skill()
    for channel in CHANNELS:
        assert channel in text, channel
    assert "không áp dụng" in text
    assert "Instagram and Yelp are not used" in text


def test_campaign_is_thirty_relative_days_with_an_objection_each() -> None:
    text = _skill()
    assert "days 1 to 30" in text and "Ngày 1" in text and "opening day" in text
    assert "no calendar date" in text
    assert "the objection it answers" in text


def test_hooks_have_no_fixed_count_and_each_names_its_objection() -> None:
    text = _skill()
    assert "no fixed count" in text
    assert "each hook" in text


def test_budget_quotes_the_owners_percentage_and_computes_nothing() -> None:
    text = _skill()
    assert "idea.md" in text and "numbers.json" in text
    assert "compute nothing new" in text
    assert "founder-cfo" in text


def test_never_invents_a_quote_a_result_or_a_channel() -> None:
    text = _skill()
    assert "Never write a customer quote" in text
    assert "Never promise reach or conversion" in text
    assert "Never add a channel" in text


def test_disclaimers_and_panel_caveat() -> None:
    text = _skill()
    assert "founder-permits" in text
    assert "no article or figure" in text
    assert "panel caveat once" in text
    assert "không phải tư vấn tài chính, thuế hay pháp lý" in text


def test_no_dollar_in_the_skill() -> None:
    assert not DOLLAR.search(_skill())
