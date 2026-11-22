Commit mã đã chấm: 6ddd7398f2ab

# Review trục Spec, issue #6, vòng 2

Phạm vi: `git diff --stat main...HEAD` và `git log --oneline main..HEAD` (18 file). Đã đọc `AGENTS.md`, `docs/founder-vn-design.md` §3 và Q37, `src/founder_vn/cfo.py`, `vnd.py`, `cli.py`, `server.py`, golden và test. Chạy lại ở `6ddd7398f2ab`: `uv run pytest -q` toàn bộ 105 passed; bốn file của issue (`test_cfo.py`, `test_cfo_cli.py`, `test_cfo_parity.py`, `test_vnd.py`) 54 passed (vòng 1: 53, thêm `test_report_carries_disclaimer`).

Phán quyết: PASS. Không còn finding chặn.

## Đóng SPEC-1 (vòng 1)

Đã đóng ở `6e8cc84`. `report()` có mục "Lưu ý" cuối báo cáo: đây là mô hình tính từ số anh/chị nhập, không phải tư vấn thuế hay tài chính; thuế suất và ngưỡng miễn thuế là số anh/chị nhập, cần đối chiếu quy định hiện hành hoặc hỏi cơ quan thuế/kế toán. Golden `tests/golden/cfo_report.json` (và `cfo_below_threshold`, `cfo_price`, `cfo_volume`) đã tạo lại và chứa mục này; `tests/test_cfo_cli.py::test_report_carries_disclaimer` khóa nó. Thay đổi vòng 2 so với vòng 1 chỉ chạm `cfo.py` (+9 dòng), golden, một test và evidence.

## Đối chiếu từng criterion

1. `numbers.json` và trường bắt buộc: đáp ứng. `NUMERIC_FIELDS` có `tax_rate_on_revenue`, `tax_free_threshold`; `_required` báo "thiếu trường '<tên>'", không mặc định. Bằng chứng: `test_cfo.py::test_missing_field_is_an_error_naming_it`, `test_cfo_cli.py::test_missing_field_exits_2_naming_it`.
2. Thuế và ba đầu vào verdict: đáp ứng. Thuế áp lên doanh thu cả năm khi `year_revenue > threshold`, bằng ngưỡng thì không thuế; lợi nhuận = doanh thu − biến đổi − cố định − thuế; có cờ vượt ngưỡng; `verdict_inputs` gồm `contribution`, `year1_operating_profit_after_tax`, `breakeven_per_day` cùng `capacity_per_day`. Bằng chứng: `test_tax_applies_to_full_year_revenue_above_threshold`, `test_no_tax_at_or_below_threshold`, `test_verdict_inputs_are_exposed_not_decided`, golden `cfo_json`, `cfo_below_threshold`.
3. Tiện ích locale: đáp ứng. Chạy lại `parse_vn_number` trên sáu chuỗi của ticket: 35000, 35000, 35000, 1200000, 1200000, 1200000. `format_vnd` dấu chấm nghìn, `đ`, không thập phân. Bằng chứng: bảng golden trong `tests/test_vnd.py`.
4. What-if và độ nhạy: đáp ứng. `--price`, `--volume`; bốn dòng gốc, giá −10%, sản lượng −20%, chi phí đơn vị +15%. Bằng chứng: `test_price_what_if_golden`, `test_volume_what_if_golden`.
5. Tiếng Việt, JSON, `cfo.md` qua lớp khóa đường dẫn: đáp ứng. Báo cáo xưng "anh/chị", tiền `35.000 đ`, golden không có `$`, có miễn trừ trách nhiệm. `--out` đi qua `files.write_text`; `test_out_writes_cfo_md_under_founder` và `test_out_outside_root_is_refused`. Fixture là quán cà phê tổng hợp, không tên người hay địa điểm dưới cấp quận.
6. Golden qua CLI và parity MCP: đáp ứng. `tests/test_cfo_cli.py` so golden qua CLI; `tests/test_cfo_parity.py` chạy 4 ca (report, json, what-if, out) qua CLI và MCP rồi so stdout và các file ghi ra. Các test nằm trong `tests/` nên thuộc phần `pytest` của cổng `unit`.

## Chưa xác minh

- Job `Gate` ở `6ddd7398f2ab` còn `in_progress` lúc chấm (run 45047148908 ghi success). Tôi chỉ có kết quả `pytest` chạy cục bộ, không có kết quả cuối của job.
- `nan`/`Infinity` đi qua `_number` thành float không hữu hạn mà không báo lỗi. Ngoài criterion của ticket, không chặn.
- Câu "tra theo luật hiện hành và ghi link" của §3 áp cho skill `founder-cfo` (ticket sau), không thuộc lát cắt gói Python này; tôi không coi là yêu cầu của #6.

<promise>PASS</promise>
