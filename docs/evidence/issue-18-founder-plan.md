# Evidence: issue #18 founder-plan skill and complete Wave A example

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: the plan compiler (`founder_vn.plan`, `founder-vn plan`, MCP `plan_compile`) already exists and stays unchanged.

- `skills/founder-plan/SKILL.md` (skill file): the instructions the host model follows. Seam because writing `summary.md` (executive summary plus a one-page partner or lender version), calling `plan_compile` / `founder-vn plan`, never writing the verdict, and explaining each failing check with the skill that fixes it live only here (criterion 1). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `examples/barbershop/founder/summary.md` and `business-plan.md` (golden case): the files the skill produces. Seam because criterion 2 asks for them. `business-plan.md` is checked against `founder_vn.plan.compile_plan` output (and `plan --check`), `summary.md` for its two parts, its figures against tool output, its links, disclaimer and panel caveat.
- `examples/barbershop/founder/` as a whole plus `README.md` (example completeness): the set of Wave A files, the anonymisation patterns of `tests/test_golden_case.py`, and the README reference (criterion 2).
- Review checklist walk over `skills/` and `examples/` (criterion 3): one test applies the machine-checkable items of `docs/review-checklist.md` to every Wave A artifact.

Design decision: `summary.md` is not an input of the compiler (`plan.SECTIONS` stays unchanged). The ticket does not imply a `plan.py` change, so the summary sits beside `business-plan.md`.

## Lát

## Cổng ba đoạn

## Giới hạn

## Giải quyết review nội bộ
