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
        "uvx --from ./dist/founder_vn-0.3.1-py3-none-any.whl founder-vn install --host kiro",
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
        for name in ("board", "competitors", "consumer", "cfo", "pricing", "plan")
    ]
    assert order == sorted(order), "founder-pricing reads cfo.md, so founder-cfo runs first"
    wave_b = [
        section.index(f"founder-{name}`") for name in ("permits", "ops", "marketing", "launch")
    ]
    plan_again = section.index("`founder-plan` again", wave_b[-1])
    check = section.index("`founder-vn plan --check`", plan_again)
    assert wave_b == sorted(wave_b) and order[-1] < wave_b[0] < wave_b[-1] < plan_again < check
    assert section.index("Deliberate major-mismatch check") > check
    assert "founder_vn-0.2.0" not in section
    assert not re.search(r"(sk-|Bearer )\w|FOUNDER_LLM_\w+=\S", section)
    # v0.2.0 is on PyPI: the page must not say the release is still to come (S1).
    assert not re.search(
        r"(?i)before the\s+`?v?[\d.]*`?\s*tag|once the `v0\.2\.0`|after the tag", text
    )
    # #118 ran on 0.3.0: the page links its record and names the defect it found.
    assert "../evidence/issue-118-wave-b-walkthrough.md" in section
    assert "issue-#118" not in text and "pending" not in section
    assert "2026-11-26" in section and "#118" in section and "#142" in section
    # #149: v0.3.1 (2026-11-27) is the current release; a clean install of it writes the ledger and
    # the two steps #142 broke were re-run on it (2026-11-28), recorded in the #149 evidence.
    assert "`v0.3.1` (published 2026-11-27) is the current release" in text
    assert "`v0.3.0` (published 2026-11-26) is the current release" not in text
    assert "`v0.3.0` (published 2026-11-26)" in text
    assert "../evidence/issue-149-release-0-3-1.md" in section
    assert "re-run on a clean install of 0.3.1 on 2026-11-28" in section and "#149" in section
    assert "lacked `permits/sources.md` (#142)" in section
    assert (
        "From the first release that" not in section and "lacks `permits/sources.md`" not in section
    )
    # #142 (Q57): the installer writes the ledger; the page no longer presents it as an open defect.
    assert "Known defect #142" not in text
    assert "step 2 (`founder-vn install --host kiro`) writes `permits/sources.md`" in text
    # #118 criterion 4 ran on 0.3.0 the day after the walkthrough: step 9 is no longer 0.2.0-only.
    assert "run on 0.2.0 only" not in section and "2026-11-27" in section


def test_kiro_step_9_expects_the_vietnamese_stop_and_keeps_the_step_1_condition() -> None:
    # #148 (Q60): the stop on a major mismatch is Vietnamese, in the shape the Protocol block quotes.
    text = _page("kiro")
    step9 = text.split("Deliberate major-mismatch check", 1)[1].split("\n\n", 1)[0]
    assert "Dừng ở bước 1 của Protocol" in step9
    assert "Vietnamese" in step9
    assert (
        "On a major mismatch, stop and tell the Facilitator to update the package or the skill"
    ) in step9
    assert "English" not in step9


def test_issue_118_evidence_records_the_kiro_cli_run() -> None:
    evidence = ROOT / "docs" / "evidence"
    assert not (evidence / "issue-#118-wave-b-walkthrough.md").exists(), "the template is replaced"
    text = (evidence / "issue-118-wave-b-walkthrough.md").read_text(encoding="utf-8")
    criteria = re.findall(r"^- \[( |x)\] (.*)$", text, re.MULTILINE)
    assert len(criteria) == 7, "the seven #118 criteria"
    ticked = [i for i, (box, _) in enumerate(criteria, 1) if box == "x"]
    assert ticked == [1, 2, 3, 4, 5, 6], ticked
    # Criterion 4 (SPEC-1 of reviews/issue-118/spec.md): the stop was observed on 0.3.0, not inferred.
    assert "observed on 0.3.0" in criteria[3][1] and "2026-11-27" in criteria[3][1]
    assert "skipped by the operator" not in criteria[3][1]
    assert "| step | command | started | duration | friction | issue filed |" in text
    rows = re.findall(r"^\|\s*(\d+(?:\.\d+)?)\s*\|", text, re.MULTILINE)
    assert len(rows) >= 15, "steps 1 to 9, one row per skill of both waves"
    for needle in (
        "uvx --no-cache --from founder-vn founder-vn --version",
        "founder-vn 0.3.0",
        "founder/business-plan.md",
        "plan --check",
        "gemini-3.5-flash-lite",
        "claude-opus-5.5",
        "#142",
        "#143",
        "#144",
        "## Giới hạn",
        # the major-mismatch run: the edit, the command, the quoted stop, the friction issue
        'version: "1.0.0"',
        "kiro-cli chat --no-interactive",
        "I stopped at the skill's first step, the version check",
        "The founder-vn MCP server reports `founder-vn 0.3.0`",
        "#148",
    ):
        assert needle in text, needle
    assert "operator fills" not in text and "No walkthrough has been recorded" not in text
    assert not re.search(r"(sk-|Bearer )\w|FOUNDER_LLM_\w+=\S", text)


def test_issue_19_evidence_records_the_kiro_cli_run() -> None:
    text = (ROOT / "docs" / "evidence" / "issue-19-wave-a-walkthrough.md").read_text(
        encoding="utf-8"
    )
    boxes = re.findall(r"^- \[( |x)\] ", text, re.MULTILINE)
    assert len(boxes) >= 4 and set(boxes[:4]) == {"x"}, "the four #19 criteria are ticked"
    assert "| step | command | started | duration | friction | issue filed |" in text
    rows = re.findall(r"^\|\s*(\d+(?:\.\d+)?)\s*\|", text, re.MULTILINE)
    assert len(rows) >= 13, "steps 1 to 8, with one row per Wave A skill"
    for needle in (
        "uvx --from founder-vn founder-vn install --host kiro",
        "founder-vn 0.2.0",
        "founder/business-plan.md",
        "plan --check",
        'version: "1.0.0"',
        "lệch số major",
        "#93",
        "#94",
        "#95",
        "## Giới hạn",
    ):
        assert needle in text, needle
    assert "operator fills" not in text and "No walkthrough has been recorded" not in text
    assert not re.search(r"(sk-|Bearer )\w|FOUNDER_LLM_\w+=\S", text)


def test_host_pages_name_the_project_registration_file_the_installer_writes() -> None:
    from founder_vn import install

    for host, (rel, _content) in install.REGISTRATION_FILES.items():
        assert rel in _page(host), host
    assert "kirocrew" not in install.REGISTRATION_FILES
