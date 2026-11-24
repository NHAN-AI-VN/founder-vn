Commit mã đã chấm: 1b8ce2d0e526

# Review trục Spec, #17 `/founder-pricing`, vòng 1

Phán quyết: **BLOCKED**. Hai tiêu chí đầu được đáp ứng bằng bằng chứng thật. Tiêu chí 3 ("Golden case run on Kiro CLI") chưa được đáp ứng đúng chữ, và lane không tự sửa được: chỉ operator chạy được Kiro CLI, hoặc sửa lời tiêu chí, như đã làm ở #16.

Phạm vi: `git diff --stat main...HEAD` (5 file: `skills/founder-pricing/SKILL.md`, `examples/barbershop/founder/pricing.md`, `examples/barbershop/founder/pricing_input.json`, `tests/test_pricing_skill.py`, `docs/evidence/issue-17-founder-pricing.md`) và `git log --oneline main..HEAD` (4 commit). Gate CI ở `1b8ce2d0e526`: success (theo tin nhắn mở đầu). Tôi đọc file thật của skill và của golden; không chạy lại test.

## Đối chiếu từng tiêu chí

### Tiêu chí 1: gọi `pricing_psm` / `founder-vn pricing`, đối chiếu `competitors.md` và `cfo.md`, cờ khi giá dưới hòa vốn CFO: ĐÁP ỨNG
- `SKILL.md` Step 2 gọi `pricing_psm` (CLI `founder-vn pricing pricing_input.json`) trên `answers` của `founder/panel/pricing_input.json`, bốn khóa `too_cheap`, `bargain`, `getting_expensive`, `too_expensive`.
- Step 1 và 3 đọc `competitors.md`, `cfo.md`, `numbers.json`; Step 3 chạy `founder-vn cfo --price` cho giá đề xuất và từng bậc, đặt cờ "giá này thấp hơn mức hòa vốn của CFO" kế bên giá và cấm giấu cờ hay dời giá để né cờ.
- Bằng chứng: `tests/test_pricing_skill.py` (8 test đọc chữ skill, 5 test `test_golden_*`); trong golden, `test_golden_flags_every_price_below_the_cfo_break_even` tự chạy `cfo.run` ở 199.000, 279.000, 389.000 đ và đòi đúng một cờ ở 199.000 đ. Test nằm trong `tests/` nên chạy trong đoạn `unit` của cổng (321 passed theo evidence).
- Giới hạn: test kiểm chữ của skill và file ví dụ, không kiểm hành vi model. Ticket không đòi hơn ở tiêu chí này.

### Tiêu chí 2: nội dung `pricing.md`: ĐÁP ỨNG
Đọc `examples/barbershop/founder/pricing.md` thật:
- Năm mục theo thứ tự: khoảng giá chấp nhận được, giá đề xuất, bậc giá, ưu đãi mở đầu để thử, theo dõi sau khi mở bán (test kiểm thứ tự).
- Số khớp đầu ra công cụ (test `test_golden_figures_are_the_tool_output`): trung vị 80.000/150.000/250.000/400.000 đ; khoảng 120.000 đến 316.667 đ; điểm cân bằng 199.625 đ; 20 câu hợp lệ, 0 loại.
- Không neo bịa: mọi giá đối thủ có trong `competitors.md` (test kiểm); Le Barbier de Saigon "chưa có số liệu" bị bỏ và nói rõ; giá "từ" được ghi là giá sàn. Bậc giá và ưu đãi lấy từ `idea.md`; chỗ thiếu số khách và số tuần thử được để ngỏ, không bịa.
- Cảnh báo dữ liệu mỏng: skill dặn chép nguyên văn đầu `pricing.md`; golden có 20 câu hợp lệ nên không có cảnh báo, và test khẳng định không có `thin_data` trong tool output. Nhánh "có cảnh báo" chỉ được bảo vệ bằng chữ trong skill, chưa có golden hay test chạy nhánh ấy (xem mục chưa xác minh).
- Phong cách chủ hộ: tiếng Việt, "anh/chị", tiền `199.000 đ`, không `$` cạnh chữ số (test regex), câu "mô phỏng, cận trên, không phải khách hàng thật" đúng một lần, có miễn trừ "không phải tư vấn tài chính, thuế hay pháp lý". Không có khẳng định pháp lý trong `pricing.md`. Tên đối thủ là tên doanh nghiệp công khai đã có sẵn trong `competitors.md` của `main`, không phải tên cá nhân.

### Tiêu chí 3: "Golden case run on Kiro CLI: `pricing.md` in the example directory; review checklist passed": CHƯA ĐÁP ỨNG (xem SPEC-1)
- Phần "`pricing.md` in the example directory" và "review checklist passed" có: file nằm ở `examples/barbershop/founder/pricing.md`; checklist đối chiếu trong evidence mục "Giới hạn" và các test ở trên.
- Phần "run on Kiro CLI" không có. `docs/evidence/issue-17-founder-pricing.md` mục "Giới hạn" ghi thẳng: "Kiro CLI is not available in the lane sandbox. The golden `pricing.md` was written by the lane agent following the skill ... No model ran in this lane."

## Finding chặn

- SPEC-1: Tiêu chí 3 đòi golden case chạy trên Kiro CLI; `pricing.md` do agent lane tự viết theo skill ở sandbox Kiro Web, không có phiên Kiro CLI nào, và evidence tự nhận điều đó. Số liệu trong file là thật (lấy từ `founder-vn pricing` và `founder-vn cfo --price`), nhưng điều tiêu chí muốn chứng minh là một phiên Kiro CLI làm theo skill (đọc bốn câu trả lời, đặt cờ hòa vốn, chép cảnh báo dữ liệu mỏng) thì chưa được chứng minh. Hai cách đóng, đều ngoài tầm lane: (a) operator chạy `/founder-pricing` trên Kiro CLI ở `examples/barbershop/`, ghi phiên đó vào evidence như #12 và #14 đã làm, hoặc (b) operator chấp nhận lượt chạy bằng CLI của package và sửa lời tiêu chí 3 trên issue, như đã làm cho #16 (`reviews/issue-16/operator-answer.md`). Lane không tự sửa được nên đây là BLOCKED, không phải CHANGES_REQUESTED.

## Câu hỏi cho operator

- [ ] Tiêu chí 3 của #17 giữ nguyên "run on Kiro CLI" (operator chạy phiên Kiro CLI rồi ghi evidence), hay chấp nhận lượt chạy bằng CLI của package và sửa lời tiêu chí như #16 (SPEC-2)? Lane không tự quyết.

## Chưa xác minh

- Hành vi của model khi làm theo skill (nhánh `thin_data`, cờ hòa vốn khi giá được người dùng thích, từ chối bịa bậc giá): chưa ai chạy; golden không có cảnh báo dữ liệu mỏng nên nhánh đó chỉ có chữ trong skill. Evidence cũng gán việc này cho T18 (#19).
- Tôi không chạy lại `pytest`; tôi dựa vào kết quả Gate ở tin nhắn mở đầu và vào việc đọc nội dung test.

<promise>BLOCKED</promise>
