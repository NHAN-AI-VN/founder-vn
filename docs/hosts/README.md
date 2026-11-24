# Host pages

One page per supported host. No host is verified end to end yet; the Kiro walkthrough (#19) is pending, and the pages
are written from the output of `founder-vn install --host <host>` and say what is not yet witnessed (design §5). The MCP server command is the same
everywhere: `uvx --from founder-vn founder-vn-mcp` (it resolves once `v0.2.0`, the first PyPI release, is published).

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

Suggested `FOUNDER_LLM_MODEL`: `gemini-3.5-flash-lite`, the reference model of the buyer panel
chosen by the bake-off of ticket T14 ([docs/bakeoff/README.md](../bakeoff/README.md): what was
tried, what was chosen, why). The panel is comparable across hosts only when this model is used;
`founder/panel/results.json` records the model that answered, so a run on another model is visible.
