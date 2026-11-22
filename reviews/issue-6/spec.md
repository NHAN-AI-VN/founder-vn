Commit mã đã chấm: 331001f15fae

# Review trục Spec, issue #6, vòng 1

Phạm vi: `git diff --stat main...HEAD` (15 file, 6 commit slice + evidence). Đã đọc `AGENTS.md`, `docs/founder-vn-design.md` §3, §4 và các mục Q37; chạy lại `uv run pytest tests/test_cfo.py tests/test_cfo_cli.py tests/test_cfo_parity.py tests/test_vnd.py`: 53 passed. Đã đọc `src/founder_vn/cfo.py`, `vnd.py`, `cli.py`, `server.py`, fixture, golden và `docs/evidence/issue-6-cfo-unit-economics.md`.

Phán quyết: CHANGES_REQUESTED, một finding chặn.

## Finding chặn

### SPEC-1: báo cáo `cfo.md` không có câu miễn trừ trách nhiệm
Criterion: "Report text in Vietnamese" cùng yêu cầu của thiết kế mà ticket trỏ tới (§3: "Giữ mọi câu miễn trừ trách nhiệm"; §4 định nghĩa "xong": "có miễn trừ trách nhiệm"). Bản báo cáo dành cho chủ hộ (`report()` trong `src/founder_vn/cfo.py`, golden `tests/golden/cfo_report.json`) chỉ nói "Mọi con số lấy từ numbers.json… Không số nào được tra cứu hay đoán" và, khi không có cảnh báo, nhắc đối chiếu báo giá. Không có câu nào nói đây là mô hình tính toán, không phải tư vấn thuế/tài chính, và thuế suất cùng ngưỡng là số anh/chị nhập, cần đối chiếu quy định hiện hành. Báo cáo in thuế suất và ngưỡng miễn thuế nên thiếu câu này là khoảng trống thật cho người sắp bỏ tiền. Cách sửa nằm trong `src/founder_vn/cfo.py` và golden của lane: thêm câu miễn trừ vào `report()` rồi tạo lại golden.

## Đối chiếu từng criterion

1. `numbers.json` và trường bắt buộc: đáp ứng. `NUMERIC_FIELDS` gồm `tax_rate_on_revenue`, `tax_free_threshold`; `_required` báo "thiếu trường '<tên>'", không mặc định. Bằng chứng: `tests/test_cfo.py::test_missing_field_is_an_error_naming_it` (parametrize) và `tests/test_cfo_cli.py::test_missing_field_exits_2_naming_it`.
2. Thuế và ba đầu vào verdict: đáp ứng. Mã đọc `crosses = year_revenue > threshold`, thuế trên doanh thu từng tháng khi vượt (tức toàn bộ doanh thu năm), bằng ngưỡng thì không thuế, lợi nhuận = doanh thu − biến đổi − cố định − thuế, có cờ vượt ngưỡng. `verdict_inputs` có `contribution`, `year1_operating_profit_after_tax`, `breakeven_per_day` với `capacity_per_day`. Bằng chứng: `test_tax_applies_to_full_year_revenue_above_threshold`, `test_no_tax_at_or_below_threshold`, `test_verdict_inputs_are_exposed_not_decided`, golden `cfo_json` và `cfo_below_threshold`. Không tính verdict là đúng phạm vi.
3. Tiện ích locale: đáp ứng. Tôi chạy thẳng `parse_vn_number` trên cả sáu chuỗi của ticket (35.000, 35k, 35 nghìn, 1,2 triệu, 1tr2, 1.200.000 đ), kết quả 35000/35000/35000/1200000/1200000/1200000. `format_vnd` cho dấu chấm nghìn, `đ`, không thập phân. Bằng chứng: `tests/test_vnd.py` (bảng golden, 34 ca theo evidence).
4. What-if và độ nhạy: đáp ứng. Cờ `--price`, `--volume`; bốn dòng độ nhạy gồm gốc, giá −10%, sản lượng −20%, chi phí đơn vị +15%. Bằng chứng: `test_price_what_if_golden`, `test_volume_what_if_golden`.
5. Tiếng Việt, JSON, `cfo.md` qua lớp khóa đường dẫn: đáp ứng phần JSON, phần ghi file và phần ngôn ngữ (xưng "anh/chị", `35.000 đ`, không `$`). `--out` đi qua `files.write_text`; `test_out_outside_root_is_refused` chứng minh bị từ chối. Phần miễn trừ trách nhiệm của báo cáo chưa đáp ứng: xem SPEC-1.
6. Golden qua CLI và parity MCP: đáp ứng. `tests/test_cfo_cli.py` so golden qua CLI; `tests/test_cfo_parity.py` chạy 4 ca (report, json, what-if, out) qua cả CLI và MCP rồi so stdout và toàn bộ file đã ghi. Các test nằm trong `tests/` nên thuộc phần `pytest` của cổng `unit`; evidence ghi 104 passed ở `23342b9`.

Artefact `cfo.md`/fixture: fixture là quán cà phê tổng hợp, không tên người hay địa điểm dưới cấp quận. Báo cáo không có `$`.

## Chưa xác minh

- Job `Gate` ở `331001f15fae` còn `in_progress` lúc chấm; bản ghi cổng trong evidence ứng với `23342b9` (commit mã cuối). Commit `331001f` chỉ đổi evidence nên tôi không coi là khác biệt, nhưng chưa thấy kết quả Gate ở đúng commit.
- Giá trị `nan`/`Infinity` (JSON `NaN` hoặc chuỗi "nan") qua `_number` thành float không hữu hạn mà không có lỗi; ngoài các criterion của ticket, chưa chạy thử đầu ra, không chặn.
- Evidence tự ghi collection-time red của `cfo.analyse` không được giữ; không thuộc trục Spec.

<promise>CHANGES_REQUESTED</promise>
