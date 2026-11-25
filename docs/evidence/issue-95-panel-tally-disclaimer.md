# Evidence: issue #95 panel tally results.md carries the disclaimer

## Seam

Inferred from the acceptance criteria of the ticket body; not written by the operator.

- `founder-vn panel tally` (CLI, `panel.results_md` in `src/founder_vn/panel.py`): the `founder/panel/results.md` it writes carries the disclaimer line after the simulated-panel caveat. The tally has one implementation reached by CLI and MCP, so the existing parity test already covers the text; no new transport slice.
- `tests/test_panel_cli.py`, `tests/golden/panel_tally.json`: the assertion on the line, and the golden regenerated.
- `examples/barbershop/founder/panel/results.md`: the golden example, same one-line change.

## Lát

No model and no network. Run with `uv run pytest tests/test_panel_cli.py -q`.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| disclaimer line | `test_results_md_is_vietnamese_with_caveat_and_no_dollar` | `assert 'Đây không phải tư vấn tài chính, thuế hay pháp lý.' in '# Panel người mua: ...'` (1 failed, 31 passed) | `tests/test_panel_cli.py tests/test_panel_parity.py` green; full suite 364 passed |

## Quyết định của lane

- The line is the wording `board.md` uses ("Đây không phải tư vấn tài chính, thuế hay pháp lý."), placed as its own paragraph right after the caveat paragraph.
- `plan_compile` embeds `results.md` verbatim, so `examples/barbershop/founder/business-plan.md` (regenerated with `plan.compile_plan`) and `tests/golden/plan_full.json` (two occurrences: the copied `results.md` and the compiled plan) gain the same one line. `plan_numbers_only.json` has no panel and is unchanged. No other golden text changed.
- `panel_tally.json` and `plan_full.json` were edited by inserting that one paragraph into the stored text (the repository has no golden regeneration command); the tests that compare them pass against the tool output, which proves the match.

## Cổng ba đoạn

Last code commit: `f759de9`. Each segment ran once at that HEAD; this evidence commit is the only commit after it.

```
static: ruff check and format clean
unit:   364 passed
build:  Successfully built founder_vn-0.2.0 sdist and wheel
verify: GREEN on f759de97164197768acc504554ccdb00b21b18de
```

## Giới hạn

- No real-model run; the change is fixed text in a report. The disclaimer is not asserted for the MCP transport separately: `tests/test_panel_parity.py` asserts byte-identical files through both.
- The walkthrough record of #19 is not touched.
