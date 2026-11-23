# Claude Code

Status: written from the installer's output; registration and a golden-case run on this host are not yet witnessed.

## Install

```bash
founder-vn install --host claude
```

Copies the skills into `.claude/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing). Alternative: `npx skills add NHAN-AI-VN/founder-vn`.

## MCP registration

Project scope, in `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "founder-vn": {
      "command": "uvx",
      "args": ["founder-vn-mcp"]
    }
  }
}
```

Or: `claude mcp add --scope project founder-vn -- uvx founder-vn-mcp`.

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository.
