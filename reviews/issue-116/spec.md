Commit mã đã chấm: 5cb4bdac045e

# Review trục Spec, vòng 1: #116 `founder-launch`

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git log --oneline main..HEAD` (9 commit của lane, kèm 2 commit review trước) và `git diff --stat main...HEAD`. Báo cáo này thay báo cáo cũ chấm `e90205c`. Từ đó nhánh có thêm `ae01d20` (sửa `launch.md`, `SKILL.md`, `business-plan.md`), `c92404a` và `5cb4bda`. Hai commit sau chỉ chạm file review và evidence. Đã đọc lại toàn bộ `SKILL.md` và `launch.md` ở commit này.

## Đối chiếu từng criterion

1. **`skills/founder-launch/SKILL.md`.** Đạt.
   - Frontmatter có `metadata.version: "0.2.0"`, bằng version gói ở `pyproject.toml`. `uv run python scripts/skill_lint.py` báo 0 finding trên 10 skill. Khối Protocol chung có đủ 5 mục.
   - Sáu mục đúng thứ tự: Thử nghiệm thật trước, Đếm ngược, Run sheet ngày khai trương, 30 ngày đầu, Người mua thật ghi đè panel, Lưu ý.
   - Mục 1 yêu cầu một thử nghiệm duy nhất ở giá niêm yết, không giảm giá. Quy tắc dừng "nếu dưới N người mua thật trong M ngày", N và M là "anh/chị chọn", cấm tự đặt hoặc suy từ panel.
   - Mục 2 là bảng D-30 đến D-0 với cột người làm và file phụ thuộc. Mục 3 là run sheet theo giờ, mỗi dòng một vai trò.
   - Mục 4 chỉ dùng ba nguồn: mốc dừng `idea.md`, hòa vốn `cfo.md`, số đo `marketing.md` mục 6. Mục 5 là một đoạn, kèm cảnh báo panel nguyên văn. Mục 6 là miễn trừ trách nhiệm.
   - Bằng chứng: `tests/test_launch_skill.py` (21 test, chạy trong `pytest` của cổng `unit`) và `skill_lint`.

2. **Không ngày, không số khách thật, chủ việc là vai trò trong `ops.md`.** Đạt.
   - Skill có ba quy tắc cứng tương ứng, thêm quy tắc "vai trò `ops.md` không liệt kê thì ghi phải tuyển trước".
   - `launch.md` không có ngày lịch (grep dd/mm/yyyy và yyyy-mm: rỗng). Ô "Kết quả thật: chưa có". Cột người làm chỉ có anh/chị, quản lý, lễ tân, thợ, phụ tá, đều có trong bảng nhân sự `ops.md`.
   - "Thợ trưởng" xuất hiện chỉ để nói rõ `ops.md` chưa có vai này, phải tuyển trước, và anh/chị quyết ở D-14. Đối chiếu `idea.md` mục ngân sách: "cần thuê một thợ trưởng", khớp.
   - Các con số trong `launch.md` đều truy được về file nguồn:
     - 199.000 đ, 50.000 đ, hoàn cọc khi hủy trước 3 giờ, 9 lượt/ghế/ngày, 55%, 70%, 265.000 đ: `idea.md`.
     - 28 lượt mỗi ngày: `cfo.md`. Tháng 1 là 14 lượt, nên câu "kế hoạch tháng 1 thấp hơn mốc hòa vốn" đúng.
     - 40%, 8 mua, 12 không mua trên 20 người: `panel/results.md`.
   - Không có `$` trong `launch.md`.

3. **Golden `launch.md` và `business-plan.md`.** Đạt.
   - `launch.md` bám đúng hình dạng skill: waitlist có cọc 50.000 đ ở giá 199.000 đ, N và M là "anh/chị chọn", bảng D-30 đến D-0 gồm 14 dòng, run sheet 08:30 đến 21:45, bảng 30 ngày đầu, đoạn ghi đè panel có cảnh báo, miễn trừ trách nhiệm ở cuối.
   - Cảnh báo "Panel là mô phỏng, cận trên…" nằm ở nơi trích 40%.
   - Quy tắc dừng đọc ở D-14 và `launch.md` nói rõ điều nó còn chặn được và điều không chặn được (đăng ký, nhà cung cấp trước D-14).
   - `uv run founder-vn plan --check` trong `examples/barbershop` báo khớp. `## Chưa làm` của `business-plan.md` đúng hai dòng: `founder-offer` và `founder-brand`. `tests/test_plan_example.py::test_business_plan_lists_only_offer_and_brand_as_not_done` khẳng định đúng danh sách này.
   - Evidence nêu giới hạn: không có Kiro CLI, lane tự chạy theo skill. Commit message của lát plan nêu lý do tái sinh.
   - Dữ liệu ẩn danh: không có tên người, địa điểm dưới cấp quận.

4. **README.** Đạt.
   - Hàng `founder-launch` có `#116`, "shipped (Wave B)" và link `launch.md`. Phần tiếng Việt cập nhật, nói `founder-offer` và `founder-brand` để sau pilot (Q12).
   - `tests/test_front_door.py` cập nhật cùng lát: chuyển `founder-launch` sang nhóm shipped, bỏ vòng "not started". `pytest` chạy 12 test của file này, đạt.

5. **Cổng xanh và evidence.** Đạt.
   - `uv run pytest -q` ở commit này: 451 passed. CI `Gate` run 45770057641 success.
   - `docs/evidence/issue-116-founder-launch.md` có bảng lát với cột "Assertion while red" và "Green rerun" (`FileNotFoundError` trước, pass sau), và mục "Giới hạn": không chạy Kiro CLI, không có dữ liệu khách thật, ngày tương đối.

Giới hạn và quyết định ticket đã chốt đều được giữ: ngày tương đối, giá thử nghiệm bằng giá niêm yết, cọc 50.000 đ phản chiếu `idea.md`, chủ việc là vai trò, `offer` và `brand` vẫn nằm trong "Chưa làm". Không thấy hành vi vượt phạm vi. `founder-offer`, `founder-brand`, dữ liệu khách thật và ngày lịch không bị đụng vào.

## Chưa xác minh

- Không chạy được Kiro CLI trong sandbox (ticket tự nêu). Việc một agent thật làm theo skill có ra một `launch.md` tương đương hay không chưa kiểm. Đó là walkthrough Wave B, phần của người, ngoài phạm vi ticket.
- Evidence ghi cổng ba đoạn chạy ở `ae01d20`. Tôi chạy lại `pytest` đầy đủ và `skill_lint` ở `5cb4bda` và kết quả khớp. Không chạy lại đoạn `build` và `verify`. CI `Gate` ở `5cb4bda` báo success.
- Khoảng cách giữa các dòng đếm ngược (D-28, D-24…) là đề xuất của lane và evidence nói rõ điều đó. Không file nào định sẵn, nên không có gì để đối chiếu.

<promise>PASS</promise>
