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


FOUNDER = ROOT / "examples" / "barbershop" / "founder"
SOURCE = re.compile(r"P\d{3}|competitors\.md|consumer\.md|idea\.md")


def _golden() -> str:
    return (FOUNDER / "marketing.md").read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    start = text.index(heading) + len(heading)
    rest = text[start:]
    nxt = re.search(r"^## ", rest, flags=re.M)
    return rest[: nxt.start()] if nxt else rest


def test_golden_has_the_seven_sections_in_order() -> None:
    text = _golden()
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)


def test_golden_campaign_has_thirty_relative_days_each_with_an_objection_source() -> None:
    rows = [
        [c.strip() for c in ln.strip("|").split("|")]
        for ln in _section(_golden(), "## 3. Chiến dịch 30 ngày").splitlines()
        if re.match(r"\| Ngày \d", ln)
    ]
    assert [r[0] for r in rows] == [f"Ngày {n}" for n in range(1, 31)]
    for row in rows:
        assert len(row) == 4, row
        assert "ShopeeFood" not in row[1] and "GrabFood" not in row[1], row
        assert SOURCE.search(row[3]), row
    assert not re.search(r"\d{1,2}/\d{1,2}/20\d\d", _section(_golden(), "## 3. Chiến dịch 30 ngày"))


def test_golden_every_quote_is_verbatim_from_the_panel_results() -> None:
    panel = (FOUNDER / "panel" / "results.md").read_text(encoding="utf-8")
    quotes = re.findall(r'"([^"|]{25,})"', _section(_golden(), "## 1. Định vị"))
    assert quotes
    for quote in quotes:
        assert quote in panel, quote


def test_golden_hooks_each_name_an_objection() -> None:
    hooks = [
        ln
        for ln in _section(_golden(), "## 4. Hook đầu tiên").splitlines()
        if ln[:2] in {f"{n}." for n in range(1, 10)}
    ]
    assert len(hooks) >= 6
    for hook in hooks:
        assert re.search(r"Trả lời [A-F]", hook), hook


def test_golden_shopeefood_grabfood_not_applicable_and_no_instagram() -> None:
    text = _golden()
    row = next(ln for ln in _section(text, "## 2. Kênh").splitlines() if "ShopeeFood" in ln)
    assert "Không áp dụng" in row
    assert "Instagram" not in text and "Yelp" not in text


def test_golden_budget_quotes_the_percentage_and_states_no_amount() -> None:
    budget = _section(_golden(), "## 5. Chia ngân sách")
    assert "marketing 4%" in budget and "founder-cfo" in budget
    assert not re.search(r"\d[\d.]*\s?(đ|đồng|triệu)", budget)


def test_golden_panel_caveat_once_and_disclaimers() -> None:
    text = _golden()
    assert text.count("Panel là mô phỏng, cận trên, không phải khách hàng thật") == 1
    assert "founder-permits" in _section(text, "## 7. Lưu ý")
    assert not re.search(r"Điều|Nghị định|Luật", _section(text, "## 7. Lưu ý"))
    assert text.rstrip().splitlines()[-1].endswith("không phải tư vấn tài chính, thuế hay pháp lý.")
    assert "anh/chị" in text
    assert not DOLLAR.search(text) and "$" not in text


def test_business_plan_carries_the_marketing_section() -> None:
    plan = (FOUNDER / "business-plan.md").read_text(encoding="utf-8")
    assert "## Tiếp thị" in plan
    assert "### 1. Định vị" in plan and "### 6. Số đo" in plan
