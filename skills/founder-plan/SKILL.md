---
name: founder-plan
description: >-
  Write the Vietnamese executive summary and a one-page partner version, compile every founder
  file into business-plan.md with a computed verdict, and explain what to fix. Dùng khi anh/chị nói
  "kế hoạch kinh doanh", "tổng hợp kế hoạch", "tóm tắt cho đối tác", "có nên mở không", "gọi vốn".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-plan

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

Hand the Owner `founder/business-plan.md` with a verdict the tool computed, and `founder/summary.md`, a Vietnamese summary the Owner can show a partner or a lender. You read, quote and explain; the package compiles (`plan_compile`; CLI: `founder-vn plan`). Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

## Step 1: read what exists

1. Read `founder/idea.md`, then every file the plan is compiled from that exists: `board.md`, `competitors.md`, `panel/results.md`, `consumer.md`, `pricing.md`, `offer.md`, `cfo.md`, `permits.md`, `marketing.md`, `brand.md`, `ops.md`, `launch.md`.
2. Run `plan_compile` with `check` set (CLI: `founder-vn plan --check`) to see whether `business-plan.md` exists. Exit code 1 means it is missing or stale; that is not an error, Step 3 rewrites it.
3. If `founder/numbers.json` does not exist, tell the Owner in Vietnamese to run `founder-cfo` first. The verdict is `Incomplete` without the numbers; you may still go on, but the summary says in its first line that the numbers are missing.
4. A section that is missing from the plan (listed under "Chưa làm") maps to the skill that writes it:

   | Mục thiếu | Skill viết mục đó |
   | --- | --- |
   | Hội đồng cố vấn | `founder-board` |
   | Đối thủ | `founder-competitors` |
   | Khách hàng (panel mô phỏng) | `founder-consumer` |
   | Giá | `founder-pricing` |
   | Đề xuất giá trị | để sau pilot, chưa có trong bản này |
   | Kinh tế đơn vị | `founder-cfo` |
   | Giấy phép và thuế | `founder-permits` |
   | Tiếp thị | `founder-marketing` |
   | Thương hiệu | để sau pilot, chưa có trong bản này |
   | Vận hành | `founder-ops` |
   | Khai trương | `founder-launch` |

If the Owner asks for the offer or brand section, say in Vietnamese that those two skills come after the pilot and are not in this version, and do not fetch, translate or improvise a skill from anywhere else (an earlier session fetched the English upstream skills); a plan section the Owner supplies by hand is compiled with the marker "chưa qua rà soát của founder-vn".

## Step 2: compile the plan

1. MCP: call `plan_compile` (without `check`). CLI: run `founder-vn plan` from the project root. The tool writes `founder/business-plan.md` and prints the verdict line.
2. Do this before writing the summary, so every figure in the summary can be read from the compiled plan. If any founder file changes later, run it again.
3. Never write the verdict, never edit `founder/business-plan.md` by hand and never copy a verdict from an earlier run: the tool output is the only source. After the summary is written, run `plan_compile` with `check` (CLI: `founder-vn plan --check`) and expect exit code 0.

## Step 3: explain each failing check

Open the "Kết luận" table of `founder/business-plan.md`. Each row says "Đạt" or "Không đạt". For every row that says "Không đạt", tell the Owner in plain Vietnamese, in the Owner's words and with the figure the tool printed in the "Số chính" table, what it means and which skill fixes it:

| Kiểm tra | Nghĩa là gì với anh/chị | Skill sửa |
| --- | --- | --- |
| Đóng góp mỗi (đơn vị bán) lớn hơn 0 | Mỗi lượt bán ra còn lại tiền để trả chi phí cố định hay không. Không đạt: giá thấp hơn chi phí mỗi lượt. | `founder-pricing` để thử giá khác, rồi `founder-cfo` để tính lại chi phí mỗi lượt |
| Lợi nhuận hoạt động năm 1 sau thuế lớn hơn 0 | Năm đầu, sau chi phí cố định và thuế doanh thu, còn lãi hay không. Không đạt: năm 1 lỗ. | `founder-cfo` (thử kịch bản giá, sản lượng, chi phí), `founder-pricing` |
| Hòa vốn không vượt công suất | Số lượt mỗi ngày để hòa vốn có nằm trong sức phục vụ của tiệm hay không. Không đạt: tiệm không bao giờ đủ chỗ để hòa vốn. | `founder-cfo` (công suất, chi phí cố định), `founder-board` (cân nhắc lại quy mô và mặt bằng) |

If all three say "Đạt", say so and still remind the Owner that the verdict only covers the numbers they gave. The panel line is a demand signal, not an input of the verdict; say so if the Owner asks why a good panel result did not change the verdict. If the verdict is `Incomplete`, name the missing file from the plan's "Chưa làm" list and the skill that writes it.

## Step 4: write `founder/summary.md`

Write it in Vietnamese with these two parts, in this order. Quote every figure exactly as it appears in `founder/business-plan.md` or the files it is compiled from; compute nothing, round nothing, make up no benchmark.

1. **Tóm tắt điều hành**: what the business is and for whom (from `idea.md`), the verdict line exactly as the tool printed it, the key numbers (price, contribution per unit, break-even per day against the plan and the capacity, year-1 revenue and profit after tax, starting capital and the cash needed), what the panel signal says with its caveat (quote the Owner-facing reading from `consumer.md` when it exists; `plan_compile` keeps reading `panel/results.md` for the plan's own panel section, so the figures match), the two or three main risks from the flags in `cfo.md` and from `board.md`, and what to do next with the fixing skill named for each failing check.
2. **Bản một trang cho đối tác hoặc bên cho vay**: at most one page: the business in two sentences, the ask (the cash needed, as the tool printed it), the unit economics in three lines, the verdict as printed, the main risk, and the next test with real customers. The page must stand on its own, and must carry the same caveat and disclaimer as part 1.

Legal and numeric claims in the summary (tax rate, tax-free threshold, competitor prices, panel result) are copied with their link and verification date from the file that holds them (`cfo.md`, `competitors.md`, `panel/results.md`), or from `permits/sources.md`; never from memory. When `permits/sources.md` is absent from the project, the ledger is written by `founder-vn install --host <host>` from the installed package: run it, and do not fill the figure from memory or from a website. If a claim has no link and no date in those files, leave it out and say so.

Close `summary.md` with the caveat once: "Panel là mô phỏng, cận trên, không phải khách hàng thật." (the full form is "mô phỏng, cận trên, không phải khách hàng thật"). Then the disclaimer: "Kết quả này không phải tư vấn tài chính, thuế hay pháp lý."

## Step 5: tell the Owner

In Vietnamese, in five lines: the verdict as the tool printed it, which checks failed (if any) and the skill for each, the one number that matters most, what the panel does and does not tell, and the first thing to do next. Name the two outputs: `founder/business-plan.md` and `founder/summary.md`.

## Rules

- The verdict is computed by `plan_compile`; this skill never writes, edits or restates it differently.
- Every figure comes from a tool output or an Owner file; none is made up or computed by hand.
- Every legal figure comes from `permits/sources.md` or a file that already carries its link and date; never from memory.
- No `$` next to a digit in anything the Owner reads.
- End your reply to the Owner with: "Đây là bản tổng hợp từ các con số anh/chị cung cấp, không phải tư vấn tài chính, thuế hay pháp lý."
