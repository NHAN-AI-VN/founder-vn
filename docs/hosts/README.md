# Host pages

One page per supported host. Only [Kiro](kiro.md) is verified end to end so far; the other pages
are written from the output of `founder-vn install --host <host>` and say what is not yet witnessed (design §5). The MCP server command is the same
everywhere: `uvx founder-vn-mcp` (it resolves once `v0.1.0` is published).

| Host | Page | State |
|---|---|---|
| Kiro CLI | [kiro.md](kiro.md) | written |
| Claude Code | [claude.md](claude.md) | written, not witnessed on host |
| Codex | [codex.md](codex.md) | written, not witnessed on host |
| Gemini / Antigravity CLI | [gemini.md](gemini.md) | pending confirmation |
| Grok Build | [grok.md](grok.md) | written, not witnessed on host |
| KiroCrew | [kirocrew.md](kirocrew.md) | written, not witnessed on host |

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the
host environment. Never write their values into a host config or into this repository.
