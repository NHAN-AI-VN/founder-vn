Commit mã đã chấm: e804d8da5f7a

# Review trục Spec, issue #18, vòng 2

Phán quyết: PASS. Không còn finding chặn.

Phạm vi: `git diff --stat main...HEAD` (12 file, gồm `skills/founder-plan/SKILL.md`, `examples/barbershop/founder/summary.md`, `examples/barbershop/founder/business-plan.md`, `README.md`, `docs/review-checklist.md`, ba file test, evidence và các file `reviews/`). `git log --oneline main..HEAD` có 18 commit; commit sửa vòng trước là `bb861e8`. CI `Gate` run 45343454643: success (theo tin nhắn mở đầu).

## Đã chạy lại độc lập

- `uv run pytest tests/test_plan_example.py tests/test_wave_a_checklist.py tests/test_plan_skill.py -q`: 26 passed. Các file nằm dưới `tests/` nên thuộc cổng `unit` (`uv run pytest -q` trong `.github/workflows/gate.yml`).
- `founder-vn plan --check` trong `examples/barbershop`: mã 0, "business-plan.md khớp với các file hiện có".
- Thử đỏ cho SPEC-1 vòng trước, trên bản sao tạm của `summary.md` (đã khôi phục, `git status` sạch):
  1. Xoá đoạn caveat và miễn trừ cuối phần "Bản một trang" (vẫn còn `## Lưu ý` bên dưới): `test_one_page_version_stands_alone_with_caveat_disclaimer_and_sources` FAIL tại `tests/test_plan_example.py:70`.
  2. Chỉ xoá câu miễn trừ khỏi phần một trang: cùng test FAIL cùng dòng.
  Lý do: `_parts()` giờ cắt phần một trang tại `\n## ` kế tiếp, nên `## Lưu ý` không còn cung cấp caveat hay miễn trừ hộ. Bản sửa chứng minh được điều nó tuyên bố. Kiểm `link` và `23/11/2026` trên `page` cũng nằm trong đoạn đã cắt.

## Đối chiếu từng criterion

### Criterion 1: skill viết `summary.md` (tóm tắt điều hành và bản một trang), gọi compiler, không tự viết verdict, giải thích từng check hỏng bằng lời chủ hộ kèm skill sửa

Đáp ứng ở mức văn bản chỉ dẫn. `skills/founder-plan/SKILL.md`: Bước 2 gọi `plan_compile` / `founder-vn plan` rồi `--check` mã 0; Bước 3 có bảng ba check với cột "Nghĩa là gì với anh/chị" và "Skill sửa", cùng đường `Incomplete`; Bước 4 yêu cầu hai phần, bản một trang tự đứng được với caveat và miễn trừ riêng; Protocol 5 và mục Rules cấm viết verdict tay. Bằng chứng: `tests/test_plan_skill.py` (gồm test bảng check bằng đúng nhãn compiler in cho ba fixture Not yet), chạy trong `unit`. `business-plan.md` bằng đúng đầu ra `plan.compile_plan` (test và `plan --check`), dòng kết luận của `summary.md` bằng nhãn tính được (`test_verdict_line_in_plan_and_summary_equals_the_computed_verdict`).

### Criterion 2: thư mục ví dụ đủ idea, board, competitors, customer/pitch/panel, pricing, numbers/cfo, summary, business-plan; ẩn danh; README dẫn tới

Đáp ứng. `examples/barbershop/founder/` có `idea.md`, `board.md`, `competitors.md`, `consumer.md`, `customer.json`, `pitch.md`, `panel/`, `pricing.md`, `numbers.json`, `cfo.md`, `summary.md`, `business-plan.md`; `tests/test_wave_a_checklist.py` kiểm đủ bộ. `README.md` dẫn tới `examples/barbershop/founder/` và `business-plan.md`, bảng skill ghi `founder-plan` shipped. Quét `examples/barbershop` tìm email, số điện thoại, "đường", "phường": không có. Địa điểm ở cấp "Quận 7 cũ".

### Criterion 3: checklist qua mọi artefact Wave A (không `$`, không tiếng Anh, link cho khẳng định pháp lý và số liệu, miễn trừ, caveat panel)

Đáp ứng. Đã đọc `summary.md` thật: xưng "anh/chị", tiền dạng `280.000 đ`, quét `$` cạnh chữ số trong `examples/barbershop/founder/*.md` không thấy, thuế suất 7% và ngưỡng 1.000.000.000 đ có link Công báo và ngày 23/11/2026 (cả ở phần điều hành lẫn bản một trang), caveat panel ở mọi chỗ nêu kết quả panel, miễn trừ có ở từng phần và ở cuối. `test_every_amount_in_the_summary_is_printed_by_a_tool` buộc mọi số tiền khớp đầu ra công cụ. Ba nhãn kết luận tiếng Anh (`Profitable (có lãi)` ...) được `docs/review-checklist.md` ghi rõ là tên riêng do công cụ in, nên không phải rò tiếng Anh. `tests/test_wave_a_checklist.py` (7 test) chạy cả bộ artefact trong `unit`.

## Chưa xác minh

- Không có lần chạy model thật của `founder-plan`; `summary.md` do lane viết theo skill (`docs/evidence/issue-18-founder-plan.md`, mục "Giới hạn"). Criterion 1 chứng minh ở mức chỉ dẫn và artefact, không ở hành vi model.
- Bước 3 chưa có ví dụ đầu ra thật cho `Not yet` hay `Incomplete` vì ca vàng là Profitable; chỉ có test bảng-nhãn theo fixture. Ticket không đòi ví dụ này.
- Phép đo chống tiếng Anh là stoplist; tôi đọc `summary.md` bằng tay, không đọc hết 404 dòng của `business-plan.md` (nó do compiler sinh và khớp `plan --check`).
- `docs/founder-vn-design.md` chỉ nhắc `plan` ở dòng 16 (thứ tự skill), 161 (PDF `business-plan.md`) và 173 (Đợt A); không có mục riêng cho `summary.md`, nên không có yêu cầu thiết kế nào bị bỏ sót hay trái.

<promise>PASS</promise>
