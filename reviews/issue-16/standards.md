Commit mã đã chấm: 56bbb3fa9b36

# Review trục Standards, issue #16, vòng 1

Verdict: CHANGES_REQUESTED

## Phạm vi đã xét

`git diff --stat main...HEAD` (32 file, không có `src/`) và `git log --oneline main..HEAD` (5 commit: `122dbee` seam, `6dda313` slice, `4c7ba40` slice, `867bc35` docs, `56bbb3f` docs). Đối chiếu với `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/review-checklist.md`, `.kiro/skills/code-review/SKILL.md`. Đã chạy `scripts/skill_lint.py`: 0 finding (4 skill, 12 file ví dụ, version 0.1.0).

Đạt:
- Hình dạng vòng lặp: (a) `seam:` (`122dbee`, có `## Seam`) đứng trước hai commit `slice(`; (b) không commit nào chạm `src/`, mỗi commit slice chạm cả test lẫn skill/ví dụ và có dòng trong `## Lát`; (c) test đọc skill và file ví dụ ở seam đã khai, `founder_vn.panel.validate_customer` là biên công khai; (d) khối `## Cổng ba đoạn` ghi `verify` GREEN ở `867bc35`, là con cháu của commit mã cuối `4c7ba40`, và `56bbb3f` chỉ chạm `docs/evidence/`, nên cổng không stale.
- `metadata.version` "0.1.0" khớp package; mục Protocol giống `founder-board`; không `$` cạnh chữ số; không lộ giá trị `FOUNDER_LLM_*` (`panel.json` chỉ ghi tên mô hình và `prompt_hash`, test khẳng định không có `api_key`/`base_url`); không gọi mạng trong test; không số hay tỷ lệ thuế hardcode; không khẳng định pháp lý/số liệu cần link; có miễn trừ trách nhiệm và cảnh báo "mô phỏng, cận trên" đúng một lần trong `consumer.md`.
- Không ghi file ngoài lớp khoá đường dẫn (không đổi mã).

## Finding chặn

### S1: `examples/barbershop/founder/consumer.md` không xưng "anh/chị" với chủ hộ
- Chỗ: `examples/barbershop/founder/consumer.md`, toàn file (16 dòng). `grep -c "anh/chị"` cho 0. Test `test_golden_readback_has_five_points_and_the_caveat_once` (`tests/test_consumer_skill.py`, cuối file) không kiểm cách xưng.
- Sai gì: đây là văn bản đọc lại cho chủ hộ nhưng viết trung tính, không xưng hô. Skill dặn "addresses the Owner as anh/chị" (Purpose của `skills/founder-consumer/SKILL.md`) và bằng chứng ghi mục này "Passed" (`docs/evidence/issue-16-founder-consumer.md`, mục Giới hạn), nên khẳng định đó chưa đúng cho file này.
- Chuẩn: `docs/agents/standards.md`, mục "Owner-facing output" ("address the Owner as "anh/chị""); `docs/review-checklist.md` dòng 7-8; vòng "Review skill" của prompt này ("xưng anh/chị", thiếu một mục là finding chặn).
- Vì sao chặn: là mục trong checklist rà soát skill/example; thiếu thì chặn theo chuẩn đã ghi.
- Cách sửa (commit bổ sung, không viết lại lịch sử): đổi `consumer.md` để xưng "anh/chị" (ví dụ ở câu mở đầu, mục 4 và 5, và câu khuyến nghị); thêm một assert vào test golden read-back (tại seam đã khai) rằng `"anh/chị" in text`, chạy đỏ trước khi sửa rồi xanh; cập nhật dòng bằng chứng, chạy lại ba đoạn cổng và `verify` ở SHA mã cuối mới. Không cần file một-chủ nào ngoài cấp phát.

## Chưa xác minh

- Skill chạy thật trên Kiro CLI không kiểm chứng được (bằng chứng đã tự khai). Golden case do agent đi theo skill từng bước, không phải một phiên host độc lập.
- Số 199.000 đ, 1.990.000 đ, 50.000 đ trong `pitch.md` đến từ `idea.md` của ví dụ; tôi chưa đối chiếu từng số với `idea.md`.
- Không chạy lại toàn bộ `uv run pytest`; dựa vào CI `Gate` success ở `56bbb3fa9b36`.

<promise>CHANGES_REQUESTED</promise>
