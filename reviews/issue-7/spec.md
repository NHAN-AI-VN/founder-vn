Commit mã đã chấm: a442adab7b7a

# Review trục Spec, issue #7, vòng 2

**Phán quyết**: PASS

Phạm vi: `git log --oneline main..HEAD` và `git diff --stat main...HEAD` (27 file). So với vòng 1 (`68a9c1d`), mã ứng dụng đổi ở `359ffee` (bỏ cờ công khai `--skills-dir` khỏi `src/founder_vn/cli.py`, `tests/test_install_cli.py`); các commit còn lại chỉ chạm `docs/evidence/issue-7-installer.md` và `reviews/issue-7/ledger.md`. Đã đọc `AGENTS.md`, `src/founder_vn/install.py`, `cli.py`, `tests/test_install_cli.py`, `tests/test_install.py`, `pyproject.toml`, ledger và câu trả lời operator. Chạy ở `a442adab7b7a`: `uv run pytest -q` cho `132 passed`; `uv run ruff check .` cho `All checks passed!`. Kết quả workflow `Gate` run 45103219267 lúc ra lệnh: success, job `Gate` còn `in_progress`; kết quả cục bộ là bằng chứng thay thế.

## Kiểm lại sau khi bỏ `--skills-dir`

- CLI gọi `install.run(Path.cwd(), host, print_only)` không truyền nguồn, nên `_copy_skills` dùng `packaged_skills_dir()`: thư mục `founder_vn/skills` trong wheel (`force-include` ở `pyproject.toml`), hoặc `skills/` của repo. Tiêu chí "sao chép skill đóng gói" vẫn đi qua đường đóng gói thật, và còn gần với ticket hơn so với lúc có cờ ghi đè.
- Golden test (`test_print_only_golden`) vá `install.packaged_skills_dir` về fixture tổng hợp, assert không lộ đường dẫn fixture, không ghi gì (`list(project_root.iterdir()) == []`). Năm file `tests/golden/install_*.json` không đổi so với vòng 1 và test vẫn xanh.
- `grep` tìm `skills-dir` ngoài `reviews/`: không trang `docs/hosts/*.md`, README hay evidence nào còn nhắc cờ này ở dạng cờ CLI. Chỉ còn tham số `skills_dir` của hàm `install.run` (seam cho test) và dòng bảng đột biến trong evidence. Không có tài liệu mô tả sai.
- `test_cli_refusal_exits_2` vẫn kiểm nhánh từ chối symlink (exit 2) qua CLI không cần cờ nguồn.

## Đối chiếu từng criterion

1. **Sao chép skill vào thư mục skill cấp dự án; idempotent; `--print-only` in kế hoạch và snippet không ghi.** Đáp ứng. `install._copy_skills` (map `SKILL_FOLDERS`, trạng thái `create`/`unchanged`/`update`, `--print-only` bỏ qua ghi). Bằng chứng trong cổng `unit`: `tests/test_install.py` (copy 5 host, idempotent, giữ file lạ, print-only, từ chối thoát project) và `test_print_only_golden`. Đóng gói wheel: `test_pyproject_ships_skills_in_the_wheel`.
2. **Snippet MCP riêng từng host.** Đáp ứng: Kiro `mcp.json`, Claude `.mcp.json` và `claude mcp add`, Codex `config.toml` với ghi chú 60 giây và `tool_timeout_sec`, Grok `config.toml`, KiroCrew dashboard và yêu cầu trust dự án. Test: golden từng host, `test_codex_snippet_carries_the_timeout_note`, `test_kirocrew_snippet_names_dashboard_and_trust`, `test_snippets_name_env_variables_without_values` (không in giá trị `FOUNDER_LLM_*`).
3. **Trang Gemini CLI / Antigravity: khai báo biến API key trong khối `env`, nhãn "pending confirmation".** Đáp ứng, `docs/hosts/gemini.md` và `tests/test_hosts.py` (chạy trong `pytest`). `gemini` không phải giá trị `--host` (ticket liệt kê đúng 5 host; có `test_gemini_is_not_a_host_value`).
4. **Golden test đầu ra installer mỗi host ở print-only.** Đáp ứng, 5 file golden qua `assert_golden`, trong cổng `unit`.
5. **Trang host điền từ stub T02.** Đáp ứng, `tests/test_hosts.py` kiểm không còn `Status: stub` và khối toml/json khớp installer; `docs/hosts/README.md` cập nhật.

## Giới hạn và phạm vi

- Không có hành vi vượt ticket. Việc bỏ `--skills-dir` thu hẹp bề mặt CLI về đúng `--host` và `--print-only` mà ticket nêu. `install` chỉ có ở CLI, không có tool MCP (design §5, "Parity decision" trong evidence), nên không cần test parity.
- Không có artefact cho chủ hộ; đầu ra tiếng Anh cho Facilitator, không `$`, không dữ liệu người thật.

## Chưa xác minh (không chặn)

- `skills/` mới chỉ có `.gitkeep`, nên việc sao chép skill thật chỉ được chứng minh trên fixture tổng hợp; chạy thật in "no skills found in the package; nothing to copy". Việc lấp thư mục thuộc các ticket skill.
- Tên bảng `[mcp_servers.founder-vn]` và đường dẫn `~/.grok/config.toml` của Grok Build, và việc Gemini có nới `$NAME` trong `env` hay không, chưa chạy trên host thật; trang host ghi rõ "not yet witnessed" hoặc "pending confirmation".
- `tool_timeout_sec = 300` là giá trị ví dụ, chưa đo.
- Job `Gate` của CI chưa hoàn tất lúc ra lệnh.

<promise>PASS</promise>
