Commit mã đã chấm: caa92fd1da54

# Review trục Standards, issue #112, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

`git log --oneline origin/main..HEAD`: 8 commit (`5c7111b` seam, 6 commit slice/evidence, `caa92fd` evidence). `git diff --stat origin/main...HEAD`: 10 file, +575/-13: `README.md`, `docs/evidence/issue-112-founder-permits.md`, `examples/barbershop/founder/business-plan.md`, `examples/barbershop/founder/permits.md`, `permits/sources.md`, `skills/founder-permits/SKILL.md`, bốn file test (`test_front_door.py`, `test_permits_example.py`, `test_permits_skill.py`, `test_sources_ledger.py`).

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (mục Shape of the code, Tests, Owner-facing output, Skills, Git), `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`.

Diff không chạm `src/`, nên các mục sau không áp dụng: khóa đường dẫn, parity CLI/MCP, số mặc định thay cho lỗi, client LLM.

## Kết quả theo mục của hướng dẫn

- Chạy lại ở HEAD: `skill_lint.py` 7 skill, 16 file ví dụ, 0 finding (phiên bản package 0.2.0); `ruff check` sạch; `ruff format --check` 226 file đúng định dạng; `pytest -q` 389 passed. Khớp với evidence và với CI Gate (run 45752338708, success).
- Test: bốn file test chỉ đọc file văn bản và sổ nguồn, không có import mạng, `httpx`, `requests` hay `urlopen`. Không có giá trị biến `FOUNDER_LLM_*` trong diff.
- Số liệu pháp lý: tỷ lệ và ngưỡng nằm trong `permits/sources.md` và được chép lại kèm link Công báo và ngày kiểm chứng, không phải hằng số trong mã. Mức lệ phí được ghi "chưa có nguồn đã kiểm chứng" thay vì số đoán.
- Checklist skill:
  - `$` cạnh chữ số: lint 0 finding.
  - Tiếng Việt và "anh/chị" trong `permits.md`: đạt. Phần tiếng Anh nằm trong chỉ dẫn của `SKILL.md`, đúng quy định ("Instructions in English").
  - Link chính thức và ngày kiểm chứng: mỗi con số trong `permits.md` có link Công báo và ngày.
  - Miễn trừ trách nhiệm: có ở phần 6 và là Rule cuối của skill.
  - Cảnh báo "panel là mô phỏng, cận trên": skill và ví dụ này không có kết quả panel, nên không áp dụng.
  - `metadata.version` "0.2.0" khớp phiên bản package; `name` khớp thư mục; có `license`, `author`, `source`, `commit`.
  - Phần Protocol dùng chung khớp `founder-cfo`.
- Golden file: `business-plan.md` đổi (+58/-1, thêm mục "Giấy phép và thuế"). Commit `8f4c0dc` nêu lý do (compiler đưa mục này vào từ `permits.md`) và evidence ghi số dòng đổi. `tests/test_plan_example.py` xanh.
- Số liệu thuế trong `permits.md` khớp `cfo.md`: tỷ lệ gộp 7%, mức tính thừa tối đa 20 triệu đồng, mốc 3 tỷ đồng và 17%.
- File một-chủ: `README.md` bị sửa. WIP là 1 nên allocation là `all`, không phải finding. `pyproject.toml`, `uv.lock` và `src/founder_vn/__init__.py` không đổi.

## Hình dạng vòng lặp (mục 4)

- (a) Commit `5c7111b` `seam:` mang mục `## Seam` và đứng trước mọi commit `slice(`. Đạt.
- (b) Không commit nào chạm `src/`. Mỗi commit `slice(` đều chạm test của lát đó, và mỗi lát có một dòng trong `## Lát`. Đạt.
- (c) Test nằm ở seam đã khai: văn bản `SKILL.md`, `permits/sources.md`, `permits.md` và hàng README. Đạt.
- (d) `## Cổng ba đoạn` ghi `GREEN on 8f4c0dca63a7e78b154365e2e8601ab9e7b77b27`. `git diff --stat 8f4c0dc HEAD` chỉ có file evidence, nên `8f4c0dc` là commit mã cuối và cổng không stale. Đạt.

## Chưa xác minh

- Tính đúng của nội dung pháp lý trong `permits/sources.md` và `permits.md`. Trục này chỉ kiểm hình thức (có nguồn, có link, có ngày). Nội dung dựa vào lần kiểm chứng của operator ngày 26/11/2026 trên bản PDF Công báo; tôi không đối chiếu lại với Công báo. Đây thuộc trục Spec và operator.
- Evidence tự khai chưa đối chiếu lại nội dung PDF hôm nay và Nghị định 253/2026, 296/2026 không trả về từ công cụ tìm kiếm. Golden đã ghi đúng điều đó bên cạnh từng con số, nên không phải finding chuẩn.

<promise>PASS</promise>
