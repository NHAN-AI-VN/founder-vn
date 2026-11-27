Commit mã đã chấm: bc8241e847e6

# Review trục Spec, #148, vòng 1

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git diff --stat origin/main...HEAD` (32 file, 7 commit từ `717ec84` tới `bc8241e`). Gate run 45971487663 xanh ở đúng commit này. Tôi cũng chạy lại tại chỗ.

## Đối chiếu từng criterion

1. Khối `## Protocol` giống hệt từng byte ở `docs/skill-conventions.md` và mười skill. Khối của mười skill có cùng một hash (sha256 `4b7cc62522f5`, mười file). Khối chuẩn nằm trong code fence nên không băm cùng. Việc so với bản chuẩn do các test lockstep của từng skill làm, và toàn bộ `pytest` pass (502 passed). Bước 1 mang nguyên văn mẫu `Dừng ở bước 1 của Protocol: gói founder-vn <phiên bản gói> và skill <tên skill> <phiên bản skill> lệch số major; anh/chị cập nhật gói hoặc skill rồi chạy lại.` và nói điểm dừng bằng tiếng Việt. Bước 2 nói điểm dừng của nó bằng tiếng Việt. Câu điều kiện của bước 1 và năm luật còn nguyên. Đạt. Bằng chứng: diff `docs/skill-conventions.md`, `skills/*/SKILL.md`, `pytest`.
2. `tests/test_front_door.py` ghim mẫu trong khối chuẩn (`test_shared_protocol_block_quotes_the_vietnamese_stop_template`), kèm câu điều kiện, "Vietnamese" ở bước 1 và bước 2. Đạt. Test chạy trong `pytest` của cổng `unit`.
3. `scripts/skill_lint.py` có luật mới `rule_has_protocol_stop`. Khối thiếu mẫu cho đúng một finding nêu file và dòng của heading `## Protocol`. Mười skill cho 0 finding (tôi chạy: `10 skills checked, 19 example file(s), 0 finding(s)`). `tests/test_skill_lint.py` phủ cả hai (finding đúng một dòng, đúng số dòng; mười skill thật). File evidence ghi lượt đỏ (0 finding, exit 0 trên bản sao thiếu dòng, trước luật) trước lượt xanh (1 finding, exit 1; 0 finding trên mười skill thật). Có thêm fixture witness và đột biến `--witness-red` cho cổng harness. Đạt.
4. `docs/hosts/kiro.md` bước 9 nêu tiền tố `Dừng ở bước 1 của Protocol` và vẫn trích câu điều kiện bước 1. `tests/test_hosts.py::test_kiro_step_9_expects_the_vietnamese_stop_and_keeps_the_step_1_condition` ghim cả hai. Đạt.
5. Thiết kế §4 có hàng mới. Q60 là mục tiếp theo sau Q59 trong nhật ký, dải đề mục đổi thành Q1–Q60, đúng dạng Q54 và có lý do. Mục skill của `docs/agents/standards.md` nêu điểm dừng tiếng Việt. `test_design_and_standards_record_q60` ghim các điểm này. Đạt.
6. Không có `$` cạnh chữ số ở dòng thêm trong diff (`grep` trên dòng `+`), và lint cho 0 finding. `metadata.version` của mười skill không đổi (diff skills không chứa dòng version). `src/` và `pyproject.toml` không có trong diff, nên đầu ra công cụ không đổi. `uv build` ở đoạn `build` của cổng xanh theo evidence, và Gate run xanh. Đạt.
7. Gate xanh ở commit mã cuối (`static`, `unit`, `build`, `verify`). Evidence `docs/evidence/issue-148-protocol-stop-vietnamese.md` có các hàng đỏ-rồi-xanh theo từng lát và mục commissioning của lint. Đạt.

Ngoài phạm vi, giữ đúng: không dịch khối sang tiếng Việt (chỉ dòng mẫu là tiếng Việt), không đụng `founder-vn install` hay README, không có quan sát bằng mô hình thật (evidence ghi rõ giới hạn này), không đụng #142, #143, #144.

## Chưa xác minh (không gắn mã, không chặn)

- Lane sửa thêm các file ngoài danh sách seam của ticket: `scripts/harness/witness.sh`, chín fixture `scripts/harness/fixtures/skill-lint/*`, `AGENTS.md`, `tests/test_install.py`. Evidence nêu lý do (witness chạy trên CI khi lint đổi; dải Q1–Q60 theo tiền lệ #144). Tôi không có comment `<!-- harness:allocation -->` nên không đối chiếu được với cấp phát của lane. Nếu `scripts/harness/` là file một-chủ ngoài cấp phát thì operator cần xem. Gate xanh, nên không có dấu hiệu hỏng.
- Điểm dừng mới chưa được quan sát với mô hình host thật. Ticket đã loại việc này khỏi phạm vi (#149 hoặc walkthrough kế tiếp).
- Luật lint chỉ kiểm chuỗi con trong mục `## Protocol`. Nó không kiểm câu quanh mẫu, vị trí khối, hay điểm dừng bước 2. Evidence đã nêu điểm mù này, và test lockstep của từng skill bù lại.

<promise>PASS</promise>
