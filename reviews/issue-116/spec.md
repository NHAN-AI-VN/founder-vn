Commit mã đã chấm: e90205c1ce23

# Review trục Spec, #116 `founder-launch`, vòng 1

Phạm vi: `git diff --stat main...HEAD` (8 file: SKILL.md, launch.md, business-plan.md, README.md, 3 test, evidence) và `git log --oneline main..HEAD` (6 commit, từ `e9af14c` đến `e90205c`). Đã đọc `AGENTS.md`, SKILL.md, `launch.md`, `business-plan.md`, evidence, và đối chiếu từng số với `idea.md`, `pricing.md`, `cfo.md`, `ops.md`, `marketing.md`, `panel/results.md`.

**Phán quyết: PASS.** Không có finding chặn.

## Đối chiếu từng criterion

1. **SKILL.md** (`skills/founder-launch/SKILL.md`): đạt. `metadata.version: "0.2.0"` bằng `__version__` ở `src/founder_vn/__init__.py`; có khối Protocol chung; `uv run python scripts/skill_lint.py` chạy lại ở HEAD: 10 skill, 19 file ví dụ, 0 finding. Sáu mục đúng thứ tự: (1) Thử nghiệm thật trước, giá niêm yết không giảm, quy tắc dừng "nếu dưới N người mua thật trong M ngày", N và M là "anh/chị chọn", không tự đặt; (2) Đếm ngược D-30 đến D-0 với cột người làm và file phụ thuộc; (3) Run sheet từng giờ; (4) 30 ngày đầu với ba nguồn (mốc dừng `idea.md`, hòa vốn `cfo.md`, số đo `marketing.md` mục 6); (5) Người mua thật ghi đè panel, có câu cảnh báo panel; (6) lưu ý/miễn trừ.
2. **Không ngày, không số khách thật, chủ bước là vai trò trong `ops.md`**: đạt. Quy tắc nằm trong SKILL.md và `launch.md` tuân theo. Tìm ngày lịch hoặc năm trong `launch.md` và SKILL.md: không có. Ô kết quả "Kết quả thật: chưa có". Các vai trò dùng (quản lý, lễ tân, thợ, phụ tá, anh/chị) đều có trong `ops.md` mục 2. "Thợ trưởng" mà `idea.md` nhắc không dùng vì `ops.md` không có vai trò đó (evidence ghi rõ).
3. **Golden `launch.md`**: đạt. Đọc file thật. Tiếng Việt, "anh/chị", không `$`. Mọi số đều khớp nguồn: 199.000 đ, 50.000 đ cọc, hoàn nếu hủy trước 3 giờ, 265.000 đ, 9 lượt/ghế/ngày, 55%, 70%, mốc dừng sau 9 tháng (`idea.md`); 28 lượt/ngày hòa vốn, tháng 1 là 14 lượt/ngày theo `numbers.json` nên "thấp hơn mốc" đúng (`cfo.md`); 40%, 8 mua / 12 không mua trên 20 (`panel/results.md`). Cảnh báo panel xuất hiện ở mục 5, nơi trích kết quả panel. Miễn trừ ở cuối. Không có hạn pháp lý hay lệ phí, chỉ trỏ `permits.md`. Không tên người, không địa điểm dưới cấp quận. `business-plan.md` được tạo lại (commit `0957023` nêu lý do); mục `## Chưa làm` chỉ còn `founder-offer` và `founder-brand`, được khẳng định bằng test so khớp chính xác hai dòng.
4. **README**: đạt. Hàng `founder-launch` ghi #116 và `launch.md`; mục tiếng Việt cập nhật; `tests/test_front_door.py` sửa trong cùng lát.
5. **Cổng và evidence**: đạt. `docs/evidence/issue-116-founder-launch.md` có bảng lát đỏ rồi xanh, giới hạn (không chạy Kiro CLI, không dữ liệu khách thật, ngày tương đối), cổng ba đoạn. CI `Gate` ở HEAD: success (run 45769648606, theo tin nhắn giao việc). Tôi chạy lại ở HEAD `tests/test_launch_skill.py`, `tests/test_plan_example.py`, `tests/test_front_door.py`: 38 passed (nằm trong `pytest` của cổng `unit`).

Phạm vi: không có file ngoài cấp phát; `numbers.json`, `cfo.md`, `pricing.md`, `ops.md`, `marketing.md`, `permits.md`, `panel/` không bị đổi; `offer` và `brand` vẫn trong bản đồ section như quyết định đã chốt.

## Chưa xác minh / quan sát (không chặn, không gắn mã)

- Không chạy Kiro CLI, không chạy mô hình: golden do lane viết theo skill, như ticket cho phép. Chỉ chứng minh cấu trúc và nội dung cấm, không chứng minh danh sách chờ sẽ chuyển đổi.
- Khoảng cách các mốc D-n là đề xuất của lane (evidence đã ghi). Một số hàng giao việc cho vai trò chưa tuyển ở thời điểm đó (D-30 "lễ tân giữ sổ", D-21 "quản lý" trong khi D-12 mới tuyển). Ticket chỉ đòi vai trò có trong `ops.md`, nên không chặn; operator có thể cân nhắc ở vòng walkthrough.
- Nhận cọc từ D-30 trong khi hồ sơ hộ kinh doanh nộp ở D-28: khẳng định pháp lý về thu cọc trước khi đăng ký chưa được kiểm chứng ở đâu cả; tài liệu không nêu khẳng định pháp lý nên không vi phạm quy tắc link/ngày, nhưng đáng nêu với operator.

<promise>PASS</promise>
