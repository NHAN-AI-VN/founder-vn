Commit mã đã chấm: 8105f044344d

# Review trục Standards, #12 vòng 1 (lượt lặp sau commit 4ee3194)

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

`git diff --stat origin/main...HEAD` và `git log --oneline origin/main..HEAD` (9 commit). Trọng tâm là hai commit mới từ lượt PASS trước (5db6f2a): `4ee3194` (slice SPEC-1) và `8105f04` (docs). Các file: `skills/founder-cfo/SKILL.md`, `examples/barbershop/founder/cfo.md`, `tests/test_cfo_skill.py`, `docs/evidence/issue-12-founder-cfo.md`, `reviews/issue-12/{ledger,operator-answer}.md`; phần còn lại của nhánh (`permits/sources.md`, `numbers.json`, `tests/test_sources_ledger.py`, mục Q52 trong `docs/founder-vn-design.md`) đã xét ở lượt trước và không đổi.

Chuẩn: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, skill `code-review` (một trục).

## Kết quả theo mục

- Không ghi file ngoài lớp khoá đường dẫn, không đổi `src/`; không phép tính nào lệch giữa CLI và MCP. Diff không chạm mã `src/`, nên không cần parity mới (`tests/test_cfo_parity.py` của T05 giữ nguyên).
- Test không gọi mạng; `test_golden_cfo_md_limits_section_cites_every_ledger_link_and_the_verification_line` sinh lại phần công cụ bằng `cfo.run` và đối chiếu từng link Công báo và dòng "kiểm chứng ngày" với `permits/sources.md`. Nó sẽ đỏ nếu `cfo.md` hay Step 6 bỏ nguồn (bằng chứng đỏ ghi ở evidence: `tests/test_cfo_skill.py:89` và `:166`).
- Tỷ lệ thuế và ngưỡng không hardcode trong mã; trong skill chúng đi qua ô `<...>` chép từ sổ nguồn. Đoạn cố định "20 triệu đồng", "3 tỷ đồng", "17%" là nội dung quyết định Q52 của thiết kế và có nguồn trong cùng file.
- Không giá trị `FOUNDER_LLM_*` trong `skills/`, `examples/`, evidence hay `reviews/issue-12/`.
- Checklist skill: `skill_lint` 0 finding (2 skill, 4 file ví dụ); không `$` cạnh chữ số; xưng "anh/chị"; mọi khẳng định pháp lý trong `cfo.md` có link Công báo và dòng "kiểm chứng ngày 23/11/2026"; có miễn trừ ở "Lưu ý" của công cụ và dòng cuối phần nối, và Rules của SKILL.md giữ câu kết bắt buộc; cảnh báo panel không áp dụng (không có kết quả panel); `metadata.version` 0.1.0 khớp phiên bản package (skill_lint xác nhận).
- Hình dạng vòng lặp: (a) `14c297b seam:` có `## Seam`, đứng trước mọi `slice(`; (b) không commit nào chạm `src/`, evidence ghi rõ và có bốn dòng trong `## Lát`, gồm dòng SPEC-1; (c) test ở seam đã khai (văn bản SKILL.md, golden file, sổ nguồn), không ở internals; (d) khối `## Cổng ba đoạn` ghi `verify: GREEN on 4ee3194f6446...`, là commit mã cuối (`git diff --stat 4ee3194 HEAD` chỉ gồm `docs/evidence/`, `reviews/issue-12/`), nên cổng không stale.
- Golden đổi (`examples/barbershop/founder/cfo.md`): commit message của `4ee3194` nêu lý do (SPEC-1, regenerate bằng lượt chạy Kiro CLI) và test golden thứ hai đổi cùng commit.
- Tên và mã khớp: phần nối của `cfo.md` tự gọi mình là phần "Giới hạn của phần thuế" và đính chính "Lưu ý" của công cụ; Giới hạn ghi trung thực rằng bản chép nguồn do script của lượt chạy làm, không chứng minh model tự chép.

## Đã chạy lại ở HEAD 8105f04

`uv sync --frozen`; `uv run ruff check .` (All checks passed); `uv run ruff format --check .` (147 files already formatted); `uv run python scripts/skill_lint.py` (0 finding); `uv run pytest -q` (259 passed). CI `Gate` run 45157206885: success.

## Chưa xác minh

- Evidence ghi "195 files already formatted" ở khối cổng, còn lần chạy ở đây đếm 147; chênh có thể do thư mục sinh ra (`.harness/`, `dist/`) trong checkout của lane. Không ảnh hưởng kết quả (cả hai xanh), không đủ để gắn mã.
- Nội dung pháp lý (7%, 1 tỷ đồng, các số Công báo) không kiểm chứng độc lập; lane và evidence đã khai điều này. Đây thuộc trục Spec và việc operator đã xác nhận ngày 23/11/2026.
- Chỉ chạy `skill_lint` và đọc văn bản skill; hành vi model ở Step 6 không kiểm được từ checkout.
- Lỗi chính tả "03 tỷ đồng" trong `cfo.md` được chép nguyên văn từ sổ nguồn (đúng quy tắc "nguyên văn" của Step 6); không phải finding.

<promise>PASS</promise>
