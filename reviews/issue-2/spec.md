Commit mã đã chấm: a90122eefc06

# Review trục Spec, issue #2, vòng 2

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git log --oneline origin/main..HEAD` (14 commit) và `git diff --stat origin/main...HEAD` (23 file). Vòng 1 chấm tại b945d20d050f (PASS). Từ đó lane thêm 5 commit đóng S1, S2, S3 của trục Standards: evidence doc, `scripts/skill_lint.py`, `tests/test_package.py`, `tests/test_release.py`, `tests/test_skill_lint.py`, `reviews/issue-2/ledger.md`. Tôi đọc lại toàn bộ mã nguồn và test của diff, không chỉ phần mới.

Tôi chạy lại tại a90122eefc06: `uv run pytest -q` (34 passed), `uv run ruff check .` (sạch), `uv build` (sdist và wheel 0.1.0). CI Gate run 45004457495 tại cùng commit: success, job Gate success (theo tin nhắn giao việc, tôi không tự truy vấn được).

## Thay đổi từ vòng 1 và ảnh hưởng tới criterion

- `scripts/skill_lint.py`: đọc phiên bản động từ `[tool.hatch.version].path`, phần còn lại là định dạng lại. Không phải file một-chủ (danh sách ở `docs/agents/parallel-lanes.md`: `pyproject.toml`, `uv.lock`, `README.md`, `src/founder_vn/__init__.py`), nên không tạo BLOCKED. Cần vì `pyproject.toml` dùng `dynamic = ["version"]`. Không thêm hành vi ngoài ticket.
- `tests/test_package.py`: so `importlib.metadata.version("founder-vn")` với `founder_vn.__version__`. Giữ nguyên đúng criterion về phiên bản một nguồn.
- Test fixtures có thêm bằng chứng đỏ (đột biến guard mạng và golden runner), ghi trong evidence doc. Củng cố criterion 3.
- Mã `src/` không đổi so với vòng 1.

## Đối chiếu từng criterion

1. `founder-vn version` và MCP `server_info` cùng văn bản: ĐẠT. Cả hai gọi `info.version_text()`. `tests/test_parity.py::test_cli_version_equals_mcp_server_info` chạy CLI (`main(["version"])`), gọi tool `server_info` qua `mcp.Client` và so từng byte (CLI chỉ thêm `\n`). `tests/test_fixtures.py` kiểm thêm qua subprocess stdio. Nằm trong `pytest` của cổng `unit`.
2. Lớp file khóa đường dẫn: ĐẠT. `src/founder_vn/files.py` từ chối `..`, tuyệt đối ngoài gốc `founder/`, symlink thoát gốc, đuôi khác `.md`/`.json`; không có hàm xoá. Mỗi kiểu từ chối có test riêng trong `tests/test_files.py`.
3. Fixture: ĐẠT. `tests/conftest.py` có `project_root`, `run_cli` với `assert_golden` (stdout và file ghi ra), `mcp_call` (stdio thật), `fake_provider` (HTTP loopback) và guard mạng tự động; `tests/test_fixtures.py` chứng minh từng cái, gồm đường thất bại.
4. CI chạy pytest, ruff, build khi push và PR, xanh: ĐẠT. `gate.yml` bật các bước Python vì nhánh có `pyproject.toml` và `uv.lock`; ba lệnh xanh cục bộ và run 45004457495 success tại đúng commit chấm.
5. Tag `v0.1.0` phát hành PyPI bằng trusted publishing; ghi `mcp.json` Kiro: ĐẠT ở phía mã. `.github/workflows/release.yml` chạy khi đẩy tag `v*`, kiểm tag bằng `v<__version__>`, `uv build`, publish bằng `pypa/gh-action-pypi-publish` với `id-token: write` và `environment: pypi`, không có token. `tests/test_release.py` kiểm văn bản workflow. `docs/hosts/kiro.md` có mục `uvx founder-vn-mcp`, `tests/test_hosts.py` kiểm JSON hợp lệ, tên khớp `[project.scripts]`, không có giá trị bí mật.
6. Python ≥ 3.11, dependency chỉ MCP SDK và HTTP client: ĐẠT. `requires-python = ">=3.11"`, `dependencies = ["mcp>=2,<3", "httpx"]`; `pytest` và `ruff` ở nhóm `dev`.

Giới hạn ticket không bị vượt: không có tool hay lệnh ngoài `version`, `--version`, `server_info`; không có dữ liệu thật hay giá trị `FOUNDER_LLM_*` trong diff.

## Chưa xác minh (không gắn mã, không chặn)

- "Version 0.1.0 is live" và `uvx founder-vn-mcp` từ PyPI khởi động, trả `server_info`: chỉ chứng minh được sau khi chủ repo cấu hình trusted publisher, tạo environment `pypi` và đẩy tag `v0.1.0`. Lane không có quyền đó; evidence doc nêu rõ giới hạn. Cần xác nhận sau phát hành.
- Thân PR (nơi ticket yêu cầu ghi `mcp.json`): không đọc được ở lượt này. Evidence doc nói thân PR nhắc lại mục đó.
- Việc Kiro thực sự nạp mục `mcp.json`: chỉ kiểm ở mức JSON và tên script.

<promise>PASS</promise>
