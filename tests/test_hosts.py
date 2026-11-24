"""The Kiro registration in docs/hosts/kiro.md is valid JSON naming the console script."""

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).parent.parent


def _snippet() -> dict:
    text = (ROOT / "docs" / "hosts" / "kiro.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```json\n(.*?)\n```", text, re.DOTALL)
    assert blocks, "docs/hosts/kiro.md has no json block"
    return json.loads(blocks[0])


def test_kiro_mcp_json_registers_the_console_script() -> None:
    entry = _snippet()["mcpServers"]["founder-vn"]
    scripts = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"][
        "scripts"
    ]
    assert entry["command"] == "uvx"
    assert entry["args"] == ["--from", "founder-vn", "founder-vn-mcp"]
    assert entry["args"][-1] in scripts


def test_kiro_doc_carries_no_secret_values() -> None:
    text = (ROOT / "docs" / "hosts" / "kiro.md").read_text(encoding="utf-8")
    assert "FOUNDER_LLM_API_KEY" in text
    assert not re.search(r"(sk-|Bearer )\w", text)


def _page(name: str) -> str:
    return (ROOT / "docs" / "hosts" / f"{name}.md").read_text(encoding="utf-8")


def test_gemini_page_is_pending_confirmation_and_declares_the_key_by_name() -> None:
    text = _page("gemini")
    assert "pending confirmation" in text
    assert "FOUNDER_LLM_API_KEY" in text and '"env"' in text
    assert not re.search(r"(sk-|Bearer )\w", text)


def test_filled_pages_have_no_stub_status_and_match_the_installer() -> None:
    from founder_vn import install

    for host in install.HOSTS:
        text = _page(host)
        assert "Status: stub" not in text, host
        assert f"founder-vn install --host {host}" in text
        assert "not yet released" not in text.split("npx skills")[0], host
        assert install.SKILL_FOLDERS[host] in text


def test_codex_page_carries_the_timeout_note_and_kirocrew_the_trust_note() -> None:
    assert "60 seconds" in _page("codex") and "tool_timeout_sec" in _page("codex")
    assert "dashboard" in _page("kirocrew") and "trust" in _page("kirocrew").lower()


def test_toml_and_json_snippets_in_pages_parse() -> None:
    for host in ("claude", "codex", "grok"):
        for block in re.findall(r"```toml\n(.*?)\n```", _page(host), re.DOTALL):
            assert "founder-vn" in tomllib.loads(block)["mcp_servers"]
    for block in re.findall(r"```json\n(.*?)\n```", _page("claude") + _page("gemini"), re.DOTALL):
        json.loads(block)


def test_hosts_readme_lists_every_page_without_stub_state() -> None:
    text = _page("README")
    for name in ("kiro", "claude", "codex", "gemini", "grok", "kirocrew"):
        assert f"({name}.md)" in text
    assert "| stub" not in text


def test_every_host_page_starts_the_server_with_uvx_from_the_package() -> None:
    for name in ("README", "kiro", "claude", "codex", "gemini", "grok", "kirocrew"):
        text = _page(name)
        assert "uvx founder-vn-mcp" not in text, name
        assert re.search(r"--from\W+founder-vn\W+founder-vn-mcp", text), name


def test_kiro_page_has_the_clean_install_walkthrough_for_19() -> None:
    text = _page("kiro")
    assert "## Clean-install walkthrough" in text
    section = text.split("## Clean-install walkthrough", 1)[1]
    for needle in (
        "uvx --from ./dist/founder_vn-0.2.0-py3-none-any.whl founder-vn install --host kiro",
        "uvx --from founder-vn founder-vn install --host kiro",
        "FOUNDER_LLM_BASE_URL",
        "FOUNDER_LLM_API_KEY",
        "FOUNDER_LLM_MODEL",
        "founder/business-plan.md",
        'version: "1.0.0"',
        "On a major mismatch, stop and tell the Facilitator to update the package or the skill",
        "| step | command | started | duration | friction | issue filed |",
    ):
        assert needle in section, needle
    order = [
        section.index(f"founder-{name}")
        for name in ("board", "competitors", "consumer", "pricing", "cfo", "plan")
    ]
    assert order == sorted(order)
    assert not re.search(r"(sk-|Bearer )\w|FOUNDER_LLM_\w+=\S", section)


def test_issue_19_template_has_unticked_boxes_and_claims_no_run() -> None:
    text = (ROOT / "docs" / "evidence" / "issue-19-wave-a-walkthrough.md").read_text(
        encoding="utf-8"
    )
    boxes = re.findall(r"^- \[( |x)\] ", text, re.MULTILINE)
    assert len(boxes) == 4 and set(boxes) == {" "}
    assert "| step | command | started | duration | friction | issue filed |" in text
    assert "operator fills" in text and "real Kiro CLI" in text
    assert not re.search(r"^\|\s*\d+\s*\|", text, re.MULTILINE)
