# Evidence: issue #112 founder-permits skill, common path

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-permits/SKILL.md`: the instructions the host model follows. Checked by `scripts/skill_lint.py` and by reading the text in `tests/test_permits_skill.py` (structure, the never-guess rule, the fallback wording, the disclaimer).
- `permits/sources.md`: the only place a legal figure may come from. Checked by `tests/test_sources_ledger.py`.
- `examples/barbershop/founder/permits.md`: the file the Owner reads. Checked for section presence, links with dates, no `$`.
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.

## Lát

(filled slice by slice)
