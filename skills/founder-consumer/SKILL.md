---
name: founder-consumer
description: >-
  Confirm the customer profile with the Owner, write the pitch, run a 20-buyer simulated panel
  through the package tools and read the result back in five points. Dùng khi anh/chị nói "khách
  hàng có mua không", "thử với khách mô phỏng", "panel người mua", "khách hàng mục tiêu".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-consumer

## Protocol

1. Check the version: call the MCP tool `server_info`, or run `founder-vn --version` in the shell.
   Compare its major version with `metadata.version` of this skill. On a major mismatch, stop and
   tell the Facilitator to update the package or the skill.
2. Prefer MCP tools. If the MCP server is not available, run the `founder-vn` CLI through the
   shell. If neither is available, stop and print the install instructions from the README.
3. Never compute a number yourself. Every figure comes from a `founder-vn` tool or command.
4. Never answer for a buyer. Simulated buyers answer only through the panel tools.
5. Never write the verdict. The verdict comes from the tool output and is shown as given.

## Purpose

Find out, before the Owner spends money, how a panel of simulated buyers reacts to the pitch, and which objections and customer groups decide it. You write the customer profile and the pitch; the package deals the persona cards, asks each buyer through the configured model and counts the answers (`panel_init`, `panel_run`, `job_status`, `panel_tally`; CLI: `founder-vn panel init`, `run`, `status`, `tally`). Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

## Step 1: the customer profile

1. Read `founder/idea.md`. If it does not exist, ask the Owner in Vietnamese, one group at a time, who the customer is, what is sold and at what price, and where. Never fill a gap with a guess.
2. If `founder/competitors.md` exists, read the complaints about competitors in it (the column "Phàn nàn thấy được" and the review themes) and use them as objections, naming the competitor they came from. A cell that says "chưa có số liệu" is not a complaint; do not turn it into one. If the file does not exist, go on without it and say so.
3. Write `founder/customer.json` with these fields, in Vietnamese:
   - `business` and `target`: the business and the customer in one line each; `where`: the area, to district level.
   - `age`: `[low, high]`.
   - `segments`: two to four groups, each with `name`, `share` and `income`, a `[low, high]` monthly VND income range (whole dong, for example `[15000000, 30000000]`). Shares are relative weights.
   - `behaviours`: how the customer buys, each with `name`, `share` and `how` (one sentence).
   - `objections`: three to six short sentences a buyer would say about hesitating, from competitor complaints and from the Owner's own worries.
   - `habits`: two to five everyday habits that bear on the purchase.
   The deal gives buyers names from one mixed list and the persona brief carries no gender field. When the product is for one gender only, write it into every segment name (for example "Nam, nhân viên văn phòng"), because the segment name is the only profile text the buyer sees.
4. Show the profile to the Owner in Vietnamese as a readable table, not as raw JSON. Mark every part that is a guess ("đoán của tôi, anh/chị sửa giúp") and say which parts come from the Owner, which from `competitors.md`, and which are guesses. Ask the Owner to correct it before dealing. Do not call `panel_init` until the Owner has confirmed the profile; apply each correction to `customer.json` and show the changed part again.

## Step 2: the pitch

Write `founder/pitch.md` in Vietnamese: three to six plain lines, in the words a seller says across the counter. State what is sold, the price the customer pays, where, and when. Use no superlative ("nhất", "số một", "tốt nhất", "rẻ nhất", "hoàn hảo") and promise nothing the business cannot deliver: take every claim from `founder/idea.md` or from what the Owner said, never from the wish to sound good. Show the pitch to the Owner and change it where the Owner corrects it.

## Step 3: the panel

1. Size: `n = 20` by default. Use 100 only when the Owner asks for it, and before running it tell the Owner in Vietnamese that it costs about five times the default in model calls and takes longer (the cost and time warning); run it only after the Owner agrees.
2. Call `panel_init` with `customer.json`, `pitch.md` and `n` (CLI: `founder-vn panel init --customer customer.json --pitch pitch.md --n 20`). It prints the seed.
3. Call `panel_run` (CLI: `founder-vn panel run`). It returns at once with a `job_id`. Poll `job_status` with that id (CLI: `founder-vn panel status <job_id>`) every few seconds until `state` is `done`, telling the Owner in Vietnamese that the buyers are answering. If the tool says the model is not configured, stop and tell the Facilitator to set `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL`; do not write an answer yourself in place of a buyer. Never answer for a buyer: not for one that failed, not for one that timed out, not to fill a gap.
4. If `state` is `error`, or buyers are excluded, say how many and why in plain words (the `last_error`), then call `panel_run` again: it asks only the buyers without a valid answer. A buyer still without a valid answer stays excluded and is reported as excluded; never fill one in.
5. Call `panel_tally` (CLI: `founder-vn panel tally`). It writes `founder/panel/results.md` and `results.json`. Every number you say comes from them.

## Step 4: read it back

Read `founder/panel/results.md` and `results.json`, then write the reading to `founder/consumer.md` in Vietnamese: a short opening paragraph (the panel size, the model, the seed, how many buyers were excluded), the five points below in this order, the caveat once, then the disclaimer, so the file holds the five points, then the caveat once, then the disclaimer. Tell the Owner the same reading in the chat reply and name the file; the chat reply stays as it is. The five points:

1. **Headline**: how many buy and how many pass, and the buy rate, as the tool gives them. Say how many buyers were excluded (with their ids) when there are any.
2. **Where it differs**: the segments and the behaviours whose buy rates differ most. A group the tool marks "(mỏng)" is thin: say so and draw no conclusion from it.
3. **Top three reasons for passing**, each with one quote each, verbatim from the results and with the buyer id. If fewer than three reasons exist, give those that exist.
4. **What would flip a no**: the most repeated "would change my mind" answers, from `flip`.
5. **What to change**: one sentence on the single change that would help most, and which skill does it: price is `founder-pricing`, a competitor gap is `founder-competitors`, the offer or the promise is `founder-board`, the numbers are `founder-cfo`.

Print the caveat once, after the five points, not on every line: "Panel là mô phỏng, cận trên, không phải khách hàng thật. Dùng nó để tìm phản đối và điểm yếu, rồi xác nhận với khách thật (bán trước, danh sách chờ) trước khi chi tiền." Say which model ran the panel (`model` in `results.json`). Never present a quote as a testimonial.

End with the disclaimer, in the file and in the chat reply: "Kết quả này không phải tư vấn tài chính, thuế hay pháp lý."

## Rules

- The Owner confirms `customer.json` before any buyer is dealt.
- Every figure comes from the panel tools; no figure, quote or buyer is made up.
- Excluded buyers are always reported, never replaced.
- No `$` next to a digit in anything the Owner reads.
