# Evidence: issue #95 panel tally results.md carries the disclaimer

## Seam

Inferred from the acceptance criteria of the ticket body; not written by the operator.

- `founder-vn panel tally` (CLI, `panel.results_md` in `src/founder_vn/panel.py`): the `founder/panel/results.md` it writes carries the disclaimer line after the simulated-panel caveat. The tally has one implementation reached by CLI and MCP, so the existing parity test already covers the text; no new transport slice.
- `tests/test_panel_cli.py`, `tests/golden/panel_tally.json`: the assertion on the line, and the golden regenerated.
- `examples/barbershop/founder/panel/results.md`: the golden example, same one-line change.
