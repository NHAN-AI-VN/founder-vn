Commit mã đã chấm: f2b87c5077e7

# Review trục Standards, vòng 1, issue #95

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD` (7 file) và `git log --oneline main..HEAD` (3 commit: `5e273e0` seam, `f759de9` slice, `f2b87c5` evidence).

- `src/founder_vn/panel.py` (`results_md`, dòng 491-492): thêm đoạn "Đây không phải tư vấn tài chính, thuế hay pháp lý." sau đoạn cảnh báo panel.
- `tests/test_panel_cli.py` (dòng 317): thêm assert đúng dòng đó vào test sẵn có ở seam CLI.
- `tests/golden/panel_tally.json`, `tests/golden/plan_full.json`, `examples/barbershop/founder/panel/results.md`, `examples/barbershop/founder/business-plan.md`: mỗi file thêm đúng một đoạn.
- `docs/evidence/issue-95-panel-tally-disclaimer.md`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape of the code, Tests, Owner-facing output, Git), `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (dòng 144: có miễn trừ trách nhiệm, có cảnh báo panel mô phỏng). Diff không chạm `docs/adr/` (thư mục không tồn tại).

## Kiểm tra theo chuẩn

- Một phép tính, hai transport: sửa ở `panel.results_md`, hàm chung của CLI và MCP; `tests/test_panel_parity.py` đã khẳng định byte-identical nên không cần slice transport mới. Đạt.
- Lớp khoá đường dẫn: diff không thêm đường ghi file nào. Đạt.
- Không số mặc định, không tỷ lệ thuế hay ngưỡng hardcode, không biến `FOUNDER_LLM_*` trong diff. Đạt.
- Test không gọi mạng; evidence ghi "No model and no network". Đạt.
- Đầu ra cho chủ hộ: tiếng Việt, không `$`. `scripts/skill_lint.py`: 6 skill, 15 file example, 0 finding. Đạt.
- Cùng câu chữ với `board.py:193` (miễn trừ trách nhiệm đã có). Đạt.
- Golden đổi: commit `f759de9` giải thích trong thân message rằng golden chỉ đổi đúng một dòng, và liệt kê từng file. Đạt.
- Mục checklist skill khác (link pháp lý, `metadata.version`, xưng "anh/chị") không bị chạm: không có thay đổi trong `skills/`, và phần cảnh báo "panel là mô phỏng, cận trên" vẫn còn nguyên.

## Hình dạng vòng lặp

- (a) `5e273e0` (`seam:` kèm `## Seam`) đứng trước `f759de9` (`slice(`). Đạt.
- (b) Commit duy nhất chạm `src/` (`f759de9`) cũng chạm `tests/test_panel_cli.py` và có một dòng trong `## Lát`. Đạt.
- (c) Test nằm ở seam đã khai (`results.md` qua CLI `panel tally`), không ở internals. Đạt.
- (d) Khối `## Cổng ba đoạn` ghi `verify: GREEN on f759de97164197768acc504554ccdb00b21b18de`; `f759de9` là commit mã cuối, `f2b87c5` chỉ thêm file evidence. Cổng không stale. Đạt.

## Đã chạy lại ở HEAD

`uv run ruff check .` sạch; `uv run ruff format --check .` sạch (212 file); `uv run pytest -q`: 364 passed; `python3 scripts/skill_lint.py`: 0 finding. CI `Gate` run 45574765586: success.

## Chưa xác minh

- Bằng chứng đỏ (1 failed, 31 passed) chỉ có trong bảng `## Lát` của evidence; commit slice gộp test và mã nên không thể tái hiện lần chạy đỏ từ git. Đây là dạng commit chuẩn đã khai trong `docs/agents/standards.md` (mục Git), nên không gắn mã.
- Hai golden JSON được sửa tay (repo chưa có lệnh sinh lại golden, evidence đã nêu); các test so sánh với đầu ra thật đều xanh, nên khớp đã được chứng minh.

<promise>PASS</promise>
