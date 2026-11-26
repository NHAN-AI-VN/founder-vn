Commit mã đã chấm: 272ed5e692d5

# Review trục Standards, #114, vòng 1

Phán quyết: CHANGES_REQUESTED

## Phạm vi đã xét

`git diff --stat main...HEAD` (7 file) và `git log --stat main..HEAD` (6 commit: `4c83039` seam, `fa9fdbf`, `92c8388`, `bf83bf5`, `b876e29` lát, `272ed5e` evidence). Đã đọc `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `.kiro/skills/code-review/SKILL.md`, `skills/founder-ops/SKILL.md`, `examples/barbershop/founder/ops.md`, `docs/evidence/issue-114-founder-ops.md`. `docs/adr/` không tồn tại. Đã chạy ở checkout này: `uv run python scripts/skill_lint.py` (8 skill, 17 file ví dụ, 0 finding), `uv run pytest -q` (404 passed), `uv run ruff check .` và `uv run ruff format --check .` (sạch).

Đã kiểm và không có finding:
- Diff không chạm `src/`: không có phép tính mới nên không có vấn đề CLI/MCP parity, đường dẫn ghi, hay số mặc định.
- Checklist skill: không `$` cạnh chữ số (lint xanh); `ops.md` bằng tiếng Việt, xưng "anh/chị"; có miễn trừ trách nhiệm ở mục 7; không có khẳng định pháp lý hay số liệu cần link (mục 6 chỉ trỏ tới `founder/permits.md`); không có kết quả panel nên không cần cảnh báo "panel là mô phỏng"; `metadata.version` "0.2.0" khớp package 0.2.0; frontmatter có `name` khớp thư mục, `license`, `author`, `source`, `commit`; khối Protocol giống `founder-pricing`.
- Hình dạng vòng lặp (a): `4c83039` là commit `seam:` đầu tiên và mang `## Seam`. (b): không commit nào chạm `src/`; mỗi commit slice chạm test của lát và có dòng trong `## Lát`. (c): test ở seam đã khai (`tests/test_ops_skill.py`, `test_plan_example.py`, `test_front_door.py`), không ở internals.
- Golden `business-plan.md` đổi: commit `bf83bf5` nêu lý do (có `ops.md` nên thêm mục Vận hành), evidence ghi +104/-1.
- Không có biến `FOUNDER_LLM_*`, mạng hay dữ liệu thật trong diff.

## Finding chặn

### S1: khối `## Cổng ba đoạn` không ghi `verify` GREEN ở một SHA

- Chỗ: `docs/evidence/issue-114-founder-ops.md`, dòng `bash scripts/harness/gate-segment.sh verify    # see the PR body for the HEAD it was green on`.
- Sai gì: dòng `verify` không ghi `GREEN on <sha>`, mà trỏ sang thân PR. Một lane kết thúc ở PR nhưng bằng chứng phải nằm trong repo; không thể đối chiếu SHA với commit mã cuối (`bf83bf5`/`b876e29`, tùy cách tính commit chạm test và README) nên không kiểm được cổng có stale hay không. Ba đoạn `static`, `unit`, `build` có ghi exit 0 nhưng không có SHA.
- Chuẩn: `docs/agents/evidence-gates.md`, mục "Where evidence lives" (khối `## Cổng ba đoạn` phải có output của `gate-segment.sh verify`, `GREEN on <sha>` nêu commit mã cuối) và nguyên tắc 3, "Reproducible evidence"; `AGENTS.md` quy tắc 5 (một khẳng định chỉ có trong câu trả lời hay thân PR không phải bằng chứng). Phép kiểm hình dạng vòng lặp (d) của lượt review này.
- Vì sao chặn: thiếu (d) là finding chặn theo hướng dẫn trục Standards.
- Cách sửa (commit bổ sung, không viết lại lịch sử): chạy lại ba đoạn `gate-segment.sh static|unit|build` rồi `verify` ở HEAD, dán dòng `gate-segment sau verify: GREEN on <sha>` vào khối, với SHA là commit mã cuối hoặc hậu duệ chỉ gồm commit docs/evidence (script đã in nhắc nhở này).

## Chưa xác minh

- Không chạy `gate-segment.sh build` và `verify` ở đây (không ghi ledger `.harness/` để khỏi tạo file ngoài báo cáo). CI `Gate` run 45753556274 ở `272ed5e692d5` báo success theo tin nhắn mở đầu.
- Cách diễn đạt "Restate no legal figure ... (restate no legal figure at all)" ở mục 6 của `skills/founder-ops/SKILL.md` lặp ý; không vi phạm chuẩn nào, chỉ nên gọn lại khi sửa.
- Lịch ca và "tối đa 5 ca một tuần" trong `ops.md` là đề xuất về vận hành, thuộc trục Spec, không xét ở đây.

<promise>CHANGES_REQUESTED</promise>
