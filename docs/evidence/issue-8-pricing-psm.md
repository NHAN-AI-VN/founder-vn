# Evidence: issue #8 pricing slice, Van Westendorp on VND

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The design does not define the input file, so the lane fixes one: a JSON file under `founder/` with `answers` (a list of objects with the keys `too_cheap`, `bargain`, `getting_expensive`, `too_expensive`) and an optional `competitor_prices` list; every price may be a number or Vietnamese text.

- `founder_vn.pricing` (module): the one function behind both transports. Parses prices through `founder_vn.vnd.parse_vn_number`, drops answers that are unparseable or not above zero and counts them, warns below 8 valid answers, computes the Van Westendorp points, renders the Vietnamese report or JSON (criteria 1, 2, 3).
- `founder-vn pricing` (CLI command): one end of the parity pair, with `--json` and `--out`; golden-file tests run through it (criteria 3, 4).
- `pricing_psm` (MCP tool of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files (criterion 4).
- `founder_vn.files.write_text` (path-locked layer): the only way `pricing.md` is written, so a path escape stays refused (criterion 3).

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| parse and drop | `tests/test_pricing_cli.py::test_parses_vietnamese_formats_and_reports_dropped` | `argparse.ArgumentError: argument command: invalid choice: 'pricing'` | `uv run pytest tests/test_pricing_cli.py -q` (1 passed) |
| Van Westendorp points | `test_van_westendorp_points_on_a_hand_checked_spread` (expected 20.000, 29.500, 39.000 worked by hand in the test comment) | `KeyError: 'points'` | same command (2 passed) |
| thin data, report, goldens | `test_thin_data_warning_below_eight_valid_answers`, `test_report_golden`, `test_json_golden` | `assert 'Dữ liệu mỏng: chỉ có 7 câu trả lời hợp lệ' in '{...'` (JSON printed instead of a report); `FileNotFoundError: tests/golden/pricing_json.json` | same command (5 passed) |
| `--out` | `test_out_writes_pricing_md_under_founder` | Passed on first run because `run` already carried `--out` from slice 1. Red witnessed by mutation: replacing `files.write_text` with a direct write made it fail with `assert 'Đã ghi founder/x.md\n' == 'Đã ghi founder/pricing.md\n'`; reverted, `git diff src` empty | same command (8 passed) |
| out-of-root refusal | `test_out_outside_root_is_refused` | Passed on first run (code came with slice 1). Red witnessed by mutation in `pricing.run`: writing `(project / "founder" / out).resolve()` with `Path.write_text` instead of `files.write_text`; the test failed with `AssertionError: assert 0 == 2 where 0 = main(['pricing', 'pricing_input.json', '--out', '../pricing.md'])`; reverted, `git diff src` empty | `uv run pytest tests/test_pricing_cli.py -q` (8 passed) |
| missing `answers` field | `test_missing_answers_exits_2_naming_the_field` | Passed on first run (code came with slice 1). Red witnessed by mutation in `pricing.analyse`: replacing `raise PricingInputError("thiếu trường 'answers'")` with `spec = {**spec, "answers": []}`; the test failed with `AssertionError: assert 0 == 2 where 0 = main(['pricing', 'empty.json'])`; reverted, `git diff src` empty | `uv run pytest tests/test_pricing_cli.py -q` (8 passed) |
| report notes (SPEC-1) | `test_report_golden` | After the `## Lưu ý` text changed, the golden compare failed: `assert {'stdout': ...khách thật chịu trả.\n\nBáo cáo này không phải tư vấn tài chính hay định giá; ...} != {'stdout': ...không phải giá chắc chắn bán được.\n'}`; golden regenerated, diff read (only the two appended paragraphs) | `uv run pytest tests/test_pricing_cli.py tests/test_pricing_parity.py -q` (11 passed) |
| `pricing_psm` | `tests/test_pricing_parity.py` (report, JSON, `--out`) | `Tool 'pricing_psm' failed: 'Unknown tool: pricing_psm'` (3 failed) | `uv run pytest tests/test_pricing_parity.py -q` (3 passed) |

The goldens `tests/golden/pricing_report.json` and `pricing_json.json` were generated once from `pricing.run` on `tests/fixtures/pricing_input.json` (the fixture's 13 answers include 3 unreadable or non-positive ones, and 2 of 6 competitor prices are dropped) and read through before commit.

## Cách tính

Curves follow the usual four-question method: too cheap and bargain count answers at or above a price, getting expensive and too expensive count answers at or below it, "not cheap" is the share of bargain answers below the price, "not expensive" the share of getting-expensive answers above it. Lower bound = too cheap meets "not cheap"; upper bound = too expensive meets "not expensive"; indifference point = bargain meets getting expensive. Meeting price: first answer price where the curves are equal, else linear interpolation across the first sign change, rounded to whole đồng; absent when they never meet. A respondent row is dropped as a whole when any of its four answers is unreadable or not above zero.

## Cổng ba đoạn

Last code commit: `7445cdf`. Each segment ran once at that HEAD; counts read from `.harness/gate-*.log`.

```
static: ruff check "All checks passed!", ruff format --check "97 files already formatted", skill-lint exit 0
unit:   143 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on 7445cdf7deecdda22630a7519234cafb6563b2ef
```

## Giới hạn

- The design does not define the input file of the pricing slice. The lane fixed it (`answers` plus optional `competitor_prices`, see Seam); the panel job (a later ticket) must write, or a converter must produce, that shape.
- `pricing.md` is written whole by `--out`; the lane does not merge into a file the pricing skill may also write prose to ("data section" is read as the data report the package owns).
- The Van Westendorp points are checked against one hand-worked spread and one golden; no comparison with an external implementation.
- Tests use no model; the real panel is not run.

## Giải quyết review nội bộ

Lane không tự chạy `/code-review` (steering lane-implement). Hai lượt review độc lập do harness dispatch sau khi PR mở; kết quả nằm ở `reviews/issue-8/`.
