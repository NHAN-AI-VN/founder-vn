Commit mã đã chấm: 62722d6264cf

# Review trục Spec, issue #144, vòng 1

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git diff --stat main...HEAD` (14 file, 5 commit từ b6bf391 tới 62722d6). Đã chạy ở checkout này: `uv run pytest -q` cho 497 passed; `scripts/skill_lint.py` cho 0 finding.

## Đối chiếu từng criterion

- Hai dòng `## Chưa làm` khi thiếu offer và brand: `plan.py` (`compile_plan`, `_ships`) in đúng dạng của mục 2; test `test_unshipped_sections_say_after_pilot_and_shipped_ones_keep_the_run_line`, `test_wave_b_checklist`. Hai golden đã so từng dòng với `main`: chỉ đúng hai dòng đổi, độ dài không đổi (167/167 và 47/47).
- Skill có trong gói giữ dòng `chạy skill`: cùng test, kiểm `founder-permits`.
- File viết tay: `test_hand_written_offer_and_brand_are_compiled_with_the_marker` kiểm dòng dấu ngay dưới `## <tiêu đề>`, nội dung hạ cấp, `Chưa làm` không liệt kê, `## Giá` không có dấu. Chuỗi dấu khớp nguyên văn mục 3.
- Tra cứu "đã đem hay chưa" đọc thư mục skill: `_ships` gọi `install.packaged_skills_dir()` và kiểm `SKILL.md`; không có tên skill nào ghi cứng trong `plan.py`. `test_shipped_skill_lookup_reads_the_packaged_skills_folder` trỏ tới thư mục fixture có và không có `founder-offer/SKILL.md`, dòng và dấu đổi theo.
- `plan --check`: logic không đổi trong diff; test hiện có (`test_plan_cli.py`) vẫn xanh.
- Parity CLI và MCP: `test_plan_with_hand_written_offer_cli_equals_mcp` so stdout và file, có một ca `offer.md` viết tay.
- Golden và ví dụ do công cụ sinh: diff của `business-plan.md` ví dụ chỉ hai dòng, `test_plan_example.py` so với `compile_plan` và xanh; `summary.md` không nằm trong diff. Bằng chứng ghi rõ cách sinh golden.
- `skills/founder-plan/SKILL.md`: hai hàng bảng và câu bước 1 đúng mục 4; `test_plan_skill.py` ghim; khối `## Protocol` không đổi; không có `$` cạnh chữ số; dòng Owner thấy là tiếng Việt.
- Design: Q59 ở cuối nhật ký (dạng Q54), tiêu đề `Q1–Q59`, mệnh đề thêm vào Q55; `AGENTS.md` và `tests/test_install.py` đổi theo `Q1–Q59`. Bằng chứng ở `docs/evidence/issue-144-plan-offer-brand-after-pilot.md` có bảng red rồi green.
- Cổng xanh ở commit mã cuối: CI `Gate` success (tin nhắn mở đầu) và bằng chứng ghi ba đoạn.
- Ngoài phạm vi: không đụng `SECTIONS`, `summary.md`, hay phát hiện tác giả file của skill có trong gói.

## Chưa xác minh

- Đường wheel (`founder_vn/skills/`) không được test bằng wheel thật; test dùng monkeypatch trên `install.packaged_skills_dir`, và bằng chứng của lane đã nêu giới hạn này. Không chặn vì hàm này đã phục vụ installer.
- Không chạy mô hình thật; không áp dụng cho ticket này.

<promise>PASS</promise>
