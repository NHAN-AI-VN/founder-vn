# Kiro: registering the founder-vn MCP server

Add this to the Kiro `mcp.json` (workspace `.kiro/settings/mcp.json` or user level):

```json
{
  "mcpServers": {
    "founder-vn": {
      "command": "uvx",
      "args": ["--from", "founder-vn", "founder-vn-mcp"]
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

Reference model for the buyer panel: set `FOUNDER_LLM_MODEL` to `gemini-3.5-flash-lite` (the model
chosen by the bake-off, [docs/bakeoff/README.md](../bakeoff/README.md)). Panel results are
comparable across hosts and across Owners only when every run uses this model; `results.json`
records the model that answered.

`uvx --from founder-vn founder-vn-mcp` resolves the package from PyPI, so it works once the `v0.2.0` release (the first on PyPI) is
published (see `.github/workflows/release.yml`).

## Installing the skills

```bash
founder-vn install --host kiro
```

Copies the skills into `.kiro/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing) and prints the `mcp.json` registration above.
