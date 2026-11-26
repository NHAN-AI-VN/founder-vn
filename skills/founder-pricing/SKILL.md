---
name: founder-pricing
description: >-
  Turn the panel's price answers, competitor prices and the CFO margin into an acceptable price
  range, a recommended price, a good/better/best ladder and an opening offer to test. Dùng khi anh/chị
  nói "định giá", "giá bao nhiêu thì hợp lý", "bán giá bao nhiêu", "bậc giá", "giá khai trương".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-pricing

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

Give the Owner a price to test, with the evidence under it: the range the simulated buyers accept (Van Westendorp), where the competitors sit, and whether the CFO model still makes money at that price. You read, compare and explain; the package computes (`pricing_psm`, `cfo_model`; CLI: `founder-vn pricing`, `founder-vn cfo`). Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

## Step 1: inputs

1. `founder/panel/pricing_input.json` holds the panel's four price answers per buyer (`too_cheap`, `bargain`, `getting_expensive`, `too_expensive`); `founder-vn panel tally` writes it. If it does not exist, tell the Owner in Vietnamese to run `founder-consumer` first and stop. Never write a price answer yourself.
2. Read `founder/competitors.md`. Take the listed price of the same service the Owner sells, one per competitor, exactly as printed. A cell that says "chưa có số liệu" is not a price: leave that competitor out and say so. A price written "từ" is a floor, not a typical price: keep it and say so. If the file does not exist, go on without competitor prices and say so.
3. Read `founder/cfo.md` and `founder/numbers.json` (the CFO model). If they do not exist, tell the Owner in Vietnamese to run `founder-cfo` first; without them the break-even check in Step 3 cannot run, and you say so in `pricing.md` instead of skipping it quietly.
4. Read `founder/idea.md` for the Owner's own price list. It supplies the ladder in Step 4; do not invent a rung the Owner does not sell.

## Step 2: the tool

1. Write `founder/pricing_input.json`: the `answers` of `panel/pricing_input.json` unchanged, plus `competitor_prices`, a list with the competitor prices from Step 1 as whole đồng. Leave `competitor_prices` out when there are none.
2. Call `pricing_psm` with `pricing_input.json` (CLI: `founder-vn pricing pricing_input.json`; add `--json` to read the numbers). Every figure in `pricing.md` comes from this output: the four medians, the lowest and highest acceptable price, the indifference point, the number of valid and dropped answers, and how many competitor prices lie inside the range.
3. The tool warns `thin_data` (the report says "Dữ liệu mỏng") when fewer than 8 answers are valid. Pass that warning through at the top of `pricing.md`, word for word, and state no recommended price as firm; say the Owner needs more answers or real customers first.

## Step 3: the CFO break-even check

1. Take the recommended price from Step 4 and every ladder price. For each, run `cfo_model` with the what-if price (CLI: `founder-vn cfo numbers.json --price <price> --json`). The tool keeps every cost at the Owner's amounts and changes only the price.
2. Read `margin_at_plan` and `breakeven_per_day` from the output. A price is below the CFO break-even when `margin_at_plan` is zero or negative, or `breakeven_per_day` is higher than the planned volume per day in `founder/numbers.json` or higher than capacity. Flag every such price in `pricing.md` in plain words ("giá này thấp hơn mức hòa vốn của CFO") with the margin and the break-even volume as the tool gives them. Never hide the flag because the price is liked by buyers, and never move the recommended price to avoid it: show both and let the Owner decide.
3. Also say where the CFO's own price (`founder/cfo.md`, "Giá bán") sits against the acceptable range.

## Step 4: write `founder/pricing.md`

Write it in Vietnamese with these sections, in this order. Use only figures from the tools and prices from the Owner's files; No fabricated anchors: no "giá thị trường", no benchmark, no competitor price that is not in `competitors.md`, no number you cannot point to.

1. **Khoảng giá chấp nhận được**: the lowest and highest acceptable price and the indifference point from the tool, the four medians, and the competitor prices against the range (listed with their names as in `competitors.md`, from the tool's count). Put the thin-data warning above it when the tool gave one.
2. **Giá đề xuất**: one price. Start from the indifference point as the tool prints it. You may name a tidy price within 1.000 đ of it (for example one that the Owner already lists in `idea.md`) and say it is a rounding of the tool's figure. Add the CFO check for it from Step 3.
3. **Bậc giá** (good / better / best): the Owner's own listed prices from `idea.md`, lowest to highest, as a table with the service name, the price, whether it lies inside the acceptable range, and its CFO margin and break-even volume from Step 3. Mark the rung that is the recommended price. If the Owner lists fewer than three prices, show the ones that exist and do not make up a rung.
4. **Ưu đãi mở đầu để thử**: one offer to test with real customers, built from the recommended price and, where the Owner has them, the Owner's own deposits, packs or discounts in `idea.md`; no new discount value that the Owner did not state. Say what to test (for example the recommended price against the CFO price), with how many customers and for how long only if the Owner gave those figures; otherwise ask the Owner.
5. **Theo dõi sau khi mở bán**: what to watch, tied to numbers the Owner already has: the stop conditions in `idea.md`, the break-even volume from the CFO, the share of customers who pick each rung, complaints about price. No new target number.

Close `pricing.md` with the caveat once: "Panel là mô phỏng, cận trên, không phải khách hàng thật. Dùng khoảng giá này để chọn giá thử, rồi xác nhận với khách thật (bán trước, danh sách chờ, trang giới thiệu có ghi giá) trước khi chi tiền." Then the disclaimer: "Kết quả này không phải tư vấn tài chính, thuế hay pháp lý."

## Step 5: tell the Owner

In Vietnamese, in five lines: the acceptable range, the recommended price, whether it is below the CFO break-even, the offer to test, and the first thing to watch. Name `founder-pricing` output as `founder/pricing.md`.

## Rules

- Every figure comes from `pricing_psm`, `cfo_model` or the Owner's files; none is made up or computed by hand.
- The thin-data warning is passed through and never softened.
- A price below the CFO break-even is always flagged, next to the price, never in a footnote.
- No `$` next to a digit in anything the Owner reads.
