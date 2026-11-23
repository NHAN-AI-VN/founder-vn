# Evidence: issue #11 server-side fan-out, panel run and job status

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.llm` (module): the one OpenAI-compatible client, configured by `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL`; unconfigured is an error with setup instructions; the request carries no `response_format`, `seed` or `temperature`. Criterion 1.
- `founder_vn.panel` (module): `brief` and `prompt_hash` (Vietnamese buyer brief from persona and pitch, hash of template, personas and pitch recorded in `panel.json`), `extract_answer` (first JSON object, validated with `answer_problem`), `start_job` and `execute` (waves of 10, per-call timeout, retry with backoff, exclusion after two invalid answers, answers written one by one, rerun only missing or invalid), `job_status` (done, pending, failed, excluded, last error). Criteria 2, 3, 4, 5.
- `founder-vn panel run` and `founder-vn panel status` (CLI commands): `run` prints a job id at once and hands the work to a detached process, so the host call returns; `status` reads the job file. Criteria 3, 6.
- `panel_run` and `job_status` (MCP tools of `founder-vn-mcp`): the other end of the parity pair; the response shapes are asserted identical to the CLI's. Criterion 6.
- `founder_vn.files` (path-locked layer): the only way answers and the job file are written. Criteria 3, 4.
- `tests/conftest.py` `fake_provider`: extended with a scripted reply (status, content, delay) and a concurrency counter, so 5xx, timeout, invalid and wave-size cases run with no network. Criterion 6.
