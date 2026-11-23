# Evidence: issue #9 panel bookkeeping, init and tally

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.panel` (module): the one set of functions behind both transports: `deal` (personas from `customer.json` and `pitch.md`, quotas by largest remainder, seeded), `init`, `check` and `save` (validate and store buyer answers, `save` refuses invalid answers, as upstream), `tally` (buy rate overall and by segment or behaviour, reasons with quotes, what would flip a no, the four price answers, excluded buyers, `results.md` and `results.json`). Criteria 1, 2, 3, 4, 5.
- `founder-vn panel init|check|save|tally` (CLI commands): one end of the parity pair; golden tests by seed run through it, and `customer.json` validation errors are asserted to name the offending field. Criteria 1, 2, 4, 5.
- `panel_init` and `panel_tally` (MCP tools of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files. Criterion 5.
- `founder_vn.files` (path-locked layer): the only way files under `founder/panel/` are written, so a path escape stays refused. Criteria 1, 3.
## Lát

Every test runs with no network and no model. Seed 7 unless a row says otherwise.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| deal cards | `tests/test_panel_cli.py::test_init_deals_vietnamese_cards_by_quota_seed_7`, `test_same_seed_same_cards_other_seed_other_cards` (quotas 4/2/1 for n=7 worked by hand in the docstring) | `founder-vn: error: argument command: invalid choice: 'panel' (choose from 'version', 'cfo', 'pricing', 'install')` (2 failed) | `uv run pytest tests/test_panel_cli.py -q` (2 passed) |
| customer.json and pitch errors | `test_customer_error_names_the_field` (10 cases), `test_empty_or_missing_pitch_and_bad_n_are_errors` | `AssertionError: assert 0 == 2` for `business`, `segments[2].share`, `age` and others; `KeyError: 'name'`, `IndexError: list index out of range` for the rest (11 failed) | same command (13 passed) |
| path lock | `test_init_writes_only_panel_json_and_personas_under_founder_panel`, `test_customer_outside_founder_is_refused` | Passed on first run (`files` was used from slice 1). Red witnessed by mutation in `panel._read`: reading with `Path(project) / 'founder' / path` instead of `files.read_text`; `test_customer_outside_founder_is_refused` failed with `assert 0 == 2 where 0 = main(['panel', 'init', '--customer', '../customer.json', '--seed', '7'])`; restored, `git diff src` empty | same command (15 passed) |
| check and save | `test_check_lists_missing_and_broken_answers_exit_1_seed_7`, `test_check_all_good_exit_0`, `test_save_extracts_first_json_object_and_files_it`, `test_save_refuses_invalid_answers_and_leaves_no_file` (4 cases) | `argument panel_command: invalid choice: 'check' (choose from 'init')` (`SystemExit: 2`; 7 failed) | same command (22 passed) |
| tally counts and `results.json` | `test_tally_counts_and_results_json_keys_seed_7`, `test_tally_reads_mode_model_prompt_hash_from_panel_json`, `test_tally_without_valid_answers_is_an_error` | `argument panel_command: invalid choice: 'tally' (choose from 'init', 'check', 'save')` (2 failed, 1 error) | same command (25 passed) |
| results.md golden, price answers | `test_tally_golden_seed_7` | `FileNotFoundError: tests/golden/panel_tally.json` | same command (28 passed) |
| results.md text | `test_results_md_is_vietnamese_with_caveat_and_no_dollar` | Passed on first run. Red witnessed by mutation: dropping `.replace("\|", "/")` in `_quotes`; failed with `assert 'Giá cao hơn quán quen / mười nghìn.' in '# Panel người mua: ...'`; restored | same command (28 passed) |
| price answers feed pricing | `test_price_answers_are_consumable_by_pricing` (runs `founder-vn pricing panel/pricing_input.json --json`, expects `{"valid": 3, "dropped": 0}`) | Passed on first run. Red witnessed by mutation: reading only the long names in `_price_row` (`row.get(long)`); failed with `assert [{'too_cheap'...e': '60.000'}] == [{'too_cheap'...e': '60.000'}]`; restored | same command (28 passed) |
| MCP parity | `tests/test_panel_parity.py` (`panel_init`, `panel_tally`, byte-identical stdout and files) | `Tool 'panel_init' failed: 'Unknown tool: panel_init'` and the same for `panel_tally` (2 failed) | `uv run pytest tests/test_panel_parity.py -q` (2 passed) |
| default `--n` is 20 (S1, SPEC-1) | `test_init_without_n_deals_twenty_cards`, `test_panel_init_default_n_is_twenty_on_cli_and_mcp` | `assert 100 == 20` style failure: `panel init` without `--n` dealt 100 cards (2 failed) | `uv run pytest tests/test_panel_cli.py tests/test_panel_parity.py -q` (32 passed) |

The golden `tests/golden/panel_tally.json` was generated once from `panel tally` (seed 7, n=7, `tests/fixtures/panel_answers.json`: P001 to P005 valid, P006 broken, P007 missing) and read through before commit: 3 mua, 2 không mua, 60%, 2 excluded, price answers from P001, P002, P003, mean 5,0 lần.

## Quyết định của lane

- Income is monthly: a multiple of 100.000 drawn uniformly from the multiples inside the segment range (so it always stays in range). Upstream rounded a yearly figure to 1.000.
- Price answers: the canonical keys in a buyer answer are the upstream names `price_too_cheap`, `price_cheap`, `price_expensive`, `price_too_expensive`; the short names pricing reads (`too_cheap`, `bargain`, `getting_expensive`, `too_expensive`) are accepted too and win when both appear. `tally` writes them as `founder/panel/pricing_input.json` (`{"business", "answers": [...]}`), the file `founder-vn pricing panel/pricing_input.json` reads. A buyer who gave fewer than four prices is not in the file; values are passed through as written and pricing drops unreadable ones.
- `share` of each segment and behaviour and `age` are required: a missing one is an error naming the field (standards: no default for a numeric input).
- `save` validates before writing, so an invalid reply leaves no file and no existing answer is overwritten (the path-locked layer cannot delete, so upstream's write-then-remove is not possible).
- `results.json` `n` is the number of buyers dealt, `answered` the valid answers, `excluded` their difference, with `excluded_buyers` listing id and problem.

## Cổng ba đoạn

Last code commit: `69ebc4d`. Each segment ran once at HEAD `cc86828` (one ledger commit after the last code commit, no code change in between); counts read from `.harness/gate-*.log`.

```
static: ruff check "All checks passed!", ruff format --check clean, skill-lint exit 0
unit:   175 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on cc868285f88080e0ed643a58b024bcbaf532ceec
```

## Giới hạn

- No model run exists in this ticket: `mode`, `model` and `prompt_hash` in `results.json` are read from `panel.json` when present, else `manual`, `null`, `null`. The test for the present case writes them by hand; nothing here proves a real run records them.
- The tests answer for the buyers with hand-written fixtures; the tally is proved on 5 valid answers of 7 dealt, not on a 100-buyer panel.
- Names are synthetic given names from a fixed list of 40; beyond 40 buyers a number is appended. The quotas are checked on one hand-worked case (n=7) and the shares of the fixture.
- `check` and `save` are CLI-only (the ticket requires MCP parity for `panel_init` and `panel_tally` only). `panel_run`, prompts and briefs belong to later tickets.
- The panel never gates the verdict; the report labels the buy rate "tín hiệu cầu (mô phỏng, cận trên)".
- Reason codes stay English in JSON and are shown in Vietnamese in `results.md`; the Vietnamese labels are not checked against a style guide.

## Giải quyết review nội bộ

Lane không tự chạy `/code-review` (steering lane-implement). Hai lượt review độc lập do harness dispatch sau khi PR mở; kết quả nằm ở `reviews/issue-9/`.
