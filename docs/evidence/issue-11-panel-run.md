# Evidence: issue #11 server-side fan-out, panel run and job status

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.llm` (module): the one OpenAI-compatible client, configured by `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL`; unconfigured is an error with setup instructions; the request carries no `response_format`, `seed` or `temperature`. Criterion 1.
- `founder_vn.panel` (module): `brief` and `prompt_hash` (Vietnamese buyer brief from persona and pitch, hash of template, personas and pitch recorded in `panel.json`), `extract_answer` (first JSON object, validated with `answer_problem`), `start_job` and `execute` (waves of 10, per-call timeout, retry with backoff, exclusion after two invalid answers, answers written one by one, rerun only missing or invalid), `job_status` (done, pending, failed, excluded, last error). Criteria 2, 3, 4, 5.
- `founder-vn panel run` and `founder-vn panel status` (CLI commands): `run` prints a job id at once and hands the work to a detached process, so the host call returns; `status` reads the job file. Criteria 3, 6.
- `panel_run` and `job_status` (MCP tools of `founder-vn-mcp`): the other end of the parity pair; the response shapes are asserted identical to the CLI's. Criterion 6.
- `founder_vn.files` (path-locked layer): the only way answers and the job file are written. Criteria 3, 4.
- `tests/conftest.py` `fake_provider`: extended with a scripted reply (status, content, delay) and a concurrency counter, so 5xx, timeout, invalid and wave-size cases run with no network. Criterion 6.

## Lát

Every test runs against the fake provider on 127.0.0.1; no network, no real model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| llm client | `tests/test_llm.py` (unconfigured names the variables, partly configured names only the missing, request is `model` + `messages` only with a Bearer header) | `ImportError: cannot import name 'llm' from 'founder_vn'` (collection error). Commit `8757144` went in with one test red (`test_partly_configured_names_only_the_missing_ones`: the setup text named every variable); `9aef9b1` moved the missing names to the first line and fixed it | `uv run pytest tests/test_llm.py -q` (3 passed) |
| brief, hash, extraction | `tests/test_panel_run.py::test_brief_is_vietnamese_...`, `test_prompt_hash_covers_...`, `test_extract_takes_the_first_json_object_in_prose`, `test_extract_reports_the_problem_...` | `AttributeError: module 'founder_vn.panel' has no attribute 'brief'` (4 failed). The test file was committed one commit late (`1c6c637` after `2276f48`) because it was untracked | `uv run pytest tests/test_panel_run.py -q` (4 passed) |
| job lifecycle | `test_job_lifecycle_answers_land_and_model_and_hash_reach_results`, `test_start_job_unconfigured_is_an_error_...`, `test_job_status_refuses_an_unknown_or_malformed_job_id` | `AttributeError: module 'founder_vn.panel' has no attribute 'start_job'` (3 failed) | same command (7 passed) |
| retry, exclusion, rerun | `test_prose_wrapped_json_is_filed`, `test_buyer_invalid_twice_is_excluded_...`, `test_buyer_invalid_once_then_valid_is_kept`, `test_5xx_is_retried_with_backoff_then_succeeds`, `test_5xx_for_good_is_failed_...`, `test_timeout_is_a_failed_buyer_not_a_hang`, `test_rerun_asks_only_buyers_...` | `assert (6, 0, 1, 0) == (6, 1, 0, 0)` (invalid twice counted failed, not excluded); `TypeError: execute() got an unexpected keyword argument 'backoff'` | same command (14 passed) |
| waves of 10 | `test_buyers_are_asked_in_waves_of_ten_concurrent_calls` (25 buyers, 0.15 s per call, provider counts concurrent calls) | `AttributeError: module 'founder_vn.panel' has no attribute 'WAVE'` | same command (15 passed) |
| CLI and MCP parity | `tests/test_panel_cli.py::test_run_unconfigured_exits_2_...`, `test_run_returns_a_job_id_at_once_...`, `test_status_of_an_unknown_job_exits_2`; `tests/test_panel_parity.py::test_panel_run_and_job_status_cli_equals_mcp_seed_7` | `argument panel_command: invalid choice: 'run' (choose from 'init', 'check', 'save', 'tally')` | `uv run pytest tests/test_panel_cli.py tests/test_panel_parity.py -q` (36 passed) |
| worker crash | `test_a_worker_crash_is_written_into_the_job` | Passed on first run. Red witnessed by mutation: `except Exception` changed to `except ZeroDivisionError` in `panel.work`; failed with `RuntimeError: hỏng giữa chừng`; restored, `git diff src` empty | `uv run pytest tests/test_panel_run.py -q -k crash` (1 passed) |

## Quyết định của lane

- Job state lives in `founder/panel/jobs/J-xxxxxxxx.json` (`state` running, done or error; `targets`, `done`, `failed`, `excluded`, `last_error`), written through the path-locked layer after each buyer. `job_status` and `panel status` read it, so the CLI can poll across processes.
- `panel run` on the CLI starts a detached `founder-vn panel work <job_id>` process (hidden command) so the call returns at once; on MCP a daemon thread of the long-lived server does the work. Both print the same JSON (`job_id`, `state`, `buyers`); `job_status` prints `job_id`, `state`, `total`, `done`, `pending`, `failed`, `excluded`, `last_error`.
- Counts: `failed` is a buyer whose call kept failing (timeout, 5xx, connection) after 3 attempts with backoff 2 s then 4 s; `excluded` is a buyer whose reply was invalid twice (the reply is asked for twice, each with the same retry rules). Neither writes an answer file; a rerun asks both again because their answer is missing.
- Prompt hash: SHA-256 of the brief template, the dealt personas JSON and the pitch, recorded once per panel in `panel.json` (with `mode: model` and `model`) at job start; `tally` already propagates these to `results.json`.
- Per-call timeout 90 s (`llm.TIMEOUT`). The wave is a barrier: the next 10 start when all of the previous 10 have settled.
- The CLI and MCP tool names `panel_run` and `job_status` follow the ticket; the design text says `panel_status`, the ticket wins and the design line is left for the operator.

## Cổng ba đoạn

Last code commit: `8ab316f`. Each segment ran once at that HEAD; counts read from `.harness/gate-*.log`.

```
static: ruff check "All checks passed!", ruff format --check clean, skill-lint exit 0
unit:   219 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on 8ab316fef07f7e962a68a4692d1207e4323f6318
```

## Giới hạn

- No real model was called. The client is proved against the fake provider only; compatibility with a given provider's wire format (beyond `choices[0].message.content`) is not shown.
- A job started through MCP runs in a thread of the server process; if that process exits, the job stays `running` and a new `panel_run` is the recovery (it asks only buyers without a valid answer). The CLI job survives the CLI call but not a machine restart.
- Two jobs started at once on the same panel would ask the same buyers twice; nothing prevents it.
- `check` and `save` remain CLI-only as before; `panel work` is internal and has no MCP tool.
- Timeouts and backoff are module constants (`llm.TIMEOUT`, `panel.BACKOFF`), not environment settings; the tests pass smaller values to `panel.execute`.
- Panel answers are the model's own; the package writes nothing for a buyer whose answer is missing or invalid. Concurrency is asserted by the provider's own counter on 25 buyers, not under load.

## Giải quyết review nội bộ

Lane không tự chạy `/code-review` (steering lane-implement). Hai lượt review độc lập do harness dispatch sau khi PR mở; kết quả nằm ở `reviews/issue-11/`.
