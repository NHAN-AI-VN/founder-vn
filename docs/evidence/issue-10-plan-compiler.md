# Evidence: issue #10 plan compiler, verdict from CFO numbers only

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.plan` (module): the one set of functions behind both transports. `verdict` (three checks over `cfo.analyse` output: contribution > 0, year-1 operating profit after revenue tax > 0, break-even within capacity; Incomplete without `numbers.json`), `panel_line` (buys, passes, mode, model from `panel/results.json`, never an input of `verdict`), `compile_plan` (key-numbers table in VND, sections in pipeline order, "Chưa làm" list naming the skill, closing disclaimer), `run` (writes `business-plan.md`, or with `check` compares without writing). Criteria 1, 2, 3, 4.
- `founder-vn plan [--check]` (CLI command): one end of the parity pair; golden tests run through it, and `--check` exit code is 0 when `business-plan.md` equals what would be compiled and 1 when it is missing or stale. Criteria 3, 4.
- `plan_compile` (MCP tool of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files. Criterion 4.
- `founder_vn.files` (path-locked layer): the only way `founder/business-plan.md` is written and the sections are read. Criteria 3, 4.

## Lát

Every test runs with no network and no model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| verdict from three checks | `tests/test_plan_cli.py::test_no_numbers_is_incomplete`, `test_all_three_checks_pass_is_profitable`, `test_each_failed_check_is_not_yet_and_named` (contribution, year-1 profit, break-even vs capacity), `test_missing_numeric_field_is_an_error_naming_it` | `SystemExit: 2` from argparse (`invalid choice: 'plan'`; 6 failed) | `uv run pytest tests/test_plan_cli.py -q` (6 passed) |
| panel line, key numbers, sections, Chưa làm, disclaimer, goldens | `test_panel_line_shows_buys_passes_mode_and_model`, `test_panel_line_without_panel_says_not_run`, `test_panel_results_without_buys_is_an_error_naming_it`, `test_key_numbers_table_is_in_vnd`, `test_sections_follow_pipeline_order_and_missing_ones_name_their_skill`, `test_plan_golden_full_state`, `test_plan_golden_numbers_only` | `assert 'Tín hiệu cầu (mô phỏng, cận trên): 3 mua, 2 không mua; chế độ llm; mô hình mo-hinh-gia.' in '# Kế hoạch kinh doanh...'`, `assert 0 == 2` (buys missing), `FileNotFoundError: tests/golden/plan_full.json` (7 failed) | same command (15 passed) |
| panel never gates the verdict | `test_panel_never_changes_the_verdict` (buys 0 and 5) | Passed on first run. Red witnessed by mutation in `plan.compile_plan`: forcing `NOT_YET` when `results.json` holds `"buys": 0`; failed with `assert 'Kết luận: Not yet ...' == 'Kết luận: Profitable ...'`; restored, `git diff src` empty | same command (15 passed) |
| `--check` | `test_check_is_0_when_current_and_writes_nothing`, `test_check_is_1_when_missing_and_creates_nothing`, `test_check_is_1_when_a_source_changed_since` | `SystemExit: 2` (`unrecognized arguments: --check`; 3 failed) | same command (18 passed) |
| MCP parity | `tests/test_plan_parity.py` (`plan_compile`, byte-identical stdout and files, with and without panel, and `check`) | `Tool 'plan_compile' failed: 'Unknown tool: plan_compile'` (3 failed) | `uv run pytest tests/test_plan_parity.py -q` (3 passed) |

The goldens `tests/golden/plan_full.json` (numbers, panel results of the T07 golden run, `cfo.md` from `founder-vn cfo --out`) and `tests/golden/plan_numbers_only.json` were generated once from `founder-vn plan` and read through before commit.

## Quyết định của lane

- Seams the ticket leaves open: `--check` writes nothing and exits 0 when `founder/business-plan.md` equals what would be compiled now, 1 when it is missing or stale, 2 on a bad input. Over MCP, `plan_compile(check=True)` returns the same text (a tool has no exit code).
- `plan` writes `founder/business-plan.md` and prints `Kết luận: <verdict>. Đã ghi founder/business-plan.md`. Verdict labels print as `Profitable (có lãi)`, `Not yet (chưa lãi)`, `Incomplete (chưa đủ số)`.
- Incomplete is only "no `founder/numbers.json`". A present but broken `numbers.json` is an error naming the field (standards: no default for a numeric input), exit 2.
- Section file map in pipeline order: board `board.md`, competitors `competitors.md`, consumer `panel/results.md`, pricing `pricing.md`, offer `offer.md`, cfo `cfo.md`, marketing `marketing.md`, brand `brand.md`, ops `ops.md`, launch `launch.md`. The cfo section is "done" when `numbers.json` exists (the key-numbers table carries it); its body is `cfo.md` when that file exists. Each section file's headings are pushed two levels down. The map is a lane decision (the design names the skills, not the files); `permits` is outside the pipeline list of design §2 and has no section.
- The break-even check is applied whenever `capacity_per_day` is present; `cfo.analyse` requires it, so "when capacity is given" is always true for a valid `numbers.json`.

## Cổng ba đoạn

Each segment ran once at HEAD `d42bbf7` (the last code commit); counts read from `.harness/gate-*.log`.

- `static`: exit 0 (`All checks passed!`, skill-lint 0 findings).
- `unit`: exit 0 (`196 passed`).
- `build`: exit 0 (`Successfully built dist/founder_vn-0.1.0-py3-none-any.whl`).
- `verify`: `GREEN on d42bbf79003d76eb51edfb3e0374ef1f797764d2`.

## Giới hạn

- No real model or panel run: the panel line is read from the T07 `results.json` shape only.
- Over MCP the `check` result is in the text; the exit code 1 exists on the CLI only.
- The compiled plan is not checked against a real `skills/` run (no `founder-plan` skill exists yet; T-skill tickets own it).
- Section files other than `cfo.md` and `panel/results.md` are embedded verbatim and unvalidated; their producers are later tickets.
