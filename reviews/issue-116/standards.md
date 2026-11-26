Commit mã đã chấm: 5cb4bdac045e

# Review trục Standards: #116 vòng 1 (lượt lại ở đầu nhánh 5cb4bda)

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

`git diff --stat origin/main...HEAD`: 10 file (`README.md`, `docs/evidence/issue-116-founder-launch.md`, `examples/barbershop/founder/business-plan.md`, `examples/barbershop/founder/launch.md`, `skills/founder-launch/SKILL.md`, `tests/test_front_door.py`, `tests/test_launch_skill.py`, `tests/test_plan_example.py`, cùng `reviews/issue-116/spec.md` và `standards.md`). Không file nào dưới `src/`.

`git log --oneline origin/main..HEAD`: `seam:` (e9af14c), 4 `slice(` (1ade3cc, 73d4b57, 0957023, 7bda96b), `docs:` e90205c, `fix(founder-launch)` ae01d20, 2 commit review, `docs:` 5cb4bda. Lượt trước chấm e90205c; lượt này chấm thêm ae01d20 và 5cb4bda.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`.

## Kết quả theo mục

- Ghi file, parity CLI/MCP, mạng, số mặc định, thuế, biến môi trường: diff không chạm `src/`, không thêm phép tính, không gọi mạng, không nhắc `FOUNDER_LLM_*`. Không áp dụng.
- File một-chủ: chỉ `README.md`, thuộc cấp `all` của WIP 1. Không chạm `pyproject.toml`, `uv.lock`, `src/founder_vn/__init__.py`.
- Skill: `scripts/skill_lint.py` báo 10 skill, 19 file ví dụ, 0 finding, phiên bản package 0.2.0 khớp `metadata.version`. Dòng `$` duy nhất trong `SKILL.md` (dòng 81) là câu quy tắc, không cạnh chữ số. `launch.md` tiếng Việt, xưng "anh/chị", tiền dạng `199.000 đ`. Không có khẳng định pháp lý hay hạn/lệ phí (trỏ sang `permits.md`). Có cảnh báo panel là mô phỏng, cận trên ở chỗ trích kết quả panel và miễn trừ ở cuối.
- ae01d20 (đã chấm thêm): sửa `SKILL.md`, `launch.md`, `business-plan.md` (3 dòng đổi), thêm 3 test. Message nêu rõ golden `launch.md` và `business-plan.md` đổi và vì sao (review 2026-11-26-070000), nên golden đổi có giải thích. "Thợ trưởng chưa có trong `ops.md`" khớp `idea.md` ("cần thuê một thợ trưởng"), không bịa số hay vai trò. Ví dụ vai trò trong `SKILL.md` giờ chỉ dùng vai trò có trong `ops.md`.
- Bằng chứng đỏ rồi xanh cho ae01d20: mục "Giải quyết review nội bộ" nêu hai test fail trước khi sửa văn bản và 21 passed sau. Test `test_skill_example_roles_are_not_an_invented_role` và `test_golden_states_what_the_test_gates_and_the_head_barber_hire` kiểm đúng chuỗi đã đổi, sẽ đỏ nếu revert.
- Hình dạng vòng lặp:
  - (a) `e9af14c seam:` với `## Seam` đứng trước cả bốn `slice(`.
  - (b) Không commit nào chạm `src/`; mỗi `slice(` kèm test và có dòng trong `## Lát`. ae01d20 cũng kèm test và có mục riêng trong bằng chứng.
  - (c) Test đo ở seam đã khai (cấu trúc `SKILL.md`, `launch.md`, `business-plan.md`, hàng README).
  - (d) Commit mã cuối là ae01d20 (e90205c, 43cf3b0, c92404a, 5cb4bda chỉ chạm file bằng chứng hoặc review). `## Cổng ba đoạn` giờ ghi "Run once at code commit `ae01d20`" và `verify` GREEN ở `ae01d20b0f048dba509ac71f7730e32d1d1db6b2`, trùng commit mã cuối. Cổng không còn stale; điều lượt trước cảnh báo đã được sửa bằng commit bổ sung 5cb4bda, không viết lại lịch sử.
- Chạy lại cục bộ: `uv run pytest tests/test_launch_skill.py tests/test_plan_example.py tests/test_front_door.py -q` 41 passed; `skill_lint` 0 finding. CI `Gate` run 45770057641 ở 5cb4bda: success.

## Ghi chú không chặn

- `73d4b57` để `test_plan_example` đỏ giữa hai commit; `## Lát` đã khai và commit kế tiếp đóng lại.
- File bằng chứng có hai tiêu đề `## Giải quyết review nội bộ` trùng tên (một cho tự rà, một cho review 2026-11-26-070000). Chỉ là thẩm mỹ, không chuẩn nào cấm.
- Mục 4 của review nội bộ ghi tỷ lệ 70% Việt trong bảng "mốc dừng" là chưa đổi vì cosmetic; hàng đó đã gắn nhãn mục tiêu.

## Chưa xác minh

- Khoản cọc "được hoàn toàn bộ nếu tiệm không mở" trong `launch.md` mục 1 so với `idea.md` (chỉ ghi hoàn cọc khi khách hủy trước 3 giờ): thuộc trục Spec, không phải chuẩn đã ghi của trục này.
- Chưa tự chạy lại cổng ba đoạn đầy đủ (451 test, `build`); tin CI `Gate` success và bản ghi `verify` GREEN ở ae01d20.

<promise>PASS</promise>
