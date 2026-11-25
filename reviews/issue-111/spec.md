Commit mã đã chấm: 6a1cd1c4332a

# Review trục Spec, issue #111, vòng 2

**Phán quyết: PASS.** Phạm vi: `git diff --stat main...HEAD` (14 file) và `git log --oneline main..HEAD` (13 commit). HEAD là `c45e1ef639a8`. Từ vòng 1 (chấm `411ddbb3756e`), mã và test không đổi; `git diff 411ddbb 6a1cd1c` chỉ chạm `docs/evidence/issue-111-plan-permits-section.md` và các file review. Tôi chạy lại ở HEAD: `uv run pytest -q` (368 passed), `uv run ruff check .` (sạch). Run Gate 45581632215 báo success.

## Đối chiếu từng criterion

1. **`plan.SECTIONS` và "Chưa làm"**: đạt. `src/founder_vn/plan.py` có `("permits", "permits.md", "Giấy phép và thuế")` ngay sau `cfo`, không mục nào khác dịch chuyển. Bằng chứng: `tests/test_plan_cli.py::test_permits_section_follows_cfo_and_missing_one_is_listed_in_tuple_order` (dòng "Chưa làm" liền trước `Tiếp thị`; khi có `permits.md`, `## Giấy phép và thuế` ngay sau `## Kinh tế đơn vị`, dòng "Chưa làm" biến mất) và `tests/test_plan_parity.py::test_plan_with_permits_section_cli_equals_mcp` (stdout và file CLI bằng MCP). Cả hai chạy trong `pytest` của cổng `unit`. Đỏ-rồi-xanh ghi ở evidence (đỏ thật cho lát compiler; lát parity đỏ bằng đột biến vì hai đường cùng gọi `plan.run`).
2. **Golden**: đạt. `tests/golden/plan_full.json`, `plan_numbers_only.json` và `examples/barbershop/founder/business-plan.md` chỉ thêm đúng dòng "Chưa làm" mới; commit `5c61ae6` và `49e7073` ghi "output changed because the section map gained permits". Không file nào khác bị ghim (suite xanh); `summary.md` không đổi. Lane nêu thẳng rằng repo không có lệnh tái tạo nên goldens ghi bằng script chạy CLI.
3. **`skills/founder-plan/SKILL.md`**: đạt. Danh sách file có `permits.md` sau `cfo.md`; bảng ánh xạ có `| Giấy phép và thuế | founder-permits |` và đủ các mục của `SECTIONS`. Test chữ: `tests/test_plan_skill.py::test_names_permits_in_the_file_list_and_the_missing_section_mapping`.
4. **Thiết kế**: đạt. Q55 và Q56 thêm đúng nội dung ticket, tiêu đề phụ lục thành Q1–Q56; câu hệ quả (2) của Q51 và danh sách "Để sau" §9 sửa theo Q56. §2 và §7 không có câu liệt kê các mục của kế hoạch (evidence giải thích; §7 đã ghi "Đợt B: permits, ops, marketing, launch"). Chú thích trên `SECTIONS` đã sửa, trích câu pipeline của spec #1, design §7 và Q55.
5. **README**: đạt. README không nằm trong diff, `founder-permits` vẫn "not started"; `tests/test_front_door.py` nằm trong 368 test xanh.
6. **Cổng và evidence**: đạt. `docs/evidence/issue-111-plan-permits-section.md` có bảng lát đỏ-rồi-xanh, mục "Giới hạn" (không skill, không ledger, không golden `permits.md`) và nay có mục "Cổng ba đoạn" ghi đầu ra của `static`, `unit`, `build` và `verify` GREEN ở `9d7c795a4c1d`. Đó là điều chưa xác minh được ở vòng 1; nó đã được ghi, và Gate CI success ở HEAD cùng kết quả chạy lại của tôi khớp.

## Ngoài phạm vi / giới hạn của ticket

Không thấy hành vi vượt phạm vi: không skill `founder-permits`, không `permits/sources.md`, không golden `permits.md`, không đường F&B, `offer` và `brand` không đổi. Dòng `Q1–Q54` thành `Q1–Q56` trong `AGENTS.md` là cập nhật số theo tiền lệ #94, ghi nhận, không chặn. Dòng mới trong ví dụ là câu chung, không lộ tên người hay địa điểm.

## Chưa xác minh

- Đột biến cho bằng chứng đỏ của lát parity chỉ được mô tả trong evidence; tôi không chạy lại.
- Đầu ra `verify` trong evidence là do lane ghi ở `9d7c795a4c1d`, không phải ở HEAD; tôi dựa vào Gate CI success ở HEAD và lượt chạy pytest/ruff của tôi.

<promise>PASS</promise>
