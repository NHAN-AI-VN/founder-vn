Commit mã đã chấm: 272ed5e692d5

# Review trục Spec, vòng 1, issue #114 (`founder-ops`)

Phán quyết: CHANGES_REQUESTED. Một finding chặn (SPEC-1), sửa được trong cấp phát của lane.

## Đã đối chiếu

Phạm vi: `git diff --stat main...HEAD` (7 file: README, evidence, `business-plan.md`, `ops.md`, SKILL.md, hai file test), `git log --oneline main..HEAD` (6 commit). Chạy lại `uv run pytest tests/test_ops_skill.py tests/test_plan_example.py tests/test_front_door.py -q`: 34 passed. `uv run python scripts/skill_lint.py`: 0 finding (8 skill, phiên bản gói 0.2.0, khớp `metadata.version` "0.2.0"). CI `Gate` ở 272ed5e: success (theo tin nhắn mở đầu).

- AC1 (SKILL.md): đạt. Frontmatter qua lint, khối Protocol chung, bảy mục đúng thứ tự, bảng nhà cung cấp, rota tuần, ba danh sách đánh số có người làm, công cụ theo loại không nêu hãng, sổ rủi ro đúng mười dòng, mục 6 trỏ `founder/permits.md` và `founder-permits` không nhắc con số pháp lý, mục 7 miễn trừ. Bằng chứng: đọc file và `tests/test_ops_skill.py` (8 test skill).
- AC2 (không bịa nhà cung cấp, báo giá, giá; câu về `numbers.json`): đạt. SKILL.md cấm rõ, nêu "no data is not data" của `founder-competitors`, và có câu tiếng Việt: `numbers.json` là file của `founder-cfo`, cập nhật qua `founder-cfo`, rồi chạy lại `founder-pricing` và `founder-plan`. Skill không ghi `numbers.json`. Golden có đúng câu này.
- AC3 (golden): đạt một phần. Bảy mục đúng thứ tự, đúng mười dòng rủi ro, mọi ô nhà cung cấp là "chưa chọn" / "chưa có báo giá", không `$`, tiếng Việt, xưng anh/chị, có miễn trừ, không con số pháp lý, nhân sự khớp `idea.md` (5 thợ, 2 phụ tá toàn thời gian, 1 phụ tá và 1 lễ tân bán thời gian, 1 quản lý kiêm lễ tân). `numbers.json`, `cfo.md`, `pricing.md`, `summary.md` không nằm trong diff (`examples` chỉ có `ops.md` và `business-plan.md`). `business-plan.md` do compiler tạo, commit `bf83bf5` nêu lý do, `tests/test_plan_example.py` xanh. Lịch ca làm có lỗi, xem SPEC-1.
- AC4 (README, front door): đạt. Hàng `founder-ops` ghi #114 và link `ops.md`, có đoạn tiếng Việt, `tests/test_front_door.py` cập nhật cùng lát.
- AC5 (cổng, evidence): đạt về hình thức. `docs/evidence/issue-114-founder-ops.md` có bảng lát đỏ rồi xanh và mục "Giới hạn" (không chạy Kiro CLI, không có báo giá thật, vòng phản hồi chi phí chỉ mô tả). Xem mục "Chưa xác minh" về đoạn `verify`.
- Ngoài phạm vi: không có thay đổi nào ở `numbers.json`, `cfo.md`, `pricing.md`, `summary.md`, không số pháp lý, không so sánh hãng.

## Finding chặn

### SPEC-1: lịch ca làm của golden `ops.md` không khớp số người trong `idea.md`

Criterion: AC1 mục (2) "roles and headcount from `idea.md`, a weekly rota" và AC3 "from `idea.md` (staffing: 5 thợ, ...)". Skill (Bước 2, mục 2) yêu cầu rota "built from the opening hours in `idea.md` and the headcount".

Điều sai (confirmed, đọc `examples/barbershop/founder/ops.md` mục 2): bảng ca xếp thợ mỗi ngày mở cửa như sau. Thứ Ba đến Năm: 3 + 3. Thứ Sáu: 3 + 4. Thứ Bảy và Chủ nhật: 4 + 4. Tổng 41 suất thợ một tuần. Chỉ có 5 thợ, và đoạn ngay dưới bảng ghi "Mỗi thợ làm tối đa 5 ca một tuần", tức tối đa 25 suất. Bảng cần gần gấp rưỡi số suất mà đội có, và tự mâu thuẫn với câu của chính nó. Ngay cả khi tính mỗi thợ làm cả hai ca một ngày (10 ca một tuần), rota vẫn cần 4 thợ có mặt cả hai ca cuối tuần, không thợ nào được nghỉ một ngày ngoài thứ Hai như câu dưới bảng hứa. Chủ hộ sẽ chép rota này làm lịch thật và đi tuyển, xếp ca theo nó.

Vì sao chặn: AC3 đòi golden dựng từ `idea.md` với đúng đội ngũ ấy; rota không dựng được từ số người đó thì bằng chứng "golden đúng" không đứng vững. Test chỉ kiểm cấu trúc, không kiểm tính khả thi, và `docs/evidence/issue-114-founder-ops.md` tự nhận rota là "đề xuất, chưa đo" nhưng không nêu mâu thuẫn số học này. Đây là hành vi sai trong chính artefact giao cho chủ hộ, không phải chuyện văn phong.

Cách sửa (trong cấp phát của lane): xếp lại rota để số suất thợ mỗi tuần không vượt số người nhân số ca tối đa đã nêu (ví dụ chia ca so le, mỗi thợ một ngày nghỉ ngoài thứ Hai, hoặc nêu rõ mỗi ca cần bao nhiêu thợ theo 4 ghế), hoặc sửa câu "tối đa 5 ca" cho khớp. Rồi chạy lại `founder-vn plan` để `business-plan.md` khớp, và thêm một test kiểm số suất thợ trong bảng ca không vượt số thợ nhân số ca tối đa. Cập nhật evidence theo lát đỏ rồi xanh. Nếu skill cần nói rõ hơn (rota phải khớp số người), chỉnh `skills/founder-ops/SKILL.md` kèm.

## Chưa xác minh

- Đoạn `verify` của cổng: evidence ghi "see the PR body for the HEAD it was green on", không nêu kết quả trong repo. CI `Gate` ở 272ed5e báo success trong tin nhắn mở đầu, nên không coi là finding; operator nên đối chiếu với thân PR #129.
- Chất lượng mười dòng rủi ro và ba quy trình với một tiệm thật: không có nguồn đối chiếu ngoài `idea.md`; evidence đã tự nhận giới hạn này.

<promise>CHANGES_REQUESTED</promise>
