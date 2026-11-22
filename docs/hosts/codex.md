# Codex

Status: stub. Registration and a golden-case run on this host are still to be done.

- Skills: `founder-vn install --host codex` (not yet released) or `npx skills add NHAN-AI-VN/founder-vn`.
- MCP server: `uvx founder-vn-mcp`, registered in the Codex configuration. Codex applies a default
  tool timeout of 60 seconds (design §1); raise it for long panel jobs.
- Environment: set `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` in the
  host environment; never write their values into a file in this repository.
