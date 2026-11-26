# Evidence: issue #116 founder-launch skill

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-launch/SKILL.md`: structure, the real-price rule, the no-invented-date/number rule, the owner-as-role rule. Checked by `scripts/skill_lint.py` and `tests/test_launch_skill.py`.
- `examples/barbershop/founder/launch.md`: sections in order, countdown rows D-30 to D-0, run sheet, panel caveat, disclaimer, no `$`. Checked in `tests/test_launch_skill.py`.
- `examples/barbershop/founder/business-plan.md`: compiler output whose `## Chưa làm` has exactly the two after-pilot lines (`tests/test_plan_example.py`).
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.
