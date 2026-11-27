# Evidence: issue #143 panel init refuses a re-deal over answers of another deal (Q58)

## Seam

Inferred from the acceptance criteria of the ticket body (the ticket's own Seam section was written by AI at triage; refined here).

- `panel.init` behind `founder-vn panel init` (`tests/test_panel_cli.py`): the refusal (exit 2, stderr text, files byte-identical) and the pass-through of an identical deal.
- MCP `panel_init` (`tests/test_panel_parity.py`): the same text as a tool error; one `panel.init`, so one text.
- `skills/founder-consumer/SKILL.md` Step 3 (`tests/test_consumer_skill.py`): the refusal sentence.
- `docs/founder-vn-design.md`: Q58 and the §2 clause.

## Lát

(filled in below)
