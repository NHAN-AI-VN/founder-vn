# Evidence: issue #14 founder-board, board_run tool, three lenses, skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.board` (new module): `run(project, detached)` starts the `board run` job, `execute(project, job_id)` asks the three lenses, `work` is the worker entry point. Seam because criterion 1 (three independent completions, fixed-shape Vietnamese memos, model and prompt hash recorded, resumable job) lives in this function, and the fake provider drives it over HTTP.
- `founder_vn.panel.job_status` (existing, extended): one poll tool for both job types (design Q50). Seam because criterion 1 says `job_status` works for a board job.
- CLI `founder-vn board run` and MCP tool `board_run`: the same function through both transports. Seam because the ticket and the design's CLI to MCP table list them; covered by a parity test (`tests/test_board_parity.py`).
- `skills/founder-board/SKILL.md` and `skills/founder-board/lenses.md` (skill files): Step 0, standalone brief, chair's summary rules, and the lens reference text with the "apply the framework, never speak as the author" rule (criteria 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in `tests/test_board_skill.py`; the lens text the model receives is the same text, tested in `tests/test_board.py`.
- `examples/barbershop/founder/board/` and `board.md` (golden case): criterion 4.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| board job (`67503c3`) | `tests/test_board.py` (10 tests: missing brief, unconfigured, lifecycle with three independent completions and model and prompt hash in `board/board.json`, fixed memo shape, lens prompts, prose-wrapped JSON, invalid twice excluded, failed after three attempts and resumed, `memo_problem`, crash written into the job) | `ImportError: cannot import name 'board' from 'founder_vn'` | `uv run pytest tests/test_board.py -q` (10 passed); with `tests/test_panel_run.py` 26 passed (shared `job_status`) |
| CLI and MCP parity (`440d64f`) | `tests/test_board_parity.py` (2 tests) | `argparse.ArgumentError: argument command: invalid choice: 'board'` | `uv run pytest tests/test_board_parity.py tests/test_board.py -q` (12 passed) |
| skill, lens reference, golden brief (`f9d1fb2`) | `tests/test_board_skill.py` (9 tests) | 8 failed, 1 passed: `FileNotFoundError` on `skills/founder-board/SKILL.md` and `lenses.md` (the golden brief test was added after `brief.md` was written, so its red was not witnessed) | `uv run pytest tests/test_board_skill.py tests/test_golden_case.py -q` (15 passed) |

Design notes: `job_status` (MCP) and `founder-vn panel status` (CLI) poll both job types (Q50); a board job lives under `founder/board/jobs/`, a panel job under `founder/panel/jobs/`. The memo is stored as `<lens>.json` (validated shape) and rendered as `<lens>.md` (Vietnamese, fixed headings). The prompt hash covers the template, the never-speak-as-the-author rule, the three lens texts and the brief.

## Cổng ba đoạn

Last code commit: `f9d1fb2`. Each segment ran once at that HEAD; counts read from `.harness/gate-*.log`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "155 files already formatted", skill-lint "3 skills checked, 5 example file(s), 0 finding(s)"
unit:   280 passed
build:  Successfully built dist/founder_vn-0.1.0.tar.gz and dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on f9d1fb2628f4a2e549d5aa90c5159ee710824d1a
```

## Golden case (tiêu chí 4): chặn

- `examples/barbershop/founder/board/brief.md` is written (Step 1 of the skill, from `idea.md`); prompt hash of a run on it: `7a0178802252049d04770140678c5b228699b15ee0e734aeed21533758fd464c`.
- `founder-vn board run` in `examples/barbershop/` started job `J-beb3019c`; the detached worker did not finish in the sandbox, and `founder-vn board work J-beb3019c` run in the foreground marked all three lenses `failed` with `last_error` "không gọi được máy chủ mô hình: UnsupportedProtocol". `FOUNDER_LLM_BASE_URL` is set in this sandbox but is not a usable URL (checked by shape only; the value was not printed). No memo was written, and the job files were removed from the example.
- So `board/offers.md`, `board/product.md`, `board/systems.md`, `board/board.json` and `board.md` are **not** in the example, and the review checklist was not run on them. The test for them is marked `⏳` in `tests/test_board_skill.py`. The lane did not write memos by hand: the skill forbids it.

## Giới hạn

- No real-model run: the memo shape, the Vietnamese prompts and the retry rules are proven against the fake provider only.
- Detached CLI worker: in the sandbox the `founder-vn board work` process launched by `board run` did not progress the job (state stayed `running`, no worker process found after about 6 minutes). The parity test proves the detached path on loopback, so this looks like the sandbox's process handling, but it is not proven.
- The tests read the skill text; they do not test how a host model follows Step 0, the brief or the chair's summary.
- The lens reference text is the lane's summary of the three frameworks; nobody has reviewed it against the books.
- README skill table and host docs were not changed.

## Giải quyết review nội bộ

No self review run (lane rule). Noted while working: none beyond the blocked golden case.
