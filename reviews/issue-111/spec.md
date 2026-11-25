Commit mã đã chấm: 411ddbb3756e

# Review trục Spec, issue #111, vòng 1

**Phán quyết: PASS.** Phạm vi: `git diff --stat main...HEAD` (11 file) và `git log --oneline main..HEAD` (8 commit). Tôi chạy lại `uv run pytest -q` (368 passed) và `uv run ruff check .` (sạch) ở HEAD. Run Gate 45580677328 báo success.

## Đối chiếu từng criterion

1. **`plan.SECTIONS` và dòng "Chưa làm"**: đạt. `src/founder_vn/plan.py` thêm đúng `("permits", "permits.md", "Giấy phép và thuế")` ngay sau `cfo`, không mục nào khác dịch chuyển. Chú thích trên `SECTIONS` đã trích câu pipeline của spec #1, design §7 và Q55. Bằng chứng: `tests/test_plan_cli.py::test_permits_section_follows_cfo_and_missing_one_is_listed_in_tuple_order` kiểm dòng "Chưa làm" nằm đúng thứ tự tuple (liền trước `Tiếp thị`) và, khi có `permits.md`, mục `## Giấy phép và thuế` nằm ngay sau `## Kinh tế đơn vị` và dòng "Chưa làm" biến mất. Đỏ-rồi-xanh: evidence ghi lỗi đỏ ở commit `c42749e`. Parity: `tests/test_plan_parity.py::test_plan_with_permits_section_cli_equals_mcp` so stdout và file giữa CLI và MCP; evidence ghi đỏ bằng đột biến (xoá mục khỏi tuple), vì test xanh ngay lần đầu do hai đường cùng gọi `plan.run`. Cả hai test chạy trong `pytest` của cổng `unit`.
2. **Golden tái tạo**: đạt. `tests/golden/plan_full.json`, `plan_numbers_only.json` và `examples/barbershop/founder/business-plan.md` đổi đúng một dòng "Chưa làm" mới (xem diff của example). Commit `5c61ae6` và `49e7073` đều ghi "output changed because the section map gained permits". Toàn bộ suite xanh nên không còn file nào khác bị ghim vào đầu ra. `summary.md` không đổi. Evidence ghi rõ goldens được ghi bằng script tạm chạy CLI vì repo chưa có lệnh tái tạo (không có lệnh "tool" riêng, đây là chỗ lane nêu thẳng).
3. **`skills/founder-plan/SKILL.md`**: đạt. Danh sách file có `permits.md` sau `cfo.md`; bảng ánh xạ mới có dòng `| Giấy phép và thuế | founder-permits |` cùng đủ các mục của `SECTIONS`. Test chữ: `tests/test_plan_skill.py::test_names_permits_in_the_file_list_and_the_missing_section_mapping`; test cũ về bảng nhãn vẫn xanh.
4. **Thiết kế**: đạt. Q55 và Q56 được thêm đúng nội dung ticket, tiêu đề đổi thành Q1–Q56. Câu hệ quả (2) của Q51 và danh sách "Để sau" ở §9 được sửa cùng lúc theo yêu cầu của Q56. Evidence giải thích §2 và §7 không có câu liệt kê các mục của kế hoạch nên không đổi; tôi đối chiếu, §7 đã ghi "Đợt B: permits, ops, marketing, launch". Chú thích `SECTIONS` đã sửa.
5. **README**: đạt. README không nằm trong diff; dòng `founder-permits` vẫn "not started (Wave B)". `tests/test_front_door.py` nằm trong 368 test xanh.
6. **Cổng và evidence**: đạt phần kiểm được. `docs/evidence/issue-111-plan-permits-section.md` có bảng lát đỏ-rồi-xanh và mục "Giới hạn" (không skill, không ledger, không golden `permits.md`). Gate success ở run nêu trên.

## Ngoài phạm vi / giới hạn của ticket

Không thấy hành vi vượt phạm vi: không có skill `founder-permits`, không mục `permits/sources.md`, không golden `permits.md`, không đường F&B, `offer` và `brand` không đổi. Sửa dòng `Q1–Q54` thành `Q1–Q56` trong `AGENTS.md` là việc theo tiền lệ #94 (evidence #94 ghi cùng thao tác) và chỉ đổi số trong một câu; ghi nhận, không chặn. Không có chỗ nào lộ tên người hay địa điểm; dòng thêm vào ví dụ là câu chung.

## Chưa xác minh

- Evidence nói đầu ra đoạn `verify` nằm trong PR; tôi không có PR hay API nên không đọc được. Gate là success ở run đã nêu.
- Bằng chứng đỏ của lát parity là đột biến mô tả trong evidence, tôi không chạy lại đột biến.

<promise>PASS</promise>
