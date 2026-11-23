# Trả lời của operator — review #12, vòng 1

Trả lời cho `reviews/issue-12/spec.md` (BLOCKED, commit mã đã chấm `e15e2e730dea`), mục "Câu hỏi cho operator" và hai finding SPEC-1, SPEC-2. File này không phải báo cáo review; nó là đầu vào cho vòng review kế. Lượt Standards vòng 1 đã PASS ở cùng commit mã.

## Câu hỏi: hoãn tiêu chí 4 hay merge sau khi chạy trên Kiro CLI

- [x] Không hoãn. Tiêu chí 4 đóng ngay trong lane này: operator đã chạy skill trên Kiro CLI tại máy mình ngày 23/11/2026 (10:26Z), kết quả ghi ở `docs/evidence/issue-12-founder-cfo.md`, mục "Lượt chạy golden case trên Kiro CLI (tiêu chí 4)". Không cần quyết định thiết kế mới về việc hoãn một acceptance criterion; câu trả lời 08:40 trên issue #12 (mục 5, "trước T18") bị thay bằng lượt chạy này.

## SPEC-1: `cfo.md` nêu số pháp lý mà không có link và ngày kiểm chứng trong file

Sửa thẳng, commit `4ee3194` (`slice(founder-cfo-skill): #12 SPEC-1 …`), test đỏ rồi xanh trong cùng commit:

- `skills/founder-cfo/SKILL.md` Step 6: phần nối giữ năm dòng cố định và thêm các ô `<...>` phải chép từ hai mục sổ nguồn đã mở ở Step 3 (dòng giá trị, các dòng căn cứ và Link kèm số và ngày Công báo, dòng "Sai lệch của cách gộp" cho hai giới hạn, dòng "Xác nhận"), không gõ từ trí nhớ; mở đầu bằng dòng đính chính mục "Lưu ý" của công cụ ("không phải số anh/chị nhập; skill lấy hai số này từ sổ nguồn").
- `examples/barbershop/founder/cfo.md`: sinh lại bởi lượt chạy Kiro CLI; phần nối mang sáu link Công báo và dòng "kiểm chứng ngày 23/11/2026 bởi operator trên bản PDF Công báo".
- `tests/test_cfo_skill.py`: `test_step_6_copies_the_ledger_sources_and_verification_into_the_report` (văn bản Step 6) và `test_golden_cfo_md_limits_section_cites_every_ledger_link_and_the_verification_line` (đọc `permits/sources.md`, đòi mọi link của hai mục và dòng kiểm chứng có mặt trong phần nối, đòi dòng đính chính). Đỏ: `assert "never from memory" in step6` (`:89`) và `assert link in limits` với link Luật 48/2024 (`:166`), 2 failed, 13 passed. Xanh: 27 passed trên `tests/test_cfo_skill.py tests/test_golden_case.py tests/test_sources_ledger.py`.
- `src/founder_vn/cfo.py` không đổi (T05): câu "là số anh/chị nhập" của công cụ còn nguyên và được đính chính ở phần nối; sửa câu trong công cụ thuộc ticket mới sau T11 (Q52).

## SPEC-2: tiêu chí 4 chưa chạy trên Kiro CLI, checklist chưa qua

Đóng bằng lượt chạy ghi trong `docs/evidence/issue-12-founder-cfo.md`: Protocol 1–2, Step 1 (Owner xác nhận `numbers.json`, "giữ nguyên"), Step 3 (hai mục sổ nguồn), Step 4 (`founder-vn cfo founder/numbers.json --out cfo.md`, `Đã ghi founder/cfo.md`), Step 5 (đọc kết quả và hai cờ cho Owner bằng tiếng Việt, không phán quyết, câu miễn trừ), Step 6 (phần nối chép từ sổ nguồn); model `claude-fable-5.1`, hash SKILL.md và `cfo.md` ghi trong bằng chứng. Năm mục của `docs/review-checklist.md` tick trong cùng mục bằng chứng với cách kiểm từng mục. Giới hạn còn lại của lượt chạy (đọc skill bằng đường dẫn thay vì slash command sau `install`; một model, một host; Step 2 không có hỏi đáp thật; MCP không chạy) ghi ở mục "Giới hạn" của bằng chứng.

## Ledger

`reviews/issue-12/ledger.md` được ghi trong cùng commit này: SPEC-1 và SPEC-2 là hai mã finding của mọi vòng tới nay, cả hai đóng bằng commit của operator chứ không bằng lượt sửa, và merger đòi ledger cho mọi mã từng được nêu (FV-D18). Lượt sửa, nếu có vòng sau, ghi lại toàn bộ file với đủ mã của mọi vòng.
