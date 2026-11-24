# Evidence: issue #15 model bake-off for the buyer panel

Lane run by the project owner on Kiro CLI (the ticket is `ready-for-human`: the dispatcher skips it, and the judgement of Vietnamese voice is the owner's). Lane branch `lane/issue-15`, target `main`. The allocation comment on #15 (2026-11-24, by the operator, `singleOwnerFiles: README.md`) was posted from this session at the owner's request; `README.md` was not touched before it existed.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.llm.complete_with_usage` (module function): the one OpenAI-compatible client returns, for one call, the reply text, the provider's `usage` token counts and the measured latency; `complete` keeps returning the text only. Criterion 1 compares latency and cost per buyer, and both come from the same call that produced the reply, so the bake-off must not carry a second HTTP client (`docs/agents/standards.md`, "one OpenAI-compatible client"). Catches: a provider reply without `usage`, the request body growing beyond `model` + `messages`. Misses: the wire format of a real provider.
- `scripts/bakeoff.py` (development script, `uv run python scripts/bakeoff.py <dir>`): reads `<dir>/models.json`, `<dir>/customer.json` and `<dir>/pitch.md`; deals five personas with `panel.deal` at a fixed seed; sends `panel.brief` of each persona to each candidate model through the client configured by `FOUNDER_LLM_BASE_URL` and `FOUNDER_LLM_API_KEY`, the candidate names coming from `models.json`; validates every reply with `panel.extract_answer`; writes `<dir>/results.json` (JSON validity rate, buys, latency, tokens, cost per buyer from the prices in `models.json`, model names, prompt hash, seed) and `<dir>/replies.md` (the five briefs' replies side by side per model, in Vietnamese, with the owner's scoring form for naturalness and honesty). It is a measurement tool of the project owner, not a computation for the Owner, so it sits next to `scripts/skill_lint.py` and has no CLI/MCP pair; the parity rule of the standards is read as not applying (inferred, stated here for the review). A missing input field is an error naming the field; a candidate's call that keeps failing (429, 5xx, timeout) is recorded as `failed`, never retried silently into a guess. Criterion 1.
- `docs/bakeoff/` inputs: `customer.json` (segments, behaviours, objections and habits drawn from the "Cho ai" paragraph of `examples/barbershop/founder/idea.md`), `pitch.md` (from its "Bán gì, giá bao nhiêu" paragraph), `models.json` (the candidates with price per 1M tokens, the official price page and the date the owner verified it; `reference` holds the chosen model once judged). Asserted: `panel.validate_customer` accepts the profile, five cards are dealt from both segments, the texts carry no `$` and no location below former-district level. Criterion 1 ("five personas drawn from the golden case's customer profile").
- Reference model in the documentation: `README.md` (single-owner), `docs/hosts/README.md` and the six host pages (a suggested `FOUNDER_LLM_MODEL` next to the three variables), and `docs/bakeoff/README.md` (the note: what was tried, what was chosen, why, and that the panel is comparable across hosts only with this model). Asserted by a test that reads `reference` from `docs/bakeoff/models.json` and finds it, with `FOUNDER_LLM_MODEL`, in each page. Criteria 2 and 3; written in the second phase, after the owner's judgement.

No automated seam judges Vietnamese voice or honesty: `replies.md` puts the texts in front of the owner, the buy count per model is printed as a signal of agreeableness, and the owner's scores and choice are recorded as data, not computed.

## Quyết định của lane

- Provider for development and for the bake-off: the Gemini API (Google AI Studio) on its free tier, through its OpenAI-compatible endpoint; decided by the project owner in this session on 2026-11-23 after the alternatives were compared (Kiro has no official OpenAI-compatible API; Amazon Bedrock is the paid path; the panel's cost on cheap paid models is of the order of a few hundred đồng per 20 buyers, so the free tier is a convenience for development, and the pilot moves to the paid tier of the same model id). The three candidates are three cheap models of that endpoint; their prices are entered in `models.json` with the official price page as source and are not trusted until the owner writes `price_verified`, which the script requires. The owner verified them on 2026-11-24 by pasting the page's three tables into the session.
- **Reference model: `gemini-3.5-flash-lite`**, chosen by the project owner on 2026-11-24 after reading `replies.md` and the judge's scores. The scoring of voice and honesty was delegated by the owner to an independent, blind sub-agent (the owner's instrument; recorded as such in `scores.json` and the note); the choice itself is the owner's. `gemini-3.8-flash` is recorded as "không chạy được trên bậc miễn phí, không đánh giá" by the owner's decision, not retried on another day.
- Two phases. Phase 1 (this lane, unattended-shaped): client slice, script, inputs, tests on the fake provider; then the owner ran the script in a shell that holds the three variables (this Kiro session has none of them) and the lane committed `results.json` and `replies.md`. Phase 2: scores and choice recorded, note and documentation written, pull request opened.
- The script writes `results.json`, `replies.md` with plain file writes into the directory the operator names on the command line: the path-locked layer guards paths chosen at run time by a model under `founder/`, and this script is not reached by a model. Stated for the Standards review.
- `README.md` was edited under the operator's allocation comment on #15 (2026-11-24, `singleOwnerFiles: README.md`), posted at the owner's request from this session with the owner's `gh`.
- One pending-work marker (`⏳`) was added as a comment in `src/founder_vn/panel.py` at `GIVEN_NAMES`: the bake-off dealt four women's names out of five buyers for a men's barbershop because `customer.json` carries no gender. Behaviour unchanged; for T15 to decide.

## Lát

Every test runs against the fake provider on 127.0.0.1; no network, no real model. Commands run in the lane's worktree (`.harness/lane-15`, see "Giới hạn").

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| llm usage | `tests/test_llm.py::test_complete_with_usage_returns_text_tokens_and_latency_from_the_same_call`, `test_complete_with_usage_tolerates_a_reply_without_usage` | `AttributeError: module 'founder_vn.llm' has no attribute 'complete_with_usage'` (2 failed, 3 passed) | `uv run pytest tests/test_llm.py -q` (5 passed), commit `dc7228c` |
| script inputs | `tests/test_bakeoff.py::test_models_file_problems_are_errors_naming_the_field`, `test_customer_and_pitch_are_checked_like_the_panel_does` | `FileNotFoundError: [Errno 2] No such file or directory: '.../scripts/bakeoff.py'` (collection error) | `uv run pytest tests/test_bakeoff.py -q` (2 passed), `73923d6` |
| run | `test_run_asks_each_candidate_the_same_five_personas_and_writes_results_and_replies` (15 calls, same five ids per model, brief identical to `panel.brief`, prompt hash, validity 4/5 for the model whose one reply is prose, buys 0 for the model that never buys, cost from the fake `usage` and the prices, `replies.md` content, no endpoint or key string in either output) | `AttributeError: module 'bakeoff' has no attribute 'run'` | same command (3 passed), `1313bf8` |
| failure path and main | `test_a_candidate_that_keeps_failing_is_recorded_failed_after_retries_with_backoff`, `test_main_exit_codes_and_messages` | `AttributeError: module 'bakeoff' has no attribute 'main'`. The retry test passed on first run (the retry loop came with `ask` in the previous slice): red witnessed by mutation `ATTEMPTS = 1`, `AssertionError: assert 5 == 15` (requests to the failing model), restored, `git diff` empty | same command (5 passed), `f0adca6` |
| repo inputs | `test_repo_inputs_come_from_the_golden_case_and_deal_five_personas_from_both_segments` | `bakeoff.BakeoffError: không thấy .../docs/bakeoff/customer.json` | same command (6 passed); `scripts/skill_lint.py`: 2 skills, 4 example files, 0 findings; `3d70360` |
| verified prices | same test, tightened to `bakeoff.load_models(BAKEOFF_DIR)` | `BakeoffError: 'models[0].price_verified' phải là ngày chủ dự án đã kiểm giá, dạng YYYY-MM-DD` | same command (6 passed), `790d291`; the owner pasted the three price tables of Google's pricing page into the session |
| --only, --timeout | `test_only_reruns_the_named_candidates_and_keeps_the_other_rows` | `TypeError: run() got an unexpected keyword argument 'only'` | same command (7 passed), `6e371fe` |
| scores, --render | `test_render_fills_the_scoring_form_from_scores_json_without_calling_any_model` | `SystemExit: 2` (argparse: unknown `--render`) | same command (8 passed), `080d6db` |
| reference model in the docs | `test_reference_model_is_named_in_readme_host_pages_and_the_note`, `test_rendered_replies_carry_the_scores_and_the_reference` | `AssertionError: README` / `assert ('`gemini-3.5-flash-lite`' in '# Host pages ...')`. The second test passed on first run (it reads files rendered the commit before): red witnessed by mutation of `reference` in `models.json` to `gemini-3.1-flash-lite`, `AssertionError: assert 'Mô hình tham chiếu đã chọn: `gemini-3.1-flash-lite`' in '# Bake-off ...'`, restored with `git checkout` | `uv run pytest tests/test_bakeoff.py tests/test_hosts.py tests/test_golden_case.py tests/test_front_door.py -q` (34 passed); `check-doc-paths`: 23 paths exist; `e490107` |
| fake provider backlog (flake found by the unit gate) | `tests/test_panel_run.py::test_buyers_are_asked_in_waves_of_ten_concurrent_calls` (existing test, unchanged) | Unit gate at `6df0a51`: `AssertionError: assert 7 == 10` (`max_active`). Diagnosis, not retry: 5/5 red in isolation on this branch, 2/3 red on unchanged `main` code in the main checkout, every red run 2 s longer than a green one (the panel's `BACKOFF`): socketserver's listen backlog of 5 refused part of a ten-connect wave, the refused call was retried after 2 s and the measured concurrency fell | `request_queue_size = 64` on the fake provider (`tests/conftest.py` only): 6/6 passed in 0.9 s, `0c22349` |

## Real runs (the owner's shell, Gemini API free tier)

The three `FOUNDER_LLM_*` variables were set only in the owner's shell; this session never held them. Evidence records model names and the prompt hash, nothing else about the configuration.

| Run | Command | Result | Commit |
|---|---|---|---|
| 1 | `uv run python scripts/bakeoff.py docs/bakeoff` (seed 14, prompt hash `919a9496dd05…1001`) | `gemini-3.1-flash-lite` 5/5 valid JSON, 4 buy, 1.6 s, 644/191 tokens, 0.000447 USD per buyer; `gemini-3.5-flash-lite` 5/5, 4 buy, 1.4 s, 644/176, 0.000632 USD; `gemini-3.8-flash` 0/5 (503, 90 s timeouts; 3 attempts each) | `f961ca3` |
| 2 | `… --only gemini-3.8-flash --timeout 180` | still 0/5: two 180 s timeouts, one 503, two 429; Flash-Lite rows kept (same seed and hash) | `d8a9168` |
| judge | blind A/B scoring by a Kiro CLI sub-agent (`claude-fable-5.1`) at the owner's request, from the ten replies, personas and pitch; names withheld | 3.1: voice 3, honesty 3; 3.5: voice 4, honesty 4; 3.8: not evaluable; per-persona notes in `docs/bakeoff/scores.json` | `967fa32` |
| render | `… --render` | `replies.md` with the filled form and "Mô hình tham chiếu đã chọn: `gemini-3.5-flash-lite`" | `967fa32` |

## Cổng ba đoạn

Last code commit: `0c22349`. Each segment ran once at that HEAD in the lane's worktree (an earlier `unit` segment at `6df0a51` was red on the flaky wave test, diagnosed and fixed in `0c22349`, so all three segments were rerun); counts read from `.harness/gate-*.log`.

```
static: ruff check "All checks passed!", ruff format --check clean, skill-lint 2 skills checked, 4 example file(s), 0 finding(s)
unit:   271 passed in 17.28s
build:  Successfully built dist/founder_vn-0.1.0.tar.gz and dist/founder_vn-0.1.0-py3-none-any.whl
  static 0 0c223496d00b61cb5bb9bb8e0820166656faa052 2026-11-24T03:58:25Z
  unit 0 0c223496d00b61cb5bb9bb8e0820166656faa052 2026-11-24T03:58:48Z
  build 0 0c223496d00b61cb5bb9bb8e0820166656faa052 2026-11-24T03:58:58Z
gate-segment verify: GREEN on 0c223496d00b61cb5bb9bb8e0820166656faa052
```

## Giới hạn

- Five buyers, one run per model, one day, one tier: a measurement of fit for the panel, not a benchmark of the models. The free tier's rate limits shaped the result for `gemini-3.8-flash` (0/5 in two runs); whether that model would answer well on the paid tier is not known.
- Voice and honesty were scored by a model (a blind Kiro CLI sub-agent), not by a Vietnamese reader; the owner chose to use that instrument and made the choice. The per-persona notes in `scores.json` are there for a human to check the scores against the replies.
- The reference model is recorded in documentation only (README, host pages, note, `models.json`); no code warns when `FOUNDER_LLM_MODEL` differs. `results.json` of every panel records the model that answered, which is what makes a divergent run visible.
- Prices are the paid-tier prices the owner read on Google's page on 2026-11-24; the `gemini-3.8-flash` price is promotional until 2026-12-31. The free tier bills nothing and, per the same page, uses requests to improve Google's products: the note restricts it to the owner's own data.
- Four of the five dealt personas carry women's given names for a men's barbershop (`panel.deal` has no notion of gender); marked `⏳` in `panel.py` for T15, not fixed here.
- The lane works in a git worktree, `.harness/lane-15` (git-ignored, branch `lane/issue-15`), because the main checkout was switched to `lane/issue-12` by the owner's parallel session while this lane was set up; the lane's first seam commit landed on `lane/issue-12` locally, was never pushed (non-fast-forward), was cherry-picked to `lane/issue-15` and removed from `lane/issue-12` with `git reset --soft` (the owner's tree unchanged). The guard's single-owner rule does not see paths inside the worktree; `README.md` was edited only after the allocation comment existed.
- The `test_buyers_are_asked_in_waves_of_ten_concurrent_calls` fix changes test infrastructure (listen backlog of the fake provider), not the panel; the panel's own behaviour under a refused connection (retry after backoff) is what the red runs showed, and it is unchanged.

## Giải quyết review nội bộ

Lane không tự chạy `/code-review` (steering lane-implement). Hai lượt review độc lập do harness dispatch sau khi PR mở; kết quả nằm ở `reviews/issue-15/`.
