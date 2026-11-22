# Grok Build

Status: stub. "Grok" here means the Grok Build CLI; chat bots without a filesystem are out of scope
for v1 (design §1).

- Skills: `founder-vn install --host grok` (not yet released) or `npx skills add NHAN-AI-VN/founder-vn`
  (installs into `.grok/skills/`).
- MCP server: `uvx founder-vn-mcp`, registered in the Grok Build configuration.
- Environment: set `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` in the
  host environment; never write their values into a file in this repository.
