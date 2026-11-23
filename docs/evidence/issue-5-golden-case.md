# Evidence: issue #5 golden case (idea.md for the chosen business)

Lane run by the project owner on Kiro CLI (the ticket is `ready-for-human`; the dispatcher skips it). The operator's allocation comment on #5 (2026-11-23T06:43:15Z) grants `README.md`, lane branch `lane/issue-5`, target `main`.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `examples/barbershop/founder/idea.md`: the idea file of the golden case, in the upstream shape (`founder-board/SKILL.md` step 0: title plus the five bullets what, who, what at what price, where and how, budget and constraints), Vietnamese, VND. It is the file every skill reads first (spec #1: "one project root per Owner", artifacts keep upstream's names; design §5: `examples/<case-mẫu>/founder/`), so its path and shape are the public boundary; asserted by content in `tests/test_golden_case.py`.
- `examples/barbershop/**/*.md` anonymised: no personal names, no phone numbers or e-mail addresses, no street address, location at former-district level, no `$` next to a digit (`scripts/skill_lint.py` scans `examples/**/*.md`; the test repeats the `$` check and adds the phone, e-mail and street-address shapes).
- `README.md` (single-owner, allocated): names `examples/barbershop/` as the golden case; asserted by `tests/test_golden_case.py`.
- `docs/founder-vn-design.md`: the sector change of the golden case (Q51, amending Q21 and the week-1 row of §7) lands in this change because the design wins over code and the owner changed the design here; not a test seam, reviewed by reading.

No automated seam exists for the skills that will consume the file (spec #1: "Skills have no automated seam"); this ticket proves the file and its pointer, not a skill run.
