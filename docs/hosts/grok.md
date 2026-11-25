# Grok Build

Status: written from the installer's output; registration and a golden-case run on this host are not yet witnessed. "Grok" here means the Grok Build CLI; chat bots without a filesystem are out of scope for v1 (design §1).

## Install

```bash
founder-vn install --host grok
```

Copies the skills into `.grok/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing). Alternative: `npx skills add NHAN-AI-VN/founder-vn`.

## MCP registration

`founder-vn install --host grok` writes `.grok/config.toml` at the project root when it does not exist; when it exists, the installer prints the snippet and leaves the file unchanged (add the entry by hand). Grok Build reads `[mcp_servers]` from the project `.grok/config.toml` (other sections belong in `~/.grok/config.toml`, which the installer never writes). The entry:

```toml
[mcp_servers.founder-vn]
command = "uvx"
args = ["--from", "founder-vn", "founder-vn-mcp"]
```

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository.

Reference model for the buyer panel: set `FOUNDER_LLM_MODEL` to `gemini-3.5-flash-lite` (the model chosen by the bake-off, [docs/bakeoff/README.md](../bakeoff/README.md)). Panel results are comparable across hosts and across Owners only when every run uses this model; `results.json` records the model that answered.
