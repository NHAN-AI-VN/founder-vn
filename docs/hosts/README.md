# Host pages

One page per supported host. Kiro CLI is verified end to end: the clean-install walkthrough of #118 ran all ten
skills from PyPI release 0.3.0 to `business-plan.md` on 2026-11-26 ([evidence](../evidence/issue-118-wave-b-walkthrough.md)),
and a clean install of 0.3.1 writes the source ledger (#142 fixed in 0.3.1; 0.3.0 on PyPI lacked it), with `founder-permits` and `founder-cfo` re-run on it on 2026-11-28 ([evidence](../evidence/issue-149-release-0-3-1.md));
the walkthrough of #19 ran the six Wave A skills from 0.2.0 on 2026-11-25 ([evidence](../evidence/issue-19-wave-a-walkthrough.md)). The other pages
are written from the output of `founder-vn install --host <host>` and say what is not yet witnessed (design §5). The MCP server command is the same
everywhere: `uvx --from founder-vn founder-vn-mcp` (it resolves from PyPI since `v0.2.0`, the first release, published 2026-11-24; the current release is `v0.3.1`, published 2026-11-27; `v0.3.0` was published 2026-11-26).

| Host | Page | State |
|---|---|---|
| Kiro CLI | [kiro.md](kiro.md) | verified end to end on 0.3.0 incl. Wave B (walkthrough 2026-11-26, #118); on 0.3.1 the installer writes the source ledger and `founder-permits`, `founder-cfo` re-run on a clean install (2026-11-28, #149; #142 fixed); Wave A first on 0.2.0 (walkthrough 2026-11-25, #19) |
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
