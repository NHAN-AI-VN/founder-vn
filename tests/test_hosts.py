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
    assert entry["args"] == ["founder-vn-mcp"]
    assert entry["args"][0] in scripts


def test_kiro_doc_carries_no_secret_values() -> None:
    text = (ROOT / "docs" / "hosts" / "kiro.md").read_text(encoding="utf-8")
    assert "FOUNDER_LLM_API_KEY" in text
    assert not re.search(r"(sk-|Bearer )\w", text)
