# Kiro: registering the founder-vn MCP server

Add this to the Kiro `mcp.json` (workspace `.kiro/settings/mcp.json` or user level):

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

`founder-vn-mcp` is the console script of the `founder-vn` package (`pyproject.toml`,
`[project.scripts]`). The server answers the `server_info` tool with the package version, the same
text as `founder-vn version`.

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the
environment of the host. Set them in the host's own environment; do not write their values into
`mcp.json` or into this repository.

`uvx founder-vn-mcp` resolves the package from PyPI, so it works once the `v0.1.0` release is
published (see `.github/workflows/release.yml`).
