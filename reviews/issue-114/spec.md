Commit mã đã chấm: edf478da67b9

# Review trục Spec, vòng 1 (chấm lại ở edf478da67b9), issue #114 (`founder-ops`)

Phán quyết: PASS. SPEC-1 của lượt trước đã được giải quyết; không còn finding chặn.

## SPEC-1 đã giải quyết chưa

Có. SPEC-1 nói rota ở mục 2 của `examples/barbershop/founder/ops.md` cần 41 suất thợ một tuần với 5 thợ (tối đa 25), và không thợ nào nghỉ ngoài thứ Hai. Đã đọc lại file thật ở HEAD:

- Bảng ca nay xếp 3, 3, 3, 4, 4, 4 thợ cho thứ Ba đến Chủ nhật, tổng 21 ca thợ, đúng bằng câu "21 ca thợ một tuần". 21 nhỏ hơn 5 thợ nhân 5 ca = 25. 21 ca chia cho 5 thợ ra 4 đến 5 ca mỗi thợ, nên mỗi thợ nghỉ ít nhất một ngày ngoài thứ Hai.
- Một ca được định nghĩa (một ngày làm, tối đa 8 giờ, vào so le, nghỉ giữa ngày). Quản lý có mặt cả ngày nên việc mở và đóng cửa 21:00 khớp với quy trình mục 3. Phụ tá: 2 toàn thời gian mỗi ngày, thêm 1 bán thời gian từ thứ Sáu đến Chủ nhật, khớp `idea.md`.
- Ba ngày thường chỉ có 3 thợ cho 4 ghế; file nói thẳng điều đó và nêu phương án 24 ca (vẫn trong 25).
- `SKILL.md` Bước 2 mục 2 nay yêu cầu rota khả thi (suất thợ không vượt số người nhân số ca tối đa, nêu người giữ việc mở và đóng cửa, nói rõ ngày dưới công suất). `tests/test_ops_skill.py` có `test_golden_rota_thợ_slots_fit_the_headcount`, `test_golden_rota_covers_every_role_the_routines_name`, `test_skill_requires_a_feasible_rota`.
- `business-plan.md` đã được compiler tạo lại (commit `be9661f`, nêu lý do) và khớp.

## Đã đối chiếu

Phạm vi: `git diff --stat main...HEAD` (9 file, không có `numbers.json`, `cfo.md`, `pricing.md`, `summary.md`) và `git log --oneline main..HEAD`. Chạy lại ở HEAD: `uv run pytest tests -q` 407 passed; `uv run python scripts/skill_lint.py` 0 finding (8 skill, gói 0.2.0). CI `Gate` run 45754117730 ở edf478da67b9: success (theo tin nhắn mở đầu).

- AC1 (SKILL.md): đạt. Frontmatter qua lint, `metadata.version` "0.2.0" bằng phiên bản gói, khối Protocol chung, bảy mục đúng thứ tự và tiêu đề, bảng nhà cung cấp bốn cột, ba danh sách đánh số có người làm, công cụ theo loại không nêu hãng, sổ rủi ro đúng mười dòng, mục 6 trỏ `founder/permits.md` và `founder-permits` không nhắc con số pháp lý, mục 7 miễn trừ. Bằng chứng: đọc file và 8 test skill, chạy trong cổng `unit`.
- AC2 (không bịa dữ liệu, câu về `numbers.json`): đạt. SKILL.md cấm bịa nhà cung cấp, báo giá, giá và dẫn quy tắc "no data is not data" của `founder-competitors`. Câu tiếng Việt về `numbers.json` là file của `founder-cfo`, cập nhật qua `founder-cfo`, rồi chạy lại `founder-pricing` và `founder-plan` có trong skill và trong golden. Skill không ghi `numbers.json`.
- AC3 (golden): đạt. Đọc `ops.md` thật: bảy mục đúng thứ tự, đúng mười dòng rủi ro, mọi ô nhà cung cấp "chưa chọn" / "chưa có báo giá", không `$` (đếm 0), tiếng Việt, xưng anh/chị, có miễn trừ, không số pháp lý, không tên người hay địa điểm. Nhân sự khớp `idea.md` (5 thợ, 2 phụ tá toàn thời gian, 1 phụ tá và 1 lễ tân bán thời gian, 1 quản lý kiêm lễ tân). Bốn file CFO không đổi. Evidence nêu giới hạn không chạy Kiro CLI.
- AC4 (README, front door): đạt. Hàng `founder-ops` ghi #114 và link `ops.md`; đoạn tiếng Việt cập nhật; `tests/test_front_door.py` cập nhật cùng lát.
- AC5 (cổng, evidence): đạt. `docs/evidence/issue-114-founder-ops.md` có bảng lát đỏ rồi xanh, ba đoạn cổng cộng `verify` ghi `GREEN on 4af23f09f72c…` (sửa điều "chưa xác minh" của lượt trước), mục "Giới hạn" (không Kiro CLI, không báo giá thật, vòng phản hồi chi phí chỉ mô tả). Từ `bafdcc7` đến `edf478d` chỉ file evidence và `standards.md` đổi (không mã, không golden).
- Ngoài phạm vi: không đổi số, không số pháp lý, không so sánh hãng.

## Chưa xác minh (không chặn, không gắn mã)

- Rota là đề xuất. Quản lý "cả ngày" ở khung 10:00–21:00 sáu ngày một tuần; định nghĩa "tối đa 8 giờ" của ca chỉ nói rõ cho thợ, nên tính khả thi của lịch quản lý (khoảng 11 giờ có mặt) chưa được file nói rõ. Test chỉ kiểm tổng suất thợ và vai trò, không kiểm nghỉ ngày của từng thợ hay giờ của quản lý. Có thể ghi chú ở lượt sau nếu operator muốn.
- Chất lượng mười dòng rủi ro và ba quy trình với một tiệm thật: không có nguồn đối chiếu ngoài `idea.md`; evidence đã tự nhận giới hạn này.

<promise>PASS</promise>
