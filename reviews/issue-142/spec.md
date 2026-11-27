Commit mã đã chấm: dc9a416defca

# Review trục Spec, #142, vòng 1

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git log --oneline main..HEAD` (6 commit: seam, install, skills, front-door, design Q57, evidence) và `git diff --stat main...HEAD` (24 file). Không có file nào ngoài phạm vi ticket. `permits/sources.md` không bị sửa (nội dung sổ ngoài phạm vi).

## Đối chiếu từng criterion

1. Wheel mang sổ: `pyproject.toml` thêm force-include `permits/sources.md` -> `founder_vn/permits/sources.md`; `test_pyproject_ships_the_ledger_in_the_wheel` ghim. Tự kiểm lại: `uv build --wheel` rồi `unzip -l` liệt kê `founder_vn/permits/sources.md` (28337 byte), `cmp` với `permits/sources.md` giống hệt. Evidence cũng ghi đúng điều này.
2. Mọi host ghi sổ: `install.run` gọi `_write_ledger` cho mọi host (kể cả kirocrew); `test_every_host_writes_the_ledger_on_an_empty_project` tham số hoá 5 host, so byte với sổ gói và kiểm dòng `create     permits/sources.md`; `test_cli_install_writes_the_ledger_on_a_clean_project` qua CLI `--host kiro`.
3. `unchanged` / `update`: `test_second_run_reports_the_ledger_unchanged`, `test_a_differing_ledger_is_updated_and_other_permits_files_are_kept` (file khác trong `permits/` còn nguyên).
4. `--print-only`: `test_print_only_plans_the_ledger_and_writes_nothing` (kirocrew, thư mục dự án rỗng sau đó).
5. Thoát khỏi dự án: `_check_inside` chạy trước mọi ghi; test symlink `permits` -> ngoài dự án raise `InstallRefused`, không ghi ra ngoài, không có `.kiro`; `test_cli_ledger_escape_exits_2` kiểm exit 2.
6. Golden: 5 file `tests/golden/install_*.json` đều đổi, dòng mới đặt trước dòng đăng ký; `test_print_only_golden` nằm trong `pytest`.
7. Ba skill mang đúng một câu (so khớp nguyên văn với mục 3 của quyết định); mỗi test skill ghim câu đó; `scripts/skill_lint.py` chạy lại: 0 finding; khối `## Protocol` không nằm trong diff.
8. Q57 ở nhật ký (heading Q1–Q57, cả `AGENTS.md`), §5, bullet installer của standards, `docs/hosts/kiro.md`, `docs/hosts/README.md`, `README.md` (EN và VI) đã sửa; `test_front_door.py` và `test_hosts.py` ghim câu mới và cấm câu "known defect"; `test_design_and_standards_record_q57` ghim design và standards.
9. Cổng: CI `Gate` success ở `dc9a416defca`; `uv run pytest -q` chạy lại tại chỗ: 481 passed. Evidence `docs/evidence/issue-142-ship-ledger.md` có bảng đỏ-rồi-xanh cho từng lát, mục wheel và ba đoạn cổng. Commit sau 823a057 chỉ là file evidence.

Giới hạn ticket: không có tool tra cứu sổ, không chuyển sổ vào thư mục skill, không đổi nội dung sổ, không gộp sửa tay, không bump phiên bản; diff không vượt qua điều nào.

## Chưa xác minh

- Chưa chạy `install` từ wheel đã cài (đường `founder_vn/permits/sources.md` của `packaged_ledger`); test chỉ phủ đường dự phòng về repo. Wheel chứa file đúng, và logic tìm hai đường giống `packaged_skills_dir`, nên rủi ro thấp. Không chặn.
- Không đọc từng dòng đầy đủ phần bullet standards (dòng dài); test ghim hai chuỗi của nó và khớp.

<promise>PASS</promise>
