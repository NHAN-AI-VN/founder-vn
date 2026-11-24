# Review trục Spec, issue #16 (founder-consumer), vòng 1

Commit mã đã chấm: 56bbb3fa9b36

**Phán quyết**: CHANGES_REQUESTED

Phạm vi: `git diff --stat main...HEAD` (32 file: `skills/founder-consumer/SKILL.md`, `tests/test_consumer_skill.py`, `examples/barbershop/founder/{customer.json,pitch.md,consumer.md,panel/**}`, `docs/evidence/issue-16-founder-consumer.md`) và `git log --oneline main..HEAD` (5 commit). Gate CI ở commit này: success (theo tin nhắn mở đầu). Đã đọc file thật của skill và của ví dụ, không chỉ test.

## Finding chặn

### SPEC-1: golden case chạy bằng mô hình không phải mô hình tham chiếu
Criterion 5 ("Golden case run on Kiro CLI with the reference model"). Mô hình tham chiếu của panel là `gemini-3.5-flash-lite`: `docs/bakeoff/models.json` (`"reference"`), `docs/bakeoff/README.md` dòng 89, `README.md` dòng 38-39 và 87, đều có trên `main` (#15). `examples/barbershop/founder/panel/results.json` ghi `"model": "gemini-3.1-flash-lite"`, `consumer.md` dòng 3 và `panel/results.md` cũng vậy. Đó là một trong hai mô hình bị loại ở bake-off, không phải mô hình tham chiếu. Chặn vì `models.json` nói rõ panel chỉ so sánh được giữa các host khi `FOUNDER_LLM_MODEL` là mô hình tham chiếu, và ví dụ này là golden case. Bằng chứng `docs/evidence/issue-16-founder-consumer.md` không nhắc đến mô hình tham chiếu. Cần chạy lại `panel init/run/tally` với `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite`, cập nhật `panel/`, `consumer.md` (số liệu, trích dẫn, mô hình) và các test golden nếu có số cứng. Lane sửa được: chỉ đổi file của lane.

### SPEC-2: golden case không chạy trên Kiro CLI, và không có bằng chứng thay thế
Criterion 5. Mục "Giới hạn" của file evidence tự nhận: "Kiro CLI is not available in the lane sandbox. The golden case was produced by the lane agent following SKILL.md step by step". Không có bản ghi phiên Kiro CLI nào. Test `tests/test_consumer_skill.py` chỉ đọc văn bản skill và kiểm file ví dụ, không chứng minh một phiên Kiro CLI làm theo skill (evidence cũng nói vậy). Criterion ghi rõ "on Kiro CLI", nên tự nhận là chưa đáp ứng. Lane không có Kiro CLI trong sandbox nên cần quyết định của operator; câu hỏi ghi ở dưới. Nếu operator chấp nhận chạy qua CLI gói `founder-vn` thay cho phiên Kiro CLI thì phải ghi chấp thuận đó trên issue và trong evidence.

## Đã đối chiếu, đáp ứng

- **Criterion 1** (`customer.json`, hiện cho Owner sửa trước khi chia bài, dùng `competitors.md`, nói phần nào là đoán): `SKILL.md` Bước 1 mục 1-4 có đủ trường (segments có `income` VND hàng tháng, behaviours, objections, habits), lệnh "Do not call `panel_init` until the Owner has confirmed", quy tắc dùng cột "Phàn nàn thấy được" của `competitors.md` và nêu khi không có, đánh dấu phần đoán. `customer.json` ví dụ qua `panel.validate_customer` (test `test_golden_customer_json_passes_the_panel_validation_and_is_gender_explicit`). Bằng chứng là văn bản skill cộng test chạy trong cổng `unit`; hành vi của host thật chưa được chứng minh (xem SPEC-2).
- **Criterion 2** (`pitch.md`, 3 đến 6 dòng, không so sánh nhất, không hứa quá): `examples/barbershop/founder/pitch.md` có 5 dòng tiếng Việt, không từ so sánh nhất; mọi khẳng định (giá 199.000 đ, 45-50 phút, mở 10:00-21:00 nghỉ thứ Hai, gói 12 lần 1.990.000 đ, cọc 50.000 đ, hủy trước 3 giờ được hoàn) đối chiếu được với `examples/barbershop/founder/idea.md`. Test `test_golden_pitch_is_three_to_six_plain_lines_without_superlatives`.
- **Criterion 3** (n=20 mặc định, 100 theo yêu cầu kèm cảnh báo chi phí và thời gian, thứ tự `panel_init → panel_run → job_status → panel_tally`, không trả lời thay người mua, báo người bị loại): `SKILL.md` Bước 3 và mục Rules; test `test_panel_size_and_tool_order`, `test_never_answers_for_a_buyer_and_reports_excluded`. Ví dụ: `panel.json` `n=20`, 20 file `answers/P001..P020`, `results.json` `excluded=0`, 7 mua + 13 không = 20.
- **Criterion 4** (đọc lại năm điểm, caveat một lần): `SKILL.md` Bước 4 liệt kê đúng năm điểm theo thứ tự, caveat in một lần sau năm điểm. `consumer.md` có năm điểm, caveat đúng một lần (test `test_golden_readback_has_five_points_and_the_caveat_once`), lời trích dẫn của P007, P012, P005 khớp nguyên văn với `panel/answers/*.json`, tỷ lệ theo nhóm khớp `results.md`, nhóm mỏng được gắn nhãn và không rút kết luận, có miễn trừ trách nhiệm, không `$`, tiền định dạng Việt.
- **Ẩn danh** (criterion 5, phần "personas anonymised"): `panel/personas.json` chỉ có tên tổng hợp, địa điểm dừng ở cấp quận ("Quận 7 cũ"); `customer.json` tự ghi "ví dụ tổng hợp".

## Chưa xác minh

- Không chạy lại panel (cần khóa `FOUNDER_LLM_*`, và luật của guard cấm in giá trị). Chưa xác minh trực tiếp rằng 20 câu trả lời là của mô hình; chỉ thấy file trả lời hợp lệ, `job J-3d5fb7f2` ở trạng thái `done`. Evidence kể job đầu bị xóa tay khỏi `panel/jobs/`; các lượt đã ghi vẫn nằm trong `answers/`.
- Tên người mua trong `panel/personas.json` lấy từ một danh sách trộn nam nữ (ví dụ P001 "Thảo Vy" thuộc nhóm "Nam, nhân viên văn phòng"). Evidence ghi giới hạn này và giao cho T15; ticket #16 không yêu cầu sửa nên không tính là finding chặn. Người đọc ví dụ sẽ thấy một người mua tên nữ trong nhóm nam.

## Câu hỏi cho operator

- [ ] SPEC-2: criterion 5 đòi golden case chạy trên Kiro CLI. Operator chạy lại phiên Kiro CLI (với `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite`) rồi commit kết quả, hay chấp nhận chạy qua CLI gói `founder-vn` và ghi chấp thuận đó lên issue #16?

<promise>CHANGES_REQUESTED</promise>
