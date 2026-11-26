# Review closure ledger — #115 founder-marketing (vòng 1)

S1 FIXED — câu cảnh báo panel thiếu "cận trên" trong SKILL.md, golden `marketing.md` và test; đổi thành "Panel là mô phỏng, cận trên, không phải khách hàng thật", `business-plan.md` sinh lại; commit "fix: #115 close S1 and SPEC-1"; `uv run pytest tests/test_marketing_skill.py tests/test_plan_example.py` 26 passed.
SPEC-1 FIXED — cùng nguyên nhân và cùng commit với S1 (một sửa đóng cả hai mã).
SPEC-2 FIXED — bỏ dòng `## Protocol` thừa trong SKILL.md; test khoá `count("## Protocol") == 1` (đỏ `assert 2 == 1` khi còn dòng thừa, xanh sau sửa); commit "fix: #115 close SPEC-2".
SPEC-3 FIXED — ngày 22, ngày 25, lý do kênh người sáng tạo và số đo của kênh này không còn mời cắt thử miễn phí (idea.md không quyết); ngày 22 là đặt lịch như khách thường, giá niêm yết; `business-plan.md` sinh lại; commit "fix: #115 close SPEC-3"; 26 passed.
