# Evidence: issue #14 founder-board, board_run tool, three lenses, skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.board` (new module): `run(project, detached)` starts the `board run` job, `execute(project, job_id)` asks the three lenses, `work` is the worker entry point. Seam because criterion 1 (three independent completions, fixed-shape Vietnamese memos, model and prompt hash recorded, resumable job) lives in this function, and the fake provider drives it over HTTP.
- `founder_vn.panel.job_status` (existing, extended): one poll tool for both job types (design Q50). Seam because criterion 1 says `job_status` works for a board job.
- CLI `founder-vn board run` and MCP tool `board_run`: the same function through both transports. Seam because the ticket and the design's CLI to MCP table list them; covered by a parity test (`tests/test_board_parity.py`).
- `skills/founder-board/SKILL.md` and `skills/founder-board/lenses.md` (skill files): Step 0, standalone brief, chair's summary rules, and the lens reference text with the "apply the framework, never speak as the author" rule (criteria 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in `tests/test_board_skill.py`; the lens text the model receives is the same text, tested in `tests/test_board.py`.
- `examples/barbershop/founder/board/` and `board.md` (golden case): criterion 4.
