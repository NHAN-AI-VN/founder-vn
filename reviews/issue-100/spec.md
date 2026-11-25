Commit mã đã chấm: fea0d09b5a75

# Review trục Spec, issue #100, vòng 1

Phán quyết: PASS. Phạm vi: `git diff --stat main...HEAD` gồm `pilot/runbook.md`, `tests/test_pilot_kit.py`, `docs/evidence/issue-100-pdf-export-recipe.md`; không đụng `src/` (đúng quyết định "không đổi gói"). CI `Gate` ở commit này: success.

## Đối chiếu từng criterion

1. Mục "Xuất PDF" dưới Buổi 2, tiếng Việt: đáp ứng. `pilot/runbook.md` có `### Xuất PDF` ngay sau danh sách Buổi 2, bước 3 trỏ tới mục này. Có đường dẫn Chrome macOS, tên `google-chrome` / `chromium` cho Linux, và quy tắc gửi PDF qua Zalo rồi xóa cùng thư mục dự án (trỏ tới "Sau 90 ngày: xóa", tồn tại ở dòng 71; khớp thiết kế §6). Các lệnh trùng công thức ticket. Một chỗ lệch có chủ ý: `"$PWD/..."` thành `` "`pwd`/..." `` vì test cũ cấm `$` trong `pilot/*.md`; cho cùng đường dẫn tuyệt đối, chấp nhận được là "tương đương" và lane đã ghi rõ.
2. Công thức được kiểm trên `examples/barbershop/founder/business-plan.md`: đáp ứng, kèm một lưu ý. Bằng chứng (`docs/evidence/issue-100-pdf-export-recipe.md`) trích các khối lệnh từ runbook, chạy bằng Chrome 158 trên Linux, đọc lại bằng `pypdf`: 15 trang, "Kết luận" và câu miễn trừ khớp nguyên văn, có các số tiền `280.000 đ`, `103.600 đ`, `176.400 đ`, không có `$`. Lệnh kiểm nguyên văn của ticket trả `False` trên Linux vì `pypdf` trích "ị" thành `i` + khoảng trắng + dấu chấm dưới; lane báo thẳng điều này và chứng minh ba chuỗi khớp sau khi bỏ khoảng trắng trước dấu kết hợp và chuẩn hóa NFC. Tôi coi đây là đặc điểm của lớp trích văn bản, không phải lỗi công thức, nên không chặn. PDF không được commit (đã kiểm: không có file `.pdf` trong diff).
3. Test ghim công thức: đáp ứng. `test_runbook_carries_pdf_export_recipe` kiểm `uvx --from markdown python -m markdown`, `--print-to-pdf`, `charset="utf-8"`, hai đường dẫn trình duyệt, câu về mạng và về Zalo/xóa. Nằm trong `tests/`, chạy ở đoạn `unit` của cổng (365 passed ở bằng chứng; tôi chạy lại `tests/test_pilot_kit.py`: 7 passed). Đỏ-trước-xanh được ghi trong `## Lát`.
4. Nói rõ cần mạng chỉ cho lần `uvx` đầu và không gửi kế hoạch đi đâu: đáp ứng, ở `pilot/runbook.md` (hai gạch đầu dòng cuối mục) và được test ghim.

Giới hạn ticket: không đổi `plan_compile`, không bìa/thương hiệu, không font ngoài mặc định: không vi phạm. Không có `$` trong `pilot/runbook.md` (đã đếm 0).

## Chưa xác minh

- Đường dẫn và Chrome trên macOS: lane không chạy được; chỉ có lời operator trong ticket (2026-11-25). Bằng chứng ghi đúng điều này.
- Hiển thị bằng mắt của PDF (dấu, bảng, tiêu đề): lane không xem ảnh trang in; kiểm chỉ qua văn bản trích. Ticket chỉ đòi kiểm bằng `pypdf`.
- Lệnh kiểm nguyên văn của ticket trả `False` trên Linux (xem criterion 2). Nếu operator muốn lệnh kiểm tái lập được ở mọi nơi thì sửa lệnh trong ticket; không thuộc lane này.
- Tôi không tự chạy lại công thức: sandbox này không có Chrome/Chromium. Kết quả 15 trang dựa vào bản bằng chứng của lane.

<promise>PASS</promise>
