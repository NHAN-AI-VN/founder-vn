# Claude Code

Status: written from the installer's output; registration and a golden-case run on this host are not yet witnessed.

## Install

```bash
founder-vn install --host claude
```

Copies the skills into `.claude/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing). Alternative: `npx skills add NHAN-AI-VN/founder-vn`.

## MCP registration

`founder-vn install --host claude` writes `.mcp.json` at the project root when it does not exist; when it exists, the installer prints the snippet and leaves the file unchanged (add the entry by hand). Project scope:

```json
{
  "mcpServers": {
    "founder-vn": {
      "command": "uvx",
      "args": ["--from", "founder-vn", "founder-vn-mcp"]
    }
  }
}
```

Or: `claude mcp add --scope project founder-vn -- uvx --from founder-vn founder-vn-mcp`.

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository.

Reference model for the buyer panel: set `FOUNDER_LLM_MODEL` to `gemini-3.5-flash-lite` (the model chosen by the bake-off, [docs/bakeoff/README.md](../bakeoff/README.md)). Panel results are comparable across hosts and across Owners only when every run uses this model; `results.json` records the model that answered.
