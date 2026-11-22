Commit mã đã chấm: 1ae561d31af5

# Review trục Spec, issue #4 (pilot kit), vòng 2

Phạm vi: `git diff --stat main...HEAD` (5 file `pilot/*.md`, `tests/test_pilot_kit.py`, `docs/evidence/issue-4-pilot-kit.md`, cùng file review) và `git log --oneline main..HEAD`. Đọc lại nguyên văn cả năm file `pilot/` ở HEAD `696ad7c`, đối chiếu `docs/founder-vn-design.md` §6, Q40, Q41 và `AGENTS.md`.

Phán quyết: PASS.

## Xác minh hai finding vòng 1

- SPEC-1 (đã sửa, confirmed). `pilot/consent.md` §5 nay nêu Điều 4 khoản 1 của Luật 91/2025/QH15, có link Công báo Chính phủ (`congbao.chinhphu.vn/van-ban/luat-so-91-2025-qh15-45578.htm`) và ngày kiểm chứng 22/11/2026. Tôi tải trang đó: trả 200 và đúng văn bản "91/2025/QH15 luật Bảo vệ dữ liệu cá nhân". Trang chỉ là trang mô tả, nội dung Điều 4 nằm trong PDF đính kèm mà tôi không đọc được trong sandbox, nên danh sách quyền trong §5 tôi chưa tự đối chiếu với văn bản điều luật (xem mục chưa xác minh). Link, ngày và điều khoản đều có, đủ yêu cầu "link chính thức + ngày kiểm chứng".
- SPEC-2 (đã sửa, confirmed). `pilot/runbook.md` Buổi 2 bước 4 giao cho người gửi mã người tham gia và kênh Zalo của Chủ hộ qua tờ liên hệ ngoài git (chỉ hai thứ đó, không tên, không dữ liệu dự án), chia sẻ riêng, hủy sau khi nhận câu trả lời; bước xóa 90 ngày (mục 2) có "tờ liên hệ của người gửi". `pilot/consent.md` §1 báo Chủ hộ việc chia sẻ Zalo cho một người khác, chỉ dùng cho việc này, xóa cùng thư mục dự án. Hai file khớp nhau và khớp Q40 (người khác gửi) và yêu cầu ẩn danh.

## Đối chiếu từng criterion

- Criterion 1 (phiếu đồng thuận tiếng Việt): đáp ứng. `consent.md` §2 nêu API mô hình bên thứ ba, §3 công bố ẩn danh (chỉ tổng hợp), §4 và §7 xóa sau 90 ngày với ô "đồng ý giữ", §6 liên hệ rút lại, §5 tham chiếu Luật 91/2025/QH15 kèm nguồn, có miễn trừ trách nhiệm ở đầu file. Bằng chứng: đọc file thật.
- Criterion 2 (baseline): đáp ứng. `baseline.md` có bốn mục (giá, địa điểm đến cấp quận/huyện, vốn, mở/không mở), "Ngày ghi", mục "Xác nhận của Chủ hộ" có ngày xác nhận và chữ ký hoặc tin nhắn.
- Criterion 3 (ba câu hỏi): đáp ứng. `follow-up-questions.md` có đúng ba câu, định nghĩa "đổi quyết định" nguyên văn theo ticket, quy định người khác gửi ở +14 ngày; đường bàn giao liên hệ nay chạy được (SPEC-2).
- Criterion 4 (bảng kết quả): đáp ứng. `results-template.md` có đủ cột (mã, ngành, bốn mục baseline, ba câu trả lời, đổi quyết định có/không, ghi chú) và lưu ý mô tả ở n = 20, không suy rộng.
- Criterion 5 (runbook): đáp ứng. `runbook.md` có buổi 1 (30 phút), đợt A ngoại tuyến, buổi 2 (45–60 phút), PDF qua Zalo, thư mục dự án từng người ngoài git, bước xóa sau 90 ngày và rút đồng ý.
- Giới hạn của ticket và AGENTS.md: không có `$`, tiền định dạng `35.000 đ`, ví dụ P00 chỉ ghi "quận A", không tên người, không số điện thoại.

Bằng chứng: `uv run pytest tests/test_pilot_kit.py -q` chạy lại ở sandbox này, 6 passed. Test nằm trong `tests/`, thuộc cổng `unit`; evidence ghi gate xanh ở `0ddcced` (51 passed), các commit sau chỉ đổi evidence và ledger. Test chỉ kiểm chuỗi nội dung nên tôi dựa vào việc đọc file thật cho chất lượng nội dung.

## Chưa xác minh / câu hỏi cho operator (không gắn mã)

- [ ] Kênh liên hệ rút lại sự đồng ý (`consent.md` §6, placeholder `[LIÊN HỆ RÚT LẠI: ...]`): design không nêu, chỉ chủ dự án biết; phải điền trước buổi 1 (runbook "Trước buổi gặp thứ nhất" bước 3 đã nhắc).
- [ ] Chốt chữ ba câu hỏi: design cố định số lượng và định nghĩa, không cố định lời; chủ dự án cần xác nhận trước khi tuyển người đầu tiên.
- [ ] Nội dung Điều 4 khoản 1 trong PDF Công báo: tôi chưa đọc được bản PDF trong sandbox, nên chưa tự đối chiếu danh sách quyền ở `consent.md` §5; lane tuyên bố đã đối chiếu (evidence, ledger). Evidence cũng khuyến nghị luật sư xem lại trước khi dùng.
- [ ] Thời hạn lưu phiếu đồng thuận (hủy ngày 90) là giả định của lane, design không nói; luật sư có thể yêu cầu lưu lâu hơn. Không chặn criterion nào.
- CI: run 45044451401 báo success nhưng bước `Gate` còn `in_progress` lúc review; tôi không có credential để kiểm lại. Evidence ghi gate ba đoạn xanh ở `0ddcced`.
- Dữ liệu của người chọn "đồng ý giữ" (Zalo, ảnh baseline) chưa có hướng dẫn riêng; không chặn.

<promise>PASS</promise>
