Commit mã đã chấm: 8a5b59a3d871

# Review trục Spec, issue #18, vòng 1

Phán quyết: CHANGES_REQUESTED (một finding chặn, sửa được trong phạm vi lane).

Phạm vi: `git diff --stat origin/main...HEAD` (8 file: `skills/founder-plan/SKILL.md`, `examples/barbershop/founder/summary.md`, `examples/barbershop/founder/business-plan.md`, `README.md`, 3 file test, `docs/evidence/issue-18-founder-plan.md`). CI `Gate` run 45342095480: success. Tôi chạy lại `uv run pytest tests/test_plan_example.py tests/test_wave_a_checklist.py tests/test_plan_skill.py -q` (22 passed) và `scripts/skill_lint.py` (0 finding). Các test nằm dưới `tests/` nên thuộc cổng `unit`.

## Đối chiếu từng criterion

### Criterion 1: skill viết `summary.md`, gọi compiler, không tự viết verdict, giải thích từng check hỏng bằng lời chủ hộ kèm skill sửa

Đáp ứng. Bằng chứng: `skills/founder-plan/SKILL.md` Bước 2 gọi `plan_compile` / `founder-vn plan`, Bước 3 có bảng ba check với "Nghĩa là gì với anh/chị" và "Skill sửa", Bước 4 có hai phần (tóm tắt điều hành, bản một trang), quy tắc "Never write the verdict". `tests/test_plan_skill.py` đọc đúng các đoạn đó. `business-plan.md` bằng đúng đầu ra `plan.compile_plan` và `plan --check` trả mã 0 (`tests/test_plan_example.py`), dòng kết luận trong plan và summary bằng verdict tính ra.

### Criterion 2: thư mục ví dụ đủ idea, board, competitors, customer/pitch/panel, pricing, numbers/cfo, summary, business-plan; ẩn danh; README dẫn tới

Đáp ứng. `test_example_holds_every_wave_a_artifact` kiểm 12 file; `README.md` dẫn tới `examples/barbershop/founder/` và `business-plan.md`. Địa điểm ở cấp "Quận 7 cũ", không thấy tên người hay địa chỉ trong `summary.md` và `business-plan.md`; tên trong hội đồng là tên lens công khai.

### Criterion 3: checklist qua mọi artefact Wave A

Đã đọc `summary.md` và `business-plan.md` thật: không `$`, xưng "anh/chị", tiền VND định dạng Việt, link Công báo kèm ngày 23/11/2026, caveat panel, có miễn trừ. Một chỗ chưa đạt, xem SPEC-1.

## Finding chặn

### SPEC-1: bản một trang cho đối tác không tự đứng được, thiếu miễn trừ trách nhiệm

Criterion 3 (disclaimer) và chính `skills/founder-plan/SKILL.md` Bước 4 mục 2: "The page must stand on its own, and must carry the same caveat and disclaimer as part 1". Trong `examples/barbershop/founder/summary.md`, phần "Bản một trang cho đối tác hoặc bên cho vay" có caveat panel nhưng không có câu "không phải tư vấn tài chính, thuế hay pháp lý". Câu đó chỉ nằm ở mục "Lưu ý" đứng sau, ngoài bản một trang. Đây là phần anh/chị đưa cho đối tác hoặc bên cho vay, tức người đọc chỉ thấy trang này sẽ không thấy miễn trừ, và có số liệu vốn cần 1.424.635.000 đ. Ví dụ vàng là mẫu cho mọi chủ hộ sau này nên lỗi này nhân rộng.

Test không bắt được: `test_summary_carries_caveat_disclaimer_and_dated_links` và `test_every_report_carries_the_disclaimer` kiểm cả file, không kiểm riêng phần một trang, nên chúng xanh dù thiếu.

Cách sửa (trong phạm vi lane): thêm miễn trừ vào bản một trang, siết test để kiểm riêng nội dung sau tiêu đề "Bản một trang…" (có caveat panel và "không phải tư vấn tài chính, thuế hay pháp lý"), và nếu cần, nêu rõ trong SKILL.md Bước 4 vị trí đặt miễn trừ cho mỗi phần.

## Chưa xác minh

- Không có lần chạy model thật của `founder-plan`; `summary.md` do lane viết theo skill (docs/evidence/issue-18-founder-plan.md mục "Giới hạn" đã nói). Criterion 1 chỉ chứng minh được ở mức văn bản chỉ dẫn, không ở hành vi model.
- Phần giải thích check hỏng (Bước 3) chưa có ví dụ đầu ra, vì ca vàng là Profitable; không có ví dụ `Not yet` hay `Incomplete`. Ticket không đòi ví dụ này, nên không chặn.
- Mục "Lưu ý" của `summary.md` lặp hai lần cùng một câu miễn trừ, và không có câu đóng "Panel là mô phỏng, cận trên, không phải khách hàng thật." như Bước 4 của skill quy định. Lệch nhỏ giữa skill và ví dụ, không chặn.
- Phép đo tự động chống tiếng Anh là danh sách từ chặn, không phải bộ nhận diện ngôn ngữ; tôi đọc `summary.md` bằng tay, không đọc hết 404 dòng của `business-plan.md`.

<promise>CHANGES_REQUESTED</promise>
