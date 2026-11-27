Commit mã đã chấm: dc9a416defca

# Review trục Standards, issue #142, vòng 1

**Phán quyết: PASS.** Không có finding chặn.

## Phạm vi đã xét

Diff `git diff --stat main...HEAD` (24 file, 6 commit: `a942c0b` seam, `71cc64b` slice install, `002f51d` slice skills, `be7fa0f` docs front-door, `823a057` docs design, `dc9a416` evidence). Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Toolchain, Shape of the code, Tests, Owner-facing output, Skills, Git), `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` §5 và Q57, `.kiro/skills/code-review/SKILL.md`. `docs/adr/` không tồn tại. Đã chạy lại ở checkout này: `ruff check` sạch, `ruff format --check` sạch, `scripts/skill_lint.py` 0 finding, `pytest -q` 481 passed (khớp với CI `Gate` success).

## Kiểm theo mục của hướng dẫn

- Khoá đường dẫn: `install._write_ledger` chỉ ghi `permits/sources.md`, đích cố định của gói. `install.run` gọi `_check_inside` trước mọi thao tác ghi (`src/founder_vn/install.py:108`), nên đích thoát dự án bị `InstallRefused` (exit 2) trước khi ghi gì. Khớp bullet bộ cài trong `docs/agents/standards.md` (Q57, #142). Không xoá file, `--print-only` không ghi.
- Parity: bộ cài là CLI-only theo standards (quyết định của operator, lane #7), nên không cần test parity.
- Mạng và credential: test không gọi mạng, không đụng `FOUNDER_LLM_*`.
- Hằng số: không có tỷ lệ thuế hay ngưỡng nào được thêm; các câu thêm vào skill cấm điền số từ trí nhớ.
- Golden: 5 file `tests/golden/install_*.json` đổi, thông điệp commit `71cc64b` giải thích ("the plan now lists permits/sources.md for all five hosts (Q57, #142)"). Diff golden đọc được: một dòng `create     permits/sources.md`, không gì khác.
- Thiết kế: Q57 được ghi vào design (§5 và nhật ký, "Q1–Q57"), `AGENTS.md` và `docs/agents/standards.md` cùng thay đổi, có test `test_design_and_standards_record_q57`. Mã khớp từng điều Q57 nêu (create/update/unchanged, KiroCrew gồm cả, hai đường tìm sổ, hatch force-include).
- Checklist skill (diff chạm `skills/`): ba câu thêm vào `founder-permits`, `founder-cfo`, `founder-plan` là chỉ dẫn tiếng Anh cho người hỗ trợ (đúng quy tắc "Instructions in English"), không có `$` cạnh chữ số, không thêm khẳng định pháp lý hay số liệu mới nên không cần link hay ngày mới, miễn trừ trách nhiệm và cảnh báo "Panel là mô phỏng, cận trên" của `founder-plan` còn nguyên, `metadata.version` không đổi và `skill_lint` xác nhận khớp 0.3.0. Phần văn bản cho chủ hộ trong README tiếng Việt vẫn tiếng Việt.
- Hình dạng vòng lặp: (a) `a942c0b` (`seam:` với `## Seam`) đứng trước mọi commit `slice(`. (b) Commit duy nhất chạm `src/` là `71cc64b`; nó chạm `tests/test_install.py`, `tests/test_install_cli.py` và golden, và bảng `## Lát` có dòng cho mọi slice. (c) Test ở seam đã khai (`install.run`, CLI `install`, pyproject, golden). (d) Khối `## Cổng ba đoạn` ghi `verify: GREEN on 823a057b60cf…`, và `823a057` là commit cuối trước commit evidence (không có commit mã nào sau nó), nên cổng không stale.
- Bằng chứng đỏ rồi xanh: bảng `## Lát` ghi dòng assertion lúc đỏ cho từng slice (KeyError, AttributeError, DID NOT RAISE, mã thoát 0 thay vì 2) và lần chạy xanh.

## Ghi chú không chặn (judgement, không gắn mã)

- `_check_inside` (`install.py:148`) lặp lại đúng biểu thức kiểm tra có sẵn trong `_plan_registration` (`install.py:175`) và `_copy_skills` (dòng 128 đến 132). Có thể gom về một hàm; đây là smell Duplicated Code, không phải vi phạm chuẩn đã ghi.
- Evidence tự nêu giới hạn: symlink treo trỏ trong dự án tại `permits/sources.md` bị ghi xuyên qua; điều này khớp quy tắc "như file skill" của Q57 và đã khai.

## Chưa xác minh

- `README.md` và `pyproject.toml` nằm trong danh sách một-chủ của `docs/agents/parallel-lanes.md`. Tôi không có comment `<!-- harness:allocation -->` của issue #142 (không có credential API trong sandbox), nên chưa kiểm được lane có được cấp hai file này. Với `HARNESS_WIP` 1 thì cấp phát là `all`; nếu allocation thực tế không cấp, đây sẽ là finding BLOCKED, và merger/guard là nơi kiểm.
- Wheel thật chưa được build lại ở lượt này; tôi tin vào mục `## Wheel` của evidence và test `test_pyproject_ships_the_ledger_in_the_wheel`.
- Không có phiên host thật (evidence đã nêu).

<promise>PASS</promise>
