Commit mã đã chấm: a9f2ed2d5bfd

# Review trục Standards, issue #18, vòng 1 (HEAD mới)

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD`: 10 file ngoài báo cáo này (README.md, docs/evidence/issue-18-founder-plan.md, docs/review-checklist.md, `examples/barbershop/founder/{business-plan,summary}.md`, `skills/founder-plan/SKILL.md`, `tests/test_plan_example.py`, `tests/test_plan_skill.py`, `tests/test_wave_a_checklist.py`, reviews/issue-18/spec.md). Không file nào dưới `src/`, `scripts/`, `pyproject.toml`, `uv.lock`. `git log --oneline main..HEAD`: 13 commit, gồm `4f53bce` seam, các slice `1d99c0e`, `c512614`, `41fcefb`, hai slice sửa review `7ade152`, `1afc6fe`, commit docs `eeb34ea` (checklist), evidence `8a5b59a`, `827dd83`, `a9f2ed2`, và các commit review.

So với lượt trước (8a5b59a) tôi xét lại phần mới: `7ade152`, `1afc6fe`, `eeb34ea`, `827dd83`, `a9f2ed2`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape, Tests, Owner-facing, Skills, Git), `docs/agents/evidence-gates.md`, `docs/review-checklist.md`, `.kiro/skills/code-review/SKILL.md` (trục Standards).

## Kiểm tra đã chạy ở a9f2ed2

- `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 196 file đã định dạng.
- `uv run python scripts/skill_lint.py`: 6 skills, 15 example file, 0 finding (package 0.1.0).
- `uv run pytest -q`: 347 passed.
- CI `Gate` run 45342730025 ở cùng commit: success (theo tin nhắn mở đầu).

## Theo từng mục chuẩn

- **Parity CLI/MCP, khóa đường dẫn, số mặc định, hằng thuế:** diff không thêm mã Python; `plan.py` không đổi. Thuế suất 7% và ngưỡng trong `summary.md` chép từ `cfo.md` / `permits/sources.md`, không là hằng số trong mã.
- **Mạng và biến `FOUNDER_LLM_*`:** ba file test chỉ đọc file và gọi `plan.compile_plan` / `plan.run(check=True)`; không có client LLM, không in giá trị biến.
- **Verdict chỉ từ số CFO:** skill ghi "Never write the verdict" (Protocol 5, Step 2.3, Rules); `business-plan.md` do `founder-vn plan` sinh và test so với `plan.compile_plan`. Test mới `test_failing_check_table_matches_the_labels_the_compiler_prints` buộc ba hàng bảng Step 3 của skill bằng nhãn compiler in ra cho ba fixture Not yet.
- **Checklist skill** (diff chạm `skills/` và `examples/`):
  - Không `$` cạnh chữ số: lint 0 finding.
  - Không lọt tiếng Anh: phần còn lại là tên riêng và nhãn verdict của công cụ; `eeb34ea` ghi danh sách tên được chấp nhận vào `docs/review-checklist.md`, đúng chỗ mà quy tắc được thi hành bằng đọc của reviewer.
  - Xưng "anh/chị": có trong skill và `summary.md` (phần 1 và mục Lưu ý).
  - Link chính thức và ngày: bản một trang giờ dẫn Luật 48/2024/QH15, Luật 109/2025/QH15 và Nghị định 253/2026/NĐ-CP, ngày 23/11/2026; ba URL này có đúng trong `cfo.md`, `business-plan.md` và `permits/sources.md` (đã grep). Số 7% khớp tổng GTGT 5% và TNCN 2%.
  - Miễn trừ trách nhiệm và cảnh báo "mô phỏng, cận trên, không phải khách hàng thật": có ở cả hai phần của `summary.md` và đóng file theo thứ tự caveat rồi disclaimer, khớp Step 4 của skill (quan sát không chặn của lượt trước đã được xử lý).
  - `metadata.version` "0.1.0" khớp package.
- **Hình dạng vòng lặp:**
  - (a) `4f53bce seam:` mang `## Seam` và đứng trước mọi commit `slice(`. Đạt.
  - (b) Không commit nào chạm `src/`. Mỗi commit `slice(` chạm test của lát (`7ade152`: `test_plan_example.py`; `1afc6fe`: `test_plan_skill.py`) và có dòng trong `## Lát`. Đạt.
  - (c) Test ở seam đã khai (văn bản skill, file ví dụ, README, checklist). Đạt.
  - (d) `## Cổng ba đoạn` ghi `verify: GREEN on 827dd83…`. `git diff --stat 827dd83 HEAD` chỉ đổi file evidence, nên 827dd83 không là tổ tiên của một commit mã nào; cổng không stale. Đạt.
- **Đỏ rồi xanh:** hai lát sửa review có dòng đỏ. Lát `7ade152` đỏ bằng hai AssertionError thật; lát `1afc6fe` ghi đỏ bằng đột biến (đổi tên hàng bảng), được khai là mutation, không phải đỏ tự nhiên.
- **Golden file:** `summary.md` đổi ở `7ade152`, commit message giải thích (bản một trang tự đứng, đóng bằng caveat rồi disclaimer); `business-plan.md` không đổi từ `c512614`.
- **Git:** nhánh `lane/issue-18`, mọi commit nêu `#18` hoặc tên lát, không viết lại lịch sử.

## Quan sát không chặn

- Evidence ghi "Last code commit: `827dd83`", nhưng `827dd83` là commit chỉ đổi evidence; commit đổi mã cuối là `1afc6fe` (test) hoặc `eeb34ea` (docs checklist). Cổng chạy ở 827dd83 vẫn bao trùm cả hai nên không stale; chỉ là nhãn không chính xác.

## Chưa xác minh

- Chưa có phiên Kiro CLI thật chạy `founder-plan`; test chỉ kiểm văn bản skill và file ví dụ (evidence `## Giới hạn` đã nêu).
- Chưa có ví dụ `Not yet` / `Incomplete` đã soạn; bảng Step 3 chỉ được kiểm bằng nhãn compiler, không bằng cách model diễn đạt.
- Test chống tiếng Anh là danh sách từ dừng; tôi đọc `summary.md` và không thấy câu tiếng Anh dành cho chủ hộ.
- Tính đúng nội dung pháp lý của các link Công báo thuộc trục Spec và lượt trước; lượt này chỉ kiểm link khớp với nguồn trong repo, không truy cập các link.

<promise>PASS</promise>
