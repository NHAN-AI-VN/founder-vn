Commit mã đã chấm: 26278a08ded3

# Review trục Spec, issue #9, vòng 1

Phạm vi: `git diff --stat main...HEAD` (10 file: `src/founder_vn/panel.py`, `cli.py`, `server.py`, fixtures, `tests/golden/panel_tally.json`, `tests/test_panel_cli.py`, `tests/test_panel_parity.py`, file evidence) và `git log --oneline main..HEAD` (9 commit, `c49cd4e` đến `26278a0`).

**Phán quyết: CHANGES_REQUESTED**

## Finding chặn

### SPEC-1: số người mua mặc định là 100, bản thiết kế quyết định 20

- Criterion: ticket nói "`panel init` deals Vietnamese persona cards" và trỏ tới `docs/founder-vn-design.md`. Mục "Panel" của bản thiết kế (dòng 96) viết "Panel mặc định `--n 20` (100 là tùy chọn)", và Q14 (dòng 225) viết "Panel mặc định 20". AGENTS.md: khi mã và thiết kế lệch nhau, thiết kế thắng.
- Mã: `src/founder_vn/cli.py` (`init_parser.add_argument("--n", type=int, default=100, ...)`) và `src/founder_vn/server.py` (`panel_init(..., n: int = 100, ...)`) đặt mặc định 100.
- Vì sao chặn: đây là quyết định thiết kế lane tự đặt, ngược với điều bản thiết kế đã chốt. Chủ hộ chạy `founder-vn panel init` không kèm `--n` sẽ nhận 100 người mua thay vì 20, nghĩa là gấp 5 lần số lượt gọi model ở các ticket sau. Không test nào khóa mặc định, nên lỗi không bị cổng nào bắt. Sửa: đổi hai mặc định về 20 và thêm test chạy `panel init` không có `--n` (cả CLI lẫn `panel_init`), kiểm đúng 20 thẻ. Chỉ chạm file của lane; nếu `cli.py` hoặc `server.py` là file một-chủ ngoài cấp phát thì operator xác nhận lại, nhưng ticket này đã sửa chính hai file đó nên coi là trong cấp phát.

## Đối chiếu từng criterion

Chạy tại `26278a08ded3`: `uv run pytest tests/test_panel_cli.py tests/test_panel_parity.py -q` cho 30 passed. Các test này nằm dưới `testpaths = ["tests"]` nên thuộc đoạn `unit` (`gate-segment.sh unit` chạy `uv run pytest -q`).

1. Personas (đáp ứng, trừ SPEC-1 về mặc định `--n`).
   - Tên Việt: `GIVEN_NAMES` (40 tên), thẻ trong golden có tên Việt.
   - Thu nhập tháng theo VND, làm tròn 100.000 đ trong khoảng của nhóm: `deal` bốc bội số của `INCOME_STEP` nằm trong `segment["income"]`; validation báo lỗi khi khoảng không chứa bội số nào. Mọi thu nhập trong golden đều chia hết cho 100.000 (28.600.000, 59.900.000, ...). Bản thiết kế dòng 28 nói làm tròn 1.000 (cho số năm của upstream); ticket nói 100.000 đ theo tháng, ticket thắng và Q14 xác nhận thu nhập theo tháng.
   - Khoảng tuổi, hành vi mua và phản đối lấy từ `customer.json`.
   - Hạn ngạch theo `share` bằng phần dư lớn nhất: `_quota`, test `test_init_deals_vietnamese_cards_by_quota_seed_7` (n=7, 4/2/1).
   - Cùng seed cùng thẻ: `test_same_seed_same_cards_other_seed_other_cards`, và golden `panel_tally.json` chứa `personas.json` của seed 7.
2. Lỗi `customer.json` nêu đúng trường (đáp ứng): `validate_customer` trả `PanelError` kèm tên trường (`segments[2].share`, `age`, `objections`, ...); `test_customer_error_names_the_field` (10 ca) kiểm thông điệp ở stderr.
3. Tally (đáp ứng): `tally` và `results_md` đếm từ file trả lời. Có tỷ lệ mua chung, theo nhóm khách và theo cách mua, lý do kèm nguyên văn (`why_not`, `why_yes`, tối đa 2 trích dẫn mỗi lý do), điều có thể đổi lời từ chối (`flip`), bốn câu trả lời giá gom vào `panel/pricing_input.json` và test pricing đọc lại được, người mua bị loại được đếm (`excluded`, `excluded_buyers`). `results.json` có `mode`, `model`, `prompt_hash`, `n`, `answered`, `excluded` (xem golden). Bằng chứng: `test_tally_counts_and_results_json_keys_seed_7`, `test_tally_reads_mode_model_prompt_hash_from_panel_json`, `test_price_answers_are_consumable_by_pricing`, `test_tally_golden_seed_7`.
4. `check` và `save` (đáp ứng): `panel check` thoát 1 khi có câu trả lời thiếu hoặc hỏng; `panel save <id>` đọc stdin, lấy đối tượng JSON đầu tiên, từ chối và không ghi file khi không hợp lệ. Bằng chứng: bốn test `check`/`save` trong `tests/test_panel_cli.py`.
5. `results.md` tiếng Việt, golden theo seed, MCP parity (đáp ứng):
   - Đọc file thật trong `tests/golden/panel_tally.json` (`panel/results.md`): tiếng Việt, xưng "anh/chị", không có `$`, có câu "Panel là mô phỏng, không phải khách hàng thật", có dòng "Tín hiệu cầu (mô phỏng, cận trên)", tiền VND định dạng Việt trong pitch (`35.000 đ`). Không có khẳng định pháp lý hay số liệu cần link. Dữ liệu fixture tổng hợp, địa điểm chỉ tới cấp quận ("Quận 1"), tên người là tên đệm tổng hợp.
   - Golden: `test_tally_golden_seed_7` so stdout và toàn bộ file.
   - Parity: `tests/test_panel_parity.py` so stdout và file của `panel init`/`panel tally` với `panel_init`/`panel_tally` qua MCP thật (`mcp_call`), byte-identical.

## Chưa xác minh

- Kết quả CI của workflow `Gate` ở `26278a08ded3` lúc ra lệnh là `in_progress`. Tôi chạy lại các test panel tại chỗ (30 passed) nhưng không chạy ba đoạn cổng đầy đủ. File evidence ghi `GREEN on c4f705ed959b...` cho commit mã cuối `c4f705e`; commit sau đó (`26278a0`) chỉ thêm file evidence.
- `mode`, `model`, `prompt_hash` chỉ được kiểm khi test tự ghi chúng vào `panel.json`; chưa có lượt chạy model nào ghi chúng (file evidence cũng nêu giới hạn này, và ticket chưa yêu cầu chạy model).
- Nhãn "manual" trong dòng "Chế độ chạy" của `results.md` là tiếng Anh. Ticket không chốt từ vựng, nên không gắn mã; ghi lại cho operator nếu muốn Việt hóa.

<promise>CHANGES_REQUESTED</promise>
