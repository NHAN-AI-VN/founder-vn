Commit mã đã chấm: ca3c7ed4621f

# Review trục Spec, #94, vòng 2

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git log main..HEAD` và `git diff --stat main...HEAD` (20 file). Từ commit đã chấm ở vòng 1 (`bf4b9a3`) đến `ca3c7ed`, chỉ `docs/agents/standards.md` đổi (bullet installer nay liệt kê `install.REGISTRATION_FILES`), cộng hai file review. `src/`, test, golden và docs host không đổi, nên các đối chiếu ở vòng 1 vẫn đúng. Tôi đã đọc lại diff của chúng và chạy lại test.

## Đối chiếu từng yêu cầu

- Kiro ghi `.kiro/settings/mcp.json` kèm mục `founder-vn` khi file chưa có: `REGISTRATION_FILES["kiro"]` và `_write_registration`. Test: `test_kiro_writes_the_registration_file_when_absent`, `test_cli_install_writes_the_registration_file_on_a_clean_project`.
- File đã có thì chỉ in, không gộp, không xoá: nhánh `os.path.lexists` trả `exists ... (not modified)`. Test `test_kiro_leaves_an_existing_registration_file_byte_unchanged` so byte.
- Claude `.mcp.json`, Codex `.codex/config.toml`, Grok `.grok/config.toml` ghi khi vắng, in khi có: `test_project_file_hosts_write_when_absent_and_print_when_present` (tham số hoá 3 host, parse JSON/TOML).
- KiroCrew giữ chỉ in: không nằm trong `REGISTRATION_FILES`. Test `test_kirocrew_has_no_registration_file`.
- `--print-only` không ghi gì: `test_print_only_writes_no_registration_file`.
- Khoá trong gốc dự án (design §2): `_plan_registration` từ chối trước khi chép skill. Test `test_registration_file_through_an_escaping_symlink_is_refused`.
- Q54 thêm vào nhật ký (tiêu đề Q1–Q54), câu §5 "in đoạn cấu hình MCP" đã sửa thành "đăng ký MCP (Q54)". Host pages và `docs/hosts/kiro.md` bước 3 nói file được ghi trên dự án sạch; `tests/test_hosts.py` kiểm tên file.
- Golden `tests/golden/install_{kiro,claude,codex,grok}.json` đổi (dòng `create` file đăng ký); lane nói rõ trong commit.
- Ngoài phạm vi giữ nguyên: không gộp vào file có sẵn, không đụng KiroCrew, không sửa bản ghi #19. CLI-only (Q34), không cần parity.
- Bằng chứng chạy: `uv run pytest tests/test_install.py tests/test_install_cli.py tests/test_hosts.py -q` cho 42 passed. CI `Gate` success ở `f28dae3` (run 45572451261). Evidence đỏ rồi xanh ở `docs/evidence/issue-94-installer-writes-mcp.md`.
- Commit `ca3c7ed` (standards.md): mô tả bốn file đăng ký, "ghi khi vắng, không gộp, không xoá", khoá trong dự án, KiroCrew chỉ in. Khớp hành vi mã, không thêm hành vi mới.

## Chưa xác minh

- Không chạy host thật nạp file Codex/Grok đã ghi. Việc chuyển trang Codex và Grok từ `~/` sang file dự án dựa trên link tài liệu ngày 2026-11-25 mà lane ghi trong Q54; tôi không mở lại các link. Q54 của operator nêu rõ "Codex and Grok TOML" là file dự án, nên đây không phải quyết định lane tự đặt.
- `docs/hosts/kiro.md` bước 3 có câu lặp ("edit `args` and put the wheel path in `args`"). Đây là văn phong, không thuộc trục Spec.

<promise>PASS</promise>
