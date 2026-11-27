---
name: founder-cfo
description: >-
  Turn the Owner's costs, price and plan into unit economics, break-even, year-1 cash and a
  revenue-tax estimate, using only the founder-vn tool. Dùng khi anh/chị nói "kinh tế đơn vị",
  "hòa vốn", "cần bao nhiêu vốn", "tính lãi lỗ", "có nên mở".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-cfo

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

Produce `founder/cfo.md` (the report) from `founder/numbers.json` (the inputs), so the Owner sees whether the business covers its costs, when it breaks even and how much cash it needs. Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign. This skill never computes: it gathers inputs, calls the tool and explains the output.

## Step 1: read what exists

1. Read `founder/idea.md` for the business, the unit sold (a haircut, a cup, a ticket), the price, the capacity and the sector.
2. If `founder/numbers.json` exists, show the Owner in Vietnamese what it holds and ask which parts to change. Otherwise build it in Step 2.

## Step 2: ask for the costs in the Owner's terms

Ask in Vietnamese, in the words a shop owner uses, one group at a time. Do not ask for "variable cost" or "fixed cost". Map the answers yourself:

- Per unit sold (`variable`): nguyên liệu (hair product, coffee, goods), bao bì (cup, lid, bag, towel and laundry), phí app giao hàng and phí thanh toán, hoa hồng thợ or staff commission per unit.
- Every month (`fixed_monthly`): thuê mặt bằng, lương (base pay, assistants, receptionist, manager), điện nước, phần mềm and internet, insurance and maintenance.
- One time before opening (`startup`): đặt cọc mặt bằng, nội thất, thiết bị, khai trương, vốn lưu động.
- Also: the selling price the customer pays (`price`), `days_per_month`, `capacity_per_day`, `plan_per_day` and `ramp_per_day` (12 numbers, units per day for months 1 to 12).

