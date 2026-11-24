Commit mã đã chấm: c53cb77e30bc

# Review trục Standards, issue #14, vòng 1

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

Diff `main...HEAD` (19 file, 8 commit: `0fa1596` seam, `67503c3`, `440d64f`, `f9d1fb2`, `915e493` slice, `599240f` và `c53cb77` evidence, `d1f6851` merge main). Đã đọc: `src/founder_vn/board.py`, phần đổi của `cli.py`, `server.py`, `panel.py`, ba file test `tests/test_board*.py`, `skills/founder-board/`, `examples/barbershop/founder/board*`, `docs/evidence/issue-14-founder-board.md`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/review-checklist.md`, `docs/founder-vn-design.md` (Q48, Q50, §2 về fan-out, bảng CLI↔MCP), `.kiro/skills/code-review/SKILL.md` (chỉ trục Standards, kèm smell baseline). `docs/adr/` và `CONTRIBUTING.md` chưa tồn tại; `docs/agents/parallel-lanes.md` không có file một-chủ nào bị diff chạm.

Máy chạy lại tại HEAD: `pytest tests/test_board.py tests/test_board_parity.py tests/test_board_skill.py` 24 passed; `scripts/skill_lint.py` 3 skills, 9 example file, 0 finding; `ruff check` sạch. CI `Gate` run 45329325114 success (theo tin nhắn giao việc).

## Kết quả theo mục chặn

- Ghi file: mọi lần ghi trong `board.py` đi qua `files.write_text`; không có `open(..., "w")` nào khác. Job nằm dưới `founder/board/jobs/`.
- CLI và MCP: `board run` / `board_run` cùng gọi `board.run`; `job_status` và `panel status` cùng `panel.job_status`; có `tests/test_board_parity.py` (đầu ra, file, trạng thái job, lỗi thiếu brief mã 2).
- Mạng: test dùng fixture `fake_provider`; không có endpoint thật. Biến `FOUNDER_LLM_*` trong test là giá trị giả (`khoa-gia`), không in ra.
- Số mặc định, tỷ lệ thuế: không có. Thiếu brief hoặc chưa cấu hình model là lỗi nêu tên file hoặc hướng dẫn cài.
- Model và prompt hash được ghi vào `board/board.json`; golden `board.json` có test.
- Tên khớp việc: `memo_problem`, `extract_memo`, `memo_md` làm đúng điều tên nói. Quy tắc "không nói thay tác giả" được thi hành bằng test prompt (`test_each_lens_prompt_carries_…`), không chỉ nằm trong comment.
- Thiết kế: lens Systems thay Monopoly (Q48) và `job_status` dùng chung (Q50) đúng như `docs/founder-vn-design.md`; lens không có thể quyết verdict (skill cấm, memo không đi vào `plan`).
- Golden: các file `examples/barbershop/founder/board/*` là file mới, không có golden cũ bị đổi; `panel.py` chỉ thêm tham số `root` mặc định `PANEL_DIR`, hành vi panel giữ nguyên (26 test panel cũ vẫn chạy trong gate).

## Checklist skill (`docs/review-checklist.md`)

- Không `$` cạnh chữ số: `skill_lint` 0 finding; test golden khẳng định `DOLLAR` không khớp `board.md` và memo.
- Không lọt tiếng Anh vào đầu ra cho chủ hộ; xưng "anh/chị". Phần Latin còn lại là tên sách, tên tác giả, tên skill và tên file.
- Khẳng định số liệu: `board.md` chỉ dùng con số đã có trong brief, không thêm số mới, không có khẳng định pháp lý.
- Miễn trừ trách nhiệm: có cả ở cuối `board.md` lẫn cuối mỗi memo.
- Cảnh báo mô phỏng: `board.md` và memo nói rõ đây là mô phỏng theo khung đã xuất bản, không thay khách hàng thật. Cụm "cận trên" của checklist gắn với tín hiệu cầu của panel người mua (`panel.py`, `plan.py`, design dòng 96); board không xuất tỷ lệ mua nên tôi không coi thiếu cụm này là finding.
- `metadata.version` là `0.1.0`, khớp phiên bản package; khối Protocol có đủ năm mục; frontmatter có `name`, `description` kèm cụm tiếng Việt, `license`, `author`, `source`, `commit`.

## Hình dạng vòng lặp

- (a) `0fa1596 seam:` mang `## Seam` và đứng trước mọi commit `slice(`. Đạt.
- (b) `67503c3` và `440d64f` chạm `src/` cùng test của lát; cả ba commit `slice(` đều có dòng trong `## Lát`. Đạt.
- (c) Test import bề mặt công khai (`board.run`, `board.prompt`, `board.memo_problem`, `panel.job_status`, `cli.main`); không test nào chạm hàm có dấu gạch dưới. Đạt.
- (d) Commit mã cuối là `915e493` (`c53cb77` chỉ đổi `docs/evidence/`, `d1f6851` đứng trước). Khối `## Cổng ba đoạn` ghi `verify` GREEN ở `915e4930186d…`. Đạt.

## Ghi chú phán đoán (không chặn, không gắn mã)

- `panel.job_status` (`panel.py` dòng 590-596) nhận biết "job không tồn tại" bằng `str(e).startswith("không thấy job")`, tức ghép vào nội dung thông báo lỗi. Có thể gọi là Mysterious Coupling kiểu smell; một lớp lỗi con sẽ bền hơn. Quy tắc nào của repo cũng không cấm, và `tests/test_board.py` bao phủ đường đi này.
- `board.py` gọi `panel._job_path` và `panel._read_job` (hàm riêng của module khác). Là Feature Envy mức nhẹ, có chủ đích (dùng chung runner, Q50).
- `start_job` ghi đè `board.json` bằng model và hash của lần chạy hiện tại, kể cả khi chạy lại chỉ hỏi các lens còn thiếu, nên memo cũ có thể đi kèm hash mới nếu brief đã đổi. `panel.start_job` làm y hệt, nên đây là mẫu sẵn có của repo, không phải lệch chuẩn của lane này.

## Chưa xác minh

- Tôi không có `.harness/gate-*.log`; số liệu "295 passed", "217 files" và `GREEN on 915e493` tôi lấy từ file evidence và từ CI đã nêu, không tự chạy lại toàn bộ gate ba đoạn.
- Lát golden brief (`f9d1fb2`) không có bước đỏ thực tế cho test `test_golden_brief_stands_alone_from_idea_md`, và các test memo/`board.json` của `915e493` đã xanh sẵn vì file đến từ lượt chạy thật. Evidence tự khai cả hai, đây là dữ liệu mẫu chứ không phải hành vi mới của mã, nên tôi không coi là finding chặn.
- Nguồn gốc lượt chạy thật trên Kiro CLI (model `gemini-3.5-flash-lite`) chỉ có lời khai trong evidence; mã không kiểm được.
- Nội dung `lenses.md` chưa ai đối chiếu với ba cuốn sách (evidence tự ghi ở mục Giới hạn).

<promise>PASS</promise>
