# Sổ nguồn pháp lý (sources ledger)

Mỗi con số pháp lý mà skill, báo cáo hay fixture dùng có một mục ở đây: link chính thức, số và ngày Công báo, điều khoản, trích đoạn nguyên văn và ngày kiểm chứng (quy tắc của `CONTRIBUTING.md`). Số liệu không có mục ở đây thì chưa được dùng. Pháp luật đổi thì mở issue theo mẫu "Law changed".

Nguồn là Công báo điện tử nước CHXHCN Việt Nam (`congbao.chinhphu.vn`), bản PDF có chữ ký số của Văn phòng Chính phủ. Trích đoạn chép từ PDF ấy.

## Văn bản áp dụng cho hộ kinh doanh ngành dịch vụ cắt tóc tại 23/11/2026

| # | Văn bản | Điều khoản dùng | Hiệu lực | Link Công báo |
|---|---|---|---|---|
| 1 | Luật Thuế giá trị gia tăng số 48/2024/QH15 (thông qua 26/11/2024) | Điều 12 khoản 2 điểm b2; Điều 5 khoản 25 | 01/7/2025; khoản 25 Điều 5 từ 01/01/2026 (Điều 18) | https://congbao.chinhphu.vn/van-ban/luat-so-48-2024-qh15-43576.htm (Công báo 1527+1528, 29/12/2024) |
| 2 | Luật số 149/2025/QH15 sửa Luật Thuế GTGT (thông qua 11/12/2025) | Điều 1 khoản 1 điểm b (khoản 25 Điều 5: 500 triệu) | 01/01/2026 | https://congbao.chinhphu.vn/van-ban/luat-so-149-2025-qh15-468709.htm (Công báo 42, 22/01/2026) |
| 3 | Luật Thuế thu nhập cá nhân số 109/2025/QH15 (thông qua 10/12/2025) | Điều 7 khoản 1, khoản 3; Điều 29 khoản 2 | 01/7/2026; thu nhập từ kinh doanh áp dụng từ kỳ tính thuế 2026 | https://congbao.chinhphu.vn/van-ban/luat-so-109-2025-qh15-468671.htm (Công báo 37, 22/01/2026) |
| 4 | Luật số 09/2026/QH16 sửa bốn luật thuế (thông qua 24/4/2026) | Điều 1 (khoản 1 Điều 7 Luật TNCN), Điều 2 (khoản 25 Điều 5 Luật GTGT): ngưỡng do Chính phủ quy định | Điều 1, 2 từ 01/01/2026 (Điều 5) | https://congbao.chinhphu.vn/van-ban/luat-so-09-2026-qh16-469536.htm (Công báo 286, 27/05/2026) |
| 5 | Nghị định 68/2026/NĐ-CP (05/3/2026) về chính sách thuế và quản lý thuế đối với hộ kinh doanh, cá nhân kinh doanh | Điều 3 (GTGT), Điều 4 (TNCN), Điều 5 (doanh thu) | từ ngày ký (Điều 19) | https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-68-2026-nd-cp-469047.htm (Công báo 152, 19/03/2026) |
| 6 | Nghị định 141/2026/NĐ-CP (29/4/2026) sửa Nghị định 68/2026 | Điều 1 khoản 1: "500 triệu đồng" thành "01 tỷ đồng" tại Điều 3, Điều 4, ... | 01/01/2026 (Điều 3) | https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-141-2026-nd-cp-469455.htm (Công báo 272, 14/05/2026) |
| 7 | Nghị định 253/2026/NĐ-CP (30/6/2026) hướng dẫn Luật Thuế TNCN | Điều 45 khoản 2; Phụ lục mục 2 ("cắt tóc, làm đầu, gội đầu": 2%) | 01/7/2026; kinh doanh áp dụng từ kỳ tính thuế 2026 (Điều 69) | https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-253-2026-nd-cp-469959.htm (Công báo 402, 16/07/2026) |

Rà soát Công báo ngày 23/11/2026: trong 360 nghị định năm 2026 đã đăng (danh mục `nghi-dinh-l1`, trang 1 đến 38), văn bản sửa Nghị định 68/2026 duy nhất là Nghị định 141/2026. Không rà thông tư của Bộ Tài chính. Hai ưu đãi tạm thời (Nghị định 174/2025/NĐ-CP; Nghị quyết 43/2026/QH16 cùng Nghị định 398/2026/NĐ-CP) chưa kiểm chứng và không đưa vào mô hình.

