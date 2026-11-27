---
name: founder-competitors
description: >-
  Print a field-survey form for the Owner, then turn the filled form into a competitor table, review
  themes, a positioning map and the gap to own. Dùng khi anh/chị nói "phân tích đối thủ", "khảo sát đối
  thủ", "đối thủ quanh đây", "khoảng trống thị trường".
license: MIT
metadata:
  version: "0.3.0"
  author: founder-vn author
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---

# founder-competitors

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

Map the competitors around the planned location from the Owner's own survey (a field survey on foot, or a desk survey from public sources, as the form declares), and find the gap the business can own. The filled survey form is the primary input; web search only supplements it (design §3). Write the result to `founder/competitors.md`. Everything the Owner reads is Vietnamese and addresses the Owner as "anh/chị"; amounts are VND in Vietnamese format (`35.000 đ`), never with a dollar sign.

## Step 1: the survey form

1. Read `founder/idea.md` for the business and the planned location.
2. Look for the filled survey form in `founder/` (the Owner's filled copy of `survey-form.md`, a file or pasted text).
3. If there is no filled form, print the full text of `survey-form.md` (shipped next to this file) so the Owner can print it and carry it on foot. Tell the Owner in Vietnamese to fill one sheet per competitor, 5 to 10 competitors, and to come back with the filled form. Then stop. Do not analyse, do not search the web, do not guess competitors from the idea. The reply when there is no filled form is the form and the stop message, nothing else.
4. If the form is filled but covers fewer than 5 competitors, say so, ask whether the Owner can survey more, and continue with what exists only if the Owner confirms.

## Step 2: read the survey method

Read the survey-method declaration in the filled form (the line "Cách khảo sát") before anything else. Copy it verbatim into the top of `founder/competitors.md`, above the first section. Then set the source column of the table by the real method:

- Field survey (the Owner went on foot): the source is `khảo sát thực địa`.
- Desk survey from public sources: the source is `khảo sát bàn giấy từ nguồn công khai, ngày <ngày>` plus the link the form gives for that competitor. Never write `khảo sát thực địa` for a desk survey.

If the form does not declare a method, ask the Owner which one it is and stop until answered.

## Step 3: analyse the filled form

Use only what the form and the web results contain. Never invent a competitor, a price, a review count, a quote, a distance or a traffic count. A blank cell stays blank and is shown as "chưa có số liệu". Never round or correct an Owner's figure; if two figures disagree, show both and ask.

Write `founder/competitors.md` in Vietnamese with these sections:

1. **Bảng đối thủ**: a table of 5 to 10 competitors, one row each: name, address, distance, price range, peak-hour traffic, menu photo (yes or no), visible complaints, source (set by the survey method of Step 2). Do not add a competitor that is not in the filled form to this table.
2. **Chủ đề đánh giá**: the review themes per competitor, from Google Maps, Facebook, ShopeeFood and GrabFood. Quote customers verbatim with channel and link when the Owner pasted them or the search returned them; where there are no quotes, write "chưa có trích dẫn". Group the themes (price, wait time, service, hygiene, space), and count only reviews that exist.
3. **Dữ liệu mỏng**: for every competitor with fewer than three reviews on a channel, print the warning "Dữ liệu mỏng: chỉ có N lượt đánh giá, chưa đủ để rút ra chủ đề" (N is the number on the form) and draw no theme from that channel. The warning applies only when the form gives a number below 3, including a 0 written explicitly. An empty review-count cell is not a number: show "chưa có số liệu" for it, never the thin-data warning.
4. **Bổ trợ từ web**: the supplementary results. Search the web only after the table exists, for facts the form lacks (opening hours, extra menu prices, reviews). Every web result is marked "bổ trợ từ web" with its link and the date of access. A competitor found only on the web goes in this section, not in the table, and is marked as not surveyed. If search is unavailable, write that and go on.
5. **Bản đồ định vị**: a positioning map as a text grid or table of the competitors on two axes chosen from the data (for example price level and service level, or price and distance). Say which axes and why. Place a competitor only where the form's figures support it.
6. **Khoảng trống**: the gap, in a few sentences: the position no surveyed competitor holds, which survey figures or complaints support it, and what the Owner's idea would have to deliver to own it. Say plainly how many competitors support the claim and that it comes from a small sample; when the form declares a desk survey, the positioning map and the gap must also say that the method is a desk survey from public sources, not a field survey.

End with the disclaimer, which varies by method. Field survey: "Phân tích này dựa trên khảo sát thực địa của anh/chị và một lượt tra web bổ trợ, không phải tư vấn tài chính, thuế hay pháp lý." Desk survey: "Phân tích này dựa trên khảo sát bàn giấy từ nguồn công khai (chưa đến tận nơi) và một lượt tra web bổ trợ nếu có, không phải tư vấn tài chính, thuế hay pháp lý."

## Rules

- The filled form is required before any analysis, and its survey-method declaration is copied into the output.
- Web results are supplementary, linked, dated, and never mixed into the surveyed table.
- No fabricated competitors or numbers. When data is missing, say so.
- No `$` next to a digit in anything the Owner reads.
