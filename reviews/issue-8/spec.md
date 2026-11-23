Commit mã đã chấm: bbedc9215206

# Review trục Spec, issue #8 (pricing-psm), vòng 2

Phạm vi: `git log --oneline main..HEAD` (12 commit, `d268160` đến `55e4894`), `git diff --stat main...HEAD` (12 file). Vòng này kiểm lại finding SPEC-1 của vòng 1 và đối chiếu lại bốn criterion. Đã đọc `AGENTS.md`, `src/founder_vn/pricing.py`, `tests/test_pricing_cli.py`, `tests/golden/pricing_report.json`, `docs/evidence/issue-8-pricing-psm.md`, commit `7445cdf`. Đã chạy `uv run pytest -q` ở `55e4894`: 143 passed.

Phán quyết: PASS.

## Đối chiếu từng criterion

| Criterion của ticket | Kết quả | Bằng chứng |
| --- | --- | --- |
| Parse giá Việt qua parser dùng chung; loại câu không dương hoặc không đọc được và báo số lượng | Đáp ứng | `pricing._price` gọi `vnd.parse_vn_number`; `test_parses_vietnamese_formats_and_reports_dropped` (valid 10, dropped 3, đối thủ loại 2); báo cáo in "Số câu bị loại". Chạy trong `pytest` của cổng unit. |
| Cảnh báo dữ liệu mỏng dưới 8 câu | Đáp ứng | `MIN_VALID_ANSWERS = 8`; test biên 7 (có cảnh báo, cả báo cáo lẫn JSON) và 8 (không có). |
| Báo cáo tiếng Việt; JSON; `pricing.md` qua lớp path-locked | Đáp ứng | `--json`, `--out` qua `files.write_text`; `test_out_writes_pricing_md_under_founder`, `test_out_outside_root_is_refused`. Evidence ghi red-by-mutation cho hai test này (`bbedc92`). Nội dung báo cáo xem SPEC-1 bên dưới. |
| Golden-file test qua CLI; MCP parity | Đáp ứng | `test_report_golden`, `test_json_golden` qua CLI; `tests/test_pricing_parity.py` so stdout và file dưới `founder/` giữa CLI và `pricing_psm` cho ba ca. |
| Mốc rẻ quá / rẻ / bắt đầu đắt / đắt quá, khoảng chấp nhận được, điểm cân bằng, không neo bịa | Đáp ứng | Trung vị bốn câu, điểm rẻ cận biên, điểm đắt cận biên, điểm cân bằng; "không xác định được" thay cho số tự đặt; không có giá đối thủ thì báo cáo nói rõ không dùng mốc ngoài số nhập. |

## Finding vòng 1 đã đóng

SPEC-1 (thiếu cảnh báo "mô phỏng, cận trên" và miễn trừ) đã đóng bởi `7445cdf`. Mục `## Lưu ý` của `pricing.report` (`src/founder_vn/pricing.py`, cuối hàm `report`) nay có đoạn "Kết quả mô phỏng, cận trên: người mua mô phỏng thường nói giá cao hơn mức khách thật chịu trả." và đoạn miễn trừ riêng "Báo cáo này không phải tư vấn tài chính hay định giá; quyết định giá bán là của anh/chị." Golden `pricing_report.json` được sinh lại (diff chỉ hai đoạn thêm), và `test_report_golden` (dòng 93 đến 94) khẳng định cả hai chuỗi trên stdout CLI. Hai chuỗi nằm trong mã sinh báo cáo, nên bỏ chúng thì test và golden đều đỏ.

## Chưa xác minh (không gắn mã)

- Job `Gate` của run 45105606390 còn `in_progress` lúc chấm. Tôi tự chạy toàn bộ `pytest` cục bộ (143 passed) nhưng không chạy các bước khác của cổng.
- Quyết định lane tự đặt, đã ghi trong evidence, không chặn: loại cả hàng người trả lời khi một câu hỏng; dạng file đầu vào `answers` và `competitor_prices`; `--out` ghi đè cả `pricing.md`; quy ước điểm giao khi hai đường cong cùng bằng 0 (lấy giá lưới đầu tiên có hiệu bằng 0). Job panel và skill pricing sau này phải theo các dạng này.
- Chưa có test cho 0 câu hợp lệ, điểm `None`, hay `competitor_prices` rỗng ở mức golden; chỉ đọc mã, không chạy. Mã có nhánh xử lý rõ ràng cho các ca đó.
- Báo cáo không chứa khẳng định pháp lý hay số liệu ngoài dữ liệu nhập, nên không cần link và ngày kiểm chứng.

<promise>PASS</promise>
