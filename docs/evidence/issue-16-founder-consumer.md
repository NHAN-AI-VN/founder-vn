# Evidence: issue #16 founder-consumer skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: the panel tools (`panel_init`, `panel_run`, `job_status`, `panel_tally`) already exist, so the seams are the shipped skill and the golden example files.

- `skills/founder-consumer/SKILL.md` (skill file): the instructions the host model follows. Seam because the customer-profile confirmation, the pitch rules, the default `n`, the tool order, the never-answer-for-a-buyer rule, the five-point read-back and the caveat live only here (criteria 1 to 4). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `examples/barbershop/founder/customer.json`, `pitch.md`, `panel/` (golden case): the files the skill produces. Seam because criterion 5 asks for them. Checked by loading `customer.json` through `panel.validate_customer`, by the pitch rules, by the panel counts and by `test_example_is_anonymised`.
- `founder_vn.panel` (existing module, unchanged): the golden test reads its output files only.
