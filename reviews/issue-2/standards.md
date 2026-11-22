Commit mã đã chấm: a90122eefc06

# Review trục Standards, issue #2, vòng 2

**Phán quyết**: PASS. S1, S2, S3 của vòng 1 đã đóng thật, và các commit sửa không đưa vào finding chặn mới.

## Phạm vi đã xét

- `git diff --stat main...HEAD` (23 file) và 16 commit của `git log --oneline main..HEAD`; trọng tâm là sáu commit sau `59e51f8` (`0a4a1ab`, `5de51b0`, `0e7f0f5`, `ad66e3f`, `a90122e`).
- Chuẩn: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/founder-vn-design.md` §2 và §5. `CONTRIBUTING.md` và `docs/adr/` chưa tồn tại.
- Chạy lại tại HEAD: `uv sync --frozen`, `ruff check .` (sạch), `ruff format --check .` (49 file sạch), `pytest -q` (34 passed), `python3 scripts/skill_lint.py` (0 skill, `package version 0.1.0`, trước đây là không có version). CI `Gate` run 45004457495 success.
- Checklist skill (mục 3): diff không chạm `skills/` hay `examples/`, không áp dụng.

## Kiểm lại ba finding vòng 1 bằng phép đo riêng

- S1 đóng. Tôi tự đột biến `tests/conftest.py`: thay `raise RuntimeError` (dòng 28) bằng `return` thì `test_network_guard_refuses_a_non_loopback_connection` đỏ với `DID NOT RAISE RuntimeError`; thay `assert ... == expected` (dòng 75) bằng `pass` thì `test_cli_golden_runner_detects_a_changed_output` đỏ với `DID NOT RAISE AssertionError`. Hai đột biến đã hoàn nguyên, `git status` sạch. Khớp với dòng `fixtures` trong `## Lát`. `## Giới hạn` nay nêu điểm mù (`connect_ex`, UDP `sendto`, tiến trình con, stderr, file ngoài `founder/`); `## Dependencies` ghi giấy phép `mcp` 2.3.0 (MIT) và `httpx` 0.28.1 (BSD-3-Clause).
- S2 đóng. Tôi vô hiệu nhánh `dynamic` của `project_version` (`scripts/skill_lint.py`): cả hai test trong `tests/test_skill_lint.py` đỏ (2 failed); khôi phục thì xanh. Test thật sự chạy script qua subprocess trên dự án tạm có `dynamic = ["version"]`, kiểm cả nhánh từ chối (`returncode == 1`, "differs from pyproject") lẫn nhánh chấp nhận. Rule `metadata.version` = phiên bản package hiện được thi hành.
- S3 đóng. `tests/test_package.py` so `importlib.metadata.version("founder-vn")` với `founder_vn.__version__`; `tests/test_release.py` không còn hằng `"0.1.0"` (diff `0e7f0f5` xoá dòng assert thừa); `test_skill_lint.py` cũng lấy version từ `founder_vn.__version__`, không hằng.

## Hình dạng vòng lặp

- (a) Đạt: `59137a0 seam:` mang `## Seam`, đứng trước mọi `slice(`. Các commit sửa là `fix:`/`docs:`, không phải slice, nên không phá thứ tự.
- (b) Đạt: không commit nào sau vòng 1 chạm `src/`. Commit chạm mã (`5de51b0` sửa `scripts/skill_lint.py`) kèm `tests/test_skill_lint.py` và có dòng `skill-lint (review S2)` trong `## Lát`.
- (c) Đạt: test mới chạy `scripts/skill_lint.py` qua CLI của nó (seam công khai của gate), không vào hàm nội bộ.
- (d) Đạt: khối `## Cổng ba đoạn` ghi `GREEN on 0e7f0f508ad0`, và `0e7f0f5` là commit cuối chạm mã hay test; `ad66e3f` chỉ thêm ledger, `a90122e` chỉ đổi file evidence. Cổng không stale.
- Ledger `reviews/issue-2/ledger.md`: tiêu đề nêu issue #2, đúng ba dòng `S1/S2/S3 FIXED — <bằng chứng>`, khớp ba mã trong báo cáo vòng 1. Mỗi dòng nêu lệnh đo lại và commit.
- Commit message nêu `#2` ở commit seam/slice; commit sửa nêu mã finding đóng (`close S1`, `close S2`, `close S3`). Không golden file nào đổi trong các commit sửa (`tests/golden/version.json` không có trong diff của chúng).

## Chưa xác minh

- Dòng `<!-- harness:allocation -->` của issue #2 (không có credential GitHub API): không đối chiếu được file một-chủ (`pyproject.toml`, `uv.lock`, `src/founder_vn/__init__.py`) với cấp phát; như vòng 1, không gắn mã.
- `project_version` trả `None` khi `pyproject.toml` có `dynamic` nhưng regex `__version__` không khớp (ví dụ đổi định dạng khai báo), và `rule_version_matches` coi `None` là khớp. Đường này không có test và là điểm mù còn lại của gate S2; chuẩn chưa quy định lỗi cứng ở đây và hiện chưa có skill nào để lộ, nên không chặn. Nên ghi vào `## Giới hạn` hoặc cho lint đỏ khi có `pyproject.toml` mà không đọc được version.
- Các mục "chưa xác minh" khác của vòng 1 (`files.write_text` kiểm đuôi trước khi resolve symlink, `anyio` nhập trực tiếp mà nhóm `dev` không khai, chính sách ghim action của `release.yml`) không đổi: ngoài diff sửa lần này, không là vi phạm chuẩn đã ghi.
- Chạy thật `release.yml` và `uvx founder-vn-mcp` từ PyPI cần Owner cấu hình trusted publisher; evidence đã khai.

<promise>PASS</promise>
