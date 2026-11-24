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

The skill and its text tests are one slice (the tests read the skill). The golden files are the second slice. The tests check instruction text and example files, not model behaviour.

## Cổng ba đoạn

Last code commit: `4c7ba40` (last commit touching `skills/`, `tests/`, `examples/`). Each segment ran once at the HEAD below it; this evidence commit touches only `docs/evidence/`. Counts read from `.harness/gate-*.log`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "175 files already formatted", skill-lint "4 skills checked, 12 example file(s), 0 finding(s)"
unit:   308 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on 867bc35c71ee5d9e6f8508189f518753e951c2c8
```

## Giới hạn

- **Kiro CLI is not available in the lane sandbox.** The golden case was produced by the lane agent following `skills/founder-consumer/SKILL.md` step by step. The panel ran through the package CLI (`founder-vn panel init`, `run`, `status`, `tally`) on the model named in `founder/panel/panel.json` (`FOUNDER_LLM_MODEL`: gemini-3.1-flash-lite), prompt hash `7602aad4...c71c6`. No other configuration value is recorded. This does not prove that a Kiro CLI session obeys the skill.
- `founder/competitors.md` of the example has no complaint data (desk survey, every complaint cell "chưa có số liệu"), so the objections in `customer.json` are guesses from `idea.md` and the skill says so; a field survey would replace them.
- The detached `panel run` worker did not survive between tool calls in this sandbox (job J-8692bbf2 stayed at 0 done). It was restarted with `founder-vn panel work` and 18 of 20 buyers answered; one buyer got HTTP 429 and one was left pending. A second `panel run` asked only those two and both answered. The stale job file of the interrupted job was deleted from `founder/panel/jobs/`; the finished job J-3d5fb7f2 stays. All 20 answers come from the model, none written by the agent.
- The 35% buy rate is a simulated upper bound from one model and 20 buyers; two behaviour groups have 6 buyers (thin).
- Gender: `panel.GIVEN_NAMES` deals one mixed name list and `customer.json` has no gender field. The skill's decision (ticket T15 owns it, per the `⏳` comment in `panel.py`): write the gender into every segment name, which the persona brief shows to the buyer. The `⏳` comment is left in place because mixed names for a men-only product remain; a name list in `customer.json` would need a Python change, outside this ticket.
- Review checklist (`docs/review-checklist.md`) against `consumer.md`, `pitch.md`, `customer.json`: no `$` next to a digit; Owner-facing text Vietnamese addressing "anh/chị" (`consumer.md` addresses the Owner as "anh/chị" in the opening, point 5 and the closing caveat; asserted by `test_golden_readback_has_five_points_and_the_caveat_once`; quotes are the model's, verbatim); no legal or numeric claim without a source (none made); disclaimer present; simulated-panel caveat printed once. Passed.

## Giải quyết review nội bộ

None yet; the harness dispatches the review turns after the PR opens.
