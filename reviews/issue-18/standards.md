Commit mã đã chấm: 8a5b59a3d871

# Review trục Standards, issue #18, vòng 1

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD`: 8 file (852 dòng thêm, 2 dòng xóa), 5 commit (`git log --oneline main..HEAD`): `4f53bce` seam, `1d99c0e`, `c512614`, `41fcefb` (ba slice), `8a5b59a` (evidence). Không file nào dưới `src/`, `scripts/`, `pyproject.toml` hay `uv.lock`; diff gồm `skills/founder-plan/SKILL.md`, `examples/barbershop/founder/{summary,business-plan}.md`, `README.md`, ba file test, file evidence.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape, Tests, Owner-facing, Skills, Git), `docs/agents/evidence-gates.md`, `docs/skill-conventions.md`, `docs/review-checklist.md`, `.kiro/skills/code-review/SKILL.md` (trục Standards).

## Kiểm tra đã chạy ở 8a5b59a

- `uv run ruff check .`: All checks passed. `uv run ruff format --check .`: 194 file đã định dạng.
- `uv run python scripts/skill_lint.py`: 6 skills, 15 example file, 0 finding (package 0.1.0).
- `uv run pytest -q`: 343 passed. Ba file test mới: 22 passed.
- CI `Gate` run 45342095480 ở cùng commit: success (theo tin nhắn mở đầu).

## Điều chỉnh theo từng mục chuẩn

- **Parity CLI/MCP, khóa đường dẫn, số mặc định, tỷ lệ thuế hardcode:** diff không thêm mã Python nên không có phép tính hay đường ghi file mới. `plan.py` không đổi. Thuế suất 7% và ngưỡng 1.000.000.000 đ trong `summary.md` được chép từ `cfo.md` / `permits/sources.md` kèm link Công báo và ngày 23/11/2026, không phải hằng số trong mã.
- **Test không gọi mạng; không in biến `FOUNDER_LLM_*`:** ba file test chỉ đọc file và gọi `plan.compile_plan` / `plan.run(check=True)`; không có client LLM. Evidence nói rõ không đọc giá trị `FOUNDER_LLM_*`.
- **Verdict chỉ từ số CFO:** skill ghi "Never write the verdict" ở Protocol bước 5 và Step 2/Rules; `business-plan.md` do `founder-vn plan` sinh, test so với `plan.compile_plan`. Ba hàng kiểm tra ở bảng Step 3 của skill khớp nhãn trong `src/founder_vn/plan.py:59-61`.
- **Checklist skill (`docs/review-checklist.md`):** không `$` cạnh chữ số (lint 0 finding); đầu ra cho chủ hộ bằng tiếng Việt, xưng "anh/chị", tiền dạng `35.000 đ`; phần tiếng Anh còn lại là tên riêng và nhãn kết luận của công cụ `Profitable (có lãi)`; mọi khẳng định thuế/pháp lý có link congbao.chinhphu.vn và ngày 23/11/2026; có miễn trừ trách nhiệm; có cảnh báo "mô phỏng, cận trên, không phải khách hàng thật" ở cả hai phần của `summary.md`. Frontmatter: `name` = `founder-plan`, `metadata.version` "0.1.0" khớp package, `author`/`source`/`commit` giống các skill khác; khối Protocol giống nguyên văn `founder-pricing`.
- **Hình dạng vòng lặp** (`git log --stat main..HEAD` với `docs/evidence/issue-18-founder-plan.md`):
  - (a) `4f53bce seam:` mang `## Seam` và đứng trước cả ba commit `slice(`. Đạt.
  - (b) Không commit nào chạm `src/`; mỗi commit slice đều kèm test của lát và có một dòng trong `## Lát`. Đạt.
  - (c) Test nằm ở seam đã khai (văn bản skill, file ví dụ, README, checklist), không ở internals. Đạt.
  - (d) `## Cổng ba đoạn` ghi `verify: GREEN on 41fcefbccf2c...`; `41fcefb` là commit mã cuối, `8a5b59a` chỉ đổi file evidence. Cổng không stale. Đạt.
- **Đỏ rồi xanh:** lát 1 đỏ vì thiếu `SKILL.md`, lát 2 đỏ vì thiếu hai file ví dụ, lát 3 đỏ ở `test_readme_references_the_complete_wave_a_example`. Evidence ghi rõ 6 trong 7 test của lát 3 không từng đỏ; đó là khai báo trung thực, không vi phạm chuẩn vì lát có một phép đỏ có thật.
- **Golden file:** `business-plan.md` và `summary.md` là file mới (không phải file golden đổi nội dung); evidence giải thích cách sinh.
- **Git:** nhánh `lane/issue-18`; commit nêu `#18` (seam, evidence) hoặc tên lát; không viết lại lịch sử.

## Quan sát không chặn

- Step 4 của skill nói đóng `summary.md` bằng cảnh báo panel một lần, trong khi `summary.md` mẫu đặt cảnh báo ở phần 1 và bản một trang rồi đóng bằng mục "Lưu ý" chỉ có miễn trừ. Hai chỗ không mâu thuẫn với chuẩn (cảnh báo có mặt nơi có kết quả panel), nên không gắn mã.

## Chưa xác minh

- Chưa có phiên Kiro CLI thật chạy `founder-plan`; test chỉ kiểm văn bản skill và file ví dụ (evidence `## Giới hạn` đã nêu).
- Chưa có ví dụ `Not yet` / `Incomplete`, nên Step 3 của skill chưa được thử trên số liệu thật.
- Test chống tiếng Anh là danh sách từ dừng, không phải bộ nhận diện ngôn ngữ; tôi đọc `summary.md` bằng mắt và không thấy câu tiếng Anh dành cho chủ hộ.
- Tính đúng của các số liệu và link Công báo trong `cfo.md` / `permits/sources.md` thuộc lượt trước và trục Spec, không xét ở đây (không có truy cập mạng tới các link trong lượt này).

<promise>PASS</promise>
