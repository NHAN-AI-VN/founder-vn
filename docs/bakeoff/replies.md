# Bake-off mô hình cho panel người mua

Chạy ngày 2026-11-24: 5 người mua mô phỏng, mỗi người hỏi 3 mô hình bằng đúng brief của `founder-vn panel run`. Seed 14, hash prompt `919a9496dd0572690e500903efcf52268c954144c0e59a4cb424a4e2e3191001`. Panel là mô phỏng, không phải khách hàng thật; tài liệu này chỉ để chọn mô hình tham chiếu.

## Số đo máy

| mô hình | JSON hợp lệ | nói mua | lỗi gọi | độ trễ TB (giây) | token vào/ra TB | chi phí TB mỗi người mua (USD) | giá vào/ra (USD mỗi 1M token, ngày kiểm) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| gemini-3.1-flash-lite | 5/5 | 4/5 | 0 | 1,6 | 644/191 | 0,000447 | 0,25/1,50 (2026-11-24) |
| gemini-3.5-flash-lite | 5/5 | 4/5 | 0 | 1,4 | 644/176 | 0,000632 | 0,30/2,50 (2026-11-24) |
| gemini-3.8-flash | 0/0 | 0/0 | 5 | — | —/— | — | 0,75/3,75 (2026-11-24) |

"Nói mua" là số người mua mô phỏng trả lời `buys: true`; một mô hình nói mua gần hết là một mô hình đang chiều người bán.

## Phiếu chấm của chủ dự án

Đọc mục "Từng người mua" rồi chấm 1–5 (5 là tốt nhất). Mô hình được chọn ghi vào trường `reference` của `models.json`.

| mô hình | giọng Việt tự nhiên (1–5) | thẳng thắn, không chiều người bán (1–5) | ghi chú |
| --- | ---: | ---: | --- |
| gemini-3.1-flash-lite |  |  |  |
| gemini-3.5-flash-lite |  |  |  |
| gemini-3.8-flash |  |  |  |

## Từng người mua

### P001 · Tố Uyên, 42 tuổi, Quản lý, chủ doanh nghiệp nhỏ, thu nhập 43.100.000 đ/tháng

Cách mua: Quen tiệm, quen thợ. Cắt ở một tiệm quen gần nhà hoặc gần chỗ làm nhiều năm, chỉ đổi khi thợ nghỉ. Điều e ngại: Tiệm quen của tôi gần hơn và thợ đã biết kiểu tóc của tôi. Thói quen: đọc đánh giá trên Google Maps trước khi thử chỗ mới

| mô hình | mua? | lý do (nguyên văn) | điều gì đổi ý | lần/tháng | rẻ nghi ngờ / đáng mua / bắt đầu đắt / quá đắt | JSON |
| --- | --- | --- | --- | ---: | --- | --- |
| gemini-3.1-flash-lite | không | Tôi đã quen cắt ở tiệm gần nhà bao năm nay, thợ đã quá hiểu kiểu tóc của tôi rồi, nên không có lý do gì phải mạo hiểm thử chỗ mới dù dịch vụ bên bạn nghe khá bài bản. | Nếu tiệm quen của tôi đóng cửa hoặc thợ nghỉ việc, tôi sẽ cân nhắc ghé thử một lần vì thấy đánh giá trên Google Maps của bạn tốt. | 0 | — / — / — / — | hợp lệ |
| gemini-3.5-flash-lite | không | Tôi đã cắt ở tiệm quen gần nhà bao năm nay, thợ rành tóc tôi rồi nên không muốn đổi qua tiệm mới làm gì. | Thợ quen nghỉ làm hoặc tiệm quen đóng cửa, cộng với việc tôi đọc được rất nhiều đánh giá 5 sao trên Google Maps khen tiệm này. | 0 | 50.000 đ / 199.000 đ / 350.000 đ / 500.000 đ | hợp lệ |
| gemini-3.8-flash | — | lỗi gọi: quá thời gian chờ 90 giây | — | — | — | — |

### P002 · Quang Vinh, 41 tuổi, Nhân viên văn phòng, thu nhập 20.500.000 đ/tháng

Cách mua: Đặt lịch qua app, trả QR. Chọn thợ và giờ trên app hoặc Zalo, trả bằng QR, không muốn ngồi chờ. Điều e ngại: Sợ vào rồi bị mời mua thêm gói, sản phẩm. Thói quen: đọc đánh giá trên Google Maps trước khi thử chỗ mới

| mô hình | mua? | lý do (nguyên văn) | điều gì đổi ý | lần/tháng | rẻ nghi ngờ / đáng mua / bắt đầu đắt / quá đắt | JSON |
| --- | --- | --- | --- | ---: | --- | --- |
| gemini-3.1-flash-lite | mua | Tôi thích cách đặt lịch qua app/Zalo và đặc biệt là cam kết không mời chào thêm gói dịch vụ khi đang ngồi ghế, điều này rất phù hợp với phong cách làm việc của dân văn phòng bận rộn như tôi. | — | 2 | 50.000 đ / 200.000 đ / 350.000 đ / 500.000 đ | hợp lệ |
| gemini-3.5-flash-lite | mua | Đặt lịch qua app, chọn đúng giờ không phải chờ đợi và cam kết không chèo kéo là đúng ý tôi. Giá 199k cho 45 phút trọn gói cũng hợp lý với thu nhập. | — | 2 | 80.000 đ / 199.000 đ / 350.000 đ / 500.000 đ | hợp lệ |
| gemini-3.8-flash | — | lỗi gọi: máy chủ mô hình trả mã 503 | — | — | — | — |

