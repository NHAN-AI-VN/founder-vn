# Evidence: issue #10 plan compiler, verdict from CFO numbers only

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.plan` (module): the one set of functions behind both transports. `verdict` (three checks over `cfo.analyse` output: contribution > 0, year-1 operating profit after revenue tax > 0, break-even within capacity; Incomplete without `numbers.json`), `panel_line` (buys, passes, mode, model from `panel/results.json`, never an input of `verdict`), `compile_plan` (key-numbers table in VND, sections in pipeline order, "Chưa làm" list naming the skill, closing disclaimer), `run` (writes `business-plan.md`, or with `check` compares without writing). Criteria 1, 2, 3, 4.
- `founder-vn plan [--check]` (CLI command): one end of the parity pair; golden tests run through it, and `--check` exit code is 0 when `business-plan.md` equals what would be compiled and 1 when it is missing or stale. Criteria 3, 4.
- `plan_compile` (MCP tool of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files. Criterion 4.
- `founder_vn.files` (path-locked layer): the only way `founder/business-plan.md` is written and the sections are read. Criteria 3, 4.
