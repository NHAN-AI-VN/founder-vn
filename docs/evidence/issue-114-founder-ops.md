# Evidence: issue #114 founder-ops skill

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-ops/SKILL.md`: structure, the no-invented-data rule, the `numbers.json` ownership sentence, the permits pointer. Checked by `scripts/skill_lint.py` and `tests/test_ops_skill.py`.
- `examples/barbershop/founder/ops.md`: seven sections in order, exactly ten risk rows, "chưa có báo giá" where no quote exists, no `$`, disclaimer. Checked in `tests/test_ops_skill.py`.
- `examples/barbershop/founder/business-plan.md`: compiler output with the `Vận hành` section (`tests/test_plan_example.py`).
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.
