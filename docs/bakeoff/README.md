# Model bake-off for the buyer panel

Ticket T14 (#15), design Q42 (`docs/founder-vn-design.md` §6): the same five simulated buyers of
the golden case were asked by three cheap models, and the project owner picked one as the
**reference model** of the buyer panel. The pick is a project decision, written here so every
Facilitator sets the same `FOUNDER_LLM_MODEL`; the measurements behind it are in this directory.

## Chosen

**`gemini-3.5-flash-lite`** (Gemini API, OpenAI-compatible endpoint), decided by the project owner on
2026-11-24. Suggested setting: `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite`, next to
`FOUNDER_LLM_BASE_URL` and `FOUNDER_LLM_API_KEY` (how to set them per host: `docs/hosts/`).

**The panel is comparable across hosts, and across Owners in the pilot, only when every run uses
this model.** Every `founder/panel/panel.json` and `results.json` records the model that answered
and the hash of the brief, so a panel run on another model is visible and is read as a different
instrument, not as a different market.

## What was tried

Three cheap models on one endpoint, run on the free tier of the Gemini API from the owner's shell on
2026-11-24 (`scripts/bakeoff.py docs/bakeoff`, seed 14, prompt hash in `results.json`). Candidates,
with the paid-tier price per 1M tokens the owner verified on Google's pricing page the same day:

| Candidate | Price in/out (USD per 1M tokens) | JSON valid | Said "buy" | Mean latency | Mean cost per buyer | Voice | Honesty |
|---|---|---:|---:|---:|---:|---:|---:|
| `gemini-3.1-flash-lite` | 0.25 / 1.50 | 5/5 | 4/5 | 1.6 s | 0.000447 USD | 3 | 3 |
| `gemini-3.5-flash-lite` | 0.30 / 2.50 | 5/5 | 4/5 | 1.4 s | 0.000632 USD | 4 | 4 |
| `gemini-3.8-flash` | 0.75 / 3.75 until 2026-12-31, then 1.50 / 7.50 | 0/0 | — | — | — | — | — |

- JSON validity, buys, latency, tokens and cost are counted by the script from the replies
  (`results.json`); cost uses the provider's `usage` and the verified prices.
- Voice (natural Vietnamese) and honesty (answers follow the persona's income, habits and
  objections rather than the seller's pitch) were scored 1–5 by an independent judge at the owner's
  request: a Kiro CLI sub-agent (`claude-fable-5.1`) that saw the two models as "A" and "B" without
  their names (`scores.json`, with its per-persona notes). The choice is the owner's.
- `gemini-3.8-flash` answered none of the five buyers in two runs on the free tier (HTTP 503,
  timeouts at 90 s and then 180 s, then HTTP 429): **not evaluable on the free tier, not scored.**
  It is kept in the table because that is a finding about the tier the project develops on.
- The five personas were dealt by `founder_vn.panel.deal` from `customer.json` (drawn from the
  "Cho ai" paragraph of `examples/barbershop/founder/idea.md`) and asked with the panel's own
  brief, so the numbers describe the panel as it really runs. `replies.md` has every reply side by
  side.

## Why this one

- Both Flash-Lite models returned valid JSON for all five buyers in about 1.5 s, and the same buyer
  (the manager loyal to her usual barber) said no in both: neither simply agrees with the seller.
- `gemini-3.5-flash-lite` answered the four price questions for all five buyers; `gemini-3.1-flash-lite`
  left them empty for two, which would starve `founder-vn pricing` (Van Westendorp) of 40 % of a
  panel. Its reasons also leaned on the pitch's own promises; 3.5's leaned on the persona card
  ("125-150k đang trả", "gần văn phòng", "sau 18:00").
- The judge scored 3.5 higher on both axes (4/4 against 3/3) and preferred it on four of five
  personas for honesty.
- Cost is not a factor at this scale: about 0.0006 USD per buyer, so a 20-buyer panel costs of the
  order of a few hundred đồng on the paid tier.

## Limits and rules of use

- Free tier for development only. Google's pricing page states that free-tier requests are used to
  improve its products; the golden case is the owner's own data, pilot participants' data is not
  sent through the free tier. The pilot uses the paid tier of the same model id, so the reference
  model does not change (design §6: the owner's key during the pilot).
- The free tier's request limits do not fit the panel's fan-out of ten concurrent buyers; expect
  `failed` buyers and rerun `founder-vn panel run` (it asks only buyers without a valid answer).
- Five buyers and one run per model: a measurement of fit, not a benchmark. Models and prices
  change; rerun `scripts/bakeoff.py` (and re-verify `price_verified`) before changing the reference.
- Four of the five dealt personas carry women's given names for a men's barbershop: `customer.json`
  has no gender and `founder_vn.panel` deals names from one mixed list. The models answered in
  character anyway; the gap is marked for the panel skill (T15), not fixed here.
- The judge is a model, not a Vietnamese reader: its scores are an instrument the owner chose to
  use, and the per-persona notes in `scores.json` let a human check them.

## Files

| File | What |
|---|---|
| `models.json` | candidates, verified prices with source and date, `reference` |
| `customer.json`, `pitch.md` | the five personas' source profile and the pitch, from the golden case |
| `results.json` | every reply with validity, latency, tokens, cost; per-model summary; prompt hash |
| `replies.md` | the replies side by side, machine measures, filled scoring form |
| `scores.json` | the judge's scores and notes |

Rerun: set the three `FOUNDER_LLM_*` variables, then `uv run python scripts/bakeoff.py docs/bakeoff`
(`--only MODEL` re-asks one candidate, `--render` rewrites `replies.md` without any call).

## Tiếng Việt

Bake-off của ticket T14 chọn **`gemini-3.5-flash-lite`** làm mô hình tham chiếu cho panel người mua
mô phỏng: cùng 5 persona của case mẫu hỏi 3 mô hình rẻ trên bậc miễn phí của Gemini API ngày
24/11/2026. Hai bản Flash-Lite đều trả JSON hợp lệ 5/5, 4/5 nói mua; 3.5 trả đủ bốn mức giá cho cả 5
người và được giám khảo độc lập (chấm mù A/B) chấm 4/4 so với 3/3 của 3.1; `gemini-3.8-flash` không
chạy được trên bậc miễn phí (503, quá giờ, 429) nên không đánh giá. Người hỗ trợ đặt
`FOUNDER_LLM_MODEL=gemini-3.5-flash-lite`: **panel chỉ so sánh được giữa các host và giữa các chủ hộ
khi mọi lần chạy dùng đúng mô hình này**; `results.json` ghi tên mô hình đã trả lời. Bậc miễn phí chỉ
dùng cho dev với dữ liệu của chủ dự án; dữ liệu người pilot đi qua bậc trả phí của cùng mô hình.
