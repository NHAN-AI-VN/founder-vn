Commit mã đã chấm: 1bad213d5743

# Review trục Spec, #16 founder-consumer (vòng 2, chạy lại sau trả lời của operator)

Phạm vi: `git diff --stat main...HEAD`, `git log --oneline main..HEAD`, và `git diff 3b4685f..HEAD` (lần chấm trước). Từ `1bfb3a3f1686` đến `1bad213d5743` chỉ đổi 5 file: `docs/evidence/issue-16-founder-consumer.md` (dòng đầu mục Giới hạn), `reviews/issue-16/{ledger,operator-answer,spec,standards}.md`. Mã, test, `skills/founder-consumer/SKILL.md` và `examples/barbershop/founder/` không đổi. Đã đọc `reviews/issue-16/operator-answer.md`. Chạy lại `uv run pytest tests/test_consumer_skill.py -q`: 13 passed. CI `Gate` ở 1bad213d5743: success.

## Đối chiếu từng criterion

1. `customer.json` có segments với khoảng thu nhập VND, behaviours, objections, habits; SKILL.md bắt buộc hiện cho Owner sửa trước khi chạy, dùng `competitors.md` khi có, nói phần đoán. ĐÁP ỨNG. Bằng chứng: SKILL.md, `customer.json` (qua `panel.validate_customer` trong test), test chạy trong cổng `unit`. Không đổi từ vòng trước.
2. `pitch.md` 5 dòng tiếng Việt, không so sánh nhất, các khẳng định lấy từ `idea.md`. ĐÁP ỨNG, có test luật pitch. Không đổi.
3. `n = 20`, 100 chỉ khi Owner yêu cầu kèm cảnh báo chi phí và thời gian, chuỗi `panel_init → panel_run → job_status → panel_tally`, không trả lời thay buyer, báo buyer bị loại. ĐÁP ỨNG ở văn bản skill và test đọc văn bản; `panel/` có `n` 20, `excluded` 0, 20 file `answers/`, `consumer.md` báo không có buyer bị loại. Không đổi.
4. Đọc lại năm điểm và caveat "mô phỏng, cận trên, không phải khách hàng thật" in một lần, xưng "anh/chị". ĐÁP ỨNG; số trong `consumer.md` khớp `panel/results.md`/`results.json`. Không đổi.
5. Bản sửa (operator, 2026-11-24, `reviews/issue-16/operator-answer.md`, mục chọn `- [x]`): golden case tạo bằng cách làm theo SKILL.md, panel chạy qua CLI gói trên model tham chiếu, tên model và hash prompt ghi trong `panel/panel.json`; `customer.json`, `pitch.md`, `panel/` trong thư mục ví dụ; checklist qua. ĐÁP ỨNG, đối chiếu file thật:
   - `examples/barbershop/founder/panel/panel.json`: `model` = `gemini-3.5-flash-lite`, khớp khoá `"reference"` trong `docs/bakeoff/models.json`; `prompt_hash` = `7602aad48363987ca4053b9c60fb76550adbc4af9bbdd18c3059ef29f04c71c6`; `seed` 837740, `n` 20, `mode` `model`.
   - Dấu vết chạy qua CLI gói: `panel/jobs/` (J-e4834377, J-f98a9a4c, J-5b1dc109), `panel/answers/` (20 file), `personas.json`, `results.json`, `results.md`; evidence mục Giới hạn mô tả `founder-vn panel work`/`run`/`tally`.
   - `customer.json`, `pitch.md`, `panel/` đều có trong thư mục ví dụ; evidence ghi checklist `docs/review-checklist.md` qua; `consumer.md` xưng "anh/chị", không `$`.
   - Phần "phiên Kiro CLI tuân theo skill" không còn thuộc criterion 5 sau bản sửa; evidence ghi rõ là giới hạn và chuyển cho T18 (#19). Dòng đầu mục Giới hạn đã khớp bản sửa (không còn "not claimed as met"), `ledger.md` ghi SPEC-2 FIXED kèm lý do, đủ S1, SPEC-1, SPEC-2.
   - Việc hạ criterion do operator làm trên ticket, đúng thẩm quyền; lane không tự hạ. Thân ticket trong tin nhắn mở đầu mang đúng nguyên văn bản sửa.

SPEC-1 và SPEC-2 của các vòng trước đã đóng. Không có finding chặn mới.

## Chưa xác minh (không gắn mã)

- Không chạy lại panel (cần endpoint mô hình và khoá). Chỉ đối chiếu số và trích dẫn của `consumer.md` với `results.md`/`results.json` và `answers/`; việc các câu trả lời do mô hình sinh dựa vào `panel.json` (model, hash), job files và lời khai của evidence.
- Phiên Kiro CLI thật của skill (xác nhận profile với Owner, không trả lời thay buyer, đọc lại năm điểm) chưa có bằng chứng ở lane này; theo bản sửa criterion 5 nó thuộc T18 (#19).
- Một số persona nữ (ví dụ P001 "Thảo Vy") nằm trong segment "Nam, ...". Evidence hoãn sang T15; không thuộc criterion nào của ticket này. Tên persona là tổng hợp, địa điểm chỉ tới cấp quận, nên không vi phạm ẩn danh.

<promise>PASS</promise>
