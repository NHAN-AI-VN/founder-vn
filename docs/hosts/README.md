# Host pages

One page per supported host. Only [Kiro](kiro.md) is verified end to end so far; the other pages
are stubs that name what still has to be confirmed (design §5). The MCP server command is the same
everywhere: `uvx founder-vn-mcp` (not yet released until `v0.1.0` is published).

| Host | Page | State |
|---|---|---|
| Kiro CLI | [kiro.md](kiro.md) | written |
| Claude Code | [claude.md](claude.md) | stub |
| Codex | [codex.md](codex.md) | stub |
| Gemini / Antigravity CLI | [gemini.md](gemini.md) | stub, needs confirmation at install |
| Grok Build | [grok.md](grok.md) | stub |
| KiroCrew | [kirocrew.md](kirocrew.md) | stub |

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the
host environment. Never write their values into a host config or into this repository.
