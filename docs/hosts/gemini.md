# Gemini / Antigravity CLI

Status: pending confirmation. This host needs confirmation at install time (design §5): check which CLI the Facilitator has before following any step here. Nothing on this page has been run on the host.

`founder-vn install` has no `gemini` host value in v1; install the skills with `npx skills add NHAN-AI-VN/founder-vn`.

## MCP registration

```json
{
  "mcpServers": {
    "founder-vn": {
      "command": "uvx",
      "args": ["founder-vn-mcp"],
      "env": {
        "FOUNDER_LLM_API_KEY": "$FOUNDER_LLM_API_KEY"
      }
    }
  }
}
```

Gemini CLI drops environment variables whose names contain `KEY` or `SECRET` when it starts an MCP server unless they are declared in the server `env` block (design §1). The block above declares `FOUNDER_LLM_API_KEY` by name and refers to the host environment; the repository holds no value. Whether the host expands the `$NAME` reference is pending confirmation.

## Environment

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the host environment. Set them there; never write their values into a config file or this repository.
