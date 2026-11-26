# Evidence: issue #116 founder-launch skill

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-launch/SKILL.md`: structure, the real-price rule, the no-invented-date/number rule, the owner-as-role rule. Checked by `scripts/skill_lint.py` and `tests/test_launch_skill.py`.
- `examples/barbershop/founder/launch.md`: sections in order, countdown rows D-30 to D-0, run sheet, panel caveat, disclaimer, no `$`. Checked in `tests/test_launch_skill.py`.
- `examples/barbershop/founder/business-plan.md`: compiler output whose `## Chưa làm` has exactly the two after-pilot lines (`tests/test_plan_example.py`).
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.

## Lát

Every test runs with no network and no model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| founder-launch skill | `tests/test_launch_skill.py` (10 skill tests: protocol block, frontmatter, six headings in order, one real test at the listed price with the Owner's N and M, D-30 to D-0, run sheet, three measurement sources, panel override, no date/number/name, disclaimer) | all 10 failed with `FileNotFoundError: .../skills/founder-launch/SKILL.md`; after the file existed 2 failed (`assert 'fewer than N real buyers in M days' in ...`, `assert 'one owner per line' in ...`), fixed in the skill | `uv run pytest tests/test_launch_skill.py -q` (10 passed); `uv run python scripts/skill_lint.py` 0 findings |
| golden `launch.md` | `tests/test_launch_skill.py` (8 golden tests: six sections in order, one waitlist at 199.000 đ with a 50.000 đ deposit and the stop rule left as "anh/chị chọn", countdown D-30 to D-0 with a role and a file per row, owners are roles present in `ops.md`, hour-by-hour run sheet, the three measurement sources quoted, panel caveat once, no calendar date, no `$`, closing disclaimer) | with `launch.md` absent: `8 failed, 10 passed` (`FileNotFoundError: .../examples/barbershop/founder/launch.md`) | `uv run pytest tests/test_launch_skill.py -q` (18 passed) |
| `business-plan.md` regenerated | `tests/test_plan_example.py::test_business_plan_lists_only_offer_and_brand_as_not_done` and the existing `test_business_plan_is_the_compiler_output_and_check_passes` | with `launch.md` present and the old plan: `2 failed, 6 passed` (plan not equal to the compiler output; `## Chưa làm` still listed `founder-launch`) | `founder-vn plan` in `examples/barbershop` (+77 lines, -1: the "Khai trương" pointer line becomes the section), `uv run pytest tests/test_plan_example.py -q` (8 passed) |
| README row and front door | `tests/test_front_door.py` (`founder-launch` moves to the shipped set with `#116` and `launch.md`; the "not started" loop is removed) | `assert ('#116' in '\| `founder-launch` \| \| not started (Wave B) \| \|')` | `uv run pytest tests/test_front_door.py -q` (12 passed) |

The golden slice commit carried the stale plan (regenerated in the next commit), so the plan-compiler test was red between those two commits. `numbers.json`, `cfo.md`, `pricing.md`, `marketing.md`, `ops.md`, `permits.md` and `panel/` are unchanged.

## Giới hạn

- No Kiro CLI run: the golden `launch.md` was written by the lane following `skills/founder-launch/SKILL.md` in the sandbox, as #13, #112, #114 and #115 did. No model call, no panel run.
- No real-buyer data: the real-test result slot reads "Kết quả thật: chưa có", and the waitlist stop rule keeps N and M as "anh/chị chọn". The golden proves the structure, not that the waitlist would convert.
- Relative dates only (D-30 to D-0, "Ngày 1" to "Ngày 30"): `idea.md` says the opening is not decided. No legal deadline or fee appears in `launch.md`; it points to `permits.md`.
- Owners are the roles of `ops.md` (quản lý, lễ tân, thợ, phụ tá) or "anh/chị". `idea.md` also names a "thợ trưởng" to hire; `ops.md` has no such role, so the golden does not use it.
- The countdown spacing (which day each step falls on) is a proposal from the lane for the Owner to adjust; no file fixes it.
- Tests check structure and forbidden content; they do not show that a launch would succeed.
- `offer` and `brand` stay in the compiler's section map and in "Chưa làm" (Q55, Q12); this ticket does not remove them.

## Giải quyết review nội bộ

Self-review of the diff against the acceptance criteria and the PR checklist (no `/code-review`, per the lane steering):

- No `$` in skill or examples: `skill_lint` 0 findings; golden test asserts it.
- Every number in `launch.md` is quoted from an Owner file: 199.000 đ, 50.000 đ, 265.000 đ, 9 lượt/ghế/ngày, 55%, 70% (`idea.md`); 28 lượt mỗi ngày (`cfo.md`); 40% and 8 mua, 12 không mua (`panel/results.md`). No computed or invented figure.
- The panel caveat appears once, in section 5, where the buy rate is quoted; the disclaimer closes the file.
- Finding handled: the countdown's D-14 decision row assumes the test fits in D-30 to D-14; the golden says to move D-30 earlier when the Owner's M is longer.

## Giải quyết review nội bộ

Review `2026-11-26-070000-review.md`:

1. Gate after the spending (fixed): section 1 of `launch.md` now says the test, read at D-14, still changes price, offer and the go decision, cannot undo commitments made before D-14 (registration, suppliers), and tells the Owner to open the waitlist earlier than D-30 to gate those. The stop rule and the D-14 row say the same. The skill now requires the author to state this.
2. "thợ trưởng" as an `ops.md` role (fixed): the skill example now says "as listed in `ops.md`" with roles that exist.
3. Head barber hire (fixed): the D-12 row says the thợ trưởng is not in `ops.md`, must be hired first, and the Owner decides at D-14. The skill requires this line for any unlisted role.
4. 70% Việt share in a "mốc dừng" table (not changed, cosmetic): its row already labels it as a target.

Red: `test_skill_tells_the_author_what_the_test_still_gates_and_the_unlisted_hire` and `test_golden_states_what_the_test_gates_and_the_head_barber_hire` failed before the text change; `tests/test_launch_skill.py` now 21 passed. `business-plan.md` regenerated with `founder-vn plan` (3 lines changed, the launch section text).

## Cổng ba đoạn

Run once at code commit `ae01d20` (the commit after it touches only this file).

```
bash scripts/harness/gate-segment.sh static    # exit 0 (All checks passed, skill-lint 0 findings)
bash scripts/harness/gate-segment.sh unit      # exit 0 (451 passed)
bash scripts/harness/gate-segment.sh build     # exit 0 (Successfully built dist/founder_vn-0.2.0-py3-none-any.whl)
bash scripts/harness/gate-segment.sh verify    # exit 0 (GREEN on ae01d20b0f048dba509ac71f7730e32d1d1db6b2)
```
