Commit mã đã chấm: 66beadeda626

# Review trục Spec, issue #9, vòng 2

Phạm vi: `git diff --stat main...HEAD` (13 file) và `git log --oneline main..HEAD` (15 commit, `c49cd4e` đến `66beade`). Commit mã cuối là `69ebc4d`; `cc86828` và `66beade` chỉ thêm ledger và evidence.

**Phán quyết: PASS**

## Finding vòng 1

- SPEC-1 (mặc định `--n` là 100, thiết kế quyết định 20): đã đóng. `panel.DEFAULT_N = 20` (`src/founder_vn/panel.py:18`); `cli.py` (`--n` default `panel.DEFAULT_N`) và `server.py` (`panel_init(n=panel.DEFAULT_N)`) dùng cùng hằng số. `grep` không còn mặc định 100 trong ba file. Khớp `docs/founder-vn-design.md` dòng ~96 và Q14.
  - Bằng chứng: `test_init_without_n_deals_twenty_cards` (CLI, đúng 20 thẻ) và `test_panel_init_default_n_is_twenty_on_cli_and_mcp` (CLI và MCP, 20 thẻ, stdout và file byte-identical). Evidence ghi đã đỏ (`100 == 20`) trước khi xanh.

## Đối chiếu từng criterion

Chạy tại `66beadeda626`: `uv run pytest tests/test_panel_cli.py tests/test_panel_parity.py -q` cho 32 passed. Các test nằm dưới `testpaths = ["tests"]` nên thuộc đoạn `unit`. CI `Gate` ở commit này: success (evidence ghi unit 175 passed, static sạch, build xong).

1. Personas (đáp ứng): tên Việt (`GIVEN_NAMES`), thu nhập tháng VND là bội số của 100.000 đ trong khoảng nhóm, khoảng tuổi, hành vi mua và phản đối từ `customer.json`, hạn ngạch phần dư lớn nhất (`test_init_deals_vietnamese_cards_by_quota_seed_7`, 4/2/1), cùng seed cùng thẻ (`test_same_seed_same_cards_other_seed_other_cards`, golden). Mặc định 20 người mua nay khớp thiết kế.
2. Lỗi `customer.json` nêu đúng trường (đáp ứng): `test_customer_error_names_the_field` (10 ca).
3. Tally (đáp ứng): tỷ lệ mua chung, theo nhóm và hành vi, lý do kèm trích dẫn, điều đổi được lời từ chối, bốn câu trả lời giá vào `panel/pricing_input.json` (pricing đọc lại được), người bị loại được đếm; `results.json` có `mode`, `model`, `prompt_hash`, `n`, `answered`, `excluded`. Bằng chứng: `test_tally_counts_and_results_json_keys_seed_7`, `test_tally_reads_mode_model_prompt_hash_from_panel_json`, `test_price_answers_are_consumable_by_pricing`, `test_tally_golden_seed_7`.
4. `check` và `save` (đáp ứng): bốn test trong `tests/test_panel_cli.py`; `save` từ chối và không ghi file khi không hợp lệ.
5. `results.md` tiếng Việt, golden theo seed, MCP parity (đáp ứng): đã đọc `panel/results.md` trong `tests/golden/panel_tally.json`: tiếng Việt, không `$`, VND định dạng Việt, có cảnh báo "mô phỏng, cận trên", dữ liệu tổng hợp. Parity thật qua `tests/test_panel_parity.py` (`panel_init`, `panel_tally`, byte-identical stdout và file).

## Chưa xác minh

- `mode`, `model`, `prompt_hash` chỉ được kiểm khi test tự ghi chúng vào `panel.json`; chưa có lượt chạy model nào ghi chúng. Ticket chưa yêu cầu chạy model; evidence nêu giới hạn này. Không phải finding.
- Nhãn "manual" trong `results.md` là tiếng Anh. Ticket không chốt từ vựng; ghi cho operator nếu muốn Việt hóa.
- Tôi không tự chạy ba đoạn cổng; dựa vào kết quả CI `Gate` success và 32 test panel chạy tại chỗ.

<promise>PASS</promise>
