Commit mã đã chấm: 476f0faa344c

# Review trục Standards, issue #115, vòng 1

**Phán quyết**: CHANGES_REQUESTED (một finding chặn, lane tự sửa được).

## Phạm vi đã xét

`git diff --stat main...HEAD`: 7 file (`README.md`, `docs/evidence/issue-115-founder-marketing.md`, `examples/barbershop/founder/business-plan.md`, `examples/barbershop/founder/marketing.md`, `skills/founder-marketing/SKILL.md`, `tests/test_front_door.py`, `tests/test_marketing_skill.py`). `git log --oneline main..HEAD`: 7 commit (`seam:` rồi 4 `slice(` rồi 2 `docs:`). Không có `src/` bị chạm, không có ADR bị chạm.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (mục Tests, Owner-facing output, Skills, Git), `docs/agents/evidence-gates.md`, `docs/founder-vn-design.md` (dòng 90-98), và checklist skill của lượt review.

Đã chạy ở checkout này: `uv run python scripts/skill_lint.py` (9 skill, 18 file ví dụ, 0 finding); `uv run pytest -q tests/test_marketing_skill.py tests/test_front_door.py tests/test_plan_example.py` (38 passed). Cổng CI `Gate` ở commit này: success (theo tin nhắn mở đầu).

## Hình dạng vòng lặp (mục 4)

- (a) `48be620 seam:` mang `## Seam` và đứng trước mọi commit `slice(`: đạt.
- (b) Không commit nào chạm `src/` (đây là skill, ví dụ và test); mỗi commit `slice(` đều kèm test (`tests/test_marketing_skill.py` hoặc `tests/test_front_door.py`), riêng commit `b059334` chỉ đổi golden `business-plan.md` và được test `test_business_plan_carries_the_marketing_section` cùng `test_plan_example.py` phủ; mỗi lát có dòng trong `## Lát`: đạt.
- (c) Test nằm ở seam đã khai (SKILL.md, `marketing.md`, `business-plan.md`, hàng README): đạt.
- (d) Khối `## Cổng ba đoạn` ghi `GREEN on fdd1089c04ca…`. Commit mã cuối là `f07fb31`; `fdd1089` không phải tổ tiên của nó (kiểm bằng `git merge-base --is-ancestor`), hai commit sau `fdd1089` chỉ đổi file bằng chứng: cổng không stale. Đạt.
- Golden `business-plan.md` đổi và commit message `b059334` nêu lý do (compiler nhúng `marketing.md`): đạt. Evidence nói rõ commit golden mang một test còn đỏ, và đây là lát cuối cùng trước khi xanh: đã khai, không phải finding.

## Finding chặn

### S1: Câu cảnh báo panel thiếu "cận trên"

- Chỗ: `skills/founder-marketing/SKILL.md:54` (câu cảnh báo skill bắt ghi), `examples/barbershop/founder/marketing.md:9` (golden ghi đúng câu đó), `tests/test_marketing_skill.py:176` (test khoá đúng chuỗi thiếu).
- Sai gì: skill và golden ghi "Panel là mô phỏng, không phải khách hàng thật". Cả ba skill khác có kết quả panel (`founder-consumer` dòng 68, `founder-pricing` dòng 61, `founder-plan` dòng 80) và các golden của chúng (`consumer.md:14`, `pricing.md:72`, `summary.md:43`, `business-plan.md:308`) ghi "Panel là mô phỏng, cận trên, không phải khách hàng thật". `marketing.md:9` trích kết quả panel ("12 trên 20 người mua mô phỏng nói không mua") ngay trước câu cảnh báo.
- Chuẩn vi phạm: checklist rà soát skill, mục "cảnh báo 'panel là mô phỏng, cận trên' nơi có kết quả panel"; `docs/agents/standards.md` mục Owner-facing output ("the simulated-panel caveat of the upstream skills is kept"); `docs/founder-vn-design.md:96` ("tín hiệu cầu (mô phỏng, cận trên)").
- Vì sao chặn: thiếu một mục của checklist skill là finding chặn. Lời cảnh báo yếu hơn bản các skill cùng bộ, và test hiện khoá đúng bản yếu nên một lần sửa mà không đổi test sẽ đỏ.
- Cách sửa (commit bổ sung, không viết lại lịch sử): đổi câu trong SKILL.md, `marketing.md` và test thành "Panel là mô phỏng, cận trên, không phải khách hàng thật; cần xác nhận với khách thật trước khi chi tiền."; chạy lại `bash scripts/harness/gate-segment.sh static|unit|build|verify` rồi cập nhật khối `## Cổng ba đoạn` ở SHA mới. `business-plan.md` nhúng `marketing.md`, nên chạy `founder-vn plan` trong `examples/barbershop` và nêu trong commit message vì sao golden đổi.

## Quan sát không chặn (không gắn mã)

- `skills/founder-marketing/SKILL.md:18` và `:20` lặp tiêu đề `## Protocol` hai lần liên tiếp; các skill khác (`founder-pricing`, `founder-ops`) chỉ có một. Nên xoá một dòng khi sửa S1; nội dung giao thức khớp bản của `founder-pricing`.

## Chưa xác minh

- `bash scripts/harness/gate-segment.sh verify` ở checkout này báo `no .harness/gate-segments.txt` (chưa chạy ba đoạn ở sandbox review), nên tôi dựa vào khối cổng trong file bằng chứng và kết quả CI `Gate` success, không tự tái tạo `GREEN on <sha>`.
- Các phản đối, câu trích P0xx và số liệu đối thủ trong `marketing.md` đã được test kiểm là nguyên văn từ `panel/results.md`; tôi chỉ đối chiếu chọn mẫu (giờ 19:45 của Tony Barber House, 12/20 không mua, mốc dừng trong `idea.md`), không đối chiếu từng hàng của 30 hàng chiến dịch. Đúng sai của nội dung so với ticket thuộc trục Spec.

<promise>CHANGES_REQUESTED</promise>