### P003 · Khánh Linh, 43 tuổi, Quản lý, chủ doanh nghiệp nhỏ, thu nhập 36.500.000 đ/tháng

Cách mua: Mua gói, săn ưu đãi. Chờ khuyến mãi khai trương hoặc gói 12 lần giá 10 rồi mới thử tiệm mới. Điều e ngại: 199.000 đ một lần cắt cao hơn chỗ tôi đang cắt, khoảng 125.000–150.000 đ. Thói quen: làm việc ở văn phòng gần tiệm, hay cắt tóc giờ trưa hoặc sau 18:00

| mô hình | mua? | lý do (nguyên văn) | điều gì đổi ý | lần/tháng | rẻ nghi ngờ / đáng mua / bắt đầu đắt / quá đắt | JSON |
| --- | --- | --- | --- | ---: | --- | --- |
| gemini-3.1-flash-lite | mua | Mức giá lẻ 199k hơi cao so với chỗ cũ, nhưng tính ra mua gói 12 lần tặng 2 thì chỉ còn tầm 165k/lần, chấp nhận được với dịch vụ trọn gói không chèo kéo. | — | 2 | 80.000 đ / 150.000 đ / 199.000 đ / 279.000 đ | hợp lệ |
| gemini-3.5-flash-lite | mua | Bình thường tôi hay cắt 125-150k nên 199k hơi cao, nhưng bên này có gói 12 lần tặng 2 thành ra mua gói thì tính ra chỉ tầm 166k/lần, lại gần văn phòng và không bị chèo kéo bán thêm mỹ phẩm nên tôi thấy hợp lý. | — | 2 | 80.000 đ / 160.000 đ / 199.000 đ / 279.000 đ | hợp lệ |
| gemini-3.8-flash | — | lỗi gọi: máy chủ mô hình trả mã 503 | — | — | — | — |

### P004 · Hồng Nhung, 29 tuổi, Nhân viên văn phòng, thu nhập 22.100.000 đ/tháng

Cách mua: Đặt lịch qua app, trả QR. Chọn thợ và giờ trên app hoặc Zalo, trả bằng QR, không muốn ngồi chờ. Điều e ngại: Không biết thợ mới có cắt hợp không, phải thử một lần đã. Thói quen: làm việc ở văn phòng gần tiệm, hay cắt tóc giờ trưa hoặc sau 18:00

| mô hình | mua? | lý do (nguyên văn) | điều gì đổi ý | lần/tháng | rẻ nghi ngờ / đáng mua / bắt đầu đắt / quá đắt | JSON |
| --- | --- | --- | --- | ---: | --- | --- |
| gemini-3.1-flash-lite | mua | Cách đặt lịch qua app/Zalo và cam kết không chèo kéo làm mình thấy thoải mái, phù hợp với giờ giấc văn phòng bận rộn của mình. | — | 1 | — / — / — / — | hợp lệ |
| gemini-3.5-flash-lite | mua | Tiệm ngay gần văn phòng, lại đặt được lịch qua app và Zalo đúng khung giờ sau 18:00 nên rất hợp với lịch bận rộn của mình. | — | 2 | 80.000 đ / 199.000 đ / 350.000 đ / 500.000 đ | hợp lệ |
| gemini-3.8-flash | — | lỗi gọi: máy chủ mô hình trả mã 503 | — | — | — | — |

### P005 · Cẩm Tú, 27 tuổi, Nhân viên văn phòng, thu nhập 19.100.000 đ/tháng

Cách mua: Đặt lịch qua app, trả QR. Chọn thợ và giờ trên app hoặc Zalo, trả bằng QR, không muốn ngồi chờ. Điều e ngại: Sợ vào rồi bị mời mua thêm gói, sản phẩm. Thói quen: làm việc ở văn phòng gần tiệm, hay cắt tóc giờ trưa hoặc sau 18:00

| mô hình | mua? | lý do (nguyên văn) | điều gì đổi ý | lần/tháng | rẻ nghi ngờ / đáng mua / bắt đầu đắt / quá đắt | JSON |
| --- | --- | --- | --- | ---: | --- | --- |
| gemini-3.1-flash-lite | mua | Tiệm có app đặt lịch và cam kết không chèo kéo làm thêm dịch vụ là điểm cộng lớn với dân văn phòng như mình. Giá Essential 199k cho 45-50 phút cũng khá hợp lý để tranh thủ cắt vào giờ nghỉ trưa hoặc tối. | — | 2 | 50.000 đ / 200.000 đ / 350.000 đ / 500.000 đ | hợp lệ |
| gemini-3.5-flash-lite | mua | Đặt lịch trước qua app, quét QR thanh toán không lằng nhằng và cam kết không chèo kéo dịch vụ là đúng gu tôi. | — | 2 | 80.000 đ / 199.000 đ / 350.000 đ / 500.000 đ | hợp lệ |
| gemini-3.8-flash | — | lỗi gọi: máy chủ mô hình trả mã 503 | — | — | — | — |
