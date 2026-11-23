Commit mã đã chấm: cada7bc77114

# Review trục Spec, issue #13, vòng 2

Phạm vi: `git diff --stat main...HEAD` (5 file: `skills/founder-competitors/SKILL.md`, `skills/founder-competitors/survey-form.md`, `examples/barbershop/founder/survey-form.md`, `tests/test_competitors_skill.py`, `docs/evidence/issue-13-founder-competitors.md`) và `git log --oneline main..HEAD` (5 commit). Gate ở `cada7bc77114`: success (theo tin nhắn mở đầu). Không chạy lại gì khác; đã đọc từng file thật trong diff.

**Phán quyết: CHANGES_REQUESTED**

## Đối chiếu từng criterion

1. **Phiếu in được, tiếng Việt, 6 trường**: ĐÃ ĐÁP ỨNG. `skills/founder-competitors/survey-form.md` có tên và địa chỉ, giá, lượng khách giờ cao điểm (đếm 15 phút), ảnh menu, phàn nàn, khoảng cách, thêm bảng số lượt đánh giá; xưng "anh/chị", không `$`. Bằng chứng: đọc file và `test_form_has_the_six_required_fields_in_vietnamese` (chạy trong `pytest` của cổng unit, 233 passed ở `c50706a`).
2. **Bắt buộc có phiếu đã điền, web là bổ trợ có link, không bịa**: ĐÃ ĐÁP ỨNG ở mức văn bản chỉ dẫn. `SKILL.md` Bước 1 dừng khi chưa có phiếu; mục "Bổ trợ từ web" bắt đánh dấu, link, ngày truy cập; quy tắc không bịa. Các test chỉ kiểm chuỗi trong văn bản (đã nói rõ trong evidence); hành vi thật của agent chỉ có thể chứng minh qua criterion 4.
3. **Đầu ra: bảng 5–10 đối thủ, chủ đề đánh giá có trích dẫn, bản đồ định vị, khoảng trống, cảnh báo dữ liệu mỏng khi dưới 3 lượt**: ĐÃ ĐÁP ỨNG trong `SKILL.md` (sáu mục). Chưa có đầu ra thật nào để đối chiếu (xem SPEC-1).
4. **Golden case: `examples/barbershop/founder/competitors.md`, khai báo khảo sát bàn giấy, cột nguồn không ghi "khảo sát thực địa", checklist đạt, nêu giới hạn Kiro CLI**: CHƯA ĐÁP ỨNG. Xem SPEC-1, SPEC-2, SPEC-3.

## Finding chặn

### SPEC-1: thiếu `examples/barbershop/founder/competitors.md` (criterion 4)

`ls examples/barbershop/founder/` chỉ có `idea.md` và `survey-form.md`. Không có `competitors.md`, nên không có lượt chạy golden case nào và không có checklist nào được chấm trên đầu ra thật. Điều kiện chặn mà evidence nêu (chưa có phiếu khảo sát) đã hết: phiếu bàn giấy đã điền, 8 đối thủ, đã nằm trong repo từ commit `d193b6a`, và ticket nói rõ đây chính là đầu vào của golden case. Lane tự sửa được: chạy agent theo `SKILL.md` trên phiếu rồi commit `competitors.md`, chỉ dùng số liệu trong phiếu (ô trống giữ "chưa có số liệu", không bịa). Chặn vì đây là criterion cuối của ticket và là bằng chứng duy nhất cho criterion 2 và 3 trên hành vi thật.

### SPEC-2: `SKILL.md` ép cột nguồn là `khảo sát thực địa`, mâu thuẫn với criterion 4

`SKILL.md` mục 1 "Bảng đối thủ" ghi cột nguồn là (`khảo sát thực địa`) và câu miễn trừ cuối cũng ghi "dựa trên khảo sát thực địa của anh/chị". Ticket cấm đúng chuỗi đó trên `competitors.md` khi phiếu là khảo sát bàn giấy, và đòi `competitors.md` mang cùng lời khai. Skill chưa có bước nào đọc phương pháp khảo sát khai trong phiếu (mục "Cách khảo sát" của `examples/barbershop/founder/survey-form.md`) rồi chép lời khai đó vào đầu ra và đặt cột nguồn theo phương pháp thật (ví dụ "khảo sát bàn giấy từ nguồn công khai, ngày 23/11/2026" kèm link). Làm theo skill nguyên văn sẽ tạo ra đúng điều ticket cấm. Sửa: thêm bước đọc và chép lời khai phương pháp, cho cột nguồn và câu miễn trừ nhận cả hai trường hợp, và thêm test cho quy tắc này.

### SPEC-3: evidence lỗi thời, nêu giới hạn sai (criterion 4)

`docs/evidence/issue-13-founder-competitors.md` vẫn viết "Criterion 4 is not proven... The ticket is BLOCKED on the real survey" và "Last code commit: `c50706a`", trong khi commit `d193b6a` và `cada7bc` đã thêm phiếu. Mục "Giới hạn" phải cập nhật sau khi chạy golden case: nêu Kiro CLI không có trong sandbox lane, lượt chạy là của chính agent, đầu vào là phiếu bàn giấy, lệnh và kết quả checklist, và lượt Gate ở commit mới.

## Chưa xác minh (không gắn mã)

- Skill nói "N là số trên phiếu" cho cảnh báo dữ liệu mỏng; phiếu golden có nhiều ô số lượt đánh giá để trống (đối thủ 1 đến 3). Cách xử lý ô trống so với "dưới 3 lượt" chưa được `SKILL.md` nói rõ; nên xem lại khi có `competitors.md` thật (ô trống phải ra "chưa có số liệu", không phải cảnh báo "chỉ có 0 lượt").
- Phiếu golden có 3 đối thủ trong quận và 5 mốc ngoài quận, còn skill bắt "bản đồ định vị" và "khoảng trống" chỉ đặt đối thủ nơi số liệu phiếu hậu thuẫn; khi chạy thật cần thấy khoảng trống nêu rõ mẫu nhỏ và bàn giấy.
- Tên doanh nghiệp công khai trong phiếu golden (Tony Barber House, 30Shine, v.v.) là tên thương hiệu, không phải tên người; địa chỉ dừng ở cấp quận cũ. Test ẩn danh của Gate đã xanh. Không coi là finding.
- Tuyên bố của `competitors.md` về luật hay số liệu (nếu có) cần link và ngày kiểm chứng; chưa có file để đọc.

<promise>CHANGES_REQUESTED</promise>
