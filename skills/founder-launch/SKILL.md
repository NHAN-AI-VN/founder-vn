---
name: founder-launch
description: >-
  Write the Owner's launch file: a cheap real-world test first (a pre-sale, a waitlist with a deposit or
  a pop-up at the real price), a countdown from D-30 to opening day with an owner for each step, the
  launch-day run sheet, the first 30 days of what to measure and change, and where real buyers can
  overrule the simulated panel. Dùng khi anh/chị nói "khai trương thế nào", "khi nào mở được",
  "bán trước", "danh sách chờ", "chạy thử", "ngày khai trương".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-launch

## Protocol

1. Check the version: call the MCP tool `server_info`, or run `founder-vn --version` in the shell.
   Compare its major version with `metadata.version` of this skill. On a major mismatch, stop and
   tell the Facilitator to update the package or the skill. The stop message is in Vietnamese and
   has this shape (fill the angle-bracket placeholders):
   `Dừng ở bước 1 của Protocol: gói founder-vn <phiên bản gói> và skill <tên skill> <phiên bản skill> lệch số major; anh/chị cập nhật gói hoặc skill rồi chạy lại.`
2. Prefer MCP tools. If the MCP server is not available, run the `founder-vn` CLI through the
   shell. If neither is available, stop and print the install instructions from the README; that
   stop message is in Vietnamese too, with the install commands as the README gives them.
3. Never compute a number yourself. Every figure comes from a `founder-vn` tool or command.
4. Never answer for a buyer. Simulated buyers answer only through the panel tools.
5. Never write the verdict. The verdict comes from the tool output and is shown as given.

## Purpose

Produce `founder/launch.md`: how the Owner finds out with real buyers whether the plan holds, then opens the doors. Read `founder/idea.md` (price list, hours, stop conditions, whether the opening is decided), `founder/pricing.md` (the recommended price), `founder/cfo.md` (the break-even volume), `founder/ops.md` (roles, shifts, suppliers), `founder/permits.md`, `founder/marketing.md` and `founder/panel/results.md`. Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

**Real buyers override the panel.** The simulated panel is a cheap guess. Anything a real buyer says or pays overrules it, and the file says so and shows where the two can differ.

- Never write a calendar date. When `idea.md` says the opening is not decided, every date is relative: D-30 to D-0 before the opening day, "Ngày 1" to "Ngày 30" after it.
- Never write a real-buyer number (buyers, deposits, sales, reviews): there is none yet. The slot reads "chưa có" until the Owner supplies it.
- Never name a person. An owner of a step is a role that exists in `ops.md` (as listed in `ops.md`, for example quản lý, lễ tân, thợ, phụ tá in the barbershop), or "anh/chị" for the Owner. A role that `ops.md` does not list is not used; say the role must be hired first.
- Never invent a price, a discount, a deadline, a target or a threshold. Quote the files; where a number is the Owner's decision and the files do not hold it, write "anh/chị chọn".

## Step 1: read what exists

1. Read the files named in Purpose. If `founder/panel/results.md`, `founder/pricing.md` or `founder/ops.md` does not exist, stop and tell the Owner which skill to run first (`founder-consumer`, `founder-pricing`, `founder-ops`): the test needs a price, the countdown needs roles.
2. If `founder/launch.md` exists, show the Owner in Vietnamese what it holds and ask what to change.
3. Ask only what the files do not say, for example how many days the Owner will run the test. Do not ask for personal identity numbers.

## Step 2: write `founder/launch.md`

Start with a title and one sentence naming the source files. Then these sections, in this order, with these headings:

## 1. Thử nghiệm thật trước

Choose exactly one test for this business and say why it fits, from `idea.md`: a pre-sale of packages (the packages in `idea.md`), a waitlist with a deposit (mirror a deposit that `idea.md` already names), or a pop-up. Run it at the listed price from `idea.md` and the recommended rung of `pricing.md`, not a discount: a discounted test measures the discount. State truthfully what the result can still change: the stop rule is read at D-14, so it gates only the spending scheduled after the read; commitments in rows before it (registration, suppliers) are not gated. Either say so in the section, or tell the Owner to start the test earlier than D-30. Say who is asked, where and how the Owner records each buyer (the booking tool, a sheet), and that the Owner returns every deposit if the shop does not open. Then the stop rule, (English: "if fewer than N real buyers in M days, revisit pricing or the offer") in the form "nếu dưới N người mua thật trong M ngày thì xem lại giá hoặc đề xuất". N and M are the Owner's choice: write them as "anh/chị chọn" unless the Owner supplies them; never invent N or M, and do not derive them from the panel. Add a slot "Kết quả thật: chưa có".

## 2. Đếm ngược

A table from D-30 to D-0 relative to the opening day. Columns: mốc, việc làm, người làm, phụ thuộc vào file nào. Rows are ordered by milestone and cover at least: the real-world test (D-30), licences and registration (`permits.md`), suppliers and equipment (`ops.md`), hiring and training the roles of `ops.md`, the campaign start (`marketing.md`), the dress rehearsal, and D-0. A role that the Owner's files say must be hired and that `ops.md` does not list (for example the head barber in `idea.md`) gets a line in the hiring row saying it must be hired first and when the Owner decides. The owner of each row is a role that exists in `ops.md` (or "anh/chị"); the dependency names the file that holds the detail (`permits.md` for licences, `ops.md` for suppliers and staff, `marketing.md` for the campaign). Write no legal deadline or fee: point to `permits.md`. A row depending on a supplier quote that `ops.md` marks "chưa có báo giá" says so.

## 3. Run sheet ngày khai trương

A table hour by hour across the opening hours in `idea.md`, plus the hour or two before opening: giờ, việc làm, người làm. With one owner per line, a role from `ops.md`, drawn from the open, serve and close routines of `ops.md`. Include what is done if the first hours are quiet and if the queue is long, without any visitor target. No invented headcount of guests.

## 4. 30 ngày đầu

What to measure and what to change, as a table: số đo, nguồn của nó, ngưỡng (quoted), và việc làm khi số đo hụt. Three sources only: the stop conditions in `idea.md` (quoted with their values), the break-even volume of `cfo.md` (quoted as the CFO states it), and the metrics of `marketing.md` section 6. Each "what to change" is one lever the Owner's files already name (price or package via `founder-pricing`, the campaign message via `marketing.md`, the shifts via `ops.md`), never a new offer or discount. The stop conditions are written for the first months of operation: say which of them can already be read in the first 30 days and which need more time.

## 5. Người mua thật ghi đè panel

One paragraph. Compare the real-test result slot ("chưa có") with the panel's buy rate quoted from `panel/results.md`, with the caveat "Panel là mô phỏng, cận trên, không phải khách hàng thật; cần xác nhận với khách thật trước khi chi tiền." Show where they can differ (the panel's objections about deposit, distance, habit; a real buyer who pays a deposit counts more than a simulated one who says yes) and say that a real result below the stop rule wins over a panel result above it. Write no real-buyer figure.

## 6. Lưu ý

The disclaimer: "Kế hoạch khai trương này dựa trên ý tưởng của anh/chị và kết quả panel mô phỏng; không phải tư vấn tài chính, thuế hay pháp lý."

## Rules

- Exactly six sections in the order above; the countdown covers D-30 to D-0.
- No calendar date, no real-buyer number, no person's name; owners are roles from `ops.md`.
- The real test is at the listed price, not a discount; N and M are the Owner's.
- `founder/numbers.json` belongs to `founder-cfo`; this skill quotes and computes nothing new.
- The panel caveat appears where the panel result is quoted; no `$` next to a digit in anything the Owner reads.