## tax_rate_on_revenue: cắt tóc, làm đầu, gội đầu

- Giá trị cho `numbers.json`: 7 (phần trăm). Là tỷ lệ gộp theo định nghĩa của Q37: GTGT 5% cộng TNCN 2%.
- GTGT 5%: Luật 48/2024/QH15, Điều 12 khoản 2 điểm b2. Link: https://congbao.chinhphu.vn/van-ban/luat-so-48-2024-qh15-43576.htm (Công báo 1527+1528, 29/12/2024).
- TNCN 2%: Luật 109/2025/QH15, Điều 7 khoản 3 điểm c. Link: https://congbao.chinhphu.vn/van-ban/luat-so-109-2025-qh15-468671.htm (Công báo 37, 22/01/2026).
- Ngành: Nghị định 253/2026/NĐ-CP, Điều 45 khoản 2 và Phụ lục mục 2. Link: https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-253-2026-nd-cp-469959.htm (Công báo 402, 16/07/2026).
- Trích đoạn:

> Luật 48/2024/QH15, Điều 12 khoản 2: "Số thuế giá trị gia tăng phải nộp theo phương pháp tính trực tiếp theo doanh thu bằng tỷ lệ % nhân với doanh thu … a2) Hộ, cá nhân sản xuất, kinh doanh … b) Tỷ lệ % để tính thuế giá trị gia tăng được quy định như sau: b1) Phân phối, cung cấp hàng hóa: 1%; b2) Dịch vụ, xây dựng không bao thầu nguyên vật liệu: 5%; b3) Sản xuất, vận tải, dịch vụ có gắn với hàng hóa, xây dựng có bao thầu nguyên vật liệu: 3%; b4) Hoạt động kinh doanh khác: 2%; c) Doanh thu để tính thuế giá trị gia tăng là tổng số tiền bán hàng hóa, dịch vụ ghi trên hóa đơn bán hàng, bao gồm các khoản phụ thu và phí thu thêm mà cơ sở kinh doanh được hưởng."

> Luật 109/2025/QH15, Điều 7 khoản 3: "Cá nhân kinh doanh có doanh thu năm trên mức quy định tại khoản 1 Điều này đến 03 tỷ đồng được lựa chọn nộp thuế theo quy định tại điểm a và điểm b khoản 2 Điều này hoặc nộp thuế theo thuế suất nhân (x) với doanh thu tính thuế. Doanh thu tính thuế và thuế suất được xác định như sau: a) Doanh thu tính thuế được xác định bằng phần doanh thu vượt trên mức quy định tại khoản 1 Điều này; b) Phân phối, cung cấp hàng hoá: thuế suất 0,5%; c) Dịch vụ, xây dựng không bao thầu nguyên vật liệu: thuế suất 2%. Riêng hoạt động cho thuê tài sản, đại lý bảo hiểm, đại lý xổ số, đại lý bán hàng đa cấp: thuế suất 5%; d) … 1,5%; đ) … 5%; e) Hoạt động kinh doanh khác: thuế suất 1%." Khoản 2 (áp dụng khi doanh thu năm trên 03 tỷ đồng, hoặc khi cá nhân chọn): thu nhập tính thuế = doanh thu − chi phí; thuế suất 15% (trên ngưỡng đến 03 tỷ), 17% (trên 03 tỷ đến 50 tỷ), 20% (trên 50 tỷ).

> Nghị định 253/2026/NĐ-CP, Điều 45 khoản 2: "Thuế suất tính trên doanh thu tính thuế quy định tại khoản 3 Điều 7 của Luật Thuế thu nhập cá nhân được quy định chi tiết theo danh mục ngành, nghề tại Phụ lục ban hành kèm theo Nghị định này." Phụ lục, mục 2 "Dịch vụ, xây dựng không bao thầu nguyên vật liệu", thuế suất 2%, gồm dòng "Dịch vụ may đo, giặt là; cắt tóc, làm đầu, gội đầu".

