Commit mã đã chấm: 68a9c1deb50d

# Review trục Spec, issue #7, vòng 1

**Phán quyết**: PASS

Phạm vi: `git log --oneline main..HEAD` (10 commit, từ `eee6595` đến `68a9c1d`) và `git diff --stat main...HEAD` (26 file). So với lượt trước (`0ec3879`), ba commit mới (`8fa0f69`, `17a2a7f`, `68a9c1d`) chỉ chạm `docs/agents/standards.md` và `reviews/issue-7/*`; `src/`, `tests/`, `pyproject.toml`, `docs/hosts/` không đổi. Đã đọc `AGENTS.md`, `docs/founder-vn-design.md` (§1 sự thật về host, §5 cài đặt, Q34), `src/founder_vn/install.py`, `cli.py`, `pyproject.toml`, 5 file golden, 6 trang `docs/hosts/*.md`, test và `docs/evidence/issue-7-installer.md`. Chạy lại ở checkout `68a9c1d`: `uv run pytest -q` cho `132 passed`, `uv run ruff check .` cho `All checks passed!`.

## Đối chiếu từng criterion

1. **Sao chép skill vào thư mục skill cấp dự án của host; idempotent; `--print-only` in kế hoạch và snippet mà không ghi.** Đáp ứng.
   - `install.py::_copy_skills` map host sang `.kiro/skills`, `.grok/skills`, `.claude/skills`, `.agents/skills`, khớp design §1 (Kiro, Grok, Codex, KiroCrew đọc `.kiro/skills/` khi dự án được trust).
   - Trạng thái `create`/`unchanged`/`update`; `--print-only` bỏ qua `write_bytes`.
   - Bằng chứng nằm trong cổng `unit`: `tests/test_install.py` (copy 5 host, idempotent, update giữ file lạ, print-only không ghi, từ chối symlink escape) và `tests/test_install_cli.py::test_print_only_golden` (assert `list(project_root.iterdir()) == []`).
   - Gói trong wheel: `pyproject.toml` `force-include`, có `test_pyproject_ships_skills_in_the_wheel`.
2. **In cấu hình đăng ký MCP riêng từng host.** Đáp ứng.
   - Kiro: `mcp.json` (workspace hoặc user).
   - Claude Code: `.mcp.json` phạm vi project và lệnh `claude mcp add --scope project`.
   - Codex: `config.toml` kèm `tool_timeout_sec` và ghi chú 60 giây (có test riêng).
   - Grok Build: `~/.grok/config.toml`.
   - KiroCrew: các bước dashboard, yêu cầu trust dự án, nói rõ không đọc `.kiro/settings/mcp.json` (có test riêng).
   - Giá trị biến `FOUNDER_LLM_*` không bao giờ được in (`test_snippets_name_env_variables_without_values`).
3. **Trang Gemini CLI / Antigravity khai báo biến API key trong khối `env` của server và gắn nhãn "pending confirmation".** Đáp ứng. `docs/hosts/gemini.md` có dòng `Status: pending confirmation`, khối JSON `"env": {"FOUNDER_LLM_API_KEY": ...}`, giải thích cơ chế xóa biến `KEY`/`SECRET` (khớp design §1). `tests/test_hosts.py::test_gemini_page_is_pending_confirmation_and_declares_the_key_by_name` chạy trong `pytest`. `gemini` cố ý không phải giá trị `--host` (ticket liệt kê đúng 5 host; có test).
4. **Golden test đầu ra installer cho từng host ở chế độ print-only.** Đáp ứng. Có 5 file `tests/golden/install_{kiro,claude,codex,grok,kirocrew}.json`, chạy qua `assert_golden` trong `pytest` của cổng `unit`. Nguồn skill là fixture tổng hợp `tests/fixtures/skills_src`, golden không chứa đường dẫn tuyệt đối.
5. **Trang host điền từ stub của T02.** Đáp ứng. 5 trang cũ không còn `Status: stub` (`test_filled_pages_have_no_stub_status_and_match_the_installer`), `README.md` trong `docs/hosts/` cập nhật bảng trạng thái, các khối toml/json trong trang được parse trong test.

## Thay đổi từ lượt trước

- `68a9c1d` ghi ngoại lệ của installer vào `docs/agents/standards.md` theo câu trả lời operator cho S1 (`reviews/issue-7/operator-answer.md`). Ngoại lệ khớp mã: chỉ ghi vào `install.SKILL_FOLDERS`, từ chối đích thoát project bằng `InstallRefused` và exit 2 trước khi ghi, không xoá, `--print-only` không ghi, CLI-only. Đây là chuẩn, không phải hành vi mới của ticket, nên không tạo finding Spec.
- Kết quả CI `Gate` run 45102747034: `success`, job `Gate` còn `in_progress` lúc ra lệnh; kết quả cục bộ ở trên là bằng chứng thay thế.
- S2 (đỏ rồi xanh) thuộc trục Standards, không xét ở đây.

## Giới hạn và phạm vi ticket

- Không có hành vi vượt ticket. `install` chỉ có ở CLI, không có tool MCP. Lý do ghi trong `docs/evidence/issue-7-installer.md` ("Parity decision"), và design §5 chỉ nêu `founder-vn install` như lệnh CLI, nên không cần test parity.
- Không có artefact cho chủ hộ nào trong diff (đầu ra tiếng Anh cho Facilitator, đúng design §4); không có dữ liệu người thật hay `$` trong đầu ra.

## Chưa xác minh (không chặn)

- `skills/` mới chỉ có `.gitkeep`, nên "sao chép skill đóng gói" chỉ được chứng minh trên fixture tổng hợp; chạy thật hiện in "no skills found in the package; nothing to copy". Evidence nêu rõ giới hạn này. Việc lấp thư mục thuộc các ticket skill, không thuộc #7.
- Tên bảng `[mcp_servers.founder-vn]` của Grok Build, đường dẫn `~/.grok/config.toml`, và việc Gemini có nới `$NAME` trong `env` hay không chưa chạy trên host thật. Các trang host đều ghi "not yet witnessed" hoặc "pending confirmation".
- `tool_timeout_sec = 300` là giá trị ví dụ, chưa đo.
- Kết quả workflow `Gate` ở commit này báo `in_progress` lúc ra lệnh; evidence ghi cổng ba đoạn xanh ở `c124219` (các commit sau chỉ đổi evidence).
- Một số test CLI phụ (ghi chú timeout, trust, tên biến env, `gemini` bị từ chối, exit 2) không có lần đỏ được chứng kiến, như evidence tự nêu; không ảnh hưởng criterion vì golden đã chốt cùng nội dung.

<promise>PASS</promise>
