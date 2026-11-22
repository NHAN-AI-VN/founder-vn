Commit mã đã chấm: 7cd567144dc3

# Review trục Standards, issue #4, vòng 1

**Phán quyết**: CHANGES_REQUESTED (hai finding chặn, lane tự sửa được bằng commit bổ sung).

## Phạm vi đã xét

`git diff --stat main...HEAD`: `pilot/{consent,baseline,follow-up-questions,results-template,runbook}.md`, `tests/test_pilot_kit.py`, `docs/evidence/issue-4-pilot-kit.md`. Ba commit: `a2724b3 seam:`, `089386c slice(pilot-kit):`, `7cd5671 docs:`. Không chạm `src/`, `skills/`, `examples/`, `pyproject.toml`, `uv.lock`, `README.md`, nên không vướng file một-chủ.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `CONTRIBUTING.md` (quy tắc cứng), `docs/founder-vn-design.md` §5, §6 và Q40, Q41, `.kiro/skills/code-review/SKILL.md` (smell baseline). Không có `docs/adr/` và `GLOSSARY.md` trong repo.

Đã chạy lại ở máy review: `uv run pytest -q tests/test_pilot_kit.py` (6 passed), `ruff check .` và `ruff format --check .` xanh, `scripts/skill_lint.py` (0 skill, 0 example, 0 finding).

## Đạt

- Hình dạng vòng lặp: commit `seam:` (mục `## Seam`) đứng trước commit `slice(`; không commit nào chạm `src/`, nên mục (b) không áp dụng; test nằm ở seam đã khai (nội dung từng file `pilot/`), không ở internals; khối `## Cổng ba đoạn` ghi `GREEN on 089386c2f37e...`, và `089386c` là commit mã cuối (`7cd5671` chỉ sửa file evidence), nên cổng không stale.
- Nội dung `pilot/` khớp chuẩn đã ghi về ngôn ngữ: tiếng Việt, xưng "anh/chị" trong phiếu cho Chủ hộ, tiền định dạng `35.000 đ`, không `$` cạnh chữ số, dữ liệu mẫu tổng hợp (`P00`, `quận A`), không tên, số điện thoại hay biến `FOUNDER_LLM_*` có giá trị.
- Test không gọi mạng; test `$`/số điện thoại đã chặn trường hợp rỗng bằng `assert len(paths) == 5`.
- Không có hằng số thuế, ngưỡng hay mặc định số nào trong diff.

## Finding chặn

### S1: Khẳng định pháp lý trong `pilot/consent.md` không có link chính thức và ngày kiểm chứng

- Chỗ: `pilot/consent.md:25` (Luật số 91/2025/QH15 và danh sách quyền: biết, truy cập, chỉnh sửa, xóa, rút lại đồng ý); `docs/evidence/issue-4-pilot-kit.md`, mục `## Giới hạn`, ý thứ tư, tự nhận là "không được kiểm chứng ... không có ngày kiểm chứng".
- Sai gì: một khẳng định pháp lý về các quyền của chủ thể dữ liệu được đưa vào văn bản người tham gia ký, không kèm link chính thức, không kèm ngày kiểm chứng. `grep 'http\|vbpl' pilot/*.md` không ra gì.
- Chuẩn: `CONTRIBUTING.md` mục "The hard rule" ("A claim without both is not merged"); `docs/agents/standards.md` mục "Owner-facing output" (mọi khẳng định pháp lý có link chính thức và ngày kiểm chứng); `docs/founder-vn-design.md` §5 (Quản trị tối thiểu) và Q39 (nguồn vbpl.vn / chinhphu.vn).
- Vì sao chặn: đây là quy tắc cứng "không merge". Mục `skills/`/`examples/` của checklist không áp dụng cho diff này, nhưng quy tắc của `CONTRIBUTING.md` nói "a skill, a report or a fixture" và `pilot/consent.md` là văn bản pháp lý-hướng-người-dùng của chính dự án; việc tự ghi giới hạn trong evidence không thay cho link và ngày.
- Cách sửa (lane tự làm được, không cần quyết định thiết kế mới, nguồn đã chốt ở Q39): thêm vào `consent.md` mục 5 link bản chính thức trên vbpl.vn hoặc chinhphu.vn kèm "kiểm chứng ngày <ngày>"; đối chiếu danh sách quyền với điều khoản; cập nhật mục `## Giới hạn` của evidence. Nếu không tra được nguồn chính thức, bỏ danh sách quyền cụ thể và chỉ nêu tên luật, kèm câu hỏi `- [ ]` cho operator.

### S2: Bảng `## Lát` của file evidence không theo định dạng đã ghi

- Chỗ: `docs/evidence/issue-4-pilot-kit.md`, mục `## Lát` (một đoạn văn xuôi).
- Sai gì: `docs/agents/evidence-gates.md` mục "Where evidence lives" yêu cầu `## Lát` là bảng, mỗi lát một dòng gồm tên test, dòng assertion lúc đỏ, lần chạy xanh lại. File hiện chỉ có đoạn văn: không nêu tên sáu test, không có dòng assertion đỏ cụ thể cho từng test (chỉ "`FileNotFoundError: ... pilot/consent.md`"), và lời "5 failed, 1 passed vacuously" không thể đối chiếu với git vì test và `pilot/` nằm chung commit `089386c`.
- Chuẩn: `docs/agents/evidence-gates.md` ("Where evidence lives", "Evidence by change type": hành vi mới cần assertion đỏ rồi test xanh); `docs/agents/standards.md` mục Git (vòng lặp đỏ-xanh nhìn thấy được trong git).
- Vì sao chặn: bằng chứng đỏ-xanh là điều reviewer và merger đọc; một đoạn văn không tên test và không có dòng assertion thì không phân biệt được với tuyên bố. Mục này cũng cho thấy checklist "Documentation" chưa có dấu vết kiểm tra path: runbook viện dẫn `docs/founder-vn-design.md` mục 6 và bốn file `pilot/`, không dòng nào ghi đã kiểm.
- Cách sửa: commit bổ sung (không viết lại lịch sử) đổi `## Lát` thành bảng sáu dòng (một dòng mỗi test trong `tests/test_pilot_kit.py`, assertion đỏ thật lấy từ lần chạy đỏ lại khi tạm bỏ `pilot/` ở working tree hoặc ghi rõ dòng nào chỉ là FileNotFoundError, lần chạy xanh lại), thêm một dòng kết quả kiểm path, rồi chạy lại cổng. Nếu commit này chỉ chạm docs, `GREEN on` vẫn là `089386c`; nếu chạm test thì chạy lại `gate-segment.sh verify`.

## Chưa xác minh

- Kết quả CI: tin nhắn giao việc ghi run 45006703309 `success` nhưng job `Gate` còn `in_progress`; tôi không có credential API để đọc lại. Tôi tự chạy pytest, ruff và skill_lint như trên, chưa chạy `gate-segment.sh build`.
- Lần đỏ trước khi có `pilot/` (evidence khai 5 failed) không kiểm lại được từ git vì test và nội dung chung một commit.
- Chất lượng tiếng Việt và tính đúng của cách đọc Luật 91/2025/QH15 không nằm trong trục này; phần pháp lý đã đưa vào S1 chỉ vì thiếu link và ngày.
- Ba câu hỏi theo dõi và lời văn phiếu do lane soạn: evidence nêu chủ dự án cần chốt trước khi tuyển; đó là việc của trục Spec và operator, không gắn mã ở đây.

<promise>CHANGES_REQUESTED</promise>
