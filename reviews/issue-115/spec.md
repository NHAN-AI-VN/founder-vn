Commit mã đã chấm: 476f0faa344c

# Review trục Spec, issue #115 (`founder-marketing`), vòng 1

Phạm vi: `git diff main...HEAD` (7 file: SKILL.md, marketing.md, business-plan.md, README.md, test_front_door.py, test_marketing_skill.py, evidence). Chạy lại ở commit này: `uv run pytest tests/test_marketing_skill.py tests/test_front_door.py tests/test_plan_example.py -q` → 38 passed; `uv run python scripts/skill_lint.py` → 9 skills, 0 finding. Gate CI: success.

Phán quyết: CHANGES_REQUESTED. Ba finding chặn, đều sửa được trong phần cấp phát của lane.

## Finding chặn

### SPEC-1: Cảnh báo panel thiếu "cận trên" (criterion 3, và mục 7 của SKILL)
Ticket đòi "panel caveat where panel numbers appear", và checklist review đòi cảnh báo "mô phỏng, cận trên" nơi có kết quả panel. Mọi artefact khác của bộ golden dùng cụm đó (`consumer.md:14`, `panel/results.md:5`, `pricing.md:72`, `summary.md`, `business-plan.md`). `marketing.md` dòng 9 nêu "12 trên 20 người mua mô phỏng nói không mua" cùng câu "Panel là mô phỏng, không phải khách hàng thật; cần xác nhận với khách thật trước khi chi tiền" mà không có "cận trên". `SKILL.md` mục 1 quy định đúng câu thiếu đó, nên lỗi nằm ở skill và lặp lại ở golden. Chặn vì skill dạy agent viết cảnh báo yếu hơn chuẩn của design (`docs/founder-vn-design.md` dòng 96, nhãn "mô phỏng, cận trên"). Sửa: đổi câu cảnh báo trong SKILL.md, golden, test (`tests/test_marketing_skill.py`), rồi sinh lại `business-plan.md`.

### SPEC-2: Khối Protocol bị lặp trong SKILL.md (criterion 1, "the common Protocol block")
`skills/founder-marketing/SKILL.md` có hai dòng `## Protocol` liên tiếp (đếm: 2; mọi skill khác có 1). Khối chung không còn đúng dạng chung và lint không bắt được. Sửa: bỏ một dòng; thêm kiểm tra vào test hoặc lint nếu muốn khóa.

### SPEC-3: Ngày 22 thêm một ưu đãi chưa được quyết (criterion 2, mục "Decisions", hook)
Hàng Ngày 22 mời người sáng tạo "đến cắt thử một lần" với nhãn "flip: cho cắt thử một lần hợp ý". Ý panel là khách mua cắt thử để hết ngại thợ lạ, không phải tặng dịch vụ cho người sáng tạo; `idea.md` không có cắt thử miễn phí. Chính `marketing.md` mục 1 và 4 nói không dùng điều chưa quyết làm thông điệp, và SKILL.md cấm "invent no offer". Ngày 25 và dòng ngân sách (1/10 cho người sáng tạo) dựa trên hàng này. Sửa: bỏ hoặc viết lại hàng Ngày 22 thành việc `idea.md` đã quyết (ví dụ mời người sáng tạo đặt lịch như khách thường, trả giá niêm yết), hoặc đưa câu hỏi cho Owner.

## Đã đối chiếu và đạt

- SKILL.md tồn tại, frontmatter qua lint, `metadata.version` 0.2.0 bằng phiên bản gói (lint báo package version 0.2.0); bảy mục đúng thứ tự; luật truy nguyên, không bịa lời khách, không hứa reach, kênh đóng, không Instagram/Yelp có trong văn bản. Bằng: đọc file, `test_marketing_skill.py` (11 test skill) chạy trong cổng `unit`.
- Golden `marketing.md`: đọc toàn văn. Bảy mục; 30 hàng "Ngày 1..30" tương đối, không ngày lịch; ShopeeFood/GrabFood "Không áp dụng" với lý do từ `idea.md`; tám hook đều có mã phản đối và nguồn; trích dẫn P001, P002, P007, P012, P015, P018, P019, P020 khớp nguyên văn `panel/results.md` và `consumer.md`; không `$`; tiếng Việt, anh/chị, VND định dạng Việt; ngân sách trích "marketing 4%" từ `idea.md` và `numbers.json`, chia 10 phần, không tính số đồng; lưu ý quảng cáo chung, không điều luật, trỏ `founder-permits`; miễn trừ trách nhiệm có. `numbers.json` không đổi (diff không chạm).
- `business-plan.md` sinh lại có mục `Tiếp thị`; commit `b059334` nêu lý do; `test_plan_example.py` xanh.
- README: hàng `founder-marketing` có #115 và `marketing.md`, mục tiếng Việt cập nhật; `test_front_door.py` cập nhật cùng lát, 12 test xanh.
- Evidence `docs/evidence/issue-115-founder-marketing.md`: có bảng lát red-then-green, mục Giới hạn (không Kiro CLI, chiến dịch tương đối, không số chi), và khối ba đoạn cổng ở commit `fdd1089`; các commit sau chỉ chạm file evidence.

## Chưa xác minh

- Không chạy lại `gate-segment.sh` ba đoạn; dựa vào kết quả CI `Gate` success ở 476f0faa344c do tin nhắn giao việc cung cấp.
- Nguồn "5 trong 8 đối thủ có điểm sao" suy từ `competitors.md` mục 1 (đối thủ 4–8 có số); chưa mở bảng để đếm lại từng dòng.
- Kênh "Người sáng tạo địa phương" không có nguồn nào cho thấy khách dùng kênh này (golden tự nói vậy). Ticket tự liệt kê kênh này nên không tính là lỗi; lane nên để operator xác nhận có giữ 1/10 ngân sách cho kênh chưa có nguồn hay không, vì tiêu chí "never adds a channel the Owner's customers were not shown to use" xung đột với danh sách của chính ticket.

<promise>CHANGES_REQUESTED</promise>
