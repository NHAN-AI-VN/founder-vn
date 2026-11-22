Commit mã đã chấm: b945d20d050f

# Review trục Spec, issue #2, vòng 1

Phán quyết: PASS. Không có finding chặn.

Phạm vi: `git diff --stat main...HEAD` (19 file, 9 commit). Tôi chạy lại tại b945d20d050f: `uv sync --frozen`, `uv run pytest -q` (32 passed), `uv run ruff check` (sạch), `uv run ruff format --check` (sạch), `uv build` (sdist và wheel 0.1.0). Ba lệnh này là cổng `static`, `unit`, `build`. Run Gate 45003536422 báo success toàn run, job Gate còn in_progress lúc nhận lệnh.

## Đối chiếu từng criterion

1. `founder-vn version` và MCP `server_info` cùng văn bản: ĐẠT. Cả hai gọi `info.version_text()` (`src/founder_vn/info.py`). `tests/test_parity.py::test_cli_version_equals_mcp_server_info` chạy CLI thật (`main(["version"])`), gọi tool `server_info` qua `mcp.Client` và so từng byte (phần CLI có thêm `\n`). `tests/test_fixtures.py::test_mcp_stdio_client_calls_server_info` kiểm tra thêm qua subprocess stdio thật. Cả hai nằm trong `pytest` của cổng `unit`.
2. Lớp file bị khóa đường dẫn: ĐẠT. `src/founder_vn/files.py` từ chối `..`, đường dẫn tuyệt đối ngoài gốc `founder/`, symlink trỏ ra ngoài (thư mục và file) và phần mở rộng khác `.md`/`.json`. Mỗi kiểu từ chối có test riêng trong `tests/test_files.py`, và test khẳng định không có file nào được tạo ở ngoài. Module không có hàm xoá: test kiểm tên công khai và kiểm mã nguồn không có lời gọi `unlink`, `rmdir`, `os.remove`, `rmtree`. Bản thiết kế (§ dòng 77-78) nói đúng các điều này, gốc là `founder/`.
3. Fixture kiểm thử: ĐẠT. `tests/conftest.py` có `project_root`, `run_cli` cùng `assert_golden` (stdout và file ghi ra, golden `tests/golden/version.json`), `mcp_call` (client MCP qua stdio thật), `fake_provider` (HTTP loopback `/v1/chat/completions`) và guard `no_external_network` tự động. `tests/test_fixtures.py` chứng minh từng fixture hoạt động và có đường thất bại (golden lệch, kết nối ngoài loopback).
4. CI chạy pytest, ruff và build khi push và PR: ĐẠT ở phía mã. `.github/workflows/gate.yml` chạy các bước này khi có `pyproject.toml` (gate.yml có sẵn ở main; nhánh này thêm `pyproject.toml` và `uv.lock` nên các bước Python bật). Cổng ba đoạn xanh cục bộ; kết quả của job Gate trên CI chưa có lúc chấm (xem "Chưa xác minh").
5. Gắn tag `v0.1.0` phát hành lên PyPI bằng trusted publishing: ĐẠT ở phía mã. `.github/workflows/release.yml` chạy khi đẩy tag `v*`, kiểm tag bằng `v<__version__>`, `uv build`, rồi publish bằng `pypa/gh-action-pypi-publish` với `id-token: write`, `environment: pypi`, không có token hay secret. `tests/test_release.py` kiểm các tính chất đó (chỉ kiểm văn bản workflow). Ghi nhận `mcp.json` của Kiro: `docs/hosts/kiro.md` có mục `uvx founder-vn-mcp`; `tests/test_hosts.py` kiểm nó là JSON hợp lệ, tên khớp `[project.scripts]` và không chứa giá trị bí mật. Bằng chứng nói smoke check từ wheel cục bộ trả `founder-vn 0.1.0` (`docs/evidence/issue-2-scaffold-parity-release.md`).
6. Python ≥ 3.11, dependency chỉ gồm MCP SDK và HTTP client: ĐẠT. `requires-python = ">=3.11"`, `dependencies = ["mcp>=2,<3", "httpx"]`; `pytest` và `ruff` chỉ ở nhóm `dev`. `uv.lock` được commit cùng lúc. Bản thiết kế Q44 cũng ghi `mcp`, `httpx`.

Giới hạn và điều ngoài phạm vi ticket không bị vượt: không thấy tool, lệnh hay hành vi nào ngoài `version` / `--version` / `server_info`; không có dữ liệu thật hay giá trị `FOUNDER_LLM_*` trong diff (tài liệu chỉ nêu tên biến).

## Chưa xác minh (không gắn mã, không chặn)

- "Version 0.1.0 is live" và "`uvx founder-vn-mcp` khởi động và trả `server_info`" từ PyPI: chỉ chứng minh được sau khi chủ repo cấu hình trusted publisher, tạo environment `pypi` và đẩy tag `v0.1.0`. Lane không có quyền làm việc đó; bằng chứng của lane nêu rõ giới hạn này và thứ tự các bước. Đây là hành động sau merge của chủ repo, không phải lỗi mã. Cần xác nhận sau khi phát hành.
- Job Gate trên CI còn in_progress ở thời điểm chấm; cần kết luận cuối là success. Lượt này không tự coi nó là bằng chứng.
- Thân PR (nơi ticket yêu cầu ghi lại đăng ký Kiro `mcp.json`): lượt này không có quyền đọc thân PR. Bằng chứng nói thân PR nhắc lại mục đó; chưa đối chiếu được.
- Việc host Kiro nạp mục `mcp.json` chỉ được kiểm ở mức JSON và tên script, như bằng chứng đã nêu.

<promise>PASS</promise>
