Commit mã đã chấm: b0a3e6203a5f

# Review trục Spec, issue #5, vòng 1

Phạm vi: `git diff --stat main...HEAD` (README.md, docs/evidence/issue-5-golden-case.md, docs/founder-vn-design.md, examples/barbershop/founder/idea.md, tests/test_golden_case.py) và 7 commit của `git log main..HEAD`. Đã đọc file thật `idea.md`, đoạn README, Q51 và file evidence. CI Gate run 45129886280 success ở commit này.

Phán quyết: CHANGES_REQUESTED (một finding chặn, sửa được trong phạm vi lane).

## Đối chiếu criterion

1. `idea.md` ở thư mục gốc dự án ví dụ: file có ở `examples/barbershop/founder/idea.md` (đúng đường dẫn `examples/<case>/founder/` của design §5). Có đủ năm mục của dạng upstream (là gì, cho ai, bán gì giá bao nhiêu bằng VND, ở đâu và bằng cách nào, ngân sách và ràng buộc) cùng tên gọi tạm. Giá VND định dạng Việt, không `$`, có miễn trừ trách nhiệm. Bằng chứng: đọc file, cộng `tests/test_golden_case.py` (chạy trong cổng `unit`, 224 passed theo evidence; CI success). Phần "ẩn danh, vị trí tới cấp quận" **chưa đáp ứng**, xem SPEC-1.
2. Chủ case đồng ý công bố ẩn danh: chủ case chính là chủ dự án, Q51 ghi là quyết định của chủ dự án và evidence ghi sự đồng ý trong phiên 2026-11-23. Chấp nhận được vì không có bên thứ ba, nhưng bằng chứng chỉ là lời ghi trong repo do lane viết; xem mục chưa xác minh.
3. README tham chiếu thư mục ví dụ là golden case: mục "Golden case" của README trỏ `examples/barbershop/` và link tới `idea.md`; test `test_readme_names_the_example_directory_as_the_golden_case` chạy trong `unit`. Đáp ứng. README là file một-chủ, lane có cấp phát (evidence ghi comment cấp phát lúc 2026-11-23T06:43:15Z; không kiểm chứng được từ sandbox này).

Việc sửa design (Q51, sửa Q21 và dòng tuần 1 §7) nằm trong phạm vi vì thân ticket tự nêu Q51; không phải quyết định tự đặt của lane.

## Finding chặn

### SPEC-1: idea.md ghi vị trí dưới cấp quận ("khu Phú Mỹ Hưng")

Criterion 1 đòi "location to district level"; AGENTS.md mục 8 cấm vị trí dưới cấp quận trong examples. Chuỗi "khu Phú Mỹ Hưng (Quận 7 cũ)" xuất hiện ở mục "Cho ai" và "Ở đâu và bằng cách nào" của `idea.md`, và "Đã quyết: ... khu Phú Mỹ Hưng" ở mục ngân sách. Phú Mỹ Hưng là một khu đô thị cụ thể nằm trong quận, tức mịn hơn cấp quận; kèm bán kính 1,5 km, 4 ghế, 55–60 m² và giá thuê thì khả năng xác định cơ sở cao hơn. Q51 mục (4) và evidence tự tuyên "vị trí ghi tới cấp quận cũ" trong khi chính văn bản lại nêu khu, nên khẳng định không khớp nội dung. Test `test_example_is_anonymised` không bắt được vì chỉ tìm số nhà, điện thoại, email, `$`. Chặn vì criterion 1 không đạt ở phần ẩn danh.

Sửa (lane làm được, không chạm file cấm): thay "khu Phú Mỹ Hưng" bằng "Quận 7 cũ, TP.HCM" trong `idea.md` (3 chỗ), sửa chữ tương ứng ở Q51 của `docs/founder-vn-design.md` và `docs/evidence/issue-5-golden-case.md`; nên thêm vào test ẩn danh một kiểm tra tên khu/đô thị đó. Lưu ý tên "Phú Mỹ Hưng" cũng đang nằm trong lịch sử git; việc đó không thuộc finding này.

## Chưa xác minh

- Đồng ý công bố (criterion 2): bằng chứng chỉ nằm trong file evidence và Q51 do lane viết. Nếu operator muốn một dấu vết ngoài lane, cần chủ dự án xác nhận trên issue #5. Không gắn mã vì chủ case trùng chủ dự án và Q51 ghi là quyết định của chủ dự án.
- Số tài chính (vốn 1,5 tỷ, thuê 35–40 triệu, lương, ngưỡng dừng): là ước tính kế hoạch từ nghiên cứu riêng, đã gán nhãn "ước tính, chưa kiểm chứng" trong file. AGENTS.md mục 8 cấm "real financials"; đọc là số vận hành thực nên không chặn, nhưng operator nên xác nhận chủ dự án chấp nhận công bố các số này.
- Comment cấp phát cho README.md không đọc được từ sandbox (không có credential tracker).
- Không chạy lại test cục bộ; dựa vào CI Gate success do briefing cung cấp.

<promise>CHANGES_REQUESTED</promise>
