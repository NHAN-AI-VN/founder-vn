Commit mã đã chấm: 1fcd43cb25d8

# Review trục Spec, vòng 2: #115 founder-marketing

Phán quyết: BLOCKED. Ba finding vòng 1 (SPEC-1, SPEC-2, SPEC-3) đã đóng. Còn một mâu thuẫn trong chính ticket về kênh người sáng tạo địa phương mà thiết kế không quyết; lane không tự trả lời được, nên đi vào câu hỏi cho operator, không gắn mã SPEC.

## Đã đóng từ vòng 1 (đã đọc file thật ở `1fcd43cb25d8`)

- SPEC-1: câu cảnh báo "Panel là mô phỏng, cận trên, không phải khách hàng thật; cần xác nhận với khách thật trước khi chi tiền" có trong `skills/founder-marketing/SKILL.md` mục 1 và trong `examples/barbershop/founder/marketing.md` đúng một lần.
- SPEC-2: `SKILL.md` chỉ còn một `## Protocol`; test khoá `count == 1`.
- SPEC-3: ngày 22 là đặt lịch như khách thường, giá niêm yết, không tặng dịch vụ; ngày 25 chỉ chia sẻ lại bài họ tự đăng; không còn ưu đãi cắt thử nào do lane đặt. Hai ưu đãi còn lại trong chiến dịch và hook (giảm 15% ngày thường 10:00–16:00, gói 12 lần giá 10) có sẵn trong `idea.md` và `pricing.md`.

## Đối chiếu từng criterion

- Criterion 1 (SKILL.md): đạt. Frontmatter, `metadata.version` "0.2.0" bằng version gói, khối Protocol, bảy mục đúng thứ tự, đủ quy tắc truy vết, ngân sách chỉ trích phần trăm, lưu ý quảng cáo chung chung không dẫn điều luật. Bằng chứng: `uv run python scripts/skill_lint.py` (9 skill, 0 finding), `tests/test_marketing_skill.py`.
- Criterion 2 (không thêm kênh mà khách chưa được chứng tỏ dùng): chưa đạt cho kênh người sáng tạo địa phương, xem câu hỏi bên dưới. Các kênh khác có nguồn: Google Maps, Facebook, Zalo, truyền miệng trong `idea.md`; biển hiệu qua P018; ShopeeFood/GrabFood ghi "Không áp dụng" kèm lý do. Trích dẫn khách: đã đối chiếu 7 câu chọn mẫu với `panel/results.md`, khớp nguyên văn; test golden cũng kiểm nguyên văn.
- Criterion 3 (golden): đạt. Đủ 30 hàng Ngày 1 đến Ngày 30, mỗi hàng một kênh, một việc, một phản đối có nguồn; không có `$`; cảnh báo panel một lần; hai lưu ý cuối có mặt; `business-plan.md` có mục `## Tiếp thị` (454), `tests/test_plan_example.py` xanh, commit b059334 nêu lý do. Số "12 trên 20", "3 đối thủ trực tiếp", "19:45", gói 12 lần giá 10 khớp nguồn.
- Criterion 4 (README, front door): đạt. Hàng `founder-marketing` có #115 và `marketing.md`, mục tiếng Việt cập nhật; `tests/test_front_door.py` xanh trong cùng lát.
- Criterion 5 (Gate, evidence): đạt về hình thức. `docs/evidence/issue-115-founder-marketing.md` có các lát đỏ rồi xanh và mục Giới hạn (không Kiro CLI, chiến dịch tương đối, không số chi tiêu). CI run 45763653954 success. Tôi chạy lại `pytest` cho `test_marketing_skill.py`, `test_front_door.py`, `test_plan_example.py`: 38 passed.

## Câu hỏi cho operator (chặn, thiết kế chưa quyết)

- [ ] Kênh người sáng tạo địa phương: danh sách kênh của ticket có kênh này, nhưng criterion 2 cấm "thêm kênh mà khách của chủ hộ chưa được chứng tỏ dùng". Golden tự nhận "chưa có nguồn nào cho thấy khách của anh/chị theo dõi người sáng tạo" (`marketing.md` mục 2), vậy mà vẫn dành cho kênh này 2 hàng chiến dịch (Ngày 22, 25) và 1 phần trong 10 ngân sách (mục 5). Lý do dựa vào P015 ("thợ quen giới thiệu") là một suy diễn: người sáng tạo không phải thợ quen. Xin operator chọn một: (a) giữ kênh ở mức nhỏ như hiện tại và chấp nhận ngoại lệ có ghi nhận cho criterion 2; (b) ghi "không áp dụng" cho barbershop như đã làm với ShopeeFood/GrabFood, bỏ Ngày 22 và 25, dồn 1 phần ngân sách sang kênh khác, sinh lại `business-plan.md`; (c) sửa ticket/design để kênh này được phép khi chưa có nguồn. Lane không tự chọn vì hai nửa của ticket mâu thuẫn nhau.

## Chưa xác minh

- Hook 1 và hook 2 cùng trả lời phản đối A (P019); `SKILL.md` yêu cầu mỗi hook trả lời một phản đối hoặc mệnh đề khác nhau. Hook 2 có thêm P020, nên tôi coi là chấp nhận được, không gắn mã. Mức độ: possible; nếu operator muốn chặt hơn thì gộp hoặc gắn hook 2 vào mệnh đề riêng.
- Hook 8 ("Tiệm có chỗ để xe máy") gắn với P018 (nói về gửi xe trước cửa của tiệm cũ), không phải một phản đối về tiệm mới; file đã ghi chú chỉ đăng khi mặt bằng có chỗ để xe. Không chặn.
- Mốc "nghỉ thứ Hai" lấy từ `idea.md`; số đo hạn mức dừng (9 lượt/ghế/ngày, 55%, 265.000 đ) khớp `pricing.md`.

<promise>BLOCKED</promise>
