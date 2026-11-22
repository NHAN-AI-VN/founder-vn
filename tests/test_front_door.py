"""The front door: README, LICENSE, CONTRIBUTING, issue template, conventions, checklist, hosts."""

import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
UPSTREAM = "Copyright (c) 2026 Jake Schincariol"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")


def _read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def test_license_is_mit_and_keeps_the_upstream_notice() -> None:
    text = _read("LICENSE")
    assert text.startswith("MIT License")
    assert UPSTREAM in text
    assert "Permission is hereby granted, free of charge" in text
    assert 'THE SOFTWARE IS PROVIDED "AS IS"' in text


def test_readme_names_purpose_audience_hosts_and_both_install_routes() -> None:
    text = _read("README.md")
    for needle in (
        "Facilitator",
        "Owner",
        "Kiro CLI",
        "Claude Code",
        "Codex",
        "Gemini",
        "Grok Build",
        "KiroCrew",
        "npx skills add NHAN-AI-VN/founder-vn",
        "founder-vn install --host",
        "uvx founder-vn-mcp",
        "not yet released",
    ):
        assert needle in text, needle
    assert re.search(r"^## .*Tiếng Việt", text, re.MULTILINE)
    assert "| Skill | Status |" in text


def test_readme_credits_upstream_with_a_commit_hash() -> None:
    text = _read("README.md")
    assert "Jake Schincariol" in text
    assert "https://github.com/Jakeschincariol/founder-skill" in text
    assert re.search(r"commit `[0-9a-f]{40}`", text)


def test_readme_has_no_dollar_next_to_a_digit() -> None:
    assert not DOLLAR.search(_read("README.md"))


def test_contributing_states_the_legal_rule_and_the_definition_of_done() -> None:
    text = _read("CONTRIBUTING.md")
    assert "every legal claim needs an official link and a verification date" in text.lower()
    for needle in ("golden", "tests", "docs/review-checklist.md", "Law changed"):
        assert needle in text, needle


def test_law_changed_issue_template_has_the_four_fields() -> None:
    text = _read(".github/ISSUE_TEMPLATE/law-changed.yml")
    assert "name: Law changed" in text
    for field_id in ("what_changed", "source_link", "effective_date", "affected_skill"):
        assert f"id: {field_id}" in text, field_id


PROTOCOL_HEADING = "## Shared protocol"


def _protocol_block() -> str:
    text = _read("docs/skill-conventions.md")
    section = text.split(PROTOCOL_HEADING, 1)[1]
    return re.findall(r"````markdown\n(.*?)\n````", section, re.DOTALL)[0]


def test_conventions_list_every_frontmatter_field() -> None:
    text = _read("docs/skill-conventions.md")
    for field in (
        "name",
        "description",
        "license",
        "metadata.version",
        "metadata.author",
        "metadata.source",
        "metadata.commit",
    ):
        assert f"`{field}`" in text, field
    assert "anh/chị" in text


def test_shared_protocol_block_carries_the_five_rules() -> None:
    block = _protocol_block()
    assert block.startswith("## Protocol")
    for needle in (
        "server_info",
        "founder-vn --version",
        "major",
        "MCP tools",
        "shell",
        "install instructions",
        "Never compute a number",
        "Never answer for a buyer",
        "Never write the verdict",
    ):
        assert needle in block, needle


def test_review_checklist_has_the_five_items() -> None:
    text = _read("docs/review-checklist.md")
    for needle in (
        "No `$`",
        "No English leaks",
        "official link and a verification date",
        "not financial, tax or legal advice",
        "mô phỏng, cận trên, không phải khách hàng thật",
    ):
        assert needle in text, needle


def test_hosts_index_links_one_existing_page_per_host() -> None:
    index = _read("docs/hosts/README.md")
    for page in ("kiro", "claude", "codex", "gemini", "grok", "kirocrew"):
        assert f"({page}.md)" in index, page
        assert (ROOT / "docs" / "hosts" / f"{page}.md").is_file(), page


def test_host_pages_carry_no_secret_values_or_dollar_amounts() -> None:
    for page in (ROOT / "docs" / "hosts").glob("*.md"):
        text = page.read_text(encoding="utf-8")
        assert not re.search(r"(sk-|Bearer )\w", text), page.name
        assert not DOLLAR.search(text), page.name
