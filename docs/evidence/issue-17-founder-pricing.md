# Evidence: issue #17 founder-pricing skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: `pricing_psm` / `founder-vn pricing` (issue #8) and `founder-vn cfo --price` already exist, so the seams are the shipped skill and the golden example files.

- `skills/founder-pricing/SKILL.md` (skill file): the instructions the host model follows. Seam because the call to `pricing_psm` / `founder-vn pricing` on the panel's four price answers, the cross-check with `competitors.md` and `cfo.md`, the below-break-even flag, the `pricing.md` sections, the no-fabricated-anchors rule and the thin-data pass-through live only here (criteria 1 and 2). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `examples/barbershop/founder/pricing_input.json` and `pricing.md` (golden case): the files the skill produces. Seam because criterion 3 asks for `pricing.md`. Checked by section presence, the numbers against the tool output, the break-even flag, the thin-data pass-through, the disclaimer and the panel caveat.
- `founder_vn.pricing` and `founder_vn.cfo` (existing modules, unchanged): the golden test reads their output only.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| skill text: calls `pricing_psm` / `founder-vn pricing` on the four price answers, cross-checks `competitors.md` and `cfo.md`, flags below CFO break-even, `pricing.md` sections, no fabricated anchors, thin-data pass-through, no `$`, lint, installer | `tests/test_pricing_skill.py` (8 tests) | `FileNotFoundError: [Errno 2] No such file or directory: '.../skills/founder-pricing/SKILL.md'` | `uv run pytest tests/test_pricing_skill.py -q` (8 passed) |
| golden case: `pricing_input.json`, `pricing.md` (sections in order, figures equal tool output, competitor prices from `competitors.md`, below-break-even flag from `cfo --price`, caveat once, disclaimer, no `$`) | 5 `test_golden_*` tests in the same file | `FileNotFoundError: ... examples/barbershop/founder/pricing.md` (5 failed, 8 passed) | same command (13 passed) |

The tests check instruction text and example files, not model behaviour.

## Golden case

Produced by following `skills/founder-pricing/SKILL.md` step by step from `examples/barbershop` (`founder/` is the project root of the case):

```
founder-vn pricing pricing_input.json          # 20 valid answers, 0 dropped, no thin_data warning
founder-vn cfo numbers.json --price <p> --json # for 199.000, 279.000, 389.000
```

- `founder/pricing_input.json`: the 20 `answers` of `panel/pricing_input.json` unchanged, plus `competitor_prices` (7 whole-dong prices copied from the table of `competitors.md`; Le Barbier de Saigon has "chưa có số liệu" and is left out).
- Tool output used: medians 80.000 / 150.000 / 250.000 / 400.000 đ; range 120.000 to 316.667 đ; indifference point 199.625 đ; 2 of 7 competitor prices inside the range.
- CFO check (`margin_at_plan`, `breakeven_per_day`, plan 40 per day, capacity 66): 199.000 đ gives -13% and 50,8 (below break-even, flagged); 279.000 đ gives 19% and 27,63; 389.000 đ gives 42% and 16,98. The recommended price (199.000 đ, within 1.000 đ of the indifference point and the Owner's own Essential Cut price) is flagged next to the price; the file leaves the choice to the Owner.

## Cổng ba đoạn

Last code commit: `06cd1ac` (HEAD of the gate run; later commits touch only `docs/evidence/`). Each segment ran once; counts read from `.harness/gate-*.log`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "183 files already formatted", skill-lint "5 skills checked, 13 example file(s), 0 finding(s)"
unit:   321 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on 06cd1ac0cb7ec22a6297514a2d64cc90cf9f38a6
```

## Giới hạn

- **Kiro CLI is not available in the lane sandbox.** The golden `pricing.md` was written by the lane agent following the skill, with the numbers from the package CLI (`founder-vn pricing`, `founder-vn cfo --price`). It does not prove that a Kiro CLI session obeys the skill (reads the four answers, flags the break-even, passes the thin-data warning). That is the job of the T18 (#19) clean-install walkthrough. No model ran in this lane; the panel answers are the existing golden panel (model `gemini-3.5-flash-lite`).
- `founder-vn cfo --price` changes only the price: every cost stays at the Owner's amount, so percentage costs (commission, materials) do not shrink with the price. The golden says so; the break-even figures for the lower rungs are therefore a bound for one sale at that price, not a forecast of a changed menu.
- The CFO model has one price. The Owner's blended ticket (about 280.000 đ) is a mix of Essential, Signature and packs; the CFO has no per-rung volume. The skill asks the Owner to watch the rung shares instead of computing a mix.
- Competitor prices are desk-survey list prices ("từ" is a floor), not prices paid; three of seven are floors.
- The panel is a simulated upper bound, 20 buyers, one model.
- Opening-offer sample size and duration are not in the Owner's files; the golden leaves them open for the Owner rather than inventing them.
- Review checklist (`docs/review-checklist.md`) against `pricing.md`: no `$` next to a digit (asserted by test); Owner-facing text Vietnamese addressing "anh/chị"; every competitor price traces to `competitors.md`, which carries the source link and the survey date 23/11/2026; the tax and legal claims are none; disclaimer present; the simulated-panel caveat printed once (asserted). Passed.

## Giải quyết review nội bộ

None yet; the harness dispatches the review turns after the PR opens.
