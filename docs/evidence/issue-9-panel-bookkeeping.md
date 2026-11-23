# Evidence: issue #9 panel bookkeeping, init and tally

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.panel` (module): the one set of functions behind both transports: `deal` (personas from `customer.json` and `pitch.md`, quotas by largest remainder, seeded), `init`, `check` and `save` (validate and store buyer answers, `save` refuses invalid answers, as upstream), `tally` (buy rate overall and by segment or behaviour, reasons with quotes, what would flip a no, the four price answers, excluded buyers, `results.md` and `results.json`). Criteria 1, 2, 3, 4, 5.
- `founder-vn panel init|check|save|tally` (CLI commands): one end of the parity pair; golden tests by seed run through it, and `customer.json` validation errors are asserted to name the offending field. Criteria 1, 2, 4, 5.
- `panel_init` and `panel_tally` (MCP tools of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files. Criterion 5.
- `founder_vn.files` (path-locked layer): the only way files under `founder/panel/` are written, so a path escape stays refused. Criteria 1, 3.
