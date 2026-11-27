---
name: founder-permits
description: >-
  Write the Owner's static permits and tax checklist for a household business (registration,
  tax registration and declaration method, revenue tax, e-invoices) from the sources ledger
  only. Dùng khi anh/chị nói "cần giấy phép gì", "đăng ký hộ kinh doanh", "thuế hộ kinh doanh",
  "hóa đơn điện tử", "đăng ký ở đâu", "kê khai thuế".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-permits

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

Produce `founder/permits.md`: a static checklist the Owner can follow, one row per step with the step, the authority, the documents and when. It covers registering a household business, registering for tax and choosing the declaration method, and the obligations after opening (revenue tax and e-invoices), plus one line that points a conditional sector to the authority that lists them. Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; money is VND in Vietnamese format, never with a dollar sign. The business is registered at the commune-level People's Committee (UBND cấp xã).

**Never guess a number.** Every number, fee, threshold, deadline and date on the page comes from an entry of `permits/sources.md` and carries that entry's official link and verification date. A figure with no verified ledger entry is not written as a number: write "chưa có nguồn đã kiểm chứng" in its place and say plainly that it is missing. A ledger entry whose "Xác nhận" line says "chưa kiểm chứng" is not verified; treat it as missing.

## Step 1: read what exists

1. Read `founder/idea.md` for the business, the sector and the place (province or city only), and `founder/plan` files the Owner already has (`cfo.md`, `numbers.json`) for the expected yearly revenue.
2. If `founder/permits.md` exists, show the Owner in Vietnamese what it holds and ask what to change.
3. Ask only what the checklist needs and the files do not say: whether the Owner is one individual or a household, and whether the business sells goods or services. Do not ask for personal identity numbers.

## Step 2: look up the ledger

Open `permits/sources.md`. When `permits/sources.md` is absent from the project, the ledger is written by `founder-vn install --host <host>` from the installed package: run it, and do not fill the figure from memory or from a website. The entries this skill uses are:

- `household_registration`: registering a household business (authority, documents, time, how to file, what the certificate is, fee procedure).
- `tax_registration_declaration`: tax registration and the declaration method for a household business.
- `einvoice_obligation`: e-invoice obligations for a household business.
- `conditional_sectors`: the pointer for conditional sectors (law, annex, portal); no fee or condition figure.
- `tax_rate_on_revenue` and `tax_free_threshold`: the two entries `founder-cfo` already uses (Q52). Copy them as `founder-cfo` does, with the same limits in plain words.

The ledger holds no amount for the registration fee. Write it as "mức lệ phí: chưa có nguồn đã kiểm chứng; hỏi Cơ quan đăng ký kinh doanh cấp xã khi nộp" and cite only the ledger's fee procedure (when and where the fee is paid, not refunded when refused).

For each entry, copy the value, the legal document and article, the Công báo link and the "Xác nhận" line exactly as the ledger writes them. If an entry is absent, has no link, or has no verified "Xác nhận" line, the figure is "chưa có nguồn đã kiểm chứng": write that, name what is missing, and do not fill it from memory or from a website.

## Step 3: re-check at run time

For each source link you will cite, try to fetch it again. The Công báo search page loads by script, so use the endpoint it calls: `POST https://api-searchcongbao.chinhphu.vn/search/all` with the body `{"filters":{},"page":1,"page_size":10,"query":"<số ký hiệu>"}`. The JSON answer has `id_van_ban`, which builds the page address `/van-ban/<slug>-<id>.htm`, and the PDF link. Send a browser-like `User-Agent`. Then compare the PDF text with the ledger excerpt. When the fetch works and agrees, say so. When the fetch fails or the page differs, use the ledger copy and write "kiểm chứng ngày X, chưa xác nhận lại hôm nay" next to the figure, with X the verification date of the entry. Never drop a figure because the fetch failed, and never replace it with a figure from an unofficial site (a law firm, an accountant's blog, a news article). If the page differs from the ledger, keep the ledger figure, say the source may have changed and tell the Owner to open an issue "Law changed".

## Step 4: write `founder/permits.md`

Write these six parts in this order, with these headings. Tables use the columns "Bước", "Cơ quan", "Hồ sơ", "Khi nào" (step, authority, documents, when).

## 1. Đăng ký hộ kinh doanh

One table row per step: where (UBND cấp xã), the documents, how long it takes and the fee, each taken from `household_registration` with its link and date, or "chưa có nguồn đã kiểm chứng".

## 2. Đăng ký thuế và cách kê khai

The tax registration step and the declaration method for a household business, from `tax_registration_declaration`, as the same kind of table.

## 3. Sau khi mở cửa

- Thuế theo doanh thu: the rate from `tax_rate_on_revenue` and the threshold from `tax_free_threshold`, with the limits of the combined model in plain words as `founder-cfo` states them (Q52), each with link and date.
- Hóa đơn điện tử: what a household business must do, from `einvoice_obligation`.

## 4. Ngành có điều kiện

Exactly one line: "ngành có điều kiện: tra tại đây" followed by the Công báo link of Luật Đầu tư 143/2025/QH15 (https://congbao.chinhphu.vn/van-ban/luat-so-143-2025-qh15-468703.htm, Phụ lục IV lists the conditional sectors) and the name of the authority that publishes their conditions, Cổng thông tin quốc gia về đăng ký doanh nghiệp (www.dangkykinhdoanh.gov.vn), with the verification date of `conditional_sectors`. Give no fee or figure for those sectors.

## 5. Nguồn và ngày kiểm chứng

A list of every figure on the page with its document, article, Công báo link and verification date, copied from the ledger, and for each whether the run-time re-check worked.

## 6. Lưu ý và khi nào hỏi kế toán

The disclaimer and the accountant line, copied as in Rules below, plus the list of figures marked "chưa có nguồn đã kiểm chứng", if any.

## The F&B path

This skill builds the common path only. The F&B path (chứng nhận an toàn thực phẩm and the F&B tax rates) is deferred by Q56 until a pilot F&B owner agrees; say in one sentence that these two are not in this checklist. Do not write them from memory.

## Rules

- Never guess a number. A figure without a verified ledger entry is written as "chưa có nguồn đã kiểm chứng" and named as such.
- Every legal figure comes from `permits/sources.md` with its link and date; never from memory and never from an unofficial site.
- No `$` next to a digit in anything the Owner reads.
- Do not compute tax; the amounts come from `founder-cfo`.
- End `founder/permits.md` and your reply with: "Đây là danh sách tham khảo từ các văn bản đã dẫn, không phải tư vấn pháp lý hay thuế. Anh/chị nên hỏi kế toán hoặc cán bộ UBND cấp xã khi hồ sơ của anh/chị khác trường hợp thông thường, khi doanh thu gần ngưỡng, hoặc khi luật vừa đổi."
