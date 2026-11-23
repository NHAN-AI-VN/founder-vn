# Evidence: issue #13 founder-competitors, field-survey form and skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: the design (§3) makes the skill a prompt plus a printable form, so the seams are the shipped files.

- `skills/founder-competitors/SKILL.md` (skill file): the instructions the host model follows. Seam because the required-form gate, the supplementary-web rule, the output shape and the thin-data warning live only here (criteria 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `skills/founder-competitors/survey-form.md` (printable form, Vietnamese): the file the skill prints for the Owner. Seam because criterion 1 lists its six fields (criterion 1).
- `founder_vn.install` (existing module, unchanged): the skill must be found and copied with its form. Tested through `install.run` against the real `skills/` folder (criteria 1, 2).

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| form, skill gates, output shape, lint, installer | `tests/test_competitors_skill.py` (8 tests) | `FileNotFoundError: [Errno 2] No such file or directory: '.../skills/founder-competitors/SKILL.md'` (and `survey-form.md`) | `uv run pytest tests/test_competitors_skill.py -q` (8 passed) |

The red run was witnessed before the skill files existed; one slice because the form and the skill are one deliverable and the tests read both. The tests check the text of the instructions (the required-form stop, the supplementary and linked rule, the no-invention rule, the table, the thin-data warning), not model behaviour.

## Cổng ba đoạn

Last code commit: `c50706a`. Each segment ran once at that HEAD; counts read from `.harness/gate-*.log`.

```
static: ruff check "All checks passed!", ruff format --check "132 files already formatted", skill-lint "1 skill checked, 0 finding(s)"
unit:   233 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl (contains skills/founder-competitors)
gate-segment verify: GREEN on c50706a8c96ed284e019e3906e8df321dac176b6
```

## Giới hạn

- **Criterion 4 is not proven.** No golden case was run: the Owner's real field survey of the barbershop case is not in the repository, and a competitor list or numbers written by the lane would be fabricated, which the skill itself forbids. `examples/barbershop/founder/competitors.md` is therefore absent and the review checklist was not passed on a real output. The ticket is BLOCKED on the real survey.
- The skill was never run on a model (Kiro CLI or other); the tests read the instruction text only. Whether a model obeys the required-form stop is untested.
- The survey form is the lane's design of the six fields in the ticket plus a review-count table (needed for the thin-data rule); the Owner has not tried it on foot.
- No CLI or MCP tool was added: the design asks for none, and the thin-data count is read from the form by the model.
- README skill table was not changed.

## Giải quyết review nội bộ
