# Evidence: issue #100, công thức xuất PDF trong pilot/runbook.md

## Seam

Suy từ tiêu chí chấp nhận (ticket không có mục Seam do lane viết; mục Seam của ticket do người vận hành viết).

- `pilot/runbook.md`, Buổi 2: nơi duy nhất Người hỗ trợ đọc bước xuất PDF. Seam là văn bản của runbook, được ghim bằng test nội dung trong `tests/test_pilot_kit.py` (cùng kiểu với các test của #4).
- Công thức xuất PDF: kiểm bằng cách chạy trên `examples/barbershop/founder/business-plan.md` rồi đọc PDF lại bằng `pypdf`. Không có seam gói: không đổi `src/`.

## Lát

1. `tests/test_pilot_kit.py::test_runbook_carries_pdf_export_recipe`
   - Đỏ (chứng kiến trước khi sửa runbook): `AssertionError: assert '### Xuất PDF' in '# Sổ tay Người hỗ trợ: ...'`, `1 failed, 6 passed`.
   - Xanh sau khi `pilot/runbook.md` thêm mục "Xuất PDF": `uv run pytest tests/test_pilot_kit.py -q` cho `7 passed`.
   - Lệch so với công thức của ticket: test cũ `test_pilot_kit_has_no_dollar_and_no_phone_numbers` cấm ký tự `$` trong `pilot/*.md`, nên runbook viết `"`pwd`/founder/..."` (thay thế lệnh bằng dấu huyền) thay cho `"$PWD/founder/..."`. Hai dạng cho cùng đường dẫn tuyệt đối.

## Kiểm công thức trên kế hoạch mẫu

- Trình duyệt: Google Chrome for Testing 158.0.8127.88 (Linux, cài bằng `npx @puppeteer/browsers install chrome@stable`), gọi qua script bọc tên `google-chrome` thêm `--no-sandbox` (sandbox chạy bằng root). macOS không chạy được ở đây: đường dẫn macOS chỉ có trong ticket (người vận hành đã chạy 2026-11-25), lane không kiểm.
- Các khối lệnh bash được trích nguyên văn từ `pilot/runbook.md` (khối chuẩn bị, khối Linux, khối `rm`) và chạy trên bản sao của `examples/barbershop/founder/` đặt trong `.harness/proj/`. Ví dụ gốc không bị sửa, PDF không được commit.
- Kết quả: `486927 bytes written`, hai file HTML trung gian đã bị xóa, còn `founder/business-plan.pdf`.
- Đọc lại bằng `pypdf`: 15 trang. Kế hoạch mẫu này ngắn hơn kế hoạch 21 trang của buổi chạy #19.

```text
literal check (lệnh của ticket): False
normalised check: True   (Kết luận, anh/chị, không phải tư vấn tài chính, thuế hay pháp lý; anh/chị xuất hiện 33 lần)
VND: ['280.000 đ', '103.600 đ', '176.400 đ']
dollar next to digit: False   (không có ký tự $ nào trong văn bản PDF)
```

Vì sao lệnh nguyên văn của ticket cho `False` ở đây: trên Linux, Chrome dùng Noto Sans và ghép "ị" từ "i" cộng dấu chấm dưới; `pypdf` trả về `anh/chi ̣` (có khoảng trắng trước dấu kết hợp). Văn bản "Kết luận" và câu miễn trừ khớp nguyên văn. Sau khi bỏ khoảng trắng trước dấu kết hợp (`re.sub(r"\s+(?=[\u0300-\u036f])","",text)`) và chuẩn hóa NFC, cả ba chuỗi khớp. Đây là đặc điểm của lớp trích văn bản, không phải của công thức; nhưng nó có nghĩa lệnh kiểm của ticket có thể cho `False` trên Linux dù PDF đúng. Lane không xem ảnh trang in nên không khẳng định về hiển thị bằng mắt.

## Cổng ba đoạn

HEAD của cổng: 846903b33368d653b206ef29a0a3a93d964a1e7f (sau đó chỉ thêm commit tài liệu bằng chứng).

```text
All checks passed!                        (static)
365 passed in 29.45s                      (unit)
Successfully built dist/founder_vn-0.2.0-py3-none-any.whl   (build)
gate-segment verify: GREEN on 846903b33368d653b206ef29a0a3a93d964a1e7f
```

## Giới hạn

- Đường dẫn macOS và Chrome trên macOS không được lane chạy; chỉ có lời người vận hành trong ticket.
- Lệnh kiểm `pypdf` nguyên văn của ticket cho `False` trên Linux vì cách tách dấu của "ị" (xem trên); kiểm có chuẩn hóa cho `True`. Chưa xem ảnh trang in.
- Trình duyệt chạy với `--no-sandbox` qua script bọc vì sandbox là root; cờ này không có trong công thức của Người hỗ trợ.
- Số trang (15) khác 21 của ticket vì kế hoạch mẫu khác.
- Mục ticket "mạng chỉ cho lần `uvx` đầu" được ghi ở runbook; lane không đo lưu lượng mạng của Chrome.
