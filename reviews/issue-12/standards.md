Commit mã đã chấm: e15e2e730dea

# Review trục Standards, issue #12, vòng 1

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

So với `main`: `git diff --stat main...HEAD` (8 file, +491/-1) và `git log --oneline main..HEAD` (6 commit: `14c297b` seam, `81429bb`, `0fa8ea1`, `a62d8fb` slice, `1bda173` Q52, `e15e2e7` evidence).

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/review-checklist.md`, `docs/skill-conventions.md`, `docs/founder-vn-design.md` (Q37, Q39, Q52, mục skill/permits). Các file đã đọc: `skills/founder-cfo/SKILL.md`, `permits/sources.md`, `examples/barbershop/founder/{cfo.md,numbers.json}`, `tests/test_cfo_skill.py`, `tests/test_sources_ledger.py`, `docs/evidence/issue-12-founder-cfo.md`.

Đã chạy ở `e15e2e730dea`: `uv run --frozen python scripts/skill_lint.py` (2 skills, 4 example file, 0 finding); `uv run --frozen pytest -q tests/test_cfo_skill.py tests/test_sources_ledger.py tests/test_golden_case.py` (25 passed). Gate CI của run 45152801864: success (theo tin nhắn giao việc).

## Kết quả theo mục chặn

- Ghi file ngoài lớp khoá đường dẫn: diff không thêm mã ghi file; `src/` không đổi.
- CLI/MCP parity: không có phép tính mới; `cfo_analyse` và `founder-vn cfo` đã có parity test của T05 (`tests/test_cfo_parity.py`), skill gọi cả hai.
- Mạng thật trong test: không; test chỉ đọc file, gọi `cfo.run` và `skill_lint.py`.
- Số mặc định thay cho lỗi nêu tên trường: SKILL.md Step 2 và Step 4 bắt hỏi lại chủ hộ trường thiếu, không đoán.
- Tỷ lệ thuế, ngưỡng hardcode: `7` và `1000000000` chỉ nằm trong `numbers.json` (đầu vào) và `permits/sources.md` (sổ nguồn có link Công báo, điều khoản, trích đoạn, ngày kiểm chứng). Skill bắt tra sổ, không lấy từ chính nó.
- Giá trị biến `FOUNDER_LLM_*`: không xuất hiện trong diff.
- Đỏ rồi xanh: bảng `## Lát` ghi lỗi đỏ cụ thể cho cả ba lát (ledger, skill, golden) và lần chạy xanh.
- Golden file đổi: `examples/barbershop/founder/cfo.md` và `numbers.json` là file mới; commit `a62d8fb` nói rõ "new golden files". `test_golden_cfo_md_is_the_tool_output_plus_the_limits_section` sinh lại phần công cụ bằng `cfo.run` nên phần đó không trôi tay được.
- Lệch thiết kế: Q52 ghi vào nhật ký (`docs/founder-vn-design.md`, heading Q1–Q52) trong cùng thay đổi, nhất quán với Q37 và Q39 (sổ nguồn, không đoán số). Q52 là quyết định của operator, không phải thiết kế mới do lane tự đặt.

## Checklist rà soát skill (`skills/`, `examples/`)

- Không `$` cạnh chữ số: `skill_lint` 0 finding; có test riêng cho SKILL.md, sổ nguồn và `cfo.md`.
- Không lọt tiếng Anh trong đầu ra cho chủ hộ, xưng "anh/chị": `cfo.md` toàn tiếng Việt, câu kết bắt buộc của skill bằng tiếng Việt. Hướng dẫn trong SKILL.md bằng tiếng Anh theo chuẩn.
- Link chính thức và ngày kiểm chứng: cả hai mục sổ nguồn có link `congbao.chinhphu.vn`, số Công báo, điều khoản, trích đoạn và dòng "kiểm chứng ngày 23/11/2026" (kiểm bằng `test_every_entry_has_link_issue_article_excerpt_and_verification`).
- Miễn trừ trách nhiệm: có trong SKILL.md (Rules) và trong `cfo.md` (mục Lưu ý và Giới hạn).
- Cảnh báo panel là mô phỏng, cận trên: không áp dụng, skill và ví dụ này không có kết quả panel.
- `metadata.version` "0.1.0" khớp `pyproject.toml`; `skill_lint` xác nhận khối protocol chung khớp `docs/skill-conventions.md`.

## Hình dạng vòng lặp

- (a) `14c297b seam: #12 founder-cfo` mang `## Seam` và đứng trước mọi commit `slice(`: đạt.
- (b) Không commit nào chạm `src/` (bằng chứng ghi rõ `cfo.py` thuộc T05); mỗi commit `slice(` chạm file test của lát và có dòng trong `## Lát`: đạt.
- (c) Test ở seam đã khai (file giao hàng: sổ nguồn, SKILL.md, golden), không ở internals: đạt.
- (d) Khối `## Cổng ba đoạn` ghi `verify` GREEN ở `1bda1736b371`; commit mã cuối là `a62d8fb`, là tổ tiên của `1bda173` (kiểm bằng `git merge-base --is-ancestor`), và từ `a62d8fb` tới HEAD không có thay đổi nào ở `src/`, `tests/`, `examples/`, `skills/`, `permits/`: cổng không stale.

## Ghi nhận không chặn

- `AGENTS.md` dòng 3 vẫn ghi "Q1–Q50" trong khi nhật ký đã tới Q52 (và Q51 có từ trước diff này). Không thuộc diff, `AGENTS.md` là file một-chủ; để operator cập nhật khi tiện.
- Phần "Lưu ý" do công cụ in trong `cfo.md` nói thuế suất và ngưỡng "là số anh/chị nhập", lệch với việc hai số lấy từ sổ nguồn. Evidence đã khai ở mục Giới hạn và Q52 đã chốt tách ticket mới; không đổi `cfo.py` trong lane này là đúng phạm vi.
- Ví dụ `cfo.md` và Step 6 của SKILL.md nêu số pháp lý (20 triệu đồng, 3 tỷ đồng, 17%) và trỏ về `permits/sources.md` thay vì chép link và ngày tại chỗ. Link, điều khoản và ngày kiểm chứng của các số này có trong sổ nguồn, nên tôi coi đủ chuẩn.

## Chưa xác minh

- Nội dung pháp lý (tỷ lệ 5% và 2%, ngưỡng 1 tỷ đồng, mốc 3 tỷ đồng và 17%, hiệu lực các văn bản) và tính tồn tại của các link Công báo: không kiểm độc lập ở lượt này; evidence ghi là operator kiểm chứng ngày 23/11/2026 trên PDF Công báo. Đây là việc của trục Spec và của operator.
- Các số `257 passed` và `GREEN` trong evidence đọc từ `.harness/gate-*.log` của lane, không có ở checkout này; tôi chỉ chạy lại các test của diff (25 passed). Cổng CI chạy lại trọn ở commit cuối.
- Hành vi thật của skill trên Kiro CLI (tiêu chí 4 của ticket) chưa chạy; evidence đã khai là giới hạn và để operator.

<promise>PASS</promise>
