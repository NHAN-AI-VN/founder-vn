# Codex

Status: written from the installer's output; registration and a golden-case run on this host are not yet witnessed.

## Install

```bash
founder-vn install --host codex
```

Copies the skills into `.agents/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing). Alternative: `npx skills add NHAN-AI-VN/founder-vn`.

## MCP registration

In `~/.codex/config.toml`:

```toml
[mcp_servers.founder-vn]
command = "uvx"
args = ["founder-vn-mcp"]
tool_timeout_sec = 300
```

Codex stops a tool call after 60 seconds by default (design §1). `tool_timeout_sec` raises that limit; keep it raised for long panel jobs.

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository.
