# Grok Build

Status: written from the installer's output; registration and a golden-case run on this host are not yet witnessed. "Grok" here means the Grok Build CLI; chat bots without a filesystem are out of scope for v1 (design §1).

## Install

```bash
founder-vn install --host grok
```

Copies the skills into `.grok/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing). Alternative: `npx skills add NHAN-AI-VN/founder-vn`.

## MCP registration

In `~/.grok/config.toml`:

```toml
[mcp_servers.founder-vn]
command = "uvx"
args = ["founder-vn-mcp"]
```

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository.
