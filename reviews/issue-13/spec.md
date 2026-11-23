Commit mã đã chấm: 4981e1d420d3

# Review trục Spec, issue #13, vòng 3

**Phán quyết**: PASS. Cả bốn criterion được đáp ứng bằng file thật trong diff `main...HEAD`. Ba finding vòng 2 (SPEC-1, SPEC-2, SPEC-3) đã được chữa.

Phạm vi: `git log --oneline main..HEAD` (11 commit) và `git diff --stat main...HEAD`. Cổng `Gate` ở `4981e1d420d3`: success (run 45149812237, theo tin nhắn giao việc).

## Đối chiếu từng criterion

1. **Phiếu in được, tiếng Việt, đủ trường** (tên, địa chỉ, giá, lượng khách giờ cao điểm, ảnh menu, phàn nàn, khoảng cách tới vị trí dự kiến): ĐÃ ĐÁP ỨNG. Đọc `skills/founder-competitors/survey-form.md`: mục 1 tên, 2 địa chỉ, 3 khoảng cách, 4 bảng giá, 5 đếm khách 15 phút giờ cao điểm, 6 ảnh menu, 7 phàn nàn, 8 điểm và số lượt đánh giá theo kênh (Google Maps, Facebook, ShopeeFood, GrabFood). Xưng "anh/chị", có câu miễn trừ. Bằng chứng chạy: `tests/test_competitors_skill.py` (13 passed khi chạy lại ở HEAD, nằm trong bước `unit` của cổng).
2. **Skill đòi phiếu đã điền trước khi phân tích; kết quả web đánh dấu bổ trợ và có link; không bịa**: ĐÃ ĐÁP ỨNG. `skills/founder-competitors/SKILL.md` Bước 1 mục 3 (không có phiếu thì in phiếu rồi dừng, không tra web, không đoán đối thủ), Bước 3 (không bịa, ô trống là "chưa có số liệu"), mục 4 "Bổ trợ từ web" (đánh dấu, link, ngày truy cập, không lẫn vào bảng) và mục Rules. Có test đọc văn bản skill. Giới hạn: các test kiểm văn bản chỉ dẫn, không kiểm hành vi mô hình; evidence nêu rõ giới hạn này.
3. **Đầu ra: bảng 5–10 đối thủ, chủ đề đánh giá có trích dẫn khi có, bản đồ định vị, khoảng trống, cảnh báo dữ liệu mỏng dưới 3 lượt**: ĐÃ ĐÁP ỨNG. `SKILL.md` Bước 3 nêu đủ sáu mục; `examples/barbershop/founder/competitors.md` có đủ sáu mục. Ô số lượt đánh giá để trống xử lý là "chưa có số liệu", không phải cảnh báo dữ liệu mỏng (đúng chữ criterion: cảnh báo khi một đối thủ có dưới ba lượt; phiếu không có số nào dưới 3, nhỏ nhất là 67).
4. **Golden case trên `examples/barbershop/founder/survey-form.md`**: ĐÃ ĐÁP ỨNG.
   - `competitors.md` có trong thư mục ví dụ, 8 đối thủ (trong khoảng 5–10).
   - Dòng "Cách khảo sát" chép nguyên văn từ phiếu lên đầu file (khảo sát bàn giấy từ nguồn công khai, ngày 23/11/2026, chưa đến tận nơi). Cột nguồn của cả 8 hàng ghi "khảo sát bàn giấy từ nguồn công khai, ngày 23/11/2026" kèm link; `grep` không thấy "khảo sát thực địa" làm nguồn. Câu miễn trừ cuối dùng bản dành cho khảo sát bàn giấy.
   - Số liệu khớp phiếu: 6 cặp điểm và số lượt (4,4/92; 4,4/556; 4,3/405; 4,4/284; 4,7/196; 4,1/67) đối chiếu với `survey-form.md`; 7 link trong `competitors.md` đều có trong phiếu (kiểm bằng script). Không có trích dẫn khách bịa: mục 2 ghi "chưa có trích dẫn", câu Vietcetera được gán rõ là lời của bài báo. Mục 4 nêu không tra web thêm. Không có `$`. Địa chỉ dừng ở cấp quận cũ.
   - Mẫu nhỏ và bàn giấy được nói rõ ở bản đồ định vị và khoảng trống, đúng yêu cầu của `SKILL.md`.
   - Evidence `docs/evidence/issue-13-founder-competitors.md` nêu giới hạn: không có Kiro CLI trong sandbox, lượt chạy là của chính agent, đầu vào là phiếu bàn giấy, checklist đã chấm từng dòng với `competitors.md`, lệnh đã chạy và kết quả (skill-lint 0 finding, 238 passed), cổng chạy ở commit mã cuối `49a103f`. Các commit sau chỉ đụng `reviews/` và `docs/evidence/`.
   - Test `test_golden_competitors_follows_the_skill_on_the_desk_survey_form` đọc file thật và nằm trong `pytest` của cổng `unit`.

## Chữa finding vòng 2

- SPEC-1: `examples/barbershop/founder/competitors.md` đã có (`49a103f`).
- SPEC-2: `SKILL.md` có Bước 2 đọc và chép lời khai phương pháp, đặt cột nguồn và câu miễn trừ theo phương pháp, ô trống không phải dữ liệu mỏng (`f26e526`), kèm bốn test.
- SPEC-3: evidence đã viết lại mục Giới hạn và Giải quyết review nội bộ, tham chiếu `49a103f`.

## Chưa xác minh (không gắn mã)

- Không chạy lại skill trên một mô hình khác; ticket cho phép lượt chạy của chính agent và evidence đã nêu giới hạn.
- Link trong `competitors.md` chép từ phiếu, chưa kiểm còn sống (evidence cũng nói vậy).
- Lệch số trong phiếu ("3 giờ 15 phút" so với 19:45 và 21:00 là 1 giờ 15 phút) được `competitors.md` giữ nguyên và báo chủ hộ xác nhận; đây là cách xử lý đúng, không phải finding.
- Mục "chuẩn mã, tên, tổ chức" thuộc trục Standards, không xét ở đây.

<promise>PASS</promise>
