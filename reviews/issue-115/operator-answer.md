# Trả lời của operator — review #115, vòng 2

Trả lời cho `reviews/issue-115/spec.md` (BLOCKED, commit mã đã chấm `1fcd43cb25d8`), mục "Câu hỏi cho operator". File này không phải báo cáo review; nó là đầu vào cho vòng review kế. Lượt Standards vòng 2 đã PASS ở cùng commit mã. Ba finding vòng 1 (S1, SPEC-1, SPEC-2, SPEC-3) đã đóng trong `reviews/issue-115/ledger.md`; câu hỏi này không mang mã finding.

## Câu hỏi: kênh người sáng tạo địa phương khi không có nguồn

- [x] Chọn **(b)**: xử lý như ShopeeFood/GrabFood. Hàng kênh ghi "**Không áp dụng (chưa có nguồn)**" kèm lý do và điều kiện mở lại; bỏ Ngày 22 và 25 của kênh này; dồn một phần ngân sách sang kênh khác; tái sinh `business-plan.md`.
- [ ] ~~(a) giữ ở mức nhỏ, ghi nhận ngoại lệ cho criterion 2~~
- [ ] ~~(c) sửa ticket/thiết kế để kênh được phép khi chưa có nguồn~~

Vì sao (b): ticket đã đặt khuôn cho chính trường hợp này ở ShopeeFood/GrabFood ("không áp dụng" kèm lý do khi kênh không hợp); luật "không thêm kênh mà khách chưa được chứng tỏ dùng" là luật mạnh nhất của skill và không nên có ngoại lệ ở golden đầu tiên; thiết kế không cần đổi vì danh sách kênh vẫn cố định, chỉ bằng chứng quyết định kênh nào được dùng. `idea.md` ghi khách biết tiệm qua Google Maps, Facebook, Zalo và truyền miệng trong khu; không buyer nào trong `panel/results.md` nêu người sáng tạo; "thợ quen giới thiệu" (P015) là bằng chứng cho kênh khác.

## Sửa thẳng trên nhánh lane

- `b93a806` `slice(founder-marketing)`: `skills/founder-marketing/SKILL.md` mục 2 thêm luật: kênh trong danh sách mà không file nào của chủ hộ cho thấy khách dùng thì ghi "không áp dụng (chưa có nguồn)", nêu điều gì mở lại, không hàng chiến dịch, không phần ngân sách, không số đo; bằng chứng của kênh khác không phải nguồn. Golden `marketing.md`: hàng kênh đổi theo; Ngày 22 thành Google Maps (khách nêu tên thợ trong đánh giá, D và E), Ngày 25 thành Zalo OA (khách đã cắt hai lần giới thiệu người quen đặt lịch với cùng thợ, D, không tặng gì); Zalo OA 2 thành 3 phần, người sáng tạo 1 thành 0, tổng vẫn 10; bỏ hàng số đo của kênh. Test đỏ rồi xanh cùng commit: `test_a_channel_with_no_source_in_the_owners_files_is_not_applicable`, `test_golden_local_creators_not_applicable_without_a_source_and_unused_downstream` (đỏ: `assert 'no file of the Owner' in …`; `assert 'Không áp dụng' in '| Người sáng tạo địa phương | Dùng ở mức nhỏ …'`), và `test_golden_budget_shares_sum_to_ten_and_not_applicable_channels_get_zero` (giữ tổng 10 khi dồn phần).
- `f6c0f9e` `slice(founder-plan)`: `business-plan.md` tái sinh bằng `founder-vn plan`; chỉ mục Tiếp thị nhúng đổi, kết luận và mọi con số giữ nguyên.
- Cổng ba đoạn chạy lại ở `f6c0f9e`: xem `docs/evidence/issue-115-founder-marketing.md`, khối `## Cổng ba đoạn`.

Hai mục "Chưa xác minh" của báo cáo (hook 1 và 2 cùng trả lời A; hook 8 gắn P018) không chặn và không sửa trong lượt này.
