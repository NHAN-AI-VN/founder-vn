# Evidence: issue #16 founder-consumer skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: the panel tools (`panel_init`, `panel_run`, `job_status`, `panel_tally`) already exist, so the seams are the shipped skill and the golden example files.

- `skills/founder-consumer/SKILL.md` (skill file): the instructions the host model follows. Seam because the customer-profile confirmation, the pitch rules, the default `n`, the tool order, the never-answer-for-a-buyer rule, the five-point read-back and the caveat live only here (criteria 1 to 4). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `examples/barbershop/founder/customer.json`, `pitch.md`, `panel/` (golden case): the files the skill produces. Seam because criterion 5 asks for them. Checked by loading `customer.json` through `panel.validate_customer`, by the pitch rules, by the panel counts and by `test_example_is_anonymised`.
- `founder_vn.panel` (existing module, unchanged): the golden test reads its output files only.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| skill text: profile confirmation, pitch rules, `n`, tool order, never answer for a buyer, five points, caveat, gender in segment name, lint, installer | `tests/test_consumer_skill.py` (9 tests) | `FileNotFoundError: [Errno 2] No such file or directory: '.../skills/founder-consumer/SKILL.md'` | `uv run pytest tests/test_consumer_skill.py -q` (9 passed) |
| golden case: `customer.json`, `pitch.md`, `panel/`, `consumer.md` | 4 `test_golden_*` tests in the same file | `FileNotFoundError: ... examples/barbershop/founder/customer.json` (also `pitch.md`, `panel/panel.json`, `consumer.md`; witnessed by moving the files away) | same command (13 passed) |
| review fix S1: `consumer.md` addresses the Owner as "anh/chị" | `test_golden_readback_has_five_points_and_the_caveat_once` | `AssertionError` on `assert "anh/chị" in text` | `uv run pytest tests/test_consumer_skill.py -q` (13 passed) |
| review fix SPEC-1: golden panel rerun on the reference model | same test (`res["model"] in text`, counts from `results.json`) | none new: the test reads `results.json`; the golden diff is regenerated data | same command (13 passed) |

The skill and its text tests are one slice (the tests read the skill). The golden files are the second slice. The tests check instruction text and example files, not model behaviour.

## Cổng ba đoạn

Last code commit: `3aa6fdc` (last commit touching `skills/`, `tests/`, `examples/`). Each segment ran once at the HEAD below it; later commits touch only `docs/` and `reviews/`. Counts read from `.harness/gate-*.log`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "already formatted", skill-lint "4 skills checked, 12 example file(s), 0 finding(s)"
unit:   308 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on f72f9ab447eff307a8bb8531442abde48fec089f
```

## Giới hạn

- **Kiro CLI is not available in the lane sandbox (SPEC-2, closed by the operator's answer).** The golden case was produced by the lane agent following `skills/founder-consumer/SKILL.md` step by step. The panel ran through the package CLI (`founder-vn panel init`, `run`, `work`, `tally`) on the reference model `gemini-3.5-flash-lite` (`docs/bakeoff/models.json` `"reference"`), recorded in `founder/panel/panel.json` (`FOUNDER_LLM_MODEL`), prompt hash `7602aad4...c71c6`. No other configuration value is recorded. On 2026-11-24 the operator accepted this run for criterion 5 and amended the criterion's wording on issue #16 accordingly (`reviews/issue-16/operator-answer.md`); criterion 5, as amended, is met by the files above and the review checklist below. What this lane does not prove: that a Kiro CLI session obeys the skill (confirms the profile with the Owner, never answers for a buyer, reads back the five points). That is verified by the T18 (#19) clean-install walkthrough, which runs the six Wave A skills on Kiro CLI on a new case.
- **SPEC-1 (fixed):** the first golden panel ran on `gemini-3.1-flash-lite`, not the reference model. It was cleared and rerun with `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite` (same seed 837740, n 20); the endpoint accepted the name. Result: 8 buy, 12 pass, 40%; groups: managers 50% (8), office staff 33% (12); "Quen một thợ" 25% (8), "Thử tiệm mới" and "Đặt lịch qua app" 50% (6 each, thin). `consumer.md` numbers and quotes were taken from `panel/results.md` and the answer files.
- `founder/competitors.md` of the example has no complaint data (desk survey, every complaint cell "chưa có số liệu"), so the objections in `customer.json` are guesses from `idea.md` and the skill says so; a field survey would replace them.
- The detached `panel run` worker did not survive between tool calls in this sandbox (job J-e4834377 stayed at 0 done). It was run in the foreground with `founder-vn panel work J-e4834377`: 19 of 20 buyers answered and P018 got HTTP 429. Two further `panel run` rounds asked only P018 (J-f98a9a4c failed with 429 again, J-5b1dc109 answered). The three job files stay in `founder/panel/jobs/`. All 20 answers come from the model, none written by the agent.
- The 40% buy rate is a simulated upper bound from one model and 20 buyers; two behaviour groups have 6 buyers (thin).
- Gender: `panel.GIVEN_NAMES` deals one mixed name list and `customer.json` has no gender field. The skill's decision (ticket T15 owns it, per the `⏳` comment in `panel.py`): write the gender into every segment name, which the persona brief shows to the buyer. The `⏳` comment is left in place because mixed names for a men-only product remain; a name list in `customer.json` would need a Python change, outside this ticket.
- Review checklist (`docs/review-checklist.md`) against `consumer.md`, `pitch.md`, `customer.json`: no `$` next to a digit; Owner-facing text Vietnamese addressing "anh/chị" (`consumer.md` addresses the Owner as "anh/chị" in the opening, point 5 and the closing caveat; asserted by `test_golden_readback_has_five_points_and_the_caveat_once`; quotes are the model's, verbatim); no legal or numeric claim without a source (none made); disclaimer present; simulated-panel caveat printed once. Passed.

## Giải quyết review nội bộ

None yet; the harness dispatches the review turns after the PR opens.
