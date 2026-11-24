# KiroCrew

Status: written from the installer's output; the dashboard steps and a golden-case run are not yet witnessed.

## Install

```bash
founder-vn install --host kirocrew
```

Copies the skills into `.kiro/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing). KiroCrew reads `<project>/.kiro/skills/` once the project is trusted.

## MCP registration

KiroCrew does not read the workspace `.kiro/settings/mcp.json`, so the registration in [kiro.md](kiro.md) does not apply. Register through the dashboard:

1. Open the KiroCrew dashboard, MCP Servers page, and add a server.
2. Name `founder-vn`, command `uvx`, arguments `founder-vn-mcp`.
3. Trust the project in KiroCrew; skills and servers load only for a trusted project.

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository. In KiroCrew use the dashboard or the host environment.

Reference model for the buyer panel: set `FOUNDER_LLM_MODEL` to `gemini-3.5-flash-lite` (the model chosen by the bake-off, [docs/bakeoff/README.md](../bakeoff/README.md)). Panel results are comparable across hosts and across Owners only when every run uses this model; `results.json` records the model that answered.
