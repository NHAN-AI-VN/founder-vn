Commit mã đã chấm: 54a3f8129a87

# Review trục Spec, vòng 2: #115 founder-marketing (vòng 2, sau câu trả lời của operator)

Phán quyết: PASS. Câu hỏi BLOCKED của lượt trước (kênh người sáng tạo địa phương) đã được operator trả lời (b) trong `reviews/issue-115/operator-answer.md`, và lane áp dụng đúng phương án đó. Không còn finding chặn.

## Điều đã kiểm ở `54a3f8129a87`

- Luật mới trong `skills/founder-marketing/SKILL.md` mục 2: kênh trong danh sách mà không file nào của chủ hộ cho thấy khách dùng thì ghi "không áp dụng (chưa có nguồn)", nêu điều mở lại, không hàng chiến dịch, không phần ngân sách, không số đo; bằng chứng của kênh khác không là nguồn. Luật này giữ danh sách kênh cố định như ticket (criterion 2 đối chiếu) và thực thi "không thêm kênh khách chưa được chứng tỏ dùng" mà không cần sửa ticket hay thiết kế.
- Golden `examples/barbershop/founder/marketing.md`: hàng "Người sáng tạo địa phương" ghi "Không áp dụng (chưa có nguồn)" với lý do, nguồn và điều kiện mở lại; ShopeeFood/GrabFood vẫn "Không áp dụng". Chiến dịch có đúng 30 hàng, Ngày 1 đến Ngày 30 liên tục (đếm bằng grep), không hàng nào dùng kênh không áp dụng; Ngày 22 (Google Maps) và Ngày 25 (Zalo OA) mỗi hàng có một việc và một phản đối có nguồn (P015, P012), không tặng dịch vụ hay giảm giá mới.
- Ngân sách: 3 + 3 + 3 + 1 + 0 + 0 = 10 phần; phần trăm chỉ trích từ `idea.md`/`numbers.json` ("marketing 4%"); không có số đồng, doanh thu hay chi phí mỗi khách. Số đo không còn hàng cho kênh không áp dụng.
- Không `$` trong file; cảnh báo panel "Panel là mô phỏng, cận trên, không phải khách hàng thật; cần xác nhận với khách thật trước khi chi tiền" đúng một lần; hai lưu ý cuối có mặt, lưu ý quảng cáo chung chung, không dẫn điều luật.
- `business-plan.md` có mục `## Tiếp thị` mang nội dung mới (hàng không áp dụng và phần 0 xuất hiện ở dòng 486 và 550); commit f6c0f9e nêu lý do tái sinh; `tests/test_plan_example.py` kiểm kết quả trùng đầu ra compiler.
- Test cho luật mới: `test_a_channel_with_no_source_in_the_owners_files_is_not_applicable` (skill), `test_golden_local_creators_not_applicable_without_a_source_and_unused_downstream`, `test_golden_budget_shares_sum_to_ten_and_not_applicable_channels_get_zero`. Bằng chứng ghi đỏ (assert cụ thể) rồi xanh ở b93a806 và f6c0f9e trong `docs/evidence/issue-115-founder-marketing.md`.
- Chạy lại ở HEAD: `uv run python scripts/skill_lint.py` 0 finding (9 skill, 18 file ví dụ); `pytest` ba file marketing, front door, plan example: 41 passed; toàn bộ `pytest`: 429 passed. CI `Gate` run 45768450645: success.
- Criterion 1, 3, 4 và 5 (SKILL.md, golden, README và `test_front_door.py`, evidence kèm mục Giới hạn nêu không Kiro CLI, chiến dịch tương đối, không số chi tiêu và kênh người sáng tạo) vẫn đạt; các commit sau vòng trước chỉ chạm SKILL.md, golden, business-plan, test và evidence. `numbers.json`, `panel/`, `standards.md`, `ledger.md`, `operator-answer.md` không bị lane sửa trong các commit này ngoài thêm file trả lời của operator.

## Chưa xác minh (không chặn, không gắn mã)

- Hook 1 và hook 2 cùng trả lời phản đối A (P019); hook 2 có thêm P020. Mức độ: possible, và SKILL.md yêu cầu mỗi hook trả lời phản đối hoặc mệnh đề khác nhau.
- Hook 8 ("Tiệm có chỗ để xe máy") gắn P018, vốn nói về tiệm cũ; file đã ghi điều kiện chỉ đăng khi mặt bằng có chỗ để xe. Operator cũng xác nhận hai mục này không chặn.
- Việc "gửi tin mời giới thiệu" ở Ngày 25 dựa trên phản đối "thợ quen giới thiệu" (P015); đây là cách đọc của lane, không phải lời khách. Không có lời khách mới nào được viết.

<promise>PASS</promise>
