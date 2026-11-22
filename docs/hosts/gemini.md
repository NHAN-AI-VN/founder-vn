# Gemini / Antigravity CLI

Status: stub. This host needs confirmation at install time (design §5): check which CLI the
Facilitator has before following any step here.

- Skills: `npx skills add NHAN-AI-VN/founder-vn`. `founder-vn install` has no `gemini` host value
  in v1.
- MCP server: `uvx founder-vn-mcp`. Gemini CLI drops environment variables whose names contain
  `KEY` or `SECRET` when it starts an MCP server unless they are declared in the server `env`
  block (design §1); declare `FOUNDER_LLM_API_KEY` there by name, with no value in the repository.
- Environment: `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL`.
