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

```
bash scripts/harness/gate-segment.sh static    # exit 0 (ruff, format, skill-lint: 8 skills, 17 example files, 0 findings)
bash scripts/harness/gate-segment.sh unit      # exit 0 (404 passed)
bash scripts/harness/gate-segment.sh build     # exit 0 (Successfully built dist/founder_vn-0.2.0-py3-none-any.whl)
bash scripts/harness/gate-segment.sh verify    # see the PR body for the HEAD it was green on
```

## Giới hạn

- No Kiro CLI run: the golden `ops.md` was written by the lane following `skills/founder-ops/SKILL.md` in the sandbox, as #13 and #112 did. No model call, no panel.
- No real quotes: every supplier, quote and source cell is "chưa chọn", "chưa có báo giá" or "chưa có". The golden proves the empty path only.
- The cost feedback loop is described to the Owner (update `numbers.json` through `founder-cfo`, then re-run `founder-pricing` and `founder-plan`), not exercised on the golden.
- The rota and the ten risks are proposals from `idea.md`, not measured; tests check structure and forbidden content, not whether the routines suit a real shop.
