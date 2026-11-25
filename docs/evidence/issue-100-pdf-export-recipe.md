# Evidence: issue #100, công thức xuất PDF trong pilot/runbook.md

## Seam

Suy từ tiêu chí chấp nhận (ticket không có mục Seam do lane viết; mục Seam của ticket do người vận hành viết).

- `pilot/runbook.md`, Buổi 2: nơi duy nhất Người hỗ trợ đọc bước xuất PDF. Seam là văn bản của runbook, được ghim bằng test nội dung trong `tests/test_pilot_kit.py` (cùng kiểu với các test của #4).
- Công thức xuất PDF: kiểm bằng cách chạy trên `examples/barbershop/founder/business-plan.md` rồi đọc PDF lại bằng `pypdf`. Không có seam gói: không đổi `src/`.
