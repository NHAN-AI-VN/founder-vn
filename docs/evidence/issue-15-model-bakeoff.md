# Evidence: issue #15 model bake-off for the buyer panel

Lane run by the project owner on Kiro CLI (the ticket is `ready-for-human`: the dispatcher skips it, and the judgement of Vietnamese voice is the owner's). Lane branch `lane/issue-15`, target `main`. The allocation comment on #15 is written by the operator by hand, as on #5; until it exists the lane treats `README.md` as not granted.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.llm.complete_with_usage` (module function): the one OpenAI-compatible client returns, for one call, the reply text, the provider's `usage` token counts and the measured latency; `complete` keeps returning the text only. Criterion 1 compares latency and cost per buyer, and both come from the same call that produced the reply, so the bake-off must not carry a second HTTP client (`docs/agents/standards.md`, "one OpenAI-compatible client"). Catches: a provider reply without `usage`, the request body growing beyond `model` + `messages`. Misses: the wire format of a real provider.
- `scripts/bakeoff.py` (development script, `uv run python scripts/bakeoff.py <dir>`): reads `<dir>/models.json`, `<dir>/customer.json` and `<dir>/pitch.md`; deals five personas with `panel.deal` at a fixed seed; sends `panel.brief` of each persona to each candidate model through the client configured by `FOUNDER_LLM_BASE_URL` and `FOUNDER_LLM_API_KEY`, the candidate names coming from `models.json`; validates every reply with `panel.extract_answer`; writes `<dir>/results.json` (JSON validity rate, buys, latency, tokens, cost per buyer from the prices in `models.json`, model names, prompt hash, seed) and `<dir>/replies.md` (the five briefs' replies side by side per model, in Vietnamese, with the owner's scoring form for naturalness and honesty). It is a measurement tool of the project owner, not a computation for the Owner, so it sits next to `scripts/skill_lint.py` and has no CLI/MCP pair; the parity rule of the standards is read as not applying (inferred, stated here for the review). A missing input field is an error naming the field; a candidate's call that keeps failing (429, 5xx, timeout) is recorded as `failed`, never retried silently into a guess. Criterion 1.
- `docs/bakeoff/` inputs: `customer.json` (segments, behaviours, objections and habits drawn from the "Cho ai" paragraph of `examples/barbershop/founder/idea.md`), `pitch.md` (from its "Bán gì, giá bao nhiêu" paragraph), `models.json` (the candidates with price per 1M tokens, the official price page and the date the owner verified it; `reference` holds the chosen model once judged). Asserted: `panel.validate_customer` accepts the profile, five cards are dealt from both segments, the texts carry no `$` and no location below former-district level. Criterion 1 ("five personas drawn from the golden case's customer profile").
- Reference model in the documentation: `README.md` (single-owner), `docs/hosts/README.md` and the six host pages (a suggested `FOUNDER_LLM_MODEL` next to the three variables), and `docs/bakeoff/README.md` (the note: what was tried, what was chosen, why, and that the panel is comparable across hosts only with this model). Asserted by a test that reads `reference` from `docs/bakeoff/models.json` and finds it, with `FOUNDER_LLM_MODEL`, in each page. Criteria 2 and 3; written in the second phase, after the owner's judgement.

No automated seam judges Vietnamese voice or honesty: `replies.md` puts the texts in front of the owner, the buy count per model is printed as a signal of agreeableness, and the owner's scores and choice are recorded as data, not computed.

## Quyết định của lane

- Provider for development and for the bake-off: the Gemini API (Google AI Studio) on its free tier, through its OpenAI-compatible endpoint; decided by the project owner in this session on 2026-11-23 after the alternatives were compared (Kiro has no official OpenAI-compatible API; Amazon Bedrock is the paid path; the panel's cost on cheap paid models is of the order of a few hundred đồng per 20 buyers, so the free tier is a convenience for development, and the pilot moves to the paid tier of the same model id). The three candidates are three cheap models of that endpoint; their prices are entered in `models.json` with the official price page as source and are not trusted until the owner writes `price_verified`, which the script requires.
- Two phases. Phase 1 (this lane, unattended-shaped): client slice, script, inputs, tests on the fake provider; then the owner runs the script in a shell that holds the three variables (this Kiro session has none of them) and commits `results.json` and `replies.md`. Phase 2: the owner scores and chooses; the lane writes the note and the documentation and opens the pull request.
- The script writes `results.json` and `replies.md` with plain file writes into the directory the operator names on the command line: the path-locked layer guards paths chosen at run time by a model under `founder/`, and this script is not reached by a model. Stated for the Standards review.

## Lát

Every test runs against the fake provider on 127.0.0.1; no network, no real model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|

## Cổng ba đoạn

(pending)

## Giới hạn

(pending)

## Giải quyết review nội bộ

Lane không tự chạy `/code-review` (steering lane-implement). Hai lượt review độc lập do harness dispatch sau khi PR mở; kết quả nằm ở `reviews/issue-15/`.