- Sai lệch của cách gộp (quyết định Q52, `docs/founder-vn-design.md`): luật tính GTGT 5% trên toàn bộ doanh thu năm khi vượt ngưỡng (Nghị định 68/2026 Điều 3 khoản 2), còn TNCN 2% chỉ trên phần vượt ngưỡng (Luật 109/2025 Điều 7 khoản 3 điểm a). Mô hình áp tỷ lệ gộp lên toàn bộ doanh thu năm nên tính thừa tối đa 2% nhân 1 tỷ đồng, tức 20 triệu đồng mỗi năm, theo hướng an toàn. Trên 03 tỷ đồng doanh thu năm, TNCN tính trên thu nhập với thuế suất 17% (Luật 109/2025 Điều 7 khoản 2), mô hình chưa có cờ cho mốc này.
- Xác nhận: kiểm chứng ngày 23/11/2026 bởi operator trên bản PDF Công báo

## tax_free_threshold: doanh thu năm không chịu thuế

- Giá trị cho `numbers.json`: 1.000.000.000 đ mỗi năm (ngưỡng theo doanh thu cả năm, không theo tháng).
- Căn cứ: Nghị định 68/2026/NĐ-CP, Điều 3 và Điều 4, sau khi Nghị định 141/2026/NĐ-CP, Điều 1 khoản 1, đổi "500 triệu đồng" thành "01 tỷ đồng" (hiệu lực 01/01/2026). Luật 09/2026/QH16 Điều 1 và Điều 2 giao mức này cho Chính phủ quy định.
- Link: https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-68-2026-nd-cp-469047.htm (Công báo 152, 19/03/2026); https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-141-2026-nd-cp-469455.htm (Công báo 272, 14/05/2026); https://congbao.chinhphu.vn/van-ban/luat-so-09-2026-qh16-469536.htm (Công báo 286, 27/05/2026).
- Trích đoạn:

> Luật 09/2026/QH16, Điều 1: "1. Cá nhân cư trú có hoạt động sản xuất, kinh doanh có doanh thu năm từ mức quy định của Chính phủ trở xuống không phải nộp thuế thu nhập cá nhân. …". Điều 2 sửa khoản 25 Điều 5 Luật GTGT cùng cách: "… có doanh thu năm từ mức quy định của Chính phủ trở xuống …".

> Nghị định 68/2026/NĐ-CP (đã sửa bởi Nghị định 141/2026/NĐ-CP, mức "500 triệu đồng" đọc là "01 tỷ đồng"), Điều 3: "1. Hộ kinh doanh, cá nhân kinh doanh có hoạt động sản xuất, kinh doanh có mức doanh thu năm từ [01 tỷ đồng] trở xuống thuộc đối tượng không chịu thuế giá trị gia tăng. 2. Hộ kinh doanh, cá nhân kinh doanh có hoạt động sản xuất, kinh doanh có mức doanh thu năm trên [01 tỷ đồng] thuộc đối tượng chịu thuế giá trị gia tăng và áp dụng phương pháp tính trực tiếp theo doanh thu bằng tỷ lệ % nhân (x) doanh thu. Tỷ lệ % và doanh thu tính thuế thực hiện theo quy định của Luật Thuế giá trị gia tăng số 48/2024/QH15 và các văn bản hướng dẫn thi hành." Điều 4 khoản 1: "… có mức doanh thu năm từ [01 tỷ đồng] trở xuống không phải nộp thuế thu nhập cá nhân." Khoản 3: "… cá nhân được áp dụng mức trừ [01 tỷ đồng] trước khi tính thuế thu nhập cá nhân …". Khoản 5 điểm a: "Phương pháp tính thuế thu nhập cá nhân theo thuế suất nhân (x) doanh thu tính thuế áp dụng đối với cá nhân kinh doanh có doanh thu năm trên [01 tỷ đồng] đến 03 tỷ đồng."

> Nghị định 141/2026/NĐ-CP, Điều 1 khoản 1: "Sửa đổi cụm từ "500 triệu đồng" thành "01 tỷ đồng" tại Điều 3, Điều 4, khoản 1 Điều 8, Điều 9, Điều 10, khoản 3 Điều 11, khoản 1 và khoản 2 Điều 12, khoản 4 Điều 17, khoản 3 Điều 18 Nghị định số 68/2026/NĐ-CP." Điều 3: "Nghị định này có hiệu lực thi hành từ ngày 01 tháng 01 năm 2026."

- Xác nhận: kiểm chứng ngày 23/11/2026 bởi operator trên bản PDF Công báo
