# Sổ tay Người hỗ trợ: pilot hai buổi gặp

Dành cho người điều phối (Người hỗ trợ) chạy pilot với một Chủ hộ. Căn cứ: `docs/founder-vn-design.md` mục 6. Công cụ này không phải tư vấn tài chính, thuế hay pháp lý; nói rõ điều đó với Chủ hộ.

Bộ tài liệu: `consent.md`, `baseline.md`, `follow-up-questions.md`, `results-template.md`.

## Trước buổi gặp thứ nhất

1. Chọn mã người tham gia (ví dụ P01) và tạo thư mục dự án riêng cho người đó **ngoài git**, ngoài cây repo (ví dụ một thư mục `pilot-data/P01/` ở nơi không thuộc bất kỳ repo nào). Không bao giờ để dữ liệu người tham gia trong cây repo `founder-vn`.
2. Bên trong thư mục ấy công cụ ghi vào `founder/`; không đặt gì khác vào đó.
3. Điền kênh liên hệ rút lại trong bản in `consent.md` (chủ dự án quyết).
4. Kiểm tra có các biến cấu hình mô hình mà không in giá trị của chúng.

## Buổi 1 (30 phút)

1. Đọc và giải thích `consent.md`; Chủ hộ chọn xóa hoặc giữ sau 90 ngày, rồi ký. Không ký thì dừng, không thu thập gì.
2. Nghe ý tưởng, lấy số liệu Chủ hộ có sẵn.
3. Ghi `baseline.md` bằng văn bản: giá dự định, địa điểm, vốn, mở hay không mở. Chủ hộ ghi ngày và xác nhận. Chụp bản này; đó là văn bản intake.
4. Giao phiếu khảo sát thực địa cho Chủ hộ.
5. Ghi ngày dự kiến buổi 2 và ngày +14 sau đó.

## Giữa hai buổi: chạy đợt A ngoại tuyến

Người hỗ trợ chạy sáu skill đợt A (board, competitors, consumer, pricing, cfo, plan) một mình, không có Chủ hộ, trong thư mục dự án của người đó. Ngoại tuyến nghĩa là không có Chủ hộ trên đường dây; các lệnh gọi mô hình vẫn đi qua API bên thứ ba như phiếu đồng thuận đã nêu. Kiểm tra `business-plan.md` đã sinh ra trước buổi 2.

## Buổi 2 (45–60 phút)

1. Đi qua `business-plan.md` từng phần với Chủ hộ.
2. Ghi phản ứng của Chủ hộ và quyết định dự định (không đẩy Chủ hộ theo hướng nào).
3. Xuất PDF và gửi qua Zalo cho Chủ hộ.
4. Báo cho người gửi câu hỏi (không phải Người hỗ trợ) ngày +14. Người gửi và người ghi bảng có thể là một người, miễn không phải Người hỗ trợ của Chủ hộ đó. Người hỗ trợ giao cho họ mã người tham gia và kênh Zalo của Chủ hộ qua một tờ liên hệ ngoài git (chỉ hai thứ đó, không tên, không dữ liệu dự án), chia sẻ riêng với người gửi; Chủ hộ đã được báo việc này ở `consent.md` mục 1. Tờ liên hệ bị hủy sau khi nhận câu trả lời.

## +14 ngày

Một người khác gửi ba câu hỏi trong `follow-up-questions.md` qua Zalo, nguyên văn. Người ghi bảng đối chiếu câu 2 với phiếu baseline, điền một dòng trong `results-template.md` (có/không đổi quyết định). Người hỗ trợ buổi gặp không gửi và không điền cột này.

## Sau 90 ngày: xóa

1. Đến ngày thứ 90 kể từ buổi 2, xóa toàn bộ thư mục dự án của người đó, trừ khi phiếu đồng thuận ghi "đồng ý giữ".
2. Xóa cả ảnh chụp phiếu baseline, tin nhắn Zalo, tờ liên hệ của người gửi và bản giấy hoặc ảnh phiếu đồng thuận nếu đã lưu ngoài thư mục.
3. Ghi vào sổ xóa riêng (ngoài git) mã người tham gia, ngày xóa; không ghi tên hay nội dung. Sổ xóa chỉ chứa mã nên được giữ.
4. Khi Chủ hộ rút lại sự đồng ý, xóa ngay, không chờ 90 ngày: thư mục dự án, ảnh baseline, tờ liên hệ, phiếu đồng thuận, và dòng của người đó trong bảng làm việc `results-template.md`; tính lại số liệu tổng hợp chưa công bố. Số liệu tổng hợp đã công bố không thu hồi (nói rõ ở `consent.md` mục 6).

## Công bố

Theo thiết kế, chỉ số liệu tổng hợp (số lượng, tỷ lệ, khoảng giá trị theo nhóm, không trích nguyên văn) và mẫu trống được đưa vào `pilot/`; bảng làm việc đã điền ở ngoài git; kết quả mô tả ở n = 20, không suy rộng.
