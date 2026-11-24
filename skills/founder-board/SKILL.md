---
name: founder-board
description: >-
  Write a standalone brief, run three lens memos (Offers, Product, Systems) on the configured
  model, then write the chair's summary that keeps the disagreements. Dùng khi anh/chị nói "hội
  đồng cố vấn", "góp ý ý tưởng", "ý tưởng này có ổn không", "ba góc nhìn", "có nên mở".
license: MIT
metadata:
  version: "0.2.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-board

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

Give the Owner three disagreeing readings of the idea, from three published frameworks, and a chair's summary that keeps the disagreements and turns the conditions into one checklist. The three memos are written by the package (`board_run` / `founder-vn board run`), not by you: each lens is a separate model completion that sees only the brief, so the readings do not leak into each other. You write the brief before and the chair's summary after. The lens texts are in `lenses.md` next to this file. Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

## Step 0: the idea

1. If `founder/idea.md` exists, reuse it: show the Owner in Vietnamese what it says in two or three lines and ask whether it is still right. Change it only where the Owner corrects it.
2. If it does not exist, write it. Ask in Vietnamese, one group at a time, in the words a shop owner uses: what the business is and the promise to the customer; who it is for; what is sold and at what price the customer pays; where and how customers find it; the budget and the constraints; what is already decided. Write the answers to `founder/idea.md`. Never fill a gap with a guess: a figure the Owner does not know stays a question in the file.

## Step 1: the brief

Write `founder/board/brief.md` in Vietnamese. It must stand alone: the three lens runs are separate model calls that cannot see the conversation, `idea.md` or any other file. Put everything a stranger needs into the brief itself:

- the business, the promise and the unit sold;
- the customer and where the Owner expects to find them;
- every price, cost, capacity and budget figure the Owner gave, copied exactly as given and marked "giả định của chủ" when it is not measured;
- the location and the competitors the Owner named, with what the Owner knows of them;
- what is decided and what is open;
- what the Owner worries about, in the Owner's words.

Do not add an opinion, a score or a recommendation. Do not invent a figure to fill a hole; write "chưa có số liệu". If a file such as `founder/competitors.md` already exists, copy only the facts you need into the brief; do not tell the lenses to read it.

## Step 2: run the three lenses

1. MCP: call `board_run`. CLI: run `founder-vn board run` in the project folder.
2. It returns at once with a `job_id`. Poll `job_status` (CLI: `founder-vn panel status <job_id>`) every few seconds until `state` is `done`; tell the Owner in Vietnamese that the three readings are being written. The memos land in `founder/board/offers.md`, `product.md` and `systems.md` as they arrive.
3. If `state` is `error`, or `failed` or `excluded` is above 0, say which lens and the `last_error` in plain words, then call `board_run` again: it asks only the lenses without a valid memo. If the tool reports that the model is not configured, stop and tell the Facilitator to set `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL`; do not write a memo yourself in place of a lens.
4. `founder/board/board.json` records the model and the prompt hash of the run.

## Step 3: the chair's summary

Read the three memos. Write `founder/board.md` in Vietnamese with these sections, in this order:

1. **Ba lens, ba cách đọc**: one block per lens (Offers, Product, Systems): the score and the vote exactly as the memo prints them, then the memo's strongest point and its deadliest risk in your own words, one or two sentences each. Do not average the scores, do not add them, do not pick a winner.
2. **Chỗ các lens không đồng ý**: every point where two lenses disagree (a different vote, or the same fact read as a strength by one and a risk by another). Name the lenses, say what each reads and why, and leave the disagreement open. A disagreement is not a mistake to smooth over; never average it away or hide it under a shared conclusion. If the lenses agree on everything, say so and say that the Owner should be suspicious of an unanimous reading from three simulated readers.
3. **Danh sách điều kiện**: merge the conditions of the three memos into one checklist of `- [ ]` items. Join two conditions only when they ask for the same thing, and keep the lens names in brackets after the item. Keep every condition that can be checked; drop none silently. Each item says what to measure or do, so the Owner can tick it.
4. **Số còn mở và skill trả lời**: a table of the open questions and numbers from the memos, one row each, with the skill that answers it: market and competitor facts and the gap to own go to `founder-competitors`; whether customers say they would buy, and why not, go to `founder-consumer`; the price the customer accepts goes to `founder-pricing`; costs, break-even, cash and tax go to `founder-cfo`. A question no skill answers (for example hiring a head barber) goes in the row marked "ngoài bộ công cụ: anh/chị tự xác minh". Never answer an open number yourself.

Close `board.md` with these two lines: "Ba bản đọc này là mô phỏng từ ba khung đã xuất bản, không nói thay tác giả của chúng, và không thay thế khách hàng thật." and "Đây không phải tư vấn tài chính, thuế hay pháp lý." Then tell the Owner in Vietnamese where `board.md` is, which disagreement matters most for the decision and what to run next. Do not give a verdict: the Profitable / Not yet / Incomplete verdict comes from `founder-cfo` numbers through `founder-plan` only, and a lens vote is not it.

## Rules

- The brief stands alone; the lenses see nothing else. Never tell a lens to read a file.
- The memos are the package's output. Never write, edit or "improve" `offers.md`, `product.md` or `systems.md`.
- Lenses apply a published framework and never speak as its author; never write a sentence in the chair's summary that quotes an author as if he were reviewing the idea.
- Keep the disagreements. Never average scores or votes.
- Never write a number the memos and the Owner did not give; route every open number to the skill named above.
- No `$` next to a digit in anything the Owner reads.
