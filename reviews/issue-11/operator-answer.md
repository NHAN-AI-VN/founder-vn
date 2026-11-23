# Trả lời của operator — review #11, vòng 1

Trả lời cho `reviews/issue-11/standards.md` (BLOCKED, commit mã đã chấm `573cedf8a2fb`), mục "Câu hỏi cho operator". File này không phải báo cáo review; nó là đầu vào cho vòng review kế. Lượt Spec vòng 1 đã PASS ở cùng commit mã.

## S1: `job_status` (ticket) hay `panel_status` (thiết kế §2 dòng 71)

- [x] Giữ `job_status`. Mã không đổi. Dòng 71 của `docs/founder-vn-design.md` sửa trong cùng commit này trên nhánh lane, kèm Q50 trong nhật ký quyết định (và Q31 trỏ tới Q50); `AGENTS.md` đổi "Q1–Q49" thành "Q1–Q50".
- [x] `board_run` dùng chung `job_status`, không có tên riêng. Đó là lý do chọn tên trên.

Căn cứ, theo thứ tự nguồn:

- Spec #1, bảng CLI↔MCP ("CLI commands and MCP tools map one-to-one"): `panel status` / `job_status`; mục job: "`panel_run` and `board_run` start a background job and return a job id immediately; `job_status` reports progress"; mục test "LLM boundary: a fake provider" nêu cả hai job trên cùng fake provider.
- Ticket T08 (#11, lane này): "`job_status` reports progress", "MCP parity for the `panel_run` / `job_status` response shapes".
- Ticket T12 (#14): "`board run` / `board_run` as a job type on the T08 runner … `job_status` works".
- Ticket T15 (#16): "runs `panel_init → panel_run → job_status (poll) → panel_tally`".

Spec và ba ticket đặt tên poll chung vì hai loại job chạy trên một runner; dòng 71 của bản thiết kế viết trước spec (21/11) và chưa được cập nhật khi spec khái quát hoá. Một tool poll cho mọi loại job đơn giản hơn hai tool theo loại và khớp giao diện mà T12 và T15 sẽ gọi. `docs/review-round5.md` dòng 50 giữ nguyên: đó là biên bản phản biện có ngày, không phải nguồn luật.

Vì vậy S1 đóng bằng sửa thiết kế, không sửa mã: `src/founder_vn/server.py` (`job_status`), lệnh `panel status`, `tests/test_panel_parity.py` và evidence giữ như ở `573cedf`.

## Ledger

`reviews/issue-11/ledger.md` được ghi trong cùng commit này: S1 là mã finding duy nhất của mọi vòng tới nay, nó đóng bằng quyết định của operator chứ không bằng lượt sửa, và merger đòi ledger cho mọi mã từng được nêu (kể cả trong phiên bản báo cáo trước) nên không thể để trống. Lượt sửa, nếu có vòng sau, ghi lại toàn bộ file với đủ mã của mọi vòng.
