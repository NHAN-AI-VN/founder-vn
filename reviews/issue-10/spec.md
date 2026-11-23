Commit mã đã chấm: 1faa999d0175

# Review trục Spec, issue #10, vòng 1

Phạm vi: `git log --oneline main..HEAD` (6 commit: seam, verdict, key numbers/panel/sections/goldens, `--check`, MCP, evidence) và `git diff --stat main...HEAD` (8 file: `src/founder_vn/plan.py`, `cli.py`, `server.py`, `tests/test_plan_cli.py`, `tests/test_plan_parity.py`, 2 golden, `docs/evidence/issue-10-plan-compiler.md`). Đã chạy lại `uv run pytest tests/test_plan_cli.py tests/test_plan_parity.py -q`: 21 passed. CI `Gate` ở commit này: success. Các test nằm trong `tests/` nên thuộc cổng `unit` (pytest toàn bộ).

**Phán quyết: PASS**

## Đối chiếu từng criterion

1. Verdict Profitable / Not yet / Incomplete từ ba kiểm tra: ĐÃ ĐÁP ỨNG. `plan.verdict` đọc `cfo.analyse()["verdict_inputs"]` (contribution > 0; `year1_operating_profit_after_tax` > 0, tính sau thuế doanh thu trong `cfo.analyse`; `breakeven_within_capacity`). `numbers.json` vắng thì `Incomplete` không kèm kiểm tra. Bằng chứng: `test_no_numbers_is_incomplete`, `test_all_three_checks_pass_is_profitable`, `test_each_failed_check_is_not_yet_and_named`, golden `plan_numbers_only`.
2. Dòng "Tín hiệu cầu (mô phỏng, cận trên)" với mua, không mua, chế độ, mô hình; không ảnh hưởng verdict; không có cổng buy-rate: ĐÃ ĐÁP ỨNG. `panel_line` chỉ in; `verdict` không nhận đầu vào từ panel; mã không có ngưỡng buy-rate. Bằng chứng: `test_panel_line_shows_buys_passes_mode_and_model`, `test_panel_never_changes_the_verdict` (buys 0 và 5, đã chứng minh đỏ bằng mutation theo evidence), golden `plan_full`.
3. Bảng số chính theo VND, mục theo thứ tự pipeline, danh sách "Chưa làm" gọi tên skill, lời miễn trừ tiếng Việt cuối: ĐÃ ĐÁP ỨNG. Đã đọc file thật `tests/golden/plan_numbers_only.json` (bản plan sinh ra): VND định dạng Việt (`45.000 đ`), không `$`, xưng "anh/chị", mục "Chưa làm" ghi `founder-<skill>` cùng file cần tạo, mục "Lưu ý" cuối nêu không phải tư vấn tài chính/thuế/pháp lý và panel là mô phỏng. `SECTIONS` đúng thứ tự §2 của design. Bằng chứng: `test_key_numbers_table_is_in_vnd`, `test_sections_follow_pipeline_order_and_missing_ones_name_their_skill`, hai golden test.
4. Đọc đúng shape `numbers.json` (T05) và `panel/results.json` (T07), `--check` có exit code, golden test, MCP parity: ĐÃ ĐÁP ỨNG. Plan dùng `cfo._load`/`cfo.analyse` và các trường `buys`, `passes`, `mode`, `model` của `panel.tally`; thiếu trường thì báo lỗi nêu tên trường (exit 2). `--check`: 0 khi khớp, 1 khi thiếu hoặc cũ, không ghi gì (3 test). Parity: `tests/test_plan_parity.py` so stdout và file giữa CLI và `plan_compile`, có và không có panel, và `check`.

Bản thiết kế §3: "Verdict ... tính từ số CFO thôi; panel in dòng riêng 'tín hiệu cầu (mô phỏng, cận trên)', không tham gia verdict" (và Q38): khớp. Không có `$`, không có tên người hay địa điểm thật trong golden (dữ liệu tổng hợp, ghi rõ "ví dụ tổng hợp").

## Chưa xác minh / ghi nhận (không chặn, không gắn mã)

- Ticket nói "break-even ≤ capacity khi có capacity". `cfo.analyse` bắt buộc `capacity_per_day`, nên kiểm tra này luôn áp dụng; thiếu trường thì lỗi exit 2 chứ không bỏ qua kiểm tra. Lane đã ghi quyết định này trong evidence; khớp shape T05 hiện có. Nếu operator muốn `capacity_per_day` tùy chọn thì đó là thay đổi ở T05 (`cfo.py`), ngoài ticket này.
- Khi `founder/numbers.json` vắng nhưng `cfo.md` có, plan kết luận Incomplete và nêu thiếu số ở mục "Kết luận", nhưng mục "Chưa làm" không liệt kê `founder-cfo`. Chỉ là lệch nhỏ về tiện dụng; criterion "mỗi mục còn thiếu gọi tên skill" vẫn đúng với các mục thiếu file.
- Nhánh hòa vốn vô hạn (`không bao giờ`) trong bảng số chính không có test riêng; nhánh `Not yet` do contribution ≤ 0 được test ở mức verdict.
- Chưa có skill `founder-plan` trong `skills/` (ngoài phạm vi ticket, evidence đã nêu).
- Phép đo của harness `reviews/issue-10/probe*.md` ngoài phạm vi.

<promise>PASS</promise>
