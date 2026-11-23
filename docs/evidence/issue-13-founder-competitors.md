# Evidence: issue #13 founder-competitors, field-survey form and skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: the design (§3) makes the skill a prompt plus a printable form, so the seams are the shipped files.

- `skills/founder-competitors/SKILL.md` (skill file): the instructions the host model follows. Seam because the required-form gate, the supplementary-web rule, the output shape and the thin-data warning live only here (criteria 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `skills/founder-competitors/survey-form.md` (printable form, Vietnamese): the file the skill prints for the Owner. Seam because criterion 1 lists its six fields (criterion 1).
- `founder_vn.install` (existing module, unchanged): the skill must be found and copied with its form. Tested through `install.run` against the real `skills/` folder (criteria 1, 2).

## Lát

(filled after the slices)
