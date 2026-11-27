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
        "uvx --from founder-vn founder-vn-mcp",
        "released, 0.3.0 on PyPI",
    ):
        assert needle in text, needle
    assert re.search(r"^## .*Tiếng Việt", text, re.MULTILINE)
    assert "| Skill | Ticket | Status |" in text


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


def test_readme_truth_table_is_honest_about_release_status_and_hosts() -> None:
    text = _read("README.md")
    english, vietnamese = re.split(r"^## .*Tiếng Việt", text, maxsplit=1, flags=re.MULTILINE)
    assert "0.3.0 (Wave B, ten skills) is the current PyPI release" in english
    assert "v0.3.0" in english and "2026-11-26" in english
    assert "0.2.0 was the first PyPI release" in english
    assert "v0.2.0" in english and "2026-11-24" in english
    assert "pending the `v0" not in english and "not yet released" not in english
    assert text.count("released, 0.3.0 on PyPI") == 2
    assert "released, 0.2.0 on PyPI" not in text
    assert "has not run yet" not in english and "pending walkthrough" not in text
    assert "0.1.0 is not published" not in text and "chưa lên PyPI" not in text
    for skill, issue, artefact in (
        ("founder-board", "#14", "board.md"),
        ("founder-competitors", "#13", "competitors.md"),
        ("founder-consumer", "#16", "consumer.md"),
        ("founder-pricing", "#17", "pricing.md"),
        ("founder-cfo", "#12", "cfo.md"),
        ("founder-plan", "#18", "business-plan.md"),
        ("founder-permits", "#112", "permits.md"),
        ("founder-ops", "#114", "ops.md"),
        ("founder-marketing", "#115", "marketing.md"),
        ("founder-launch", "#116", "launch.md"),
    ):
        row = next(line for line in english.splitlines() if f"`{skill}`" in line and "|" in line)
        assert issue in row and f"examples/barbershop/founder/{artefact}" in row, skill
    permits_row = next(line for line in english.splitlines() if "`founder-permits`" in line)
    assert "#142" in permits_row, "a clean install has no source ledger (#142)"
    kiro_row = next(line for line in english.splitlines() if line.startswith("| Kiro CLI"))
    assert "full pipeline incl. Wave B verified on 0.3.0 (walkthrough 2026-11-26, #118)" in kiro_row
    assert "#142" in kiro_row
    assert "verified on 0.2.0 (walkthrough 2026-11-25, #19)" in kiro_row
    # #118 criterion 4: the major-mismatch stop was observed on 0.3.0 as well (2026-11-27).
    assert "major-mismatch stop observed on 0.2.0 (#19) and on 0.3.0 (2026-11-27, #118)" in kiro_row
    assert "not rerun on 0.3.0" not in kiro_row
    for host in ("Claude Code", "Codex", "Gemini / Antigravity CLI", "Grok Build", "KiroCrew"):
        row = next(line for line in english.splitlines() if line.startswith(f"| {host}"))
        assert "not yet verified" in row and "verified on" not in row, host
    hosts_index = _read("docs/hosts/README.md")
    kiro_index_row = next(
        line for line in hosts_index.splitlines() if line.startswith("| Kiro CLI")
    )
    assert (
        "verified end to end on 0.3.0 incl. Wave B (walkthrough 2026-11-26, #118" in kiro_index_row
    )
    assert "#142" in kiro_index_row and "#19" in kiro_index_row
    assert "../evidence/issue-118-wave-b-walkthrough.md" in hosts_index
    assert "pending walkthrough" not in hosts_index
    assert "No host is verified end to end yet" not in hosts_index
    for needle in ("0.2.0", "v0.2.0", "#19", "đã xác nhận", "chưa xác nhận", "chưa bắt đầu"):
        assert needle in vietnamese, needle
    assert "v0.3.0" in vietnamese and "26/11/2026" in vietnamese
    assert "Bản hiện hành trên PyPI là 0.3.0" in vietnamese
    assert "đang chờ tag" not in vietnamese and "đang chờ walkthrough" not in vietnamese
    assert "đã xác nhận trên 0.3.0 (walkthrough 26/11/2026, #118)" in vietnamese
    assert vietnamese.count("#142") == 2, "the Kiro CLI line and the founder-permits line"
