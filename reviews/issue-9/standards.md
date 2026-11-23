Commit mã đã chấm: 26278a08ded3

# Review trục Standards, issue #9, vòng 1

Phán quyết: CHANGES_REQUESTED (một finding chặn, S1; lane sửa được, không chạm file một-chủ).

## Phạm vi đã xét

`git diff --stat main...HEAD` (10 file, +1035/-2) và `git log --oneline main..HEAD` (9 commit: 1 `seam:`, 7 `slice(`, 1 `docs:`). Đọc: `src/founder_vn/panel.py`, `cli.py`, `server.py`, `tests/test_panel_cli.py`, `tests/test_panel_parity.py`, fixture và golden, `docs/evidence/issue-9-panel-bookkeeping.md`. Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `evidence-gates.md`, `parallel-lanes.md`, `docs/founder-vn-design.md`. Repo chưa có `CONTRIBUTING.md` nội dung liên quan, `docs/adr/` và `GLOSSARY.md` chưa tồn tại. Diff không chạm `skills/` hay `examples/`, nên checklist skill không áp dụng.

Đã chạy lại ở HEAD: `ruff check` sạch, `ruff format --check` sạch, `scripts/skill_lint.py` 0 finding, `pytest -q` 173 passed.

## Đạt

- Ghi file: mọi ghi và đọc dưới `founder/panel/` đi qua `files.write_text`/`files.read_text`; không có `open(..., "w")` hay `Path.write_text` trong `panel.py`. Có test `test_customer_outside_founder_is_refused`.
- Parity: `panel_init` và `panel_tally` bọc cùng hàm `panel.init`/`panel.run_tally` với CLI; `tests/test_panel_parity.py` so stdout và file từng byte.
- Test không gọi mạng, không dùng `FOUNDER_LLM_*`; panel không gác verdict, kết quả mang dòng "mô phỏng, cận trên".
- Lỗi thiếu trường nêu tên trường (`validate_customer`, `_weighted`, `_pair`); không có thuế suất hay ngưỡng thuế hardcode.
- Hình dạng vòng lặp: (a) `c49cd4e seam:` mang `## Seam` và đứng trước mọi `slice(`; (b) mọi commit chạm `src/` (`b4d4d25`, `9b5a781`, `7411144`, `03e0d76`, `eef3548`, `c4f705e`) cũng chạm test, và có dòng trong `## Lát` (`3ee15d8` chỉ chạm test, đỏ được chứng minh bằng đột biến); (c) test đi qua CLI và MCP, không import internals; (d) khối `## Cổng ba đoạn` ghi `GREEN on c4f705ed959b…`, đúng commit mã cuối `c4f705e`, chưa stale (`26278a0` chỉ đổi evidence).
- Golden `tests/golden/panel_tally.json`: commit `eef3548` nêu nguồn sinh (seed 7, n=7, fixture) và nội dung đã đọc.

## Finding chặn

### S1: mặc định `--n 100` lệch quyết định thiết kế "Panel mặc định `--n 20`"

- Chỗ: `src/founder_vn/cli.py` (`init_parser.add_argument("--n", type=int, default=100, ...)`, khối `panel init`); `src/founder_vn/server.py` (`panel_init(..., n: int = 100, ...)`).
- Sai gì: cả hai transport mặc định chia 100 người mua. Bản thiết kế ghi "Panel mặc định `--n 20` (100 là tùy chọn)" (`docs/founder-vn-design.md`, §3, mục panel; Q14 "Panel mặc định 20"). Chạy `founder-vn panel init` không tham số ra 100 thẻ thay vì 20, nên mỗi lượt chạy panel sau này tốn gấp 5 lần lời gọi mô hình mà chủ hộ không chọn. Mọi test đều truyền `--n` tường minh, nên không test nào đỏ vì lệch này.
- Chuẩn: `AGENTS.md` ("When code and the design disagree, the design wins and the fix lands in the same change"); `docs/agents/standards.md` mục Shape of the code (mặc định số phải theo thiết kế) và Tests (test nêu số).
- Vì sao chặn: mặc định là hành vi công khai của cả CLI lẫn MCP và lệch một quyết định thiết kế có số hiệu; `evidence` không ghi đây là quyết định của lane, nên không có cơ sở để giữ 100.
- Cách sửa (commit bổ sung, không viết lại lịch sử): đỏ trước, thêm test chạy `panel init` không `--n` và kiểm `personas.json` có 20 thẻ, trên cả CLI và `panel_init` (một dòng trong `test_panel_parity.py`); rồi đổi cả hai mặc định thành 20 (nên dùng một hằng chung trong `panel.py`, ví dụ `DEFAULT_N = 20`, để hai transport không lệch nhau); thêm dòng vào `## Lát` và chạy lại `gate-segment.sh verify` ở SHA mới, vì cổng hiện tại sẽ stale.

## Chưa xác minh

- `check` và `save` chỉ có ở CLI (`docs/evidence/issue-9-panel-bookkeeping.md`, mục Giới hạn nói ticket chỉ đòi MCP cho `panel_init`/`panel_tally`). `docs/agents/standards.md` nói tính năng chỉ ở một transport là chưa đầy đủ. Tôi không có thân ticket #9 nên không kiểm được phạm vi; trục Spec sẽ phân xử. Nếu ticket không loại hai lệnh này, đây thành finding chặn ở vòng sau.
- `THIN_GROUP = 8` trong `panel.py` là ngưỡng trình bày "(mỏng)", không phải ngưỡng thuế; thiết kế không nêu giá trị 8. Không coi là vi phạm, ghi lại để Spec đối chiếu.
- Bước làm tròn thu nhập 100.000 đ (`INCOME_STEP`) là quyết định của lane theo Q14 (thu nhập theo tháng); thiết kế không nêu bước. Lane đã ghi trong `## Quyết định của lane`.
- Kết quả CI `Gate` run 45107775100 ở tin nhắn mở đầu còn `in_progress`; tôi chỉ xác nhận được các lệnh chạy cục bộ ở trên.

<promise>CHANGES_REQUESTED</promise>
