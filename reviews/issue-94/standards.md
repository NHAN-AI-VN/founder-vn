Commit mã đã chấm: bf4b9a3018ef

# Review trục Standards, #94, vòng 1

Phán quyết: CHANGES_REQUESTED (một finding chặn, S1, lane này sửa được).

## Phạm vi đã xét

`git diff --stat main...HEAD` (16 file) và `git log --oneline main..HEAD` (6 commit: `seam:`, hai `slice(install)`, một `slice(install-cli)`, hai `docs:`). Đã đọc `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (§5 và Q54), `docs/evidence/issue-94-installer-writes-mcp.md`, `src/founder_vn/install.py` và các test, golden mới. Diff không chạm `skills/` hay `examples/`, nên checklist skill không áp dụng. `CONTRIBUTING.md` không đọc (chưa xác minh là có hay không). Không có ADR nào bị chạm.

Các mục đạt:
- Ghi file: `_plan_registration` kiểm đường dẫn đã resolve nằm trong project trước khi chép bất cứ gì, có test symlink thoát (`InstallRefused`). Không xoá, `--print-only` không ghi.
- CLI-only: không có phép tính mới, installer đã được miễn parity.
- Không mạng, không giá trị `FOUNDER_LLM_*`, không số mặc định hay tỷ lệ thuế.
- Hình dạng vòng lặp: (a) `seam:` đứng trước mọi `slice(`; (b) hai commit chạm `src/` (`ae32b66`, `5808f8a`) đều chạm `tests/test_install.py` và có dòng trong `## Lát`; (c) test gọi `install.run`, seam đã khai; (d) khối `## Cổng ba đoạn` ghi cổng ở `b2c5f1a`, là hậu duệ của commit mã cuối (`3a650f4`), chỉ `bf4b9a3` (evidence) đứng sau.
- Golden đổi (`tests/golden/install_*.json`) có giải thích trong message của `3a650f4`.

## Finding chặn

### S1: `docs/agents/standards.md` vẫn ghi installer chỉ ghi file skill, mã nay ghi thêm file đăng ký MCP

- Chỗ nó ở: `docs/agents/standards.md`, mục "Shape of the code", bullet "The installer (`founder_vn.install`, …)"; đối chiếu `src/founder_vn/install.py` (`REGISTRATION_FILES`, `_write_registration`). Diff không sửa `docs/agents/standards.md`.
- Điều sai: bullet đó nói installer ghi `<project>/<host skills folder>/<skill>/…` và "the files it writes are exactly the files shipped under the package's `skills/<name>/`". Sau #94 installer còn ghi `.kiro/settings/mcp.json`, `.mcp.json`, `.codex/config.toml`, `.grok/config.toml`: các file nằm ngoài `SKILL_FOLDERS`, không nằm trong `skills/`, và `.toml` nằm ngoài giới hạn `.md`/`.json` của lớp khoá. Bullet liền trước ("No other code path opens a file for writing, with the one exception below") chỉ miễn trừ đúng tập file cũ. Quy tắc đã ghi nay sai so với mã, và mã ghi ra ngoài tập mà chuẩn cho phép.
- Chuẩn vi phạm: `docs/agents/standards.md`, "Shape of the code" (ngoại lệ của installer với lớp khoá đường dẫn, chỉ cấp cho tập file cố định đã liệt kê); `AGENTS.md` ("When code and the design disagree, the design wins and the fix lands in the same change"). Q54 trong `docs/founder-vn-design.md` là quyết định của operator đã ghi, nên đây không phải quyết định thiết kế mới: chỉ thiếu việc đưa nó vào file chuẩn.
- Vì sao chặn: một lượt Standards sau sẽ đọc bullet cũ và coi bốn file đăng ký là ghi trái phép, hoặc người khác thêm đích ghi mới viện cớ "installer được miễn". Ngoại lệ ngoài lớp khoá phải được liệt kê chính xác trong chuẩn. `docs/agents/standards.md` không nằm trong danh sách một-chủ của `docs/agents/parallel-lanes.md`, nên lane này sửa được bằng commit bổ sung.
- Cách sửa (commit bổ sung, không viết lại lịch sử): cập nhật bullet để nêu thêm tập đích cố định `REGISTRATION_FILES` (bốn đường dẫn trên, nội dung do package cố định, chỉ ghi khi file chưa có, không gộp, không xoá, vẫn kiểm tra nằm trong project và `InstallRefused` trước khi ghi gì), nói rõ giới hạn `.md`/`.json` không áp dụng cho `.toml` vì cùng lý do, và dẫn Q54 cùng #94.

## Chưa xác minh

- Lượt này không chạy lại Gate; kết quả CI `success` ở `bf4b9a3018ef` lấy từ tin nhắn giao việc.
- `_write_registration` gọi `mkdir(parents=True, exist_ok=True)`: nếu `.kiro`, `.codex` hay `.grok` là file thường thì có thể ném `FileExistsError` thô, sau khi các file skill đã được chép. Chưa có test, chưa chạy thật; đây là nghi v���n về cách báo lỗi, không gắn mã.
- Nội dung `.codex/config.toml` và `.grok/config.toml` được kiểm bằng parse TOML, không bằng host thật (evidence đã ghi ở `## Giới hạn`).

<promise>CHANGES_REQUESTED</promise>
