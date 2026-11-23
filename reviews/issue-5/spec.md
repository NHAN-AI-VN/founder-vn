Commit mã đã chấm: 1df28538728a

# Review trục Spec, #5 golden case, vòng 2

Phán quyết: PASS. SPEC-1 của vòng 1 đã đóng; không có finding chặn mới.

## SPEC-1 (vòng 1) đã đóng

`examples/barbershop/founder/idea.md` không còn tên khu đô thị dưới cấp quận. Vị trí ghi "Quận 7 cũ, TP.HCM" (idea.md, Q51 trong `docs/founder-vn-design.md`, `docs/evidence/issue-5-golden-case.md`). `grep -rniE "Phú Mỹ|Mỹ Hưng"` ngoài `reviews/` chỉ còn khớp ở hằng `SUB_DISTRICT_NAMES` của test và dòng bằng chứng red. `test_example_is_anonymised` từ chối tên đó (commit 8b92b89).

## Đối chiếu criterion

- Criterion 1, `idea.md` ở gốc dự án mẫu: đã đáp ứng. Đã đọc file thật: tiêu đề cùng năm mục (là gì, cho ai, bán gì giá bao nhiêu bằng VND định dạng Việt, ở đâu và bằng cách nào, ngân sách và ràng buộc), tên gọi tạm, không tên người, không tên thương hiệu thật, không `$`, có miễn trừ trách nhiệm và nhãn "ước tính kế hoạch". Bằng chứng: `uv run pytest tests/test_golden_case.py -q` cho 6 passed ở HEAD; `tests/` nằm trong cổng `unit` (evidence: unit 225 passed ở be96eb7, Gate run 45130634472 success ở HEAD); `scripts/skill_lint.py`: 0 finding.
- Criterion 2, chủ case đồng ý công bố ẩn danh: chủ case là chủ dự án; Q51 trong design ghi đây là quyết định của chủ dự án, evidence ghi sự đồng ý ngày 2026-11-23. Chấp nhận như đã ghi nhận trong repo; xem mục chưa xác minh.
- Criterion 3, README: đã đáp ứng. README có mục "Golden case" trỏ `examples/barbershop/` và `idea.md`; test `test_readme_names_the_example_directory_as_the_golden_case` pass.
- Thay đổi design Q51 (đổi ngành, sửa Q21 và dòng tuần 1) nhất quán với ticket, không đổi acceptance criteria. Q51 nêu hệ quả (đường F&B của permits ở đợt B) và hoãn quyết, lane không tự quyết.
- Không có nội dung thừa ngoài phạm vi: số liệu giá đối thủ và thuế suất, luật lao động đã bỏ khỏi idea.md (vòng 1 S2), để skill tra có nguồn.

## Chưa xác minh

- Sự đồng ý của chủ dự án trên issue #5: sandbox không có quyền đọc tracker; repo chỉ có câu ghi lại trong evidence và Q51.
- Việc chủ dự án chấp nhận công bố các số tài chính kế hoạch (vốn 1,5 tỷ đồng, lương, chi phí cố định) chưa có xác nhận riêng; evidence nói chủ chấp nhận khi chọn case.
- Ghi chú README về cấp phát file một-chủ không đọc được từ sandbox.
- Chất lượng tiếng Việt và độ đúng của các con số: test chỉ kiểm hình dạng, nhãn "ước tính" đã có trong file.

<promise>PASS</promise>
