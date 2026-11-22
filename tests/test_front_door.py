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
