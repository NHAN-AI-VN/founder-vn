---
name: founder-marketing
description: >-
  Write the Owner's marketing file: a positioning statement that answers the objections of the simulated
  buyers, the channels the Owner's customers use, a 30-day campaign relative to opening day, the first
  hooks, a split of the Owner's marketing budget and the numbers to watch. Dùng khi anh/chị nói
  "làm sao để có khách", "kênh quảng cáo", "chiến dịch", "hook", "định vị", "ngân sách tiếp thị".
license: MIT
metadata:
  version: "0.2.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-marketing

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

Produce `founder/marketing.md`: how the Owner gets the first customers, built from what the simulated buyers and the Owner's own files already say. Read `founder/idea.md`, `founder/panel/results.md` (the "Vì sao không mua" table and the "Điều gì có thể đổi một lời từ chối" list), `founder/consumer.md`, `founder/competitors.md` and `founder/pricing.md`; read `founder/numbers.json` only to quote the marketing percentage. Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

**Every message answers an objection.** An objection is a "why not" answer or a "what would flip a no" answer in `panel/results.md` (or `consumer.md`), a gap in `competitors.md`, or something a real buyer told the Owner. A message that answers none of these is not written.

- Never write a customer quote that is not in the panel results or supplied by the Owner. Quote the words exactly, with the buyer id (for example P007) or "anh/chị cung cấp".
- Never promise reach or conversion: no number of views, visits, bookings or sales is predicted or targeted.
- Never add a channel the Owner's customers were not shown to use. The channel list below is closed; a channel is justified by `idea.md`, `consumer.md`, `panel/results.md` or `competitors.md`, and the file says which.
- Instagram and Yelp are not used.

## Step 1: read what exists

1. Read the files named in Purpose. If `founder/panel/results.md` does not exist, stop and tell the Owner to run `founder-consumer` first: without objections there is nothing to answer.
2. If `founder/marketing.md` exists, show the Owner in Vietnamese what it holds and ask what to change.
3. Ask only what the files do not say, for example whether the Owner already has a Zalo OA or a Facebook page. Do not ask for personal identity numbers.

## Step 2: write `founder/marketing.md`

Start with a title and one sentence naming the source files. Then these sections, in this order, with these headings:

## 1. Định vị

Write one statement (one statement of one or two sentences, not a list of slogans), then a table of its clauses: clause, objection or gap it answers, source. Each clause traces to an objection in `panel/results.md` or `consumer.md`, or to a competitor gap in `competitors.md`, quoted with its source (file and buyer id, or the competitor row). A clause with no source is deleted. Put the panel caveat once, in this section, where the panel results are first quoted: "Panel là mô phỏng, cận trên, không phải khách hàng thật; cần xác nhận với khách thật trước khi chi tiền."

## 2. Kênh

One subsection or table row per channel, each with why it fits this Owner's customers (with the source file): Biển hiệu và khách đi ngang (foot traffic and signage), Google Maps, Zalo OA, Facebook (trang và nhóm), ShopeeFood/GrabFood, người sáng tạo địa phương. Write ShopeeFood/GrabFood as "không áp dụng" with the reason when the business does not sell food or drink for delivery. A channel that does not fit is written as "không áp dụng" with the reason, not dropped silently.

## 3. Chiến dịch 30 ngày

A table of days 1 to 30, one row per day, relative to the opening day: "Ngày 1" is the opening day. `idea.md` may say the opening is not decided; then write no calendar date and say so in one sentence. Columns: ngày, kênh, việc làm, the objection it answers (with its source). Every row names one channel from section 2 (not one marked "không áp dụng"), one concrete action and one objection. No reach, conversion or spend figure in any row.

## 4. Hook đầu tiên

The first hooks, as many as the objections support, no fixed count. Each hook is one line the Owner can post or say, with the objection it answers and its source; each hook answers a different objection or a different clause of the positioning. A hook states only what `idea.md` and `pricing.md` already decide (a price, an hour, a policy); it invents no offer and no discount.

## 5. Chia ngân sách

Quote the Owner's input: the marketing percentage of revenue as `idea.md` and `numbers.json` name it. Divide that percentage into shares across the channels that are in use, as parts of the Owner's marketing budget (for example "1 phần trong 4"). You compute nothing new: no revenue figure, no absolute VND spend, no cost per customer. Absolute amounts belong to `founder-cfo`; tell the Owner to apply the shares to the amount `founder-cfo` gives. This skill writes no `numbers.json` and changes no number.

## 6. Số đo

Per channel, what to watch and how often, tied to numbers the Owner already has (for example the booking count, the repeat rate in the stop conditions of `idea.md`, the average ticket). Name where the Owner reads each number (the booking tool, the Google Maps profile, the Zalo OA report). No target value that the Owner's files do not already contain.

## 7. Lưu ý

Two short paragraphs. First, the advertising-rule caution, generic: "Quảng cáo dịch vụ có điều kiện phải theo quy định của ngành; xem `founder-permits` và `founder/permits.md`." Cite no article or figure of any law (no article or figure). Second, the disclaimer: "Kế hoạch tiếp thị này dựa trên ý tưởng của anh/chị và kết quả panel mô phỏng; không phải tư vấn tài chính, thuế hay pháp lý."

## Rules

- No invented quote, channel, result or discount; every message and hook traces to an objection with its source.
- Exactly seven sections in the order above; thirty campaign rows.
- The panel caveat appears once in the file; the advertising disclaimer is generic and cites no law.
- `founder/numbers.json` belongs to `founder-cfo`; this skill quotes the Owner's percentage and computes nothing new.
- No `$` next to a digit in anything the Owner reads.