Accept Vietnamese number forms the Owner types (`35k`, `1,2 triệu`, `35.000`). If the Owner knows a cost only as a percentage, ask for the amount in đồng per unit at the planned price; do not convert it yourself. A figure the Owner does not know stays a question, never a guess. Cost items the Owner names that no tool field covers (for example the landlord's house-rent tax) are listed back as "chưa tính", not estimated.

## Step 3: look up the two legal figures

`numbers.json` needs `tax_rate_on_revenue` (percent, VAT plus personal income tax for the sector) and `tax_free_threshold` (annual revenue in đồng). They are never typed from memory and never taken from this file.

1. Open `permits/sources.md` and find the entry for each key and the Owner's sector. The entry must carry an official link and a verification date. When `permits/sources.md` is absent from the project, the ledger is written by `founder-vn install --host <host>` from the installed package: run it, and do not fill the figure from memory or from a website.
2. Use the value the entry gives. Tell the Owner in Vietnamese the value, the legal document, the link and the verification date.
3. If there is no entry for the sector, or the entry has no link or no verification date, do not write a rate. Ask the Owner for the figure and its official source, mark it "chưa kiểm chứng" in your reply, and say that the number is the Owner's input, not a checked legal figure.

Then write `founder/numbers.json` with the Owner's inputs and these two values. Every numeric field is required.

## Step 4: run the tool

1. MCP: call `cfo_analyse` with `numbers` = `founder/numbers.json` and `out` = `cfo.md`. CLI: run `founder-vn cfo founder/numbers.json --out cfo.md`.
2. For what-if questions, call it again with `price` (for example `40k`) or `volume` (a multiplier) and show the table the tool prints. Do not edit the numbers file to explore.
3. If the tool answers with an error naming a missing field, ask the Owner for that field and rerun.

## Step 5: read the result back in plain Vietnamese

Read `founder/cfo.md` and explain it to the Owner in plain Vietnamese, in a few short paragraphs: the contribution of one unit, the break-even per day against the plan and the capacity, year-1 profit after tax, the payback month and the cash needed. Quote every figure exactly as the tool printed it. Then go through the flags (the "Cảnh báo" section, `flags` in JSON) one by one, say what each means for the decision in everyday words and what the Owner can change (price, volume, a cost line). If there are no flags, say so and still remind the Owner to check each cost against a real quote. Do not give a verdict; the verdict comes from the tool output only.

## Step 6: append the limits of the tax model, with their sources

After the tool has written `founder/cfo.md`, append the section below to the end of the file. The tool does not write it: it records Q52 of the design, and it corrects the tool's "Lưu ý" paragraph, which calls the rate and the threshold the Owner's own input. The Owner reads `cfo.md` and does not open `permits/sources.md`, so every legal figure in this section must carry its document, its link and its verification date inside `cfo.md`.

Keep the fixed lines unchanged. Fill each `<...>` slot by copying from the two ledger entries you opened in Step 3, never from memory: the value line, the "Căn cứ" and "Link" lines with their Công báo number and date exactly as the entry writes them, the "Sai lệch của cách gộp" line of the rate entry (it names the documents behind the two limits), and the "Xác nhận" line of each entry. If an entry has no link or no "Xác nhận" line, the figure is not usable (Step 3, point 3): do not append a source you cannot copy.

```markdown
## Giới hạn của phần thuế

- Đính chính mục "Lưu ý" ở trên: thuế suất <giá trị của mục tax_rate_on_revenue>% và ngưỡng miễn thuế <giá trị của mục tax_free_threshold> không phải số anh/chị nhập; skill lấy hai số này từ sổ nguồn `permits/sources.md`, căn cứ và link ghi ở cuối mục này.
- Mô hình áp một tỷ lệ gộp (GTGT cộng TNCN) lên toàn bộ doanh thu năm khi doanh thu năm vượt ngưỡng. Luật chỉ tính TNCN trên phần doanh thu vượt ngưỡng, nên mô hình có thể tính thừa tối đa 20 triệu đồng mỗi năm. Sai lệch này theo hướng an toàn: thuế cao hơn, lợi nhuận thấp hơn thực tế.
- Trên 3 tỷ đồng doanh thu năm, cách tính thuế theo tỷ lệ phần trăm trên doanh thu không còn áp dụng: TNCN tính trên thu nhập (doanh thu trừ chi phí) với thuế suất 17%. Công cụ chưa có cờ cho mốc này, nên nếu kế hoạch của anh/chị gần hoặc vượt 3 tỷ đồng một năm thì phần thuế ở trên chỉ là ước lượng thô.
- Ưu đãi thuế: có ưu đãi tạm thời, chưa tính.
- Căn cứ của thuế suất, chép từ mục `tax_rate_on_revenue` của sổ nguồn:
  - <từng dòng căn cứ và link của mục ấy, nguyên văn, mỗi dòng một gạch đầu dòng>
  - <dòng "Sai lệch của cách gộp" của mục ấy, nguyên văn>
- Căn cứ của ngưỡng, chép từ mục `tax_free_threshold` của sổ nguồn:
  - <dòng "Căn cứ" của mục ấy, nguyên văn>
  - <dòng "Link" của mục ấy, nguyên văn>
- Kiểm chứng: <dòng "Xác nhận" của hai mục, nguyên văn>.
- Kết quả này không phải tư vấn tài chính hay thuế.
```

When you read the result back, state these limits in plain words too. Add no figure to the "có ưu đãi tạm thời, chưa tính" line.

## Rules

- Never compute a number: no sums, percentages or conversions of your own. If a figure is missing, rerun the tool.
- Every legal figure comes from `permits/sources.md` with its link and date; never from memory.
- No `$` next to a digit in anything the Owner reads.
- End your reply to the Owner with: "Đây là mô hình tính toán từ các con số anh/chị cung cấp, không phải tư vấn tài chính hay thuế."
