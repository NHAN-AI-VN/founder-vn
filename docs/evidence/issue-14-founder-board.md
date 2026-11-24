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
| golden case, real Kiro CLI run (`915e493`) | `tests/test_board_skill.py` golden tests: `test_golden_board_json_records_the_model_and_prompt_hash`, `test_golden_memos_have_the_fixed_shape_and_match_the_package_renderer`, `test_golden_board_md_is_the_chair_summary_over_the_real_memos` | `FileNotFoundError` on `examples/barbershop/founder/board.md` (`test_golden_board_md_…`); the memo and `board.json` tests were already green because the real run had produced the files (1 failed, 11 passed) | `uv run pytest tests/test_board_skill.py -q` (12 passed) |

Design notes: `job_status` (MCP) and `founder-vn panel status` (CLI) poll both job types (Q50); a board job lives under `founder/board/jobs/`, a panel job under `founder/panel/jobs/`. The memo is stored as `<lens>.json` (validated shape) and rendered as `<lens>.md` (Vietnamese, fixed headings). The prompt hash covers the template, the never-speak-as-the-author rule, the three lens texts and the brief.

## Cổng ba đoạn

Last code commit: `915e493` (golden-case slice). The lane was first merged onto current `main` (`d1f6851`, which carries #15's reference model `gemini-3.5-flash-lite`); `panel.py` auto-merged (the regions did not overlap). Each segment ran once at HEAD `915e493`; counts read from `.harness/gate-*.log`. The evidence commit touches only `docs/evidence/`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "217 files already formatted", skill-lint "3 skills checked, 9 example file(s), 0 finding(s)"
unit:   295 passed
build:  Successfully built dist/founder_vn-0.1.0.tar.gz and dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on 915e4930186d8d2974e3b021122198824458a472
```

Earlier block of the lane, kept for the record: each segment ran once at HEAD `f9d1fb2` before the golden case and the merge (static "155 files already formatted", skill-lint "3 skills, 5 example files, 0 findings"; unit 280 passed; build both artefacts; `verify: GREEN on f9d1fb2628f4a2e549d5aa90c5159ee710824d1a`).

## Lượt chạy golden case trên Kiro CLI (tiêu chí 4)

The owner ran the skill in a Kiro CLI session (macOS) on 2026-11-24; the session agent is model `claude-fable-5.1`; the three `FOUNDER_LLM_*` variables were present in that session's shell and never printed, written or forwarded (only the model name is recorded here). The project model, from `board/board.json`, is **`gemini-3.5-flash-lite`** (the reference chosen by the #15 bake-off). The skill was read by path at `915e493`; the project folder was `examples/barbershop/`.

| Step of SKILL.md | What was done | Result |
|---|---|---|
| Protocol 1 | `uv run founder-vn --version` | `founder-vn 0.1.0`, same major as `metadata.version` 0.1.0 |
| Protocol 2 | the session had no founder-vn MCP server | used the CLI over the shell |
| Step 0 / 1 | `founder/idea.md` and the standalone `founder/board/brief.md` already existed (committed earlier in the lane) | reused; the brief stands alone |
| Step 2 | `founder-vn board run` in `examples/barbershop/` → `{"job_id": "J-d9c8202e", "state": "running", "lenses": 3}`; polled `founder-vn panel status J-d9c8202e` | `state` `done` after ~9 s; `done` 3, `failed` 0, `excluded` 0; the detached worker finished on its own, no foreground `board work` needed |
| — | the three memos and `board/board.json` were written | `board.json`: `model` `gemini-3.5-flash-lite`, `prompt_hash` `7a0178802252049d04770140678c5b228699b15ee0e734aeed21533758fd464c`, `lenses` offers/product/systems |
| Step 3 | wrote `founder/board.md` (chair's summary) from the three memos | four sections; disagreements kept; five `- [ ]` conditions with lens tags; nine open-number rows routed to the skills; two closing lines; no verdict |

Readings produced by the run: Offers 5/10, Product 6/10, Systems 4/10, all "làm có điều kiện". The three memos disagree on where the biggest risk sits (offer structure vs product focus vs operations) and on whether the wide service-and-price menu is a strength or a dilution; `board.md` keeps those open rather than averaging them.

Review checklist (`docs/review-checklist.md`) on `board.md`, the three memos and `board.json`:

- [x] No `$` next to a digit: `skill_lint` 0 findings over 9 example files; the golden tests assert the `DOLLAR` regex does not match `board.md` or any memo.
- [x] No English leaking into Owner-facing text; the Owner is "anh/chị". Latin strings left are file names, the three book titles (`100M Offers`, `The E-Myth Revisited`), author names and the `founder-*` skill names in the routing table.
- [x] Every legal or numeric claim carries a source: `board.md` cites only figures that already appear in the brief (199.000 đ, 279.000 đ, 389.000 đ, 1.990.000 đ, 15–50 triệu đồng, Quận 7 cũ); it introduces no new number and answers no open number itself.
- [x] Disclaimer present: the two closing lines of `board.md` ("không nói thay tác giả…" and "không phải tư vấn tài chính, thuế hay pháp lý").
- [x] Simulated-panel caveat: `board.md` says the three readings are a simulation of three published frameworks and do not replace real customers; it gives no verdict (that is `founder-plan`'s, from `founder-cfo` numbers).

The memo `<lens>.md` files are checked byte-for-byte against `board.memo_md(lens, <lens>.json)`, so the rendered memo cannot drift from its validated JSON; the memo JSON is checked against `board.memo_problem` (the same shape gate the package enforces). `board.md` is hand-written by the chair step, so its test pins structure, the exact score/vote line of each memo, the checklist tags, the skill routing and the closing lines, not the model's wording.

## Giới hạn

- One real run, one model, one host: the golden case is a single `board run` of `gemini-3.5-flash-lite` driven from one Kiro CLI session. The memo shape, the Vietnamese prompts and the retry rules (failed after three attempts, invalid twice excluded) are still proven only against the fake provider (`tests/test_board.py`); the real run shows the three lenses answer with valid, in-shape memos once, not how another model or host behaves, and not the failure branches.
- The detached CLI worker finished on its own here (macOS); the sandbox's earlier stall (state stayed `running`) was the sandbox's process handling. The foreground `founder-vn board work` fallback was not needed this time.
- `board.md` is written by the host model at Step 3, so its test pins structure (sections, each memo's exact score/vote line, checklist tags, skill routing, closing lines), not wording; how faithfully a different model keeps disagreements or routes open numbers is not proven here.
- The lens reference text is the lane's summary of the three frameworks; nobody has reviewed it against the books.
- `README.md` skill table and host docs were not changed (out of scope for criterion 4; the installer-ships-the-skill path is covered by `test_installer_ships_the_skill_with_its_lens_reference`).
- The transient job record (`founder/board/jobs/<job_id>.json`) is not committed; it is per-run scratch, regenerated by the next `board run`.

## Giải quyết review nội bộ

No self review run (lane rule). Noted while working: none beyond the blocked golden case.
