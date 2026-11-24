Commit mã đã chấm: 3cdb342f146d

# Review trục Spec, #17 founder-pricing, vòng 1

Phán quyết: PASS. SPEC-1 của vòng trước (tiêu chí 3, `pricing.md` chưa chạy trên Kiro CLI) đã được đóng bằng lượt chạy của operator. Không có finding chặn mới.

Phạm vi: `git diff --stat origin/main...HEAD` (9 file: `skills/founder-pricing/SKILL.md`, `tests/test_pricing_skill.py`, `examples/barbershop/founder/pricing.md`, `examples/barbershop/founder/pricing_input.json`, `docs/evidence/issue-17-founder-pricing.md`, và `reviews/issue-17/*`). CI `Gate` ở commit này: success.

## Đối chiếu từng criterion

1. Gọi `pricing_psm` hoặc `founder-vn pricing` trên bốn câu trả lời giá; đối chiếu `competitors.md` và `cfo.md`; cờ khi giá đề xuất dưới biên hòa vốn CFO: ĐÁP ỨNG.
   - `skills/founder-pricing/SKILL.md` Protocol 2, Step 2 (gọi `pricing_psm` / `founder-vn pricing`), Step 1.2 và 1.3 (đọc `competitors.md`, `cfo.md`, `numbers.json`), Step 3 (chạy `cfo_model --price` cho giá đề xuất và mọi bậc, cờ "giá này thấp hơn mức hòa vốn của CFO" đặt cạnh giá, không dời giá).
   - Golden `pricing.md` thực hiện đúng: 199.000 đ bị cờ (-13%, 50,8 lượt so với kế hoạch 40), cờ nằm ngay trong mục "Giá đề xuất" và bảng bậc.
   - Bằng chứng chạy được: `uv run pytest tests/test_pricing_skill.py -q` cho 13 passed ở checkout này; cổng `unit` (321 passed) nằm trong Gate đã success.
2. `pricing.md` có khoảng chấp nhận được, giá đề xuất, bậc giá, ưu đãi mở đầu để thử, theo dõi sau mở bán; không neo bịa; cảnh báo dữ liệu mỏng chuyển tiếp: ĐÁP ỨNG.
   - Đọc file thật: năm mục đúng thứ tự; số khớp đầu ra công cụ trong bằng chứng (trung vị 80.000/150.000/250.000/400.000, khoảng 120.000 đến 316.667, điểm cân bằng 199.625, 2/7 giá đối thủ trong khoảng); giá đối thủ chép từ `competitors.md` kèm ngày khảo sát 23/11/2026; Le Barbier de Saigon bị loại vì "chưa có số liệu"; ba bậc lấy từ `idea.md`, không thêm bậc; ưu đãi không đặt mức giảm mới, số khách và thời gian thử để ngỏ vì chủ hộ không cho, không bịa.
   - Nhánh `thin_data` được viết trong Step 2.3 của skill (chuyển nguyên văn, không nêu giá chắc chắn). Golden không kích hoạt nhánh này (20 câu hợp lệ); đây là phần skill-text, không có golden riêng (xem mục chưa xác minh).
   - Artefact chủ hộ: tiếng Việt, "anh/chị", tiền `199.000 đ`, `grep -c '\$'` bằng 0, caveat "mô phỏng, cận trên" đúng một lần, có miễn trừ cuối file, không khẳng định pháp lý, không có tên người hay địa điểm dưới cấp quận (chỉ tên tiệm đối thủ công khai và tên dịch vụ trong ví dụ tổng hợp).
3. Golden case chạy trên Kiro CLI, `pricing.md` trong thư mục ví dụ, checklist đạt: ĐÁP ỨNG.
   - `reviews/issue-17/operator-answer.md` và `docs/evidence/issue-17-founder-pricing.md` ("Lượt chạy golden case trên Kiro CLI") ghi: phiên 24/11/2026 05:58Z đến 06:24Z, model `claude-fable-5.1`, skill đọc theo blob `91b0d8dc7f0e`, từng bước 1 đến 5 với lệnh và số đầu ra, năm mục checklist `docs/review-checklist.md` và cách kiểm từng mục.
   - Kiểm chéo trong repo: blob của `skills/founder-pricing/SKILL.md` ở HEAD đúng là `91b0d8dc7f0e`; `pricing.md` ở HEAD là file của phiên (commit `27d3c44`, thay file do lane viết); số trong file khớp số bằng chứng cho từng bước; việc hỏi chủ hộ ở Step 4.4 và câu trả lời "để ngỏ" hiện đúng trong file; `ledger.md` có SPEC-1 FIXED, mã duy nhất của mọi vòng.
   - Bằng chứng này là bản ghi của operator chứ không phải log phiên máy đọc được; chấp nhận vì operator là người có thẩm quyền trả lời tiêu chí này, file đầu ra nhất quán với skill, và tiêu chí giữ nguyên chữ.
   - Cổng kiểm nội dung golden (năm `test_golden_*`) nằm trong `pytest` của cổng `unit`, không phải lời khẳng định.

Không có hành vi vượt phạm vi ticket: không sửa `src/`, không thêm bậc, không thêm mức giảm, không tự tính số.

## Chưa xác minh

Không thể kiểm từ sandbox này (không có Kiro CLI): bản thân phiên Kiro CLI đã xảy ra như operator ghi. Điều đã kiểm được là tính nhất quán của file đầu ra với skill và với đầu ra công cụ. Nhánh `thin_data`, truyền tải MCP, gọi skill bằng slash command sau `founder-vn install` và nhiều model/host không được golden này chứng minh; bằng chứng đã nêu thẳng các giới hạn đó, và pipeline Wave A đầy đủ thuộc T18 (#19), ngoài phạm vi ticket này.

<promise>PASS</promise>
