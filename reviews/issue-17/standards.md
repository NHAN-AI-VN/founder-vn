Commit mã đã chấm: 1b8ce2d0e526

# Review trục Standards, issue #17, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

Diff `main...HEAD` (4 commit: `afc1e6c` seam, `77d914a` slice, `06cd1ac` slice, `1b8ce2d` docs): `skills/founder-pricing/SKILL.md`, `tests/test_pricing_skill.py`, `examples/barbershop/founder/pricing.md`, `examples/barbershop/founder/pricing_input.json`, `docs/evidence/issue-17-founder-pricing.md`.

Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`.

## Kết quả theo mục

- Không đụng `src/`: không có ghi file ngoài lớp khoá đường dẫn, không có phép tính chỉ ở một transport, không có hằng số thuế hay ngưỡng. Skill gọi `pricing_psm` / `founder-vn pricing` và `cfo_model` / `founder-vn cfo --price`, đã có sẵn từ issue #8 và CFO.
- Test không gọi mạng và không in biến `FOUNDER_LLM_*`.
- Checklist skill:
  - `scripts/skill_lint.py` chạy lại: 5 skill, 13 file ví dụ, 0 finding.
  - Frontmatter khớp `founder-cfo` và `founder-competitors`: `name` bằng tên thư mục, `license`, `metadata.version` 0.1.0 bằng phiên bản package, `author`/`source`/`commit`.
  - Khối `## Protocol` giống nguyên văn hai skill kia.
  - `pricing.md` bằng tiếng Việt, xưng "anh/chị", tiền theo dạng VND, không có `$`.
  - Giá đối thủ lấy từ `competitors.md` (có link nguồn và ngày khảo sát 23/11/2026). Không có khẳng định pháp lý hay thuế mới.
  - Có miễn trừ trách nhiệm. Cảnh báo "Panel là mô phỏng, cận trên" xuất hiện đúng một lần.
- Hình dạng vòng lặp:
  - (a) Commit `seam:` có mục `## Seam` và đứng trước hai commit `slice(`.
  - (b) Không commit nào chạm `src/`; mỗi commit slice đều chạm `tests/test_pricing_skill.py` và có một dòng trong `## Lát`. Số test khớp: 8 ở `77d914a`, 13 ở `06cd1ac`.
  - (c) Test nằm ở seam đã khai (file skill và file golden), không ở internals.
  - (d) `## Cổng ba đoạn` ghi `gate-segment verify` GREEN trên `06cd1ac0cb7e`, đúng là commit mã cuối. `1b8ce2d` chỉ đổi `docs/evidence/`.
- Golden file: cả hai file mới, không có file đổi. Đã chạy lại `uv run pytest tests/test_pricing_skill.py -q` (13 passed) và `uv run ruff check .` (sạch). CI `Gate` ở `1b8ce2d0e526` success theo tin nhắn giao việc.
- Con số trong `pricing.md` (28 lượt hòa vốn, giá bán 280.000 đ) khớp `cfo.md`.

## Chưa xác minh

- Chưa chạy lại `founder-vn pricing` và `founder-vn cfo --price` để so từng con số với đầu ra công cụ (test của lane có kiểm 5 test `test_golden_*`; CI xanh).
- Việc có đủ yêu cầu của ticket hay không thuộc trục Spec, không xét ở đây.
- Evidence ghi rõ không có Kiro CLI trong sandbox lane nên chưa chứng minh một phiên host tuân theo skill; việc này thuộc T18 (#19).

<promise>PASS</promise>
