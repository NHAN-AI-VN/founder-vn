Commit mã đã chấm: e90205c1ce23

# Review trục Standards: #116 vòng 1

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD`: 8 file (`README.md`, `docs/evidence/issue-116-founder-launch.md`, `examples/barbershop/founder/business-plan.md`, `examples/barbershop/founder/launch.md`, `skills/founder-launch/SKILL.md`, `tests/test_front_door.py`, `tests/test_launch_skill.py`, `tests/test_plan_example.py`). 6 commit: `seam:`, 4 `slice(`, 1 `docs:`. Không file nào dưới `src/`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape of the code, Tests, Owner-facing output, Skills, Git), `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`.

## Kết quả theo mục

- Ghi file, parity CLI/MCP, mạng, số mặc định, thuế, biến môi trường: diff không chạm `src/`, không thêm phép tính, không gọi mạng, không nhắc `FOUNDER_LLM_*`. Không áp dụng.
- File một-chủ: chỉ `README.md` thuộc danh sách, và WIP là 1 nên cấp `all`. Không chạm `pyproject.toml`, `uv.lock`, `src/founder_vn/__init__.py`.
- Skill (`skills/founder-launch/SKILL.md`): `name` khớp thư mục, `metadata.version` `0.2.0` khớp package 0.2.0, có `license`, `author`, `source`, `commit`, mô tả có cụm kích hoạt tiếng Việt, có khối Protocol 5 bước. `scripts/skill_lint.py`: 10 skill, 19 file ví dụ, 0 finding.
- Đầu ra cho chủ hộ (`launch.md`): tiếng Việt, xưng "anh/chị", tiền dạng `199.000 đ`, không có `$`. Mọi con số (199.000 đ, 50.000 đ, 265.000 đ, 9 lượt/ghế/ngày, 55%, 70%, 28 lượt, 40%, 8 mua/12 không mua) khớp với `idea.md`, `cfo.md`, `panel/results.md`. Không có khẳng định pháp lý hay hạn/lệ phí: tài liệu trỏ sang `permits.md`, nên không cần link chính thức mới. Có cảnh báo "Panel là mô phỏng, cận trên" ở chỗ trích kết quả panel (mục 5) và miễn trừ ở mục 6. Không có ngày lịch, tên người hay số liệu khách thật.
- Golden: `business-plan.md` đổi `+77 -1`, commit `0957023` giải thích; kết quả là output của compiler (`test_business_plan_is_the_compiler_output_and_check_passes` xanh). `launch.md` là file mới, commit ghi rõ.
- Hình dạng vòng lặp:
  - (a) `e9af14c seam:` với `## Seam` đứng trước cả bốn commit `slice(`.
  - (b) Không commit nào chạm `src/`. Mỗi `slice(` đều kèm test (`test_launch_skill.py`, `test_plan_example.py`, `test_front_door.py`) và có dòng trong `## Lát`.
  - (c) Test đo ở seam đã khai (cấu trúc `SKILL.md`, `launch.md`, `business-plan.md`, hàng README), không đo internals.
  - (d) `## Cổng ba đoạn` ghi `verify` GREEN ở `7bda96be1a87`, là commit mã cuối. Commit sau nó (`e90205c`) chỉ sửa file bằng chứng nên cổng không stale.
- Chạy lại cục bộ: `pytest tests/test_launch_skill.py tests/test_plan_example.py tests/test_front_door.py` 38 passed; `skill_lint` 0 finding. CI `Gate` ở `e90205c1ce23`: success.

## Ghi chú không chặn

- `73d4b57` để `test_plan_example` đỏ giữa hai commit (plan chưa tái sinh). `## Lát` của file bằng chứng đã khai điều này, và commit kế tiếp đóng lại. Không phải finding.

## Chưa xác minh

- `launch.md` mục 1 viết khoản cọc "được hoàn toàn bộ nếu tiệm không mở", đặt trong câu dẫn `idea.md`. `idea.md` chỉ ghi hoàn cọc khi khách hủy trước 3 giờ; điều "hoàn nếu tiệm đóng" của `idea.md` nói về gói 12 lần. Quy tắc này do `SKILL.md` yêu cầu, nên thuộc trục Spec (ticket có đòi không), không phải chuẩn đã ghi của trục này.
- `SKILL.md` liệt kê "thợ trưởng" trong ví dụ vai trò, còn `ops.md` của barbershop không có vai trò đó. Golden không dùng vai trò này và file bằng chứng đã nêu. Không có chuẩn nào bị vi phạm.
- Chưa chạy lại cổng ba đoạn đầy đủ (`unit` toàn bộ 448 test, `build`) ở đây; tin vào CI `Gate` success và bản ghi `verify` GREEN.

## Ghi chú về đầu nhánh đã dịch chuyển

Khi tôi push, `origin/lane/issue-116` đã có thêm `ae01d20 fix(founder-launch)` (sửa `SKILL.md`, `launch.md`, `business-plan.md`, thêm 3 test) và `43cf3b0 review(spec)`. Phán quyết trên chỉ áp dụng cho `e90205c1ce23`, commit harness giao. Tôi không chấm `ae01d20`. Cần biết cho vòng sau: `## Cổng ba đoạn` của file bằng chứng vẫn ghi `verify` GREEN ở `7bda96be1a87`, là tổ tiên của commit mã mới `ae01d20`, nên theo mục 4(d) cổng đã stale ở đầu nhánh hiện tại cho tới khi chạy lại cổng và ghi SHA mới. Điều này có thể là finding chặn ở vòng sau.

<promise>PASS</promise>
