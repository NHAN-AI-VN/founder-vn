Commit mã đã chấm: a9f2ed2d5bfd

# Review trục Spec, issue #18, vòng 1

Phán quyết: CHANGES_REQUESTED (một finding chặn, sửa được trong phạm vi lane).

Phạm vi: `git diff --stat main...HEAD` (10 file ngoài `reviews/`: `skills/founder-plan/SKILL.md`, `examples/barbershop/founder/summary.md`, `examples/barbershop/founder/business-plan.md`, `README.md`, `docs/review-checklist.md`, 3 file test, `docs/evidence/issue-18-founder-plan.md`). CI `Gate` run 45342730025: success. Tôi chạy lại `uv run pytest tests/test_plan_example.py tests/test_wave_a_checklist.py tests/test_plan_skill.py -q` (26 passed) và `founder-vn plan --check` trong `examples/barbershop` (mã 0, "business-plan.md khớp với các file hiện có"). Các test nằm dưới `tests/` nên thuộc cổng `unit`.

## Đối chiếu từng criterion

### Criterion 1: skill viết `summary.md` (tóm tắt điều hành và bản một trang), gọi compiler, không tự viết verdict, giải thích từng check hỏng bằng lời chủ hộ kèm skill sửa

Đáp ứng ở mức văn bản chỉ dẫn. `skills/founder-plan/SKILL.md`: Bước 2 gọi `plan_compile` / `founder-vn plan` rồi kiểm `--check`; Bước 3 có bảng ba check ("Nghĩa là gì với anh/chị", "Skill sửa") và đường `Incomplete`; Bước 4 có hai phần; Protocol 5 và mục Rules cấm viết verdict tay. `tests/test_plan_skill.py` kiểm các đoạn đó. `business-plan.md` khớp đầu ra compiler (`plan --check` mã 0).

### Criterion 2: thư mục ví dụ đủ idea, board, competitors, customer/pitch/panel, pricing, numbers/cfo, summary, business-plan; ẩn danh; README dẫn tới

Đáp ứng. Đủ file trong `examples/barbershop/founder/` (có `test_example_holds_every_wave_a_artifact`); `README.md` dẫn tới thư mục và `business-plan.md`. Địa điểm ở cấp "Quận 7 cũ"; không thấy tên người, địa chỉ, số điện thoại, email trong các file đã quét.

### Criterion 3: checklist qua mọi artefact Wave A

Đáp ứng cho artefact. Đã đọc `summary.md` thật: không `$`, xưng "anh/chị", VND định dạng Việt, link Công báo kèm ngày 23/11/2026, caveat panel và miễn trừ. SPEC-1 của vòng trước đã được sửa: bản một trang giờ có link nguồn, caveat và miễn trừ riêng ở cuối phần. `docs/review-checklist.md` thêm danh sách tên riêng được chấp nhận, nói rõ phép đo chống tiếng Anh là stoplist.

## Finding chặn

### SPEC-1: test mới cho bản một trang không bắt được việc thiếu miễn trừ, nên bằng chứng của criterion 3 vẫn chưa chứng minh được điều nó tuyên bố

Criterion 3 (disclaimer, caveat) cùng yêu cầu của vòng trước: "siết test để kiểm riêng nội dung sau tiêu đề Bản một trang". `tests/test_plan_example.py` hàm `_parts()` cắt `text.split(marker)[1]`, tức mọi thứ từ tiêu đề bản một trang đến hết file. Phần đó gồm cả mục `## Lưu ý` đứng sau, và mục ấy chứa nguyên caveat và miễn trừ (tôi kiểm: `"## Lưu ý" in page` là True). Vì vậy `test_one_page_version_stands_alone_with_caveat_disclaimer_and_sources` vẫn xanh nếu xoá caveat và miễn trừ khỏi bản một trang, đúng lỗi vòng trước. Test chạy trong cổng `unit` nhưng không fail khi lỗi quay lại, nên gác cổng này là hình thức. (Hai kiểm `link` và `23/11/2026` trong `page` cũng yếu như vậy, dù hai thứ này hiện chỉ nằm trong phần một trang.)

Cách sửa (trong phạm vi lane): cắt bản một trang đến tiêu đề `## ` kế tiếp (hoặc đến `## Lưu ý`), rồi kiểm caveat, miễn trừ, link và ngày trên đoạn đã cắt. Thử đỏ: xoá miễn trừ khỏi bản một trang thì test phải fail.

## Chưa xác minh

- Không có lần chạy model thật của `founder-plan`; `summary.md` do lane viết theo skill (`docs/evidence/issue-18-founder-plan.md`, mục "Giới hạn"). Criterion 1 chứng minh được ở mức chỉ dẫn, không ở hành vi model.
- Bước 3 chưa có ví dụ đầu ra cho `Not yet` hay `Incomplete` vì ca vàng là Profitable. Ticket không đòi ví dụ này.
- Phép đo chống tiếng Anh là stoplist; tôi đọc `summary.md` bằng tay và không đọc hết 404 dòng của `business-plan.md`.
- `docs/founder-vn-design.md` không có mục nào khớp từ khoá `summary` hay `plan_compile` theo grep của tôi; tôi không đối chiếu thêm điều thiết kế nói về `founder-plan` ngoài các file ticket nêu.

<promise>CHANGES_REQUESTED</promise>
