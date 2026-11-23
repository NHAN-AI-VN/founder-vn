Commit mã đã chấm: 573cedf8a2fb

# Review trục Standards, issue #11, vòng 1

**Phán quyết: BLOCKED** (một finding chặn, cần quyết định của operator về một quyết định thiết kế; không có finding nào khác).

## Phạm vi đã xét

`git diff --stat main...HEAD` (10 file, 934 dòng thêm) và `git log --oneline main..HEAD` (11 commit): `src/founder_vn/{llm,panel,cli,server}.py`, `tests/{conftest,test_llm,test_panel_cli,test_panel_parity,test_panel_run}.py`, `docs/evidence/issue-11-panel-run.md`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (§2 dòng 71 là chỗ liên quan), `docs/review-round5.md` dòng 50. Diff không chạm `skills/`, `examples/` hay golden file, nên checklist skill không áp dụng. Không có ADR bị chạm.

Đã chạy lại ở checkout này: `uv run ruff check .` sạch, `uv run ruff format --check .` sạch, `uv run pytest -q` 219 passed. CI `Gate` ở commit này: success.

## Kết quả theo từng chuẩn

- Khoá đường dẫn: mọi ghi (`panel.json`, `answers/*.json`, `jobs/J-*.json`) đi qua `files.write_text`; `_job_path` chỉ nhận `J-[0-9a-f]{8}`. Đạt.
- Parity CLI/MCP: `panel run`/`panel_run` và `panel status`/`job_status` cùng gọi `panel.run`/`panel.job_status`; có test parity byte-identical (`tests/test_panel_parity.py::test_panel_run_and_job_status_cli_equals_mcp_seed_7`). `panel work` là lệnh nội bộ ẩn, đã nêu trong mục Giới hạn của evidence. Đạt.
- Không mạng thật: test dùng fake provider trên 127.0.0.1; `tests/test_fixtures.py` là bài test của chính fixture. Đạt.
- Cấu hình thiếu là lỗi nêu tên biến (`llm.load_config`), không có nhà cung cấp mặc định; request chỉ có `model` và `messages`; JSON trích lỏng rồi kiểm (`extract_answer`); model và prompt hash ghi vào `panel.json`. Đạt.
- Không giá trị `FOUNDER_LLM_*` nào bị in ra: thông báo lỗi `CallFailed` không chứa URL hay khoá; test dùng giá trị giả. Đạt.
- Không tỷ lệ thuế hay ngưỡng pháp lý hardcode. Hằng số kỹ thuật (`WAVE`, `ATTEMPTS`, `BACKOFF`, `TIMEOUT`) được nêu trong evidence. Đạt.
- Hình dạng vòng lặp: (a) `9b64cf5 seam:` có `## Seam`, đứng trước mọi commit `slice(`. Đạt. (b) Các commit chạm `src/` có test của lát; ngoại lệ ghi ở mục "chưa xác minh" bên dưới. (c) Test nằm ở seam đã khai (`founder_vn.llm`, `founder_vn.panel`, CLI, MCP). Đạt. (d) `GREEN on 8ab316fef07f`, và `8ab316f` là commit mã cuối (`573cedf` chỉ đổi docs). Đạt.
- Bằng chứng đỏ rồi xanh: bảng `## Lát` có dòng cho mọi lát; lát "worker crash" đỏ bằng đột biến, đã ghi rõ.

## Finding chặn

### S1: tên công cụ MCP `job_status` và lệnh `panel status` lệch quyết định của bản thiết kế (`panel_status`)

- Chỗ: `src/founder_vn/server.py:76-79` (`def job_status`), `src/founder_vn/cli.py` (lệnh `panel status`), `tests/test_panel_parity.py:103-131`; ghi nhận ở `docs/evidence/issue-11-panel-run.md:35` ("the ticket wins and the design line is left for the operator").
- Sai gì: `docs/founder-vn-design.md:71` quyết định "`panel_run` và `board_run` là job bất đồng bộ (`job_id` + `panel_status`, …)", và `docs/review-round5.md:50` nhắc lại `panel_status`. Diff đặt tên công cụ poll là `job_status`. Lane tự chọn ticket hơn thiết kế và không sửa dòng thiết kế trong cùng thay đổi.
- Chuẩn: `AGENTS.md` dòng đầu ("When code and the design disagree, the design wins and the fix lands in the same change"); `docs/agents/evidence-gates.md` cuối ("no decision of the design has been bypassed").
- Vì sao chặn: tên công cụ MCP là giao diện công khai mà các skill sau này (`board_run`, skill `founder-panel`) sẽ gọi theo thiết kế. Đổi tên về sau là thay đổi phá giao diện. Chọn giữa tên của ticket và tên của thiết kế là quyết định thiết kế, không phải việc reviewer hay lane tự định; sửa đúng cách có thể là đổi mã về `panel_status` hoặc sửa `docs/founder-vn-design.md` dòng 71, cả hai đều cần operator chọn.

### Câu hỏi cho operator

- [ ] Tên công cụ MCP poll của job panel là `job_status` (ticket #11, đang ở mã) hay `panel_status` (thiết kế §2 dòng 71)? Nếu giữ `job_status`, cần sửa dòng 71 của `docs/founder-vn-design.md` (và ghi vào nhật ký quyết định) trong cùng thay đổi; nếu theo thiết kế, đổi `server.py`, tên lệnh `panel status` nếu cần cho khớp, test parity và evidence.
- [ ] `board_run` (cùng dòng thiết kế) sẽ dùng `job_status` chung hay một tên riêng? Câu trả lời quyết định tên nên chọn ở trên.

## Chưa xác minh

- Thân ticket #11 không có trong tài liệu giao cho lượt này, nên khẳng định "ticket gọi là `job_status`" trong evidence chưa kiểm được; lượt Spec xét việc ấy.
- Commit `2276f48` chạm `src/` mà không chạm test; test của lát được thêm ở `1c6c637` ngay sau đó, và evidence tự nêu điều này. Tôi coi commit bổ sung đó đã đáp ứng cách sửa ghi trong quy trình (không viết lại lịch sử), nên không gắn mã; đây là lệch nhẹ khỏi `docs/agents/standards.md` mục Git.
- Chưa chạy lại `scripts/harness/gate-segment.sh verify` (cần `.harness/` của lane); tôi chạy tay ba lệnh tương đương ở trên. Số liệu `GREEN on 8ab316f...` trong evidence là lời khai của lane, CI `Gate` xanh ở `573cedf8a2fb` hỗ trợ nó.
- Tác động đồng thời hai job trên cùng panel, và job MCP mất khi tiến trình server thoát: evidence đã nêu ở mục Giới hạn, nằm ngoài chuẩn đã ghi nên không xét thêm.

<promise>BLOCKED</promise>
