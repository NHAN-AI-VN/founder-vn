# Evidence: issue #114 founder-ops skill

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-ops/SKILL.md`: structure, the no-invented-data rule, the `numbers.json` ownership sentence, the permits pointer. Checked by `scripts/skill_lint.py` and `tests/test_ops_skill.py`.
- `examples/barbershop/founder/ops.md`: seven sections in order, exactly ten risk rows, "chưa có báo giá" where no quote exists, no `$`, disclaimer. Checked in `tests/test_ops_skill.py`.
- `examples/barbershop/founder/business-plan.md`: compiler output with the `Vận hành` section (`tests/test_plan_example.py`).
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.

## Lát

Every test runs with no network and no model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| founder-ops skill | `tests/test_ops_skill.py` (8 skill tests) | all failed with `FileNotFoundError: .../skills/founder-ops/SKILL.md`; after the file existed, the protocol-block test failed on a stray blank line and the permits test on the wording `restate no legal figure`, both fixed in the skill | `uv run pytest tests/test_ops_skill.py -q` (8 passed); `uv run python scripts/skill_lint.py` 0 findings |
| golden `ops.md` | `tests/test_ops_skill.py` (6 golden tests: seven sections in order, exactly ten risk rows, every supplier row "chưa chọn" / "chưa có báo giá" with no digit, ownership sentence, permits pointer with no digit and no `%`, disclaimer, no `$`) | 6 failed with `FileNotFoundError: .../examples/barbershop/founder/ops.md` | `uv run pytest tests/test_ops_skill.py -q` (14 passed) |
| `business-plan.md` regenerated | `tests/test_plan_example.py::test_business_plan_is_the_compiler_output_and_check_passes`; `tests/test_ops_skill.py::test_business_plan_carries_the_ops_section` | with `ops.md` present and the old plan file: `AssertionError: assert '# Kế hoạch k... == '# Kế hoạch k...'`; the new test failed with `assert '## Vận hành' in ...` on the old plan | `founder-vn plan` in `examples/barbershop` (+104 lines, -1: the "Vận hành" pointer becomes the section), then `uv run pytest tests/test_plan_example.py tests/test_ops_skill.py -q` (22 passed) |
| README row and front door | `tests/test_front_door.py` (`founder-ops` moves to the shipped set with `#114` and `ops.md`; marketing and launch stay "not started") | with the README row restored: `assert ('#114' in '| `founder-ops` | | not started (Wave B) | |')` | `uv run pytest tests/test_front_door.py -q` (12 passed) |

`numbers.json`, `cfo.md`, `pricing.md` and `summary.md` are unchanged (`git diff main --stat` lists none of them). The only compiler output that changed is `business-plan.md`, regenerated because `ops.md` now exists.

## Cổng ba đoạn

Rerun after the review fixes, once per segment, on code commit `4af23f0` (the last commit that changed code or golden files is `bafdcc7`; `a25e076` and `4af23f0` touch only evidence and review files).

```
bash scripts/harness/gate-segment.sh static    # exit 0 (ruff check, ruff format --check, skill-lint: 0 findings)
bash scripts/harness/gate-segment.sh unit      # exit 0 (407 passed)
bash scripts/harness/gate-segment.sh build     # exit 0 (Successfully built dist/founder_vn-0.2.0-py3-none-any.whl)
bash scripts/harness/gate-segment.sh verify    # gate-segment verify: GREEN on 4af23f09f72c3b38d8bdf689d5dc2b77c6efe581
```

## Giới hạn

- No Kiro CLI run: the golden `ops.md` was written by the lane following `skills/founder-ops/SKILL.md` in the sandbox, as #13 and #112 did. No model call, no panel.
- No real quotes: every supplier, quote and source cell is "chưa chọn", "chưa có báo giá" or "chưa có". The golden proves the empty path only.
- The cost feedback loop is described to the Owner (update `numbers.json` through `founder-cfo`, then re-run `founder-pricing` and `founder-plan`), not exercised on the golden.
- The rota and the ten risks are proposals from `idea.md`, not measured; tests check structure and forbidden content, not whether the routines suit a real shop.

## Giải quyết review nội bộ

Sources: `.agents/tasks/task-founder-ops-skill/2026-11-26-050000-review.md` (four issues) and `reviews/issue-114/spec.md` round 1 (SPEC-1, the same rota defect as review issue 2, counted as 41 thợ slots against 25).

| Issue | Decision | Where |
|---|---|---|
| 1. Closing routine assigns the manager, rota had the manager only in the morning | Fixed: the rota now has "quản lý cả ngày" on every open day, plus the part-time lễ tân on the afternoon | `ops.md` section 2 |
| 2. Rota did not reconcile with headcount (also SPEC-1) | Fixed: one ca is defined as one working day of at most 8 hours; the rota lists thợ per day (3, 3, 3, 4, 4, 4 = 21 ca a week), which fits 5 thợ at 5 ca (25) and leaves each thợ a day off besides Monday | `ops.md` section 2 |
| 3. Weekdays show 3 thợ against 4 chairs | Fixed by stating it: the text says Tuesday to Thursday run below the planned capacity of 4 chairs and that full staffing would need 24 ca, still within 25 | `ops.md` section 2 |
| 4. No test relates the routines to the rota | Fixed: two tests in `tests/test_ops_skill.py` | see below |

Red then green:

- `test_golden_rota_covers_every_role_the_routines_name`: red on the old `ops.md` with `IndexError: list index out of range` (the old table had no per-role columns); green on the new one.
- `test_golden_rota_thợ_slots_fit_the_headcount`: red with `assert '20 ca thợ một tuần' in ...` against the old staffing text (summing to 41 slots would also have failed the `<= 25` bound); green now.
- `test_skill_requires_a_feasible_rota`: red with `assert 'The rota must be feasible' in ...` before the skill sentence existed; green after. The skill now tells the model to make the rota add up, name who holds each opening and closing duty, and say where a day runs below capacity (the SPEC-1 suggestion to tighten the skill).
- Rerun: `uv run pytest tests/test_ops_skill.py tests/test_plan_example.py -q`.

`business-plan.md` was regenerated with `founder-vn plan` in its own commit, because the compiler embeds `ops.md` and section 2 changed. `numbers.json`, `cfo.md`, `pricing.md` and `summary.md` are unchanged.

Not fixed: the rota is still a proposal. The tests check that it adds up and names every role; they do not show it suits a real shop. The golden is still written by the lane, not by a model run.

### Review standards, round 1 (`reviews/issue-114/standards.md`)

| Issue | Decision | Where |
|---|---|---|
| S1. The `verify` line pointed to the PR body and named no SHA | Fixed: the block above now records the rerun of the three segments and `verify` with `GREEN on 4af23f09f72c3b38d8bdf689d5dc2b77c6efe581`; later commits are evidence only | `## Cổng ba đoạn` |
| Wording in section 6 of the skill repeats "restate no legal figure" (reviewer note, not a violation) | Not fixed: the review names no violated standard, the lint and tests pass, and a wording-only edit would force a new gate rerun for no behaviour change | `skills/founder-ops/SKILL.md` |

The spec review's SPEC-1 is answered in the table above (issue 2). Its unverified note about the `verify` line is answered by S1.
