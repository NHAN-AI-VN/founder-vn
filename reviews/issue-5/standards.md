Commit mã đã chấm: 1df28538728a

# Review trục Standards, issue #5, vòng 2

**Phán quyết: PASS** (S1 và S2 của vòng 1 đã đóng bằng commit bổ sung; không còn finding chặn).

## Phạm vi đã xét

`git log --oneline main..HEAD` (13 commit, gồm 4 commit sau vòng 1: `8b92b89`, `c68fc52`, `be96eb7`, `1df2853`) và `git diff --stat main...HEAD` (8 file: `README.md`, `docs/evidence/issue-5-golden-case.md`, `docs/founder-vn-design.md`, `examples/barbershop/founder/idea.md`, `reviews/issue-5/{ledger,spec,standards}.md`, `tests/test_golden_case.py`). Chuẩn đối chiếu: `AGENTS.md` (quy tắc 7, 8), `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (Q21, Q51, §7). CI `Gate` ở commit này: success (run 45130634472, theo tin nhắn mở đầu).

## Đối chiếu finding vòng 1

- S1 (địa điểm dưới cấp quận): đã đóng. `idea.md`, Q51 trong design và README đều ghi "Quận 7 cũ, TP.HCM"; `grep` trên cây (trừ `reviews/` và `.git/`) không còn tên khu ở `examples/` hay `docs/founder-vn-design.md`. `test_example_is_anonymised` nay kiểm `SUB_DISTRICT_NAMES` trên mọi `examples/barbershop/**/*.md`; evidence ghi dòng đỏ ở `## Lát`.
- S2 (thuế suất và nghĩa vụ lao động không nguồn): đã đóng. `idea.md` dòng 7 không còn "10%", "bảo hiểm xã hội", "48 giờ/tuần"; chỗ cần thuế thuê nhà ghi "theo luật hiện hành (skill tra khi chạy)"; disclaimer cuối file khớp với nội dung. `test_idea_file_carries_no_unsourced_legal_or_tax_claim` giữ lại, có dòng đỏ trong `## Lát`.

## Đã đạt

- Không đụng `src/`: không có lệch CLI/MCP, không ghi file ngoài lớp khoá, không số mặc định thay lỗi, không thuế suất hardcode. Test không gọi mạng và không đọc `FOUNDER_LLM_*`.
- Hình dạng vòng lặp: (a) `4c4c87e` (`seam:`, có `## Seam`) đứng trước `dbfbf1a` và `811b7bf` (`slice(`); (b) không commit nào chạm `src/`, mỗi slice kèm `tests/test_golden_case.py` và có dòng trong `## Lát`, hai commit sửa vòng 1 (`8b92b89`, `c68fc52`) cũng kèm test và dòng đỏ; (c) test ở seam đã khai (đường dẫn, nội dung `idea.md`, README); (d) `## Cổng ba đoạn` ghi `verify: GREEN on be96eb7df82a`, và `be96eb7` là commit mã cuối (chạm `tests/`); `1df2853` chỉ chạm `docs/evidence/` và `reviews/`, nên cổng không stale.
- Đã chạy lại ở lượt này: `uv run pytest tests/test_golden_case.py -q` (6 passed), `uv run python scripts/skill_lint.py` (0 finding), `uv run ruff check .` (pass), `uv run ruff format --check .` (128 file đã đúng định dạng).
- Checklist skill/example: không `$` cạnh chữ số; không số thuế hay khẳng định pháp lý trong `idea.md`; số liệu thị trường (giá đối thủ) đã bỏ, số còn lại được gắn nhãn ước tính của chủ dự án; có miễn trừ trách nhiệm; không có kết quả panel; `metadata.version` không áp dụng (diff không chạm `skills/`).
- Không golden file nào đổi. README là file một-chủ đã cấp phát trên #5. Q51 và dòng tuần 1 §7 vào design cùng thay đổi, đúng quy tắc "design wins".

## Ghi chú không chặn

- Dòng 32 của `docs/evidence/issue-5-golden-case.md` trích nguyên dòng đỏ của test, trong đó có tên khu mà S1 đã loại khỏi `idea.md`. Tên này buộc phải nằm ở danh sách chặn của test, và history git đã giữ nó từ trước. Nếu lane muốn gọn hơn, thay chuỗi trích bằng một chỗ giữ chỗ trong lần sửa evidence kế tiếp; không đủ để chặn.

## Chưa xác minh

- Tính đúng của các con số kế hoạch (giá, vốn, công suất): ước tính của chủ dự án nằm ngoài repo, evidence đã nói rõ.
- Chất lượng tiếng Việt và việc không lọt tiếng Anh: các từ Anh còn lại trong `idea.md` (Essential Cut, Signature Cut, app, QR, podium) là tên gói hoặc từ mượn; tôi coi là chấp nhận được, reviewer Spec có thể có ý khác.
- `uv run pytest` toàn bộ và bước `build`: không chạy lại; dựa vào Gate success và khối `## Cổng ba đoạn`.

<promise>PASS</promise>
