Commit mã đã chấm: f2b87c5077e7

# Review trục Spec: #95 vòng 1

Phán quyết: PASS. Không có finding chặn.

## Criterion đã đối chiếu

Ticket có ba mục đề xuất và một yêu cầu ngầm (không vượt phạm vi). Mỗi mục dưới đây đối chiếu với diff `main...HEAD` (3 commit, 7 file).

- `panel_tally` thêm dòng miễn trừ sau caveat. Đáp ứng. `src/founder_vn/panel.py` `results_md` thêm một đoạn riêng "Đây không phải tư vấn tài chính, thuế hay pháp lý." ngay sau đoạn "Panel là mô phỏng...". Câu đúng chữ với câu `panel.py` dùng ở nơi khác, và khớp mẫu của các báo cáo khác. Không có `$`.
- Golden `examples/barbershop/founder/panel/results.md` được tạo lại, commit message giải thích thay đổi một dòng. Đáp ứng. File thật có đúng một dòng thêm, đã đọc. Commit `f759de9` nêu rõ dòng thêm và danh sách golden đổi.
- `tests/test_panel_cli.py` kiểm tra dòng này. Đáp ứng. Một assert thêm vào `test_results_md_is_vietnamese_with_caveat_and_no_dollar`. Test này chạy trong `pytest` của cổng `unit`. Bằng chứng đỏ rồi xanh nằm ở `docs/evidence/issue-95-panel-tally-disclaimer.md`.
- Ngoài phạm vi: thay đổi chỉ một dòng. Đáp ứng. Lan sang `business-plan.md` của ví dụ, `tests/golden/panel_tally.json` và `plan_full.json` là hệ quả bắt buộc, vì `plan_compile` nhúng `results.md` nguyên văn, và ticket nêu đúng điều đó. Mỗi file chỉ thêm đúng đoạn này.

## Đã chạy tại f2b87c5077e7

- `uv run pytest tests/test_panel_cli.py tests/test_panel_parity.py tests/test_plan*.py -q`: 76 passed.
- `uv run pytest tests/test_plan_example.py tests/test_golden_case.py tests/test_wave_a_checklist.py -q`: 20 passed.
- Gate của CI ở run 45574765586: success (theo tin nhắn giao việc).
- Artefact cho chủ hộ: đã đọc diff `examples/barbershop/founder/panel/results.md` và `business-plan.md`. Tiếng Việt, "anh/chị", không `$`, caveat "mô phỏng" còn nguyên, ví dụ không chứa tên thật.

## Chưa xác minh

- Parity CLI/MCP chỉ được chứng minh qua `tests/test_panel_parity.py` (so file byte-identical, đã chạy xanh); lane không thêm assert riêng cho MCP. Ticket không yêu cầu.
- Evidence ghi các golden JSON được sửa tay (repo không có lệnh tái tạo). Test so với đầu ra thật của công cụ đều xanh, nên không thành finding.

<promise>PASS</promise>
