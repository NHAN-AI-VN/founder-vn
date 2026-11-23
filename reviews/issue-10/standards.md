Commit mã đã chấm: 1faa999d0175

# Review trục Standards, #10, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD` (8 file) và `git log --oneline main..HEAD` (6 commit: `8c302dc` seam, bốn `slice(plan)`, `1faa999` evidence). Đối chiếu với `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md` và `docs/founder-vn-design.md` (dòng 16, 94, 172). `docs/adr/` chưa tồn tại. Diff không chạm `skills/` hay `examples/`, nên checklist skill không áp dụng.

## Kết quả theo chuẩn

- Khoá đường dẫn: `plan.py` chỉ ghi qua `files.write_text` và đọc qua `files.read_text` / `files.resolve`. `--check` không ghi gì.
- Hai transport: `plan.run` là một hàm duy nhất, được `cli.py` (`plan [--check]`) và `server.py` (`plan_compile`) bọc. `tests/test_plan_parity.py` so stdout và file byte-identical, có và không panel, có `check`.
- Không có số mặc định cho trường số: `numbers.json` hỏng đi qua `cfo.analyse` và báo lỗi nêu tên trường, CLI trả mã 2. `panel/results.json` thiếu `buys`/`passes` báo lỗi nêu tên trường. Không có thuế suất hay ngưỡng hardcode (các ngưỡng `> 0` là định nghĩa của ba phép kiểm).
- Verdict chỉ nhận đầu ra của `cfo.analyse`; `panel_line` tách riêng và có test panel không đổi verdict (đã chứng kiến đỏ bằng đột biến, ghi ở `## Lát`).
- Đầu ra cho chủ hộ: tiếng Việt, "anh/chị", VND qua `format_vnd`, không `$`, có miễn trừ trách nhiệm và cảnh báo "mô phỏng, cận trên" ở dòng panel và phần lưu ý.
- Test: không mạng, không model; golden `plan_full.json`, `plan_numbers_only.json` là file mới và commit `d485d6b` ghi cách sinh ra.
- Không có giá trị `FOUNDER_LLM_*` trong diff.
- Hình dạng vòng lặp: (a) `8c302dc` seam có `## Seam` đứng trước mọi `slice(`; (b) bốn commit slice đều chạm `src/` cùng test và đều có dòng trong `## Lát`; (c) test đi qua `founder_vn.cli.main` và công cụ MCP, tức seam đã khai; (d) `## Cổng ba đoạn` ghi `verify` `GREEN on d42bbf79...`, đúng commit mã cuối (`1faa999` chỉ đổi docs).
- Đo lại: `ruff check` sạch, `ruff format --check` sạch, `pytest tests/test_plan_cli.py tests/test_plan_parity.py` 21 passed. CI `Gate` run 45115901896: success.

## Chưa xác minh

- Không thuộc finding: `plan.py` gọi hàm riêng `cfo._load` từ module khác. Chuẩn đã ghi không cấm điều này, nên chỉ ghi nhận.
- Số khẳng định "6 failed", "3 failed" ở cột đỏ của `## Lát` tôi không chạy lại ở các commit trung gian.

<promise>PASS</promise>
