Commit mã đã chấm: ca3c7ed4621f

# Review trục Standards, #94, vòng 2

Phán quyết: PASS (S1 của vòng 1 đã được sửa; không còn finding chặn).

## S1 của vòng 1: đã sửa

`ca3c7ed` sửa bullet installer trong `docs/agents/standards.md`, mục "Shape of the code". Bullet nay nêu tập đích cố định `install.REGISTRATION_FILES` (`.kiro/settings/mcp.json`, `.mcp.json`, `.codex/config.toml`, `.grok/config.toml`), nội dung do package cố định, chỉ ghi khi file chưa có (kể cả symlink treo thì để nguyên), không gộp, không xoá. Nó giữ việc kiểm đường dẫn nằm trong project với `InstallRefused` và exit code 2 trước khi ghi gì, nói giới hạn `.md`/`.json` không áp cho `.toml` vì cùng lý do, nêu KiroCrew vẫn print-only, và dẫn Q54 và #94. Nội dung khớp `src/founder_vn/install.py` (`REGISTRATION_FILES`, `_plan_registration`, `_write_registration`; `os.path.lexists` cho trường hợp symlink treo). `AGENTS.md` đã đổi Q1–Q53 thành Q1–Q54. `f28dae3` chỉ thêm `reviews/issue-94/ledger.md`.

## Phạm vi đã xét

`git diff --stat main...HEAD` (20 file) và `git log --oneline main..HEAD`. Đã đọc `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (§5, Q54), `CONTRIBUTING.md` (có; quy tắc liên kết pháp lý và không ghi giá trị `FOUNDER_LLM_*` không bị diff chạm), `docs/evidence/issue-94-installer-writes-mcp.md`, `install.py`, test và golden. Diff không chạm `skills/` hay `examples/`, nên checklist skill không áp dụng. Không có ADR nào bị chạm. Diff vòng 2 so với vòng 1 (`14e577a..ca3c7ed`) chỉ là một dòng trong `docs/agents/standards.md`, nên các mục đạt của vòng 1 (kiểm đường dẫn trước khi ghi, không xoá, `--print-only` không ghi, CLI-only nên không cần parity, không mạng, không giá trị `FOUNDER_LLM_*`, golden đổi có giải thích ở message `3a650f4`) giữ nguyên.

Hình dạng vòng lặp: (a) `463b02d seam:` với mục `## Seam` đứng trước mọi `slice(`; (b) `ae32b66` và `5808f8a` chạm `src/` đều chạm `tests/test_install.py` và có dòng trong `## Lát`; (c) test gọi `install.run`, seam đã khai; (d) cổng ghi ở `b2c5f1a`, hậu duệ của commit `src/` cuối (`5808f8a`). Các commit sau (`bf4b9a3`, `ca3c7ed`, `f28dae3`) chỉ đổi tài liệu và review; CI `Gate` success ở `f28dae3`.

## Chưa xác minh

- Đã chạy thử: nếu `.codex` (tương tự `.grok`) là file thường, `install.run(..., "codex", False)` ném `FileExistsError` thô từ `mkdir` trong `_write_registration`. Với `.kiro` là file thường, lỗi `NotADirectoryError` thô đã xảy ra ở bước chép skill, trước cả bước đăng ký. Không có chuẩn đã ghi nào yêu cầu thông báo lỗi sạch cho trường hợp này, và bước chép skill ở `main` cũng không bắt lỗi tương tự, nên không gắn mã. Operator có thể muốn một ticket riêng.
- Chưa xác minh `.codex/config.toml` và `.grok/config.toml` bằng host thật (evidence đã ghi ở `## Giới hạn`).

<promise>PASS</promise>
