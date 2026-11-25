Commit mã đã chấm: bf4b9a3018ef

# Review trục Spec, #94, vòng 1

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git log main..HEAD` (6 commit: seam, kiro, claude/codex/grok, goldens, docs Q54, evidence) và `git diff --stat main...HEAD` (16 file). Đã đọc `AGENTS.md`; đối chiếu design §2, §5 và nhật ký quyết định.

## Đối chiếu từng yêu cầu

- Kiro ghi `.kiro/settings/mcp.json` kèm mục `founder-vn` khi file chưa có: `install._write_registration` + `REGISTRATION_FILES["kiro"]`; test `test_kiro_writes_the_registration_file_when_absent` và `test_cli_install_writes_the_registration_file_on_a_clean_project` (thuộc `pytest` của cổng unit, testpaths = tests).
- File đã có thì chỉ in, không gộp, không xoá: nhánh `os.path.lexists` trả `exists ... (not modified)`; test `test_kiro_leaves_an_existing_registration_file_byte_unchanged` so byte. Symlink treo cũng tính là đã có, không bị ghi đè.
- Claude `.mcp.json`, Codex `.codex/config.toml`, Grok `.grok/config.toml`: ghi khi vắng, in khi có; test tham số hoá 3 host (`test_project_file_hosts_write_when_absent_and_print_when_present`). Nội dung Codex giữ `tool_timeout_sec = 300` như đoạn in trước đó.
- KiroCrew giữ chỉ in: không có trong `REGISTRATION_FILES`; test `test_kirocrew_has_no_registration_file` và `test_hosts.py` khẳng định.
- `--print-only` không ghi gì: nhánh `if not print_only`; test `test_print_only_writes_no_registration_file`. Dòng kế hoạch vẫn liệt kê `create`.
- Khoá trong gốc dự án (design §2): `_plan_registration` kiểm `resolve().is_relative_to` trước khi chép skill, raise `InstallRefused`; test symlink thoát được. CLI exit 2 đã có test sẵn cho đường từ chối.
- Q54 thêm vào nhật ký, tiêu đề đổi thành Q1–Q54 (design và `AGENTS.md`); câu §5 "in đoạn cấu hình MCP" đã sửa thành "đăng ký MCP (Q54)".
- Trang host và `docs/hosts/kiro.md` bước 3 nói file được ghi trên dự án sạch; `test_host_pages_name_the_project_registration_file_the_installer_writes` kiểm tên file ở từng trang.
- Golden `tests/golden/install_{kiro,claude,codex,grok}.json` đổi (kế hoạch có dòng `create` file đăng ký); commit 3a650f4 nói rõ goldens đổi vì Q54. Đã chạy lại `uv run pytest tests/test_install.py tests/test_install_cli.py tests/test_hosts.py -q`: 42 passed.
- Ngoài phạm vi giữ nguyên: không có gộp vào file có sẵn, không đụng KiroCrew, không sửa bản ghi walkthrough #19. Không có tham số MCP/parity (CLI only, Q34).
- CI: Gate success (run 45571735592) ở đúng commit này; bằng chứng đỏ-rồi-xanh nằm ở `docs/evidence/issue-94-installer-writes-mcp.md`.

## Chưa xác minh

- Không chạy host thật nạp file Codex/Grok đã ghi (evidence của lane cũng nêu). Việc đổi trang Codex và Grok từ `~/` sang file dự án dựa trên link tài liệu chính thức ngày 2026-11-25 mà lane ghi; tôi không mở lại các link đó. Q54 của operator nêu rõ "Codex and Grok TOML" là file dự án, nên không coi là quyết định tự đặt.
- `docs/hosts/kiro.md` bước 3 có câu hơi lặp ("edit `args` and put the wheel path in `args`"); đây là văn phong, không phải finding Spec.

<promise>PASS</promise>
