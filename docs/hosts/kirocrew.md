# KiroCrew

Status: stub.

- Skills: `founder-vn install --host kirocrew` (not yet released). KiroCrew reads
  `<project>/.kiro/skills/` once the project is trusted.
- MCP server: add `uvx founder-vn-mcp` through the KiroCrew dashboard. KiroCrew does not read the
  workspace `mcp.json`, so the registration in [kiro.md](kiro.md) does not apply.
- Environment: set `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` in the
  dashboard or host environment; never write their values into a file in this repository.
