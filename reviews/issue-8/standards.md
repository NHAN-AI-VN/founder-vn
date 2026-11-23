Commit mã đã chấm: 7445cdf7deec

# Review trục Standards, issue #8, vòng 2

Phán quyết: PASS. Không còn finding chặn. S1 của vòng 1 đã đóng.

## Phạm vi đã xét

`git log --oneline main..HEAD` (12 commit, HEAD `55e4894e2ac7`) và `git diff --stat main...HEAD` (12 file). Commit mã cuối là `7445cdf`; `bbedc92` và `55e4894` chỉ chạm `docs/evidence/` và `reviews/`. Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape of the code, Tests, Owner-facing output, Git), `docs/agents/evidence-gates.md` (bảng "Evidence by change type", "Where evidence lives"), `docs/agents/parallel-lanes.md`, `CONTRIBUTING.md`. Diff không chạm `skills/` hay `examples/` nên checklist skill không áp dụng.

Từ vòng 1 có thêm: `7445cdf` (sửa SPEC-1 trong `src/founder_vn/pricing.py`, golden `tests/golden/pricing_report.json`, `tests/test_pricing_cli.py`) và `bbedc92` (bằng chứng cho S1).

## S1 của vòng 1: đã đóng

`docs/evidence/issue-8-pricing-psm.md` giờ có dòng `## Lát` riêng cho `test_out_outside_root_is_refused` và `test_missing_answers_exits_2_naming_the_field`, mỗi dòng ghi đột biến và assertion đỏ. Tôi chạy lại cả hai đột biến ở HEAD, rồi `git checkout src`:

- Thay `files.write_text` bằng `Path.write_text` trong `pricing.run`: `assert 0 == 2 where 0 = main(['pricing', 'pricing_input.json', '--out', '../pricing.md'])`, 1 failed, 7 passed.
- Thay `raise PricingInputError("thiếu trường 'answers'")` bằng `spec = {**spec, "answers": []}`: `assert 0 == 2 where 0 = main(['pricing', 'empty.json'])`, 1 failed, 7 passed.

Kết quả khớp từng chữ với bằng chứng tự khai. `git status` sạch sau khi hoàn nguyên.

## Đã kiểm ở HEAD

- `uv run ruff check .` sạch, `ruff format --check .` 100 file sạch, `uv run pytest -q` 143 passed, `scripts/skill_lint.py` 0 finding.
- Hình dạng vòng lặp: (a) `seam:` `d268160` có `## Seam` và đứng trước mọi `slice(`; (b) mọi commit chạm `src/` cũng chạm test và có dòng `## Lát`, kể cả `7445cdf` (có dòng "report notes (SPEC-1)"); (c) test đi qua CLI và MCP, tức seam đã khai; (d) `## Cổng ba đoạn` ghi `GREEN on 7445cdf7…`, đúng commit mã cuối, không stale.
- Golden đổi ở `7445cdf` có giải thích trong commit message (chỉ hai đoạn `Lưu ý` thêm vào), đúng bảng "Golden file" của evidence-gates.
- Ghi file chỉ qua `files.write_text`, đọc qua `files.read_text`. `pricing.run` là một hàm sau CLI `pricing` và MCP `pricing_psm`, có parity test (báo cáo, `--json`, `--out`). Không file một-chủ nào bị sửa. Báo cáo xưng "anh/chị", không có `$` cạnh chữ số, VND định dạng bằng `format_vnd`, có cảnh báo "mô phỏng, cận trên" và miễn trừ. Không gọi mạng hay LLM; không in giá trị `FOUNDER_LLM_*`; fixture là dữ liệu tổng hợp. Thiếu `answers` là lỗi nêu tên trường. Không có tỷ lệ thuế.

## Chưa xác minh (không gắn mã)

- Đường lỗi qua MCP: `pricing_psm` không bắt `PricingInputError`/`PathRefused`, parity test chỉ phủ đường thành công. `server.py` không có `except` nào, kể cả ở `cfo_analyse` có sẵn, nên cách làm nhất quán với mã cũ. Chưa kiểm cách host MCP hiển thị lỗi ném ra.
- `MIN_VALID_ANSWERS = 8`: lượt Spec ghi "dưới 8 câu hợp lệ" là tiêu chí chấp nhận của ticket. Thân ticket không có trong sandbox, nên tôi không tự đối chiếu.
- Hợp đồng file đầu vào (`answers`, `competitor_prices`) do lane đặt, đã khai trong `## Giới hạn` của evidence. Công thức Van Westendorp chỉ kiểm bằng một phép tính tay và một golden, chưa so với cài đặt ngoài.
- Job `Gate` ở `55e4894` còn `in_progress` lúc chấm; cổng CI chạy lại trọn ở commit cuối.

<promise>PASS</promise>
