Commit mã đã chấm: 52bb5ea825e3

# Review trục Standards: issue #3, vòng 1

Phán quyết: **PASS**. Không có finding chặn.

## Phạm vi đã xét

Diff `origin/main...HEAD` (merge-base `8d8aab7`), 6 commit, 14 file: `README.md`, `LICENSE`, `CONTRIBUTING.md`, `.github/ISSUE_TEMPLATE/law-changed.yml`, `docs/skill-conventions.md`, `docs/review-checklist.md`, `docs/hosts/{README,claude,codex,gemini,grok,kirocrew}.md`, `tests/test_front_door.py`, `docs/evidence/issue-3-front-door.md`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (§ quản trị, Q23, Q24, mục upstream), `.kiro/steering/lane-implement.md`.

## Kiểm tra theo mục của hướng dẫn

- **Ghi file ngoài lớp khoá đường dẫn, CLI/MCP parity, mạng thật, số mặc định, thuế hardcode:** diff không chạm `src/`; không áp dụng. Test chỉ đọc file trong repo, không mở file để ghi, không gọi mạng.
- **Biến môi trường:** `FOUNDER_LLM_*` chỉ được nêu tên trong README, CONTRIBUTING, `docs/hosts/*`, không có giá trị. Test `test_host_pages_carry_no_secret_values_or_dollar_amounts` chặn `sk-`/`Bearer `.
- **Skill checklist:** diff không chạm `skills/` hay `examples/`, nên checklist rà soát skill không áp dụng. `scripts/skill_lint.py`: 0 skill, 0 finding. `grep` tìm `$` cạnh chữ số trong mọi file mới: không có. Ví dụ frontmatter trong `docs/skill-conventions.md` có `metadata.version: "0.1.0"`, khớp `src/founder_vn/__init__.py`.
- **Khớp thiết kế:** LICENSE MIT giữ nguyên thông báo upstream, README ghi công kèm commit 40 ký tự, có mục tiếng Việt (Q24), CONTRIBUTING có quy tắc cứng và định nghĩa xong, có mẫu issue "Law changed" (Q23). Nhãn `needs-triage` nằm trong từ vựng `docs/agents/triage-labels.md`.
- **Hình dạng vòng lặp:**
  - (a) `91623e8 seam: #3 front-door` có mục `## Seam` và đứng trước cả bốn commit `slice(`.
  - (b) Không commit nào chạm `src/`. Mỗi commit slice đều chạm `tests/test_front_door.py` và có dòng trong `## Lát`.
  - (c) Test nằm ở seam đã khai (nội dung tài liệu gốc), không ở internals.
  - (d) `## Cổng ba đoạn` ghi `verify` GREEN trên `79e0347`, là commit mã cuối. Commit sau đó (`52bb5ea`) chỉ chạm file bằng chứng, nên cổng không stale.
- **Golden file:** không đổi.
- **File một-chủ:** `README.md` nằm trong danh sách một-chủ của `docs/agents/parallel-lanes.md`. Với `HARNESS_WIP=1` dispatcher cấp `all`, nên lane này được sửa. Chưa xác minh comment `harness:allocation` (xem dưới).

## Kiểm chạy lại tại chỗ

`uv sync --frozen`, `uv run ruff check .` (pass), `uv run ruff format --check .` (61 file đã format), `uv run pytest -q` (45 passed), `python3 scripts/skill_lint.py` (0 finding). Khớp số liệu trong file bằng chứng.

## Ghi chú không chặn

- Commit `f5fcc2b` được đẩy với một test đỏ (lỗi tên trường `author` trong test), `79e0347` sửa test. File bằng chứng khai rõ chỗ lệch này ("Deviation"). Cổng xanh ở commit mã cuối nên không thành finding.
- Ba commit `slice(front-door): ...` không có `#3` trong message, trong khi `docs/agents/standards.md` (mục Git) nói message nêu ticket. Định dạng `slice(<seam>): <hành vi>` do `.kiro/steering/lane-implement.md` quy định lại không có số ticket, và lịch sử không được viết lại, nên không có cách sửa hợp lệ ở lane này. Đề xuất cho operator: làm rõ hai tài liệu cho khớp.
- Bảng `## Lát` ghi tên test và lỗi lúc đỏ (`FileNotFoundError`) nhưng lệnh chạy lại xanh nằm một dòng chung, không theo từng hàng. Hình thức, không đổi kết luận.

## Chưa xác minh

- Comment `<!-- harness:allocation -->` trên issue #3 không đọc được ở sandbox này (không có credential API), nên chưa xác nhận việc cấp phát `README.md`.
- Kết quả CI: tin nhắn mở đầu ghi run 45006076202 là success nhưng job Gate còn `in_progress`. Tôi chỉ xác nhận bằng chạy lại cục bộ, không bằng CI. Cổng CI chạy lại trọn ở commit cuối.
- Chất lượng văn bản tiếng Việt trong README, ngoài phạm vi kiểm bằng mã.
- Tính đúng của khẳng định về host (timeout Codex 60 giây, hành vi Gemini với biến `KEY`) dẫn từ design §1, chưa kiểm với nguồn ngoài.

<promise>PASS</promise>
