Commit mã đã chấm: db6ebd675522

# Review trục Standards, issue #11, vòng 1 (chạy lại sau trả lời của operator)

**Phán quyết: PASS** (không còn finding chặn).

## Phạm vi đã xét

`git diff --stat main...HEAD` (16 file) và `git log --oneline main..HEAD` (14 commit). Mã: `src/founder_vn/{llm,panel,cli,server}.py`; test: `tests/{conftest,test_llm,test_panel_cli,test_panel_parity,test_panel_run}.py`; tài liệu: `docs/evidence/issue-11-panel-run.md`, `docs/founder-vn-design.md`, `AGENTS.md`, `reviews/issue-11/{operator-answer,ledger}.md`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` §2 và Q31/Q50. Diff không chạm `skills/`, `examples/` hay golden file, nên checklist skill không áp dụng. Không có ADR bị chạm.

Thay đổi kể từ lượt trước (`573cedf8a2fb`): `git diff 573cedf..HEAD -- src tests skills examples` rỗng. Commit `db6ebd6` chỉ đổi tài liệu và file review.

Đã chạy lại ở checkout này: `uv run ruff check .` sạch, `uv run ruff format --check .` sạch (122 file), `uv run pytest -q` 219 passed. CI `Gate` ở `db6ebd675522`: success.

## Đóng finding S1 của lượt trước

S1 (tên tool poll `job_status` lệch dòng 71 của thiết kế, `panel_status`) đã được đóng bằng quyết định của operator, không bằng đổi mã:

- `docs/founder-vn-design.md` §2 (dòng 71-73) nay ghi `job_id` + `job_status`, một tool poll chung cho mọi loại job (Q50). Mã (`server.py`, lệnh `panel status`, `tests/test_panel_parity.py`) khớp thiết kế.
- Q50 có trong nhật ký quyết định (dòng 273-278), Q31 trỏ tới Q50, tiêu đề phụ lục và `AGENTS.md` đổi thành Q1–Q50. Quy tắc "thiết kế thắng, sửa cùng thay đổi" (`AGENTS.md` dòng đầu) được giữ: thiết kế sửa trong cùng nhánh lane trước khi merge.
- `reviews/issue-11/operator-answer.md` tick cả hai ô; `reviews/issue-11/ledger.md` có dòng `S1 FIXED`.
- Còn một chỗ ghi `panel_status`: `docs/review-round5.md:50`. Quyết định Q50 nêu rõ file này là biên bản phản biện có ngày, không phải nguồn luật, nên không phải lệch thiết kế.

## Kết quả theo từng chuẩn

- Khoá đường dẫn: mọi ghi (`panel.json`, `answers/*.json`, `jobs/J-*.json`) đi qua `files.write_text`; `_job_path` chỉ nhận `J-[0-9a-f]{8}`. Đạt.
- Parity CLI/MCP: `panel run`/`panel_run` và `panel status`/`job_status` cùng gọi `panel.run`/`panel.job_status`; test parity byte-identical `tests/test_panel_parity.py::test_panel_run_and_job_status_cli_equals_mcp_seed_7`. `panel work` là lệnh nội bộ ẩn, đã nêu ở mục Giới hạn của evidence. Đạt.
- Không mạng thật: test dùng fake provider trên 127.0.0.1. Đạt.
- Cấu hình thiếu là lỗi nêu tên biến, không có nhà cung cấp mặc định; request chỉ có `model` và `messages`; JSON trích lỏng rồi kiểm; model và prompt hash ghi vào `panel.json`. Đạt.
- Không giá trị `FOUNDER_LLM_*` nào bị in ra; test dùng giá trị giả. Đạt.
- Không tỷ lệ thuế hay ngưỡng pháp lý hardcode; hằng số kỹ thuật (`WAVE`, `ATTEMPTS`, `BACKOFF`, `TIMEOUT`) nêu trong evidence. Đạt.
- Hình dạng vòng lặp: (a) `9b64cf5 seam:` có `## Seam`, đứng trước mọi commit `slice(`. (b) Các commit chạm `src/` có test của lát; ngoại lệ ở mục "chưa xác minh". (c) Test nằm ở seam đã khai. (d) `GREEN on 8ab316fef07f` và `8ab316f` là commit mã cuối (các commit sau chỉ đổi docs và review). Đạt.
- Bằng chứng đỏ rồi xanh: bảng `## Lát` có dòng cho mọi lát; lát "worker crash" đỏ bằng đột biến, đã ghi rõ.

## Chưa xác minh

- Commit `2276f48` chạm `src/` mà không chạm test; test của lát thêm ở `1c6c637` ngay sau, evidence tự nêu. Đó đúng là cách sửa quy trình cho phép (commit bổ sung, không viết lại lịch sử), nên không gắn mã; đây là lệch nhẹ khỏi `docs/agents/standards.md` mục Git.
- Chưa chạy lại `scripts/harness/gate-segment.sh verify` (cần `.harness/` của lane); đã chạy tay ba lệnh tương đương ở trên. Dòng `GREEN on 8ab316f...` trong evidence là lời khai của lane, CI `Gate` xanh ở `db6ebd675522` hỗ trợ nó.
- Thân ticket #11 và spec #1 không có trong tài liệu giao cho lượt này, nên các trích dẫn của operator-answer về spec/T08/T12/T15 chưa kiểm được; lượt Spec xét phần đó.
- Đồng thời hai job trên cùng panel và job MCP mất khi tiến trình server thoát: evidence đã nêu ở mục Giới hạn, nằm ngoài chuẩn đã ghi.

<promise>PASS</promise>
