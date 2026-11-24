Commit mã đã chấm: 1bfb3a3f1686

# Review trục Spec, #16 founder-consumer (vòng 2)

Phạm vi: `git diff --stat main...HEAD` và `git log --oneline main..HEAD`. Đã đọc `skills/founder-consumer/SKILL.md`, `examples/barbershop/founder/{customer.json,pitch.md,consumer.md,panel/*}`, `docs/evidence/issue-16-founder-consumer.md`, `reviews/issue-16/ledger.md`, `docs/bakeoff/models.json`. Chạy lại `uv run pytest tests/test_consumer_skill.py -q`: 13 passed. CI `Gate` ở 1bfb3a3f1686: success.

## Đối chiếu từng criterion

1. `customer.json` + trình cho Owner + dùng `competitors.md` + nói phần đoán: ĐÁP ỨNG. File có segments (thu nhập VND theo khoảng), behaviours, objections, habits. SKILL.md bắt buộc hiện cho Owner sửa trước khi chạy; evidence nói rõ `competitors.md` của ví dụ không có số liệu khiếu nại nên objections là đoán. Bằng chứng: SKILL.md, `customer.json`, test `tests/test_consumer_skill.py` (chạy trong cổng `unit`).
2. `pitch.md`: ĐÁP ỨNG. 5 dòng tiếng Việt, không từ so sánh nhất, các khẳng định (giờ mở, giá 199.000 đ, gói 12 lần, cọc 50.000 đ) lấy từ `idea.md` theo evidence; có test kiểm quy tắc pitch.
3. `n = 20`, 100 chỉ khi Owner yêu cầu kèm cảnh báo chi phí và thời gian, chuỗi `panel_init → panel_run → job_status → panel_tally`, không trả lời thay buyer, báo buyer bị loại: ĐÁP ỨNG ở mức văn bản skill (SKILL.md dòng 52 đến 55, 76) và test đọc văn bản. `results.json`: `n` 20, `excluded` 0, `consumer.md` báo "Không có người mua nào bị loại".
4. Đọc lại năm điểm + caveat một lần: ĐÁP ỨNG. `consumer.md` có đủ: tỷ lệ 8 mua/12 không (40%), nhóm khác nhau nhất, ba lý do kèm một trích dẫn, điều đổi được lời từ chối, một câu nên đổi gì và skill nào (`founder-board`), caveat "mô phỏng, cận trên, không phải khách hàng thật" in một lần ở cuối. Số khớp `panel/results.md`.
5. Golden case chạy trên Kiro CLI với model tham chiếu: CHƯA ĐÁP ỨNG một nửa, xem dưới.
   - Nửa model: SPEC-1 vòng 1 ĐÃ ĐÓNG. `panel/results.json` và `panel/panel.json` ghi `gemini-3.5-flash-lite`, khớp `"reference"` trong `docs/bakeoff/models.json`; `consumer.md` ghi cùng model; tệp `panel/answers/` hiện cùng seed 837740, n 20.
   - Nửa "chạy trên Kiro CLI": SPEC-2 vẫn mở.
   - Checklist review: evidence tự khai đã qua; `consumer.md` xưng "anh/chị", không `$`, có miễn trừ.

## Finding chặn

### SPEC-2: criterion 5 chưa đáp ứng, và lane không tự sửa được

Criterion 5 nói "Golden case run on Kiro CLI with the reference model". Evidence (mục Giới hạn) và ledger (`SPEC-2 DEFERRED`) đều thừa nhận golden case được tạo bởi agent của lane làm theo SKILL.md, panel chạy qua CLI gói `founder-vn panel init/run/work/tally`, không phải phiên Kiro CLI. Điều này chưa chứng minh một phiên Kiro CLI tuân theo skill (đọc lại năm điểm, xác nhận profile với Owner, không trả lời thay buyer), là phần cốt lõi của criterion. Evidence nói "criterion 5 is not claimed as met", nên lane trung thực, nhưng "DEFERRED" không phải đóng: criterion vẫn thiếu bằng chứng.

Vì sao `BLOCKED` chứ không phải `CHANGES_REQUESTED`: sandbox không có Kiro CLI, nên lane không thể tạo bằng chứng; chấp nhận một lần chạy bằng CLI gói thay cho phiên Kiro CLI là quyết định của operator, thiết kế chưa quyết điều này. Lane không được tự hạ criterion.

- [ ] Câu hỏi cho operator: chấp nhận golden case chạy bằng CLI gói `founder-vn` theo SKILL.md (ghi rõ trong evidence) cho criterion 5, hay yêu cầu một phiên Kiro CLI thật với `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite` (chạy lại và đối chiếu `consumer.md`, `panel/`)? Nếu chọn chấp nhận, đổi checklist trên #16 và chỉnh dòng criterion 5 cho khớp.

## Chưa xác minh (không gắn mã)

- Không chạy lại panel (cần endpoint mô hình và khóa); chỉ đối chiếu số trong `consumer.md` với `results.md`/`results.json` và đọc các tệp `answers/`. Không kiểm được rằng câu trả lời do mô hình sinh, ngoài lời khai của evidence.
- Tên nữ trong phân khúc "Nam, ..." (ví dụ P001 "Thảo Vy", cũng "Hà My", "Ngọc Lan"): `customer.json` không có trường giới tính, `panel.GIVEN_NAMES` chia tên lẫn lộn; evidence gán cho T15. Ticket #16 không đòi điều này; không chặn, nhưng buyer mô phỏng "Nam" mang tên nữ có thể làm lệch câu trả lời của panel.
- Tên trong `personas.json` là tên riêng tổng hợp do gói chia, không phải người thật; nơi chỉ đến cấp "Quận 7 cũ". Không thấy dữ liệu định danh.

<promise>BLOCKED</promise>
