# Evidence: issue #115 founder-marketing skill

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-marketing/SKILL.md`: structure, the channel list, the objection-traceability rule, the no-invented-quote rule. Checked by `scripts/skill_lint.py` and `tests/test_marketing_skill.py`.
- `examples/barbershop/founder/marketing.md`: sections in order, 30 campaign rows, every hook with an objection source, panel caveat once, disclaimers, no `$`. Checked in `tests/test_marketing_skill.py`.
- `examples/barbershop/founder/business-plan.md`: compiler output with the `Tiếp thị` section (`tests/test_plan_example.py`).
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.
