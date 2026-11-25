Commit mã đã chấm: c98853143557

# Review trục Spec, issue #93, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Đối chiếu từng criterion

- Step 4 của `skills/founder-consumer/SKILL.md` ghi `founder/consumer.md` gồm đoạn mở đầu ngắn, năm điểm theo thứ tự cũ, cảnh báo một lần, rồi miễn trừ; phản hồi trong chat giữ nguyên và nêu tên file. Đã đọc diff của skill. Bằng chứng: `test_read_back_is_written_to_consumer_md_in_order` (kiểm tên file, thứ tự Headline, What to change, caveat, disclaimer). Chạy lại ở HEAD: `tests/test_consumer_skill.py` và `tests/test_plan_skill.py` có 28 passed; `scripts/skill_lint.py` có 0 finding.
- `founder-plan` trích `consumer.md` cho phần đọc dành cho chủ hộ, còn `plan_compile` vẫn đọc `panel/results.md`. Đã đọc diff của `skills/founder-plan/SKILL.md`. Bằng chứng: `test_plan_skill_quotes_consumer_md_and_plan_compile_still_reads_results`. `src/` không đổi (diff chỉ có 4 file: skill, skill, test, evidence), `plan.py:33` vẫn trỏ `panel/results.md`.
- Golden `examples/barbershop/founder/consumer.md`: đã đọc file thật. Tiếng Việt, xưng "anh/chị", không có `$`, tiền định dạng `199.000 đ`, năm điểm, cảnh báo "mô phỏng, cận trên" một lần, miễn trừ ở cuối, địa danh chỉ ở cấp quận ("Quận 7 cũ"), model và seed khớp `panel/results.json` (gemini-3.5-flash-lite, 837740). Có đoạn mở đầu đúng như skill mới yêu cầu nên file đã khớp hình dạng đó. Bằng chứng: `test_golden_readback_has_five_points_and_the_caveat_once` (có sẵn) và `test_golden_readback_order_is_five_points_then_caveat_then_disclaimer` (mới).
- README: bảng trạng thái vẫn gọi `consumer.md` là artefact của `founder-consumer` (dòng 52), không đổi.
- Ngoài phạm vi: không đụng `panel_tally` (#95), không đổi `plan_compile`. Đúng giới hạn của ticket.
- Cổng CI `Gate` ở commit này: success (theo tin nhắn giao việc). Các test trên nằm trong cổng `unit`.

## Chưa xác minh / lưu ý (không chặn)

- Quyết định nói golden được "tạo lại bằng cách theo skill" và commit message giải thích vì sao đổi. Lane giữ golden nguyên và ghi trong `docs/evidence/issue-93-consumer-md.md` rằng nó chỉ được đối chiếu bằng cách đọc với skill đã sửa, vì skill mới không đòi hình dạng khác. Điều này nhất quán với "giữ cùng hình dạng năm điểm" và không có thay đổi golden nào bị lặng lẽ, nên tôi không coi là thiếu.
- Không có bằng chứng một agent chạy skill thật sự ghi ra `consumer.md`; test chỉ đọc văn bản skill. Evidence của lane đã nêu giới hạn này. Cần một lần chạy walkthrough (#19) để xác nhận hành vi.
- Câu "so the file holds the five points, then the caveat once, then the disclaimer" trong Step 4 lặp ý câu trước, có vẻ chỉ để test bám vào. Đây là chuyện văn phong (trục Standards), không xét ở đây.

<promise>PASS</promise>
