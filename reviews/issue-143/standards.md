Commit mã đã chấm: 7cb6894 (commit mã cuối; HEAD ffa4b0fa3dd2 chỉ đổi file bằng chứng)

# Review trục Standards, #143, vòng 1

Phán quyết: CHANGES_REQUESTED

## Phạm vi đã xét

`git diff --stat main...HEAD` (10 file) và `git log --stat main..HEAD` (3 commit: `seam:`, `slice(panel.init)`, `docs:`). Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape of the code, Tests, Owner-facing output, Skills, Git), `docs/agents/evidence-gates.md` (Where evidence lives), `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` §2 và Q58. Đã đọc `src/founder_vn/panel.py`, `src/founder_vn/server.py`, `skills/founder-consumer/SKILL.md` và các test thêm vào. Không chạy lại gate; CI `Gate` run 45962968015 là success ở `ffa4b0fa3dd2`.

## Finding chặn

### S1: khối `## Cổng ba đoạn` không ghi `verify` GREEN ở SHA của commit mã cuối

- Chỗ: `docs/evidence/issue-143-panel-init-redeal-guard.md`, mục `## Cổng ba đoạn`. Nội dung duy nhất là "See the `verify` output of the last HEAD (`.harness/gate-segments.txt`)".
- Sai gì: khối không có ba lệnh `gate-segment.sh static|unit|build`, không có đầu ra của `gate-segment.sh verify`, và không có `GREEN on <sha>`. Nó trỏ tới `.harness/gate-segments.txt`, thư mục này không nằm trong cây git (`ls .harness` không thấy) nên người đọc PR không kiểm được. Commit mã cuối là `7cb6894`, nên dòng `GREEN on` phải ghi SHA đó (hoặc một hậu duệ của nó mà không đổi mã).
- Chuẩn: `docs/agents/evidence-gates.md`, "Where evidence lives" (khối đóng bằng ba lệnh và đầu ra `verify`, `GREEN on <sha>` phải nêu commit mã cuối) và "Operating rules" 3 (tự khai không phải bằng chứng); `AGENTS.md` quy tắc 5.
- Vì sao chặn: bước (d) của vòng lặp. CI xanh không thay thế được bằng chứng trong repo, và tham chiếu tới file ngoài cây không kiểm chứng được.
- Cách sửa (commit bổ sung, không viết lại lịch sử): chạy `bash scripts/harness/gate-segment.sh static`, `unit`, `build`, rồi `verify` ở HEAD; dán lệnh và đầu ra có `GREEN on <sha>` vào khối đó.

## Đã đối chiếu, không có finding

- (a) `17a762e seam:` có `## Seam` và đứng trước `slice(`.
- (b) Commit chạm `src/` (`7cb6894`) cũng chạm `tests/test_panel_cli.py`, `tests/test_panel_parity.py`, `tests/test_consumer_skill.py`; mỗi test có dòng trong `## Lát` (kèm lệnh đỏ: 9 failed, 7 passed; xanh: 63 passed).
- (c) Test ở seam đã khai: CLI `panel init`, MCP `panel_init`, SKILL.md. Không có test vào `_refuse_other_deal`.
- Parity: `panel.init` là một hàm, hai đường CLI và MCP; `test_panel_init_refusal_is_the_same_text_through_cli_and_mcp` khẳng định cùng văn bản.
- Đường ghi file: guard chỉ đọc qua `files.resolve` và `files.read_text`; không có đường ghi mới.
- Không có mạng, không có tỷ lệ hay ngưỡng hardcode, không in biến `FOUNDER_LLM_*`.
- Skill: câu thêm vào `founder-consumer/SKILL.md` không có `$`; chỉ chạm một bước hướng dẫn, `metadata.version` không đổi; chuỗi dành cho chủ hộ (lỗi từ chối) bằng tiếng Việt. Không thêm khẳng định pháp lý hay số liệu, nên không cần link mới.
- Golden file: không đổi.
- Số quyết định `Q1–Q58` khớp giữa `AGENTS.md`, phụ lục thiết kế và `tests/test_install.py`.

## Ghi nhận không chặn

Evidence tự khai `## Lát` rằng các lát đỏ-xanh nằm trong một commit mã thay vì mỗi lát một commit `slice(`, trái `docs/agents/standards.md` mục Git ("one commit `slice(<seam>)`: per red-green slice"). Bước (b) của hướng dẫn chỉ đòi test cùng commit và dòng trong `## Lát`, cả hai đã có, nên không gắn mã. Không sửa bằng viết lại lịch sử.

## Chưa xác minh

- Q58 ghi "quyết định của operator, từ #143". Thân ticket không có trong repo và sandbox không có quyền API, nên không đối chiếu được nó khớp ticket. Nếu operator chưa quyết, đó là quyết định thiết kế chưa có và phán quyết đổi thành BLOCKED.
- Không chạy lại `pytest`, `ruff`, `skill_lint.py` cục bộ; tin CI run 45962968015.
- Số "9 failed, 7 passed" của lần chạy đỏ chỉ có trong lời khai của evidence, không có artefact.

<promise>CHANGES_REQUESTED</promise>
