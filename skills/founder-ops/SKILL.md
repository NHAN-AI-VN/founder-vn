---
name: founder-ops
description: >-
  Write the Owner's day-one operations file: suppliers and quotes, staffing and weekly rota, opening,
  serving and closing routines, a minimal tool stack and a ten-item risk register. Dùng khi anh/chị
  nói "ngày đầu vận hành thế nào", "nhà cung cấp", "ca làm", "quy trình mở cửa", "sổ rủi ro".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-ops

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

Produce `founder/ops.md`: how the business runs on day one, from the Owner's own files. Read `founder/idea.md` (roles and headcount, opening hours, services) and, when they exist, `founder/cfo.md` and `founder/numbers.json` (the planned costs). Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

**Never invent a supplier, a quote or a price.** A supplier the Owner has not named is "chưa chọn". A cost the Owner has not quoted is "chưa có báo giá". The rule of `founder-competitors` applies: no data is not data, so a blank stays blank and is shown as such. Never fill a cell from general knowledge of the market. A figure on the page is either copied from the Owner's files (and says which file) or it is not there.

## Step 1: read what exists

1. Read `founder/idea.md` for the business, the services, the opening hours and the staffing by role.
2. Read `founder/numbers.json` and `founder/cfo.md` if they exist, only to quote the planned costs already there. This skill writes no `numbers.json` and changes no number.
3. If `founder/ops.md` exists, show the Owner in Vietnamese what it holds and ask what to change.
4. Ask only what the files do not say: which supplies the business buys, which suppliers the Owner has already talked to, and whether the Owner holds any written quote. Do not ask for personal identity numbers.

## Step 2: write `founder/ops.md`

Start with a title and one sentence naming the source files. Then these sections, in this order, with these headings:

## 1. Nhà cung cấp

A table with the columns: what (the supply or service), supplier or "chưa chọn", quote or "chưa có báo giá", source. The source is the Owner: "anh/chị cung cấp" for a quote the Owner gave, "chưa có" where there is none. One row per kind of supply the business needs (from `idea.md`). Never invent a supplier, a quote or a price.

After the table, tell the Owner in Vietnamese: when anh/chị có báo giá thật, `founder/numbers.json` là file của `founder-cfo`. Để dùng chi phí mới, anh/chị cập nhật nó qua `founder-cfo`, rồi chạy lại `founder-pricing` và `founder-plan`. This skill writes no `numbers.json`, and does not edit `cfo.md`, `pricing.md` or `summary.md`.

## 2. Nhân sự và ca làm

The roles and the headcount from `idea.md`, as a table (role, headcount, full or part time). Then a weekly rota: one row per day the business is open, one column per shift or role group, built from the opening hours in `idea.md` and the headcount. Give the day off the business declares. The rota must be feasible: define what one shift is, make the weekly person-slots add up to no more than headcount times the maximum shifts you state, name who holds each closing and opening duty on every open day, and say plainly where a day runs below the capacity in `idea.md`. Do not state a wage; costs stay in `cfo.md`.

## 3. Quy trình mở cửa, phục vụ, đóng cửa

Three numbered lists, one each for opening, serving and closing. Every step names who does it (a role from section 2). Steps describe what happens in this business, from `idea.md`, and carry no legal figure.

## 4. Bộ công cụ tối thiểu

The minimal tool stack as generic categories, for example đặt lịch, thanh toán QR, hóa đơn điện tử, chấm công, with one line each on what it is for. Name no vendor and make no comparison and no endorsement: the Owner chooses.

## 5. Sổ rủi ro

A table of exactly ten rows with the columns: risk, early sign, what to do, who. The risks come from this business (staff, supply, equipment, customers, cash, safety, bookings). Exactly ten rows, no more, no fewer; "who" is a role from section 2.

## 6. Giấy phép và nghĩa vụ

One paragraph pointing the Owner to `founder/permits.md` and to the `founder-permits` skill for every licence, registration, tax and e-invoice obligation. Restate no legal figure, fee, threshold or deadline here (restate no legal figure at all): those live only in `permits.md`, with their sources. If `founder/permits.md` does not exist yet, say so and tell the Owner to run `founder-permits`.

## 7. Lưu ý

End with the disclaimer: "Tài liệu vận hành này dựa trên ý tưởng và số liệu của anh/chị, chưa có báo giá nhà cung cấp thật; không phải tư vấn tài chính, thuế hay pháp lý."

## Rules

- No invented supplier, quote or price: "chưa chọn" and "chưa có báo giá" are the correct values when the Owner gave none.
- Exactly seven sections in the order above; the risk register has exactly ten rows.
- `founder/numbers.json` belongs to `founder-cfo`; this skill only tells the Owner how to feed real costs back.
- No `$` next to a digit in anything the Owner reads.
