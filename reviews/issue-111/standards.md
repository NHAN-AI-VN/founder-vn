Commit mã đã chấm: 411ddbb3756e

# Review trục Standards, #111, vòng 1

Phán quyết: CHANGES_REQUESTED

## Phạm vi đã xét

`git diff --stat main...HEAD` (11 file) và `git log --oneline main..HEAD` (8 commit: `437dc44` seam, `c42749e`, `a171dd8`, `357f881` slice, hai commit golden/ví dụ, `4c8457c` design, `411ddbb` evidence). Đã đọc: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/evidence/issue-111-plan-permits-section.md`, diff của `src/founder_vn/plan.py`, `skills/founder-plan/SKILL.md`, `docs/founder-vn-design.md` (Q55, Q56, §9), `examples/barbershop/founder/business-plan.md`, `tests/golden/plan_*.json`, các test `test_plan_cli.py`, `test_plan_parity.py`, `test_plan_skill.py`. CI `Gate` ở `411ddbb3756e`: success (theo tin nhắn mở đầu).

Đã đạt:
- Không có file ghi ngoài lớp khoá đường dẫn, không số mặc định, không tỷ lệ thuế hardcode, không biến `FOUNDER_LLM_*` bị in.
- Phép tính nằm trong `plan.run`, CLI và MCP cùng gọi; có test parity `test_plan_with_permits_section_cli_equals_mcp`; đỏ của test parity được chứng minh bằng đột biến (ghi trong evidence).
- Hình dạng vòng lặp (a), (b), (c): `437dc44` (`seam:`, có `## Seam`) đứng trước mọi `slice(`; commit chạm `src/` (`c42749e`) chạm test cùng lát và có dòng trong `## Lát`; test ở seam đã khai.
- Golden đổi có giải thích trong message (`5c61ae6`, `49e7073`: "output changed because the section map gained permits").
- Q55, Q56 là số kế tiếp, tiêu đề Q1–Q56 khớp `AGENTS.md`.
- Checklist skill (`skills/founder-plan/SKILL.md`): không `$` cạnh chữ số, `metadata.version` không đổi, phần tiếng Anh/Việt theo quy ước skill; thay đổi chỉ thêm tên file và bảng ánh xạ, không thêm khẳng định pháp lý hay số liệu.

## Finding chặn

### S1: khối `## Cổng ba đoạn` không ghi `verify` GREEN ở SHA của commit mã cuối

- Chỗ: `docs/evidence/issue-111-plan-permits-section.md`, mục `## Cổng ba đoạn` (dòng 29 đến 31 ở HEAD).
- Sai gì: khối chỉ nói các đoạn "ran at the HEAD of the last code and docs commit (`4c8457c`)" và "The `verify` output is in the PR". Không có đầu ra của `gate-segment.sh verify`, không có dòng `GREEN on <sha>`. Ngoài ra `4c8457c` là commit docs; commit mã cuối là `357f881` (chạm `tests/`) hoặc `c42749e` (chạm `src/`), nên không đọc được từ file rằng cổng xanh đúng ở commit mã cuối. Một PR chưa tồn tại thì "trong PR" không phải bằng chứng nằm trong repo.
- Chuẩn: `docs/agents/evidence-gates.md`, mục "Where evidence lives" (khối `## Cổng ba đoạn` gồm ba lệnh `gate-segment.sh` và đầu ra của `verify`, `GREEN on <sha>` phải nêu commit mã cuối); `AGENTS.md` quy tắc 5 (bằng chứng ở trong repo, không ở câu trả lời).
- Vì sao chặn: bước 4(d) của hướng dẫn review coi thiếu mục này là finding chặn; thiếu nó thì không phân biệt được cổng xanh ở commit mã cuối với cổng đã stale.
- Cách sửa (trong phạm vi lane, file `docs/evidence/` của chính ticket): chạy ba đoạn `scripts/harness/gate-segment.sh static|unit|build` rồi `gate-segment.sh verify` ở HEAD, dán lệnh và đầu ra có `GREEN on <sha>` vào khối, bằng một commit bổ sung. Lưu ý: commit bổ sung chỉ chạm docs nên SHA mã cuối vẫn là `357f881`; không viết lại lịch sử.

## Chưa xác minh

- Không chạy lại `uv run pytest` hay `gate-segment.sh verify` ở sandbox này; dựa vào CI `Gate` success đã nêu trong tin nhắn mở đầu. Con số "368 passed" trong evidence chưa đối chiếu độc lập.
- Nội dung `.harness/gate-*.log` mà evidence viện dẫn không nằm trong cây git, nên không kiểm được.

<promise>CHANGES_REQUESTED</promise>
