# Giá: Tiệm cắt tóc nam kiểu barbershop ở Quận 7 cũ (ví dụ tổng hợp, không phải số liệu thật)

Anh/chị đọc file này như một giá để thử ngoài thực tế, không phải giá chốt. Số liệu lấy từ 20 câu trả lời giá hợp lệ của panel mô phỏng (0 câu bị loại; không có cảnh báo dữ liệu mỏng), từ bảng giá trong `founder/competitors.md` và từ mô hình CFO trong `founder/numbers.json`. Mọi con số do `founder-vn pricing` và `founder-vn cfo` tính; không số nào do tôi tự tính hay đoán.

## Khoảng giá chấp nhận được

| câu hỏi của panel | trung vị |
| --- | ---: |
| Rẻ đến mức nghi ngờ chất lượng | 80.000 đ |
| Rẻ, đáng mua | 150.000 đ |
| Bắt đầu thấy đắt | 250.000 đ |
| Đắt đến mức không mua | 400.000 đ |

- Giá thấp nhất còn chấp nhận được: **120.000 đ**.
- Giá cao nhất còn chấp nhận được: **316.667 đ**.
- Điểm cân bằng (rẻ và đắt có số người chọn bằng nhau): **199.625 đ**.

Giá đối thủ lấy nguyên từ `founder/competitors.md` (khảo sát bàn giấy ngày 23/11/2026, giá niêm yết một lần cắt; "từ" nghĩa là giá sàn, không phải giá thường gặp): 4RAU Barber Shop từ 70.000 đ, 30Shine từ 94.000 đ, Vu Tri Barbershop từ 100.000 đ, Liem Barber Shop 120.000 đ, Tony Barber House 180.000 đ, emo. Hair Salon 350.000 đ, House of Barbaard 400.000 đ. Le Barbier de Saigon chưa có số liệu giá của tiệm nên không đưa vào. Công cụ cho kết quả: 2 trên 7 giá đối thủ nằm trong khoảng chấp nhận được (Liem Barber Shop và Tony Barber House). Các tiệm còn lại hoặc rẻ hơn mức thấp nhất của panel (ba tiệm giá sàn), hoặc đắt hơn mức cao nhất (emo. và House of Barbaard).

Giá bán trong mô hình CFO là 280.000 đ (`founder/cfo.md`, "Giá bán"): nằm trong khoảng chấp nhận được, nhưng cao hơn mức trung vị "bắt đầu thấy đắt" là 250.000 đ.

## Giá đề xuất

**199.000 đ** cho Essential Cut, làm tròn từ điểm cân bằng 199.625 đ của công cụ (lệch dưới 1.000 đ) và là giá anh/chị đã niêm yết trong `founder/idea.md`.

- 199.000 đ: thấp hơn mức hòa vốn của CFO. Với giá này mô hình CFO cho biên lợi nhuận theo kế hoạch -13% và hòa vốn 50,8 lượt mỗi ngày, trong khi kế hoạch là 40 lượt mỗi ngày (công suất tối đa 66). Mô hình giữ nguyên các khoản chi phí theo số tiền anh/chị nhập (không co theo giá), nên đây là con số cho một lượt bán đúng giá này.
- Hai chỗ này kéo ngược nhau và tôi không chọn thay anh/chị: panel muốn giá quanh 199.000 đ, còn mô hình CFO chỉ có lãi khi giá bình quân mỗi lượt cao hơn. Vé gộp bình quân dự kiến trong `founder/idea.md` là khoảng 280.000 đ, nên kết quả phụ thuộc vào việc khách có chọn Signature và gói hay không (xem phần theo dõi).

## Bậc giá

Các bậc là bảng giá của chính anh/chị trong `founder/idea.md`; tôi không thêm bậc nào.

| bậc | dịch vụ | giá | trong khoảng chấp nhận được | biên lợi nhuận theo kế hoạch (CFO) | hòa vốn mỗi ngày (CFO) |
| --- | --- | ---: | --- | ---: | ---: |
| good (giá đề xuất) | Essential Cut | 199.000 đ | có | -13% | 50,8 lượt, dưới hòa vốn |
| better | Signature Cut | 279.000 đ | có | 19% | 27,63 lượt |
| best | Signature + cạo | 389.000 đ | không, cao hơn 316.667 đ | 42% | 16,98 lượt |

Bậc best nằm ngoài khoảng chấp nhận được của panel, nên đừng dựa vào nó để bù cho bậc good khi chưa có khách thật mua thử.

## Ưu đãi mở đầu để thử

Thử hai giá cạnh nhau với khách thật: Essential Cut 199.000 đ và Signature Cut 279.000 đ, cùng lời hứa trong `founder/pitch.md`. Mục đích là xem bao nhiêu khách tự chọn Signature, vì đó là chỗ mô hình CFO bắt đầu có lãi.

- Đặt cọc 50.000 đ cho khung 17:00 đến 21:00 và cuối tuần: trong lý do không mua nhóm "thời điểm" của panel (6 người), hai lời nguyên văn (P001, P007) nhắc đúng khoản đặt cọc này. Anh/chị cân nhắc bỏ cọc trong giai đoạn thử để không lẫn phản ứng với giá.
- Số khách cần thử và số tuần thử: file của anh/chị chưa có con số nào cho việc này, nên tôi không đặt; anh/chị cho tôi biết rồi ghi vào đây.
- Không dùng thêm mức giảm nào ngoài những gì anh/chị đã ghi (giảm 15% ngày thường 10:00 đến 16:00, gói 12 lần giá 10).

## Theo dõi sau khi mở bán

- Tỷ lệ khách chọn từng bậc, so với giả định trong `founder/idea.md` (55% Essential, 25% Signature, 20% gói trọn bộ). Nếu Essential chiếm nhiều hơn, vé gộp bình quân thấp hơn 280.000 đ và hòa vốn xa hơn 28 lượt mỗi ngày.
- Số lượt mỗi ngày so với hòa vốn của CFO (28 lượt ở giá 280.000 đ, 50,8 lượt nếu mọi lượt chỉ bán ở 199.000 đ).
- Điều kiện dừng anh/chị đã đặt sau 9 tháng: dưới 9 lượt mỗi ghế mỗi ngày, tỷ lệ khách quay lại trong 60 ngày dưới 55%, vé gộp thực thu dưới 265.000 đ.
- Lời phàn nàn về giá và câu "đắt" hay "rẻ quá" khách nói tại quầy; ghi lại nguyên văn.
- Khi có 20 khách thật trả lời bốn câu hỏi giá, chạy lại `founder-vn pricing` với số của họ thay cho panel.

Panel là mô phỏng, cận trên, không phải khách hàng thật. Dùng khoảng giá này để chọn giá thử, rồi xác nhận với khách thật (bán trước, danh sách chờ, trang giới thiệu có ghi giá) trước khi chi tiền. Panel chạy bằng mô hình gemini-3.5-flash-lite.

Kết quả này không phải tư vấn tài chính, thuế hay pháp lý.
