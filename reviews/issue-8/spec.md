Commit mã đã chấm: 61c236555191

# Review trục Spec, issue #8 (pricing-psm), vòng 1

Phạm vi: `git log --oneline main..HEAD` (7 commit, `d268160` đến `61c2365`), `git diff --stat main...HEAD` (9 file: `src/founder_vn/pricing.py`, `cli.py`, `server.py`, `tests/test_pricing_cli.py`, `tests/test_pricing_parity.py`, fixture, 2 golden, file evidence). Đã đọc `AGENTS.md`, `docs/agents/evidence-gates.md`, các mục §2, §3, §4 của `docs/founder-vn-design.md`, `pricing.py`, hai file test, hai golden. Đã chạy `uv run pytest tests/test_pricing_cli.py tests/test_pricing_parity.py -q`: 11 passed.

Phán quyết: CHANGES_REQUESTED. Bốn trong năm criterion đáp ứng bằng bằng chứng thật; một yêu cầu về nội dung báo cáo cho chủ hộ (cảnh báo "mô phỏng, cận trên" và miễn trừ trách nhiệm) chưa đáp ứng.

## Đối chiếu từng criterion

| Criterion của ticket | Kết quả | Bằng chứng |
| --- | --- | --- |
| Parse giá Việt qua parser dùng chung; loại câu không dương hoặc không đọc được và báo số lượng | Đáp ứng | `pricing._price` gọi `vnd.parse_vn_number` (kiểm tay: `1,5 triệu`, `35.000 đ` đọc đúng; `abc`, rỗng, `True`, số thực lẻ bị từ chối). `test_parses_vietnamese_formats_and_reports_dropped` kiểm `valid 10, dropped 3`, đối thủ bị loại 2; fixture có `-5k`, `rẻ quá`, `0`. Báo cáo tiếng Việt in "Số câu bị loại: 3". Chạy trong `pytest` của cổng unit. |
| Cảnh báo dữ liệu mỏng dưới 8 câu hợp lệ | Đáp ứng | `MIN_VALID_ANSWERS = 8`; `test_thin_data_warning_below_eight_valid_answers` kiểm biên 7 (có cảnh báo, cả báo cáo lẫn JSON) và 8 (không có). |
| Báo cáo tiếng Việt; chế độ JSON; `pricing.md` ghi qua lớp path-locked | Đáp ứng một phần | Có báo cáo, `--json`, `--out` đi qua `files.write_text`; `test_out_writes_pricing_md_under_founder`, `test_out_outside_root_is_refused` (`../pricing.md` bị từ chối, exit 2). Nội dung báo cáo thiếu cảnh báo "cận trên" và miễn trừ, xem SPEC-1. |
| Golden-file test qua CLI; MCP parity | Đáp ứng | `test_report_golden`, `test_json_golden` qua `run_cli` với `assert_golden`; đã đọc `tests/golden/pricing_report.json`: tiếng Việt, "anh/chị", `35.000 đ`, không `$`. `tests/test_pricing_parity.py` so stdout và toàn bộ file dưới `founder/` giữa CLI và `pricing_psm` cho ba ca (báo cáo, JSON, `--out`). |
| Mốc "rẻ quá / rẻ / bắt đầu đắt / đắt quá", khoảng chấp nhận được, điểm cân bằng, không neo bịa (thân ticket) | Đáp ứng | Báo cáo in trung vị bốn câu, điểm rẻ cận biên, điểm đắt cận biên, điểm cân bằng; khi không có giá đối thủ thì báo cáo nói rõ không dùng mốc nào ngoài số nhập; điểm không xác định in "không xác định được" thay vì số tự đặt. Điểm tính đúng trên ví dụ tính tay (20.000 / 29.500 / 39.000). |

## Finding chặn

### SPEC-1: báo cáo `pricing.md` thiếu cảnh báo "mô phỏng, cận trên" và miễn trừ trách nhiệm

- Criterion: "Vietnamese report" và `pricing.md` (artefact cho chủ hộ). Thiết kế §3 dòng "Giữ mọi câu miễn trừ trách nhiệm và cảnh báo 'panel là mô phỏng, không phải khách hàng'", §4 checklist "có miễn trừ trách nhiệm, có cảnh báo panel mô phỏng"; §3 đặt quy ước cho kết quả panel là "mô phỏng, cận trên".
- Hiện trạng: mục `## Lưu ý` của `pricing.report` (`src/founder_vn/pricing.py`, dòng 191 đến 196) nói "panel mô phỏng hoặc khảo sát nhỏ, không thay cho khách thật" và "không phải giá chắc chắn bán được". Không có chữ "cận trên" (các mốc giá từ người mua mô phỏng là cận trên của mức sẵn lòng trả thật), và không có câu miễn trừ trách nhiệm đứng riêng (báo cáo không phải tư vấn tài chính hay định giá, quyết định giá là của anh/chị). Test chỉ khẳng định chuỗi `panel mô phỏng`, nên thiếu sót không bị bắt.
- Vì sao chặn: đây là artefact đưa tới chủ hộ sắp quyết định giá bán; thiết kế coi cảnh báo này là điều kiện "xong" của skill. Sửa nằm trong cấp phát của lane (`pricing.py`, hai golden, test), không chạm file một-chủ.
- Hướng sửa (để người sửa quyết định): thêm vào `## Lưu ý` câu "mô phỏng, cận trên" và câu miễn trừ; sinh lại golden `pricing_report.json` theo quy tắc golden (đọc diff, ghi lý do trong commit); mở rộng `test_report_golden` kiểm các chuỗi này.

## Chưa xác minh (không gắn mã)

- Kết quả CI: tin nhắn giao việc ghi run 45105069777 là success nhưng job `Gate` còn `in_progress`. File evidence tự khai 143 passed ở `7a48901`. Tôi chỉ chạy lại hai file test pricing (11 passed), không chạy toàn bộ cổng.
- Cách hiểu "drop answers": mã loại cả hàng người trả lời khi một trong bốn câu không đọc được, và đếm theo hàng. Ticket không nói đơn vị. Lane đã ghi quyết định này trong evidence (mục Cách tính, Giới hạn); hợp lý nhưng là quyết định lane tự đặt, cần operator biết.
- Dạng file đầu vào (`answers`, `competitor_prices` dưới `founder/`) do lane tự đặt vì thiết kế chưa định nghĩa; evidence ghi rõ ở mục Giới hạn. Job panel sau này phải sinh đúng dạng này.
- `--out` ghi đè cả file `pricing.md`, không chỉ một "data section"; evidence ghi lane hiểu "data section" là báo cáo dữ liệu do package sở hữu. Nếu skill pricing sau này viết phần văn xuôi vào cùng file thì sẽ bị ghi đè.
- Điểm giao khi hai đường cong cùng bằng 0 trên một đoạn: `_cross` lấy giá lưới đầu tiên có hiệu bằng 0 (ví dụ điểm rẻ cận biên 20.000 trong ví dụ tính tay là nơi `too_cheap` vừa về 0). Đây là quy ước hợp lý nhưng chưa đối chiếu với cài đặt Van Westendorp bên ngoài; evidence cũng thừa nhận điều này.
- Không có test cho nhánh `pmc`, `pme` hay `ipp` là `None` hoặc khi 0 câu hợp lệ (báo cáo `n == 0`); không có test cho `competitor_prices` rỗng. Chỉ đọc mã, không chạy.

<promise>CHANGES_REQUESTED</promise>
