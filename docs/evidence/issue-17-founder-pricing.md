# Evidence: issue #17 founder-pricing skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: `pricing_psm` / `founder-vn pricing` (issue #8) and `founder-vn cfo --price` already exist, so the seams are the shipped skill and the golden example files.

- `skills/founder-pricing/SKILL.md` (skill file): the instructions the host model follows. Seam because the call to `pricing_psm` / `founder-vn pricing` on the panel's four price answers, the cross-check with `competitors.md` and `cfo.md`, the below-break-even flag, the `pricing.md` sections, the no-fabricated-anchors rule and the thin-data pass-through live only here (criteria 1 and 2). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `examples/barbershop/founder/pricing_input.json` and `pricing.md` (golden case): the files the skill produces. Seam because criterion 3 asks for `pricing.md`. Checked by section presence, the numbers against the tool output, the break-even flag, the thin-data pass-through, the disclaimer and the panel caveat.
- `founder_vn.pricing` and `founder_vn.cfo` (existing modules, unchanged): the golden test reads their output only.
