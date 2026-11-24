# Giá: Tiệm cắt tóc nam kiểu barbershop ở Quận 7 cũ (ví dụ tổng hợp, không phải số liệu thật)

Anh/chị đọc file này như một giá để thử với khách thật, không phải giá chốt. Nguồn số: 20 câu trả lời giá hợp lệ của panel mô phỏng (0 câu bị loại; công cụ không báo dữ liệu mỏng; panel chạy bằng mô hình gemini-3.5-flash-lite, ghi trong `founder/panel/panel.json`), bảng giá niêm yết trong `founder/competitors.md`, mô hình CFO trong `founder/numbers.json` và `founder/cfo.md`, và bảng giá của chính anh/chị trong `founder/idea.md`. Mọi con số dưới đây do `founder-vn pricing` và `founder-vn cfo --price` tính; tôi chỉ đọc, so và giải thích, không tự tính hay đoán số nào.

## Khoảng giá chấp nhận được

Bốn câu hỏi giá của panel, lấy trung vị:

| câu hỏi | trung vị |
| --- | ---: |
| Rẻ đến mức nghi ngờ chất lượng | 80.000 đ |
| Rẻ, đáng mua | 150.000 đ |
| Bắt đầu thấy đắt | 250.000 đ |
| Đắt đến mức không mua | 400.000 đ |

- Giá thấp nhất còn chấp nhận được: **120.000 đ**.
- Giá cao nhất còn chấp nhận được: **316.667 đ**.
- Điểm cân bằng (số người thấy rẻ bằng số người thấy đắt): **199.625 đ**.

Giá đối thủ, mỗi tiệm một giá cho một lần cắt tóc nam, chép nguyên từ `founder/competitors.md` (khảo sát bàn giấy ngày 23/11/2026, giá niêm yết, không phải giá thực thu; chữ "từ" là giá sàn, không phải giá thường gặp):

| đối thủ | giá một lần cắt | so với khoảng 120.000 đ đến 316.667 đ |
| --- | ---: | --- |
| 4RAU Barber Shop | từ 70.000 đ | dưới khoảng (giá sàn) |
| 30Shine | từ 94.000 đ | dưới khoảng (giá sàn) |
| Vu Tri Barbershop | từ 100.000 đ | dưới khoảng (giá sàn) |
| Liem Barber Shop | 120.000 đ | trong khoảng, đúng mức thấp nhất |
| Tony Barber House | 180.000 đ | trong khoảng |
| emo. Hair Salon (thợ Việt) | 350.000 đ | trên khoảng |
| House of Barbaard | 400.000 đ | trên khoảng |

Công cụ đếm 2 trên 7 giá đối thủ nằm trong khoảng chấp nhận được (Liem Barber Shop và Tony Barber House). Le Barbier de Saigon không có trong bảng: ô giá của tiệm này trong `founder/competitors.md` ghi "chưa có số liệu" (bài nguồn chỉ nêu khoảng giá của một nhóm tiệm, không phải giá của tiệm), nên không được tính là giá.

Giá bán trong mô hình CFO là 280.000 đ (`founder/cfo.md`, "Giá bán"; theo `founder/idea.md` đó là vé gộp bình quân dự kiến, không phải một dịch vụ niêm yết): nằm trong khoảng chấp nhận được, nhưng cao hơn trung vị "bắt đầu thấy đắt" 250.000 đ. Ở giá này mô hình CFO cho biên lợi nhuận theo kế hoạch 20% và hòa vốn 27,48 lượt mỗi ngày.

## Giá đề xuất

**199.000 đ** cho một lần Essential Cut.

- Xuất phát từ điểm cân bằng 199.625 đ của công cụ. 199.000 đ là giá tròn cách điểm đó dưới 1.000 đ và là giá anh/chị đã niêm yết cho Essential Cut trong `founder/idea.md`, nên tôi lấy nó làm số làm tròn của con số công cụ.
- 199.000 đ: thấp hơn mức hòa vốn của CFO. Mô hình cho biên lợi nhuận theo kế hoạch -13% và hòa vốn 50,8 lượt mỗi ngày, trong khi kế hoạch của anh/chị là 40 lượt mỗi ngày và công suất tối đa 66 lượt (`founder/numbers.json`). Mô hình giữ mọi khoản chi phí theo số tiền anh/chị nhập và chỉ đổi giá, nên đây là con số khi mọi lượt đều bán đúng 199.000 đ.
- Panel và mô hình CFO kéo về hai phía và tôi không chọn thay anh/chị: người mua mô phỏng cân bằng quanh 199.000 đ, còn mô hình CFO chỉ có lãi khi vé bình quân mỗi lượt cao hơn (280.000 đ trong `founder/numbers.json`). Cả hai số đứng cạnh nhau ở đây để anh/chị quyết; tôi không dời giá đề xuất để né cờ hòa vốn.

