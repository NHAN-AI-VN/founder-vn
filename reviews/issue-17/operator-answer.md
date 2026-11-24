# Trả lời của operator — review #17, vòng 1

Trả lời cho `reviews/issue-17/spec.md` (BLOCKED, commit mã đã chấm `1b8ce2d0e526`), finding SPEC-1 và câu hỏi "cho operator" trong đó. File này không phải báo cáo review; nó là đầu vào cho vòng review kế. Lượt Standards vòng 1 đã PASS ở cùng commit mã.

## Câu hỏi: giữ "run on Kiro CLI" (operator chạy) hay chấp nhận lượt chạy bằng CLI gói và sửa lời tiêu chí như #16

- [x] **Giữ nguyên tiêu chí 3. Operator đã chạy skill trên Kiro CLI** ngày 24/11/2026 (05:58Z đến 06:24Z) tại máy mình, model `claude-fable-5.1`, project `examples/barbershop/`, operator đóng vai chủ hộ; `pricing.md` của phiên ấy thay file do agent lane viết (commit `27d3c44`, message giải thích vì sao golden đổi). Lượt chạy ghi ở `docs/evidence/issue-17-founder-pricing.md`, mục "Lượt chạy golden case trên Kiro CLI (tiêu chí 3)".
- [ ] ~~Chấp nhận lượt chạy bằng CLI gói và sửa lời tiêu chí 3 như #16.~~ Không chọn: khác #16 (nơi phần "model trả lời" đã chạy thật trên model tham chiếu và nằm trong `panel/`), ở #17 chưa có gì chạy ngoài hai lệnh CLI, nên phần tiêu chí 3 muốn chứng minh (một phiên làm theo skill: đọc bốn câu trả lời, đặt cờ hòa vốn, hỏi chủ hộ chỗ thiếu số, không bịa bậc) chưa có bằng chứng nào. Tiêu chí giữ nguyên chữ; không sửa thân ticket.

## SPEC-1: tiêu chí 3 chưa có phiên Kiro CLI

Đóng bằng lượt chạy trong bằng chứng. Tóm tắt điều phiên đã làm theo `skills/founder-pricing/SKILL.md` (blob `91b0d8dc7f0e`):

- Protocol: `founder-vn --version` cho 0.1.0, khớp `metadata.version`; máy không có MCP server `founder-vn` nên mọi tool chạy bằng CLI qua shell (Protocol 2); phiên không tự tính số nào.
- Step 1: đọc `founder/panel/pricing_input.json` (20 câu), `founder/competitors.md` (bảy giá một lần cắt chép nguyên, Le Barbier de Saigon "chưa có số liệu" bị loại và nói rõ), `founder/cfo.md` và `founder/numbers.json`, `founder/idea.md` (ba bậc 199.000 / 279.000 / 389.000 đ; hai dịch vụ 139.000 và 129.000 đ không phải một lần cắt nên không xếp bậc).
- Step 2: `founder/pricing_input.json` tái tạo, `diff` với file của lane: giống hệt; `founder-vn pricing pricing_input.json --json`: 20 hợp lệ, 0 loại, không `thin_data`, 120.000 / 199.625 / 316.667 đ, 2 trên 7 giá đối thủ trong khoảng.
- Step 3: `founder-vn cfo numbers.json --price` ở 199.000 (-13%, 50,8 lượt), 279.000 (19%, 27,63), 389.000 (42%, 16,98) và 280.000 đ (20%, 27,48; giá của CFO cho Step 3.3). Chỉ 199.000 đ dưới hòa vốn; cờ đặt ngay cạnh giá đề xuất, giá không bị dời.
- Step 4: phiên viết `pricing.md` năm mục đúng thứ tự; Step 4.4 hỏi chủ hộ số khách và thời gian thử (không có trong file của chủ hộ), chủ hộ trả lời "để ngỏ", file ghi là chưa đặt số. Step 5: đọc lại năm dòng cho chủ hộ trong phiên.
- Kiểm: `tests/test_pricing_skill.py` 13 passed trên file mới (năm `test_golden_*` là cổng trên nội dung: thứ tự mục, số bằng đầu ra công cụ, giá đối thủ từ `competitors.md`, cờ hòa vốn đúng một lần ở 199.000 đ, caveat một lần, miễn trừ, không `$`); `skill_lint.py` 0 finding; checklist `docs/review-checklist.md` năm mục, cách kiểm từng mục ghi trong bằng chứng. Cổng ba đoạn chạy lại ở `27d3c44`: `verify` GREEN (static, unit 321 passed, build).

Giới hạn của lượt chạy, ghi trong bằng chứng: một phiên, một host, một model; skill đọc bằng đường dẫn chứ không qua slash command sau `founder-vn install`; nhánh `thin_data` không xảy ra (20 câu hợp lệ); MCP không chạy. Pipeline đầy đủ Wave A từ cài mới vẫn thuộc T18 (#19).

## Ledger

`reviews/issue-17/ledger.md` được ghi trong cùng commit này: SPEC-1 là mã finding duy nhất của mọi vòng tới nay, đóng bằng commit của operator chứ không bằng lượt sửa, và merger đòi ledger cho mọi mã từng được nêu (FV-D18). Lượt sửa, nếu có vòng sau, ghi lại toàn bộ file với đủ mã của mọi vòng.