## Bậc giá

Ba bậc là ba mức giá cho một lần cắt mà anh/chị đã niêm yết trong `founder/idea.md`, xếp từ thấp đến cao; tôi không thêm bậc nào. Cạo khăn nóng hoặc tỉa râu 139.000 đ và Gội dưỡng sinh 129.000 đ cũng có trong bảng giá của anh/chị nhưng là dịch vụ riêng, không phải một lần cắt mà panel đã trả lời giá, nên không xếp vào bậc.

| bậc | dịch vụ | giá | trong khoảng chấp nhận được | biên lợi nhuận theo kế hoạch (CFO) | hòa vốn mỗi ngày (CFO) |
| --- | --- | ---: | --- | ---: | ---: |
| tốt (good), **giá đề xuất** | Essential Cut | 199.000 đ | có | -13% | 50,8 lượt, dưới hòa vốn (kế hoạch 40 lượt) |
| tốt hơn (better) | Signature Cut | 279.000 đ | có | 19% | 27,63 lượt |
| tốt nhất (best) | Signature + cạo | 389.000 đ | không, cao hơn 316.667 đ | 42% | 16,98 lượt |

Bậc tốt nhất nằm ngoài khoảng panel chấp nhận; đừng dựa vào nó để bù cho bậc đề xuất trước khi có khách thật mua.

## Ưu đãi mở đầu để thử

Một ưu đãi để thử với khách thật: bán Essential Cut 199.000 đ cạnh Signature Cut 279.000 đ đúng giá niêm yết, cùng lời hứa trọn gói trong `founder/idea.md` (gội, khăn nóng, tạo kiểu, đồ uống, không mời mua thêm), và giữ nguyên những ưu đãi anh/chị đã ghi: giảm 15% ngày thường 10:00 đến 16:00; gói 12 lần giá 10 (Essential 1.990.000 đ, Signature 2.790.000 đ); đặt cọc 50.000 đ cho khung 17:00 đến 21:00 và cuối tuần; phụ phí 50.000 đ khi chọn thợ bậc cao nhất ở khung đó. Không thêm mức giảm nào khác ngoài những gì anh/chị đã ghi.

Điều cần đo: bao nhiêu phần khách tự chọn Signature Cut thay vì Essential Cut. 199.000 đ là giá panel cân bằng nhưng dưới hòa vốn CFO; 279.000 đ là bậc đầu tiên mô hình CFO có lãi và đứng sát giá bán 280.000 đ của mô hình. Đây là phép thử giá đề xuất của panel đứng cạnh giá bán của CFO.

Số khách cần thử và thời gian thử: tôi đã hỏi, anh/chị chọn để ngỏ, nên file này không đặt con số; anh/chị điền vào đây trước ngày mở bán.

## Theo dõi sau khi mở bán

- Tỷ lệ khách chọn từng bậc so với giả định của anh/chị trong `founder/idea.md` (55% Essential, 25% Signature, 20% gói trọn bộ). Essential chiếm nhiều hơn thì vé gộp bình quân rơi dưới 280.000 đ và hòa vốn lùi xa mốc 28 lượt mỗi ngày của `founder/cfo.md`.
- Số lượt mỗi ngày so với hòa vốn CFO: 28 lượt ở giá 280.000 đ (`founder/cfo.md`); 27,63 lượt nếu mọi lượt bán ở 279.000 đ; 50,8 lượt nếu mọi lượt chỉ bán ở 199.000 đ.
- Ba điều kiện dừng anh/chị đã đặt cho mốc 9 tháng: dưới 9 lượt mỗi ghế mỗi ngày, tỷ lệ khách quay lại trong 60 ngày dưới 55%, vé gộp thực thu dưới 265.000 đ.
- Lời phàn nàn về giá tại quầy và trên kênh đặt lịch, ghi nguyên văn, cả câu "đắt" lẫn câu "rẻ quá".
- Khi có câu trả lời của khách thật cho bốn câu hỏi giá, chạy lại `founder-vn pricing` với số của họ thay cho panel và so với file này.

Panel là mô phỏng, cận trên, không phải khách hàng thật. Dùng khoảng giá này để chọn giá thử, rồi xác nhận với khách thật (bán trước, danh sách chờ, trang giới thiệu có ghi giá) trước khi chi tiền.

Kết quả này không phải tư vấn tài chính, thuế hay pháp lý.
