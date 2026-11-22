Commit mã đã chấm: b945d20d050f

# Review trục Standards, issue #2, vòng 1

**Phán quyết**: CHANGES_REQUESTED (3 finding chặn, lane tự sửa được, không cần file một-chủ ngoài cấp phát).

## Phạm vi đã xét

- Diff `git diff --stat main...HEAD` (19 file) và 9 commit của `git log --oneline main..HEAD`.
- Chuẩn: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` §2 và §5. `CONTRIBUTING.md` và `docs/adr/` chưa tồn tại.
- Đã chạy lại tại HEAD: `uv sync --frozen`, `ruff check .`, `ruff format --check .`, `pytest -q` (32 passed), `python3 scripts/skill_lint.py` (0 skill, 0 finding). Tất cả xanh.
- Checklist skill (mục 3): diff không chạm `skills/` hay `examples/`, nên không áp dụng.

## Hình dạng vòng lặp

- (a) Đạt: `59137a0 seam:` mang `## Seam`, đứng trước mọi commit `slice(`.
- (b) Đạt: `e0864b1`, `ee134b0`, `70896dc` chạm `src/` đều chạm test của lát và có dòng trong `## Lát`. Các commit `fixtures`, `release`, `hosts` không chạm `src/`.
- (c) Đạt: test nhập `founder_vn.files`, `cli.main`, `server.mcp`, `info`, đúng các seam đã khai.
- (d) Đạt: khối `## Cổng ba đoạn` ghi `GREEN on 1bca1223cebd`, là commit mã cuối (`2f627b0` và `b945d20` chỉ đổi file evidence). `.harness/gate-segments.txt` không nằm trong repo nên không đối chiếu được dòng log, nhưng ba đoạn đã chạy lại xanh tại HEAD.

## Finding chặn

### S1: Network guard và golden runner là cổng mới, không có bằng chứng đỏ rồi xanh và không có khai báo điểm mù

- Chỗ: `tests/conftest.py:20-30` (fixture `no_external_network`), `tests/conftest.py:80-86` (`assert_golden`); `docs/evidence/issue-2-scaffold-parity-release.md`, dòng `fixtures` trong `## Lát` ("No separate red") và mục `## Giới hạn`.
- Sai gì: hai fixture này là cổng thi hành chuẩn "No network in tests" và "Golden files for every report". Commit `deb442d` đưa cổng và test của nó vào cùng lúc, evidence tự ghi không có đỏ riêng. `## Giới hạn` không nêu điểm mù của guard: nó chỉ vá `socket.socket.connect`, nên `connect_ex`, UDP `sendto`, và tiến trình con (fixture `mcp_call` chạy server bằng `subprocess`) không bị chặn.
- Chuẩn: `docs/agents/standards.md` mục Tests ("A new gate ... is commissioned red-then-green"); `docs/agents/evidence-gates.md` mục "Commission a new gate" bước 3-4 và bảng "Evidence by change type" (dòng "New or changed gate": witnessed red mutation, restored green run, scope/blind-spot statement).
- Vì sao chặn: xanh mà chưa từng thấy đỏ chỉ chứng minh lệnh thoát 0. Mọi ticket sau tin vào guard này để không gọi mạng thật.
- Cách sửa (commit bổ sung, không viết lại lịch sử): vô hiệu guard (hoặc đổi `LOOPBACK` thành chứa mọi địa chỉ) và ghi test `test_network_guard_refuses_a_non_loopback_connection` đỏ đúng dòng assert; khôi phục, chạy xanh; làm tương tự cho `assert_golden`. Ghi hai lần chạy và một câu về điểm mù vào evidence (`## Lát` và `## Giới hạn`).

### S2: Đổi `[project].version` sang `dynamic` làm rule `metadata.version` = phiên bản package của `scripts/skill_lint.py` thành no-op

- Chỗ: `pyproject.toml:6` (`dynamic = ["version"]`, `[tool.hatch.version]`), `scripts/skill_lint.py:124-134` (`project_version`) và `rule_version_matches` (`return project is None or skill == project`).
- Sai gì: `project_version()` chỉ đọc khoá `version` tĩnh trong `[project]`. Với `dynamic`, nó trả `None`, và `rule_version_matches` coi `None` là khớp. Từ commit `e0864b1`, mọi `skills/*/SKILL.md` có `metadata.version` sai vẫn qua `skill-lint` xanh. Diff vừa sửa `skill_lint.py` (format lại) mà không thấy điều này, và chưa có test nào của gate này.
- Chuẩn: `docs/agents/standards.md` mục Skills ("`metadata.version` equals the package version ... `scripts/skill_lint.py` checks the machine-checkable half"); `docs/founder-vn-design.md` §2 ("cùng số phiên bản") và §5; `docs/agents/evidence-gates.md` bảng "Documentation, skill or example" (`skill_lint.py` green phải có nghĩa).
- Vì sao chặn: quy tắc còn trong tài liệu và trong tên hàm nhưng không còn gì thi hành. Ticket skill đầu tiên sẽ qua cổng mà không bị kiểm.
- Cách sửa: cho `project_version` đọc `src/founder_vn/__init__.py` (qua `[tool.hatch.version].path`) khi `version` là `dynamic`, hoặc đưa version tĩnh vào `[project]`; thêm test dưới `tests/` đưa một `SKILL.md` lệch phiên bản vào thư mục tạm và yêu cầu `skill_lint` đỏ, rồi xanh khi khớp (đúng bước đỏ rồi xanh của evidence-gates). Ghi hai lần chạy vào evidence.

### S3: Tên test nói một điều, mã làm điều khác

- Chỗ: `tests/test_package.py:4-5` (`test_package_has_single_source_version`); `tests/test_release.py:34` (dòng `assert founder_vn.__version__ == "0.1.0"` trong `test_release_builds_with_uv_and_checks_tag_against_version`).
- Sai gì: test đầu tên là "single source" nhưng chỉ so `__version__` với hằng `"0.1.0"`; không kiểm `pyproject` (qua hatch) và metadata của wheel cùng trả `__version__`. Test sau tên nói về build và kiểm tag, nhưng kết thúc bằng một assert hằng số không liên quan; lần nâng phiên bản đầu tiên sẽ làm hai test đỏ vì lý do sai, và dòng đó nằm chen vào test của workflow.
- Chuẩn: `docs/agents/standards.md` (reviewer chấm "tên nói một điều mà mã làm điều khác" là finding chặn); `docs/founder-vn-design.md` §2 (phiên bản một nguồn, skill và package cùng số).
- Cách sửa: đổi test đầu thành so `importlib.metadata.version("founder-vn")` (hoặc đọc `[tool.hatch.version].path`) với `founder_vn.__version__`, và bỏ hằng `"0.1.0"` khỏi cả hai test; xoá dòng assert thừa ở `test_release.py`. Ghi dòng `## Lát` của `scaffold` cho khớp.

## Chưa xác minh

- Dòng `<!-- harness:allocation -->` của issue #2 (không có credential GitHub API trong sandbox). Diff sửa `pyproject.toml`, `uv.lock`, `src/founder_vn/__init__.py`, ba file một-chủ trong `docs/agents/parallel-lanes.md`; với `HARNESS_WIP=1` allocation là `all`, nên không gắn mã, nhưng chưa đối chiếu được.
- Kết quả `Gate` run 45003536422: tin nhắn ghi `success` nhưng job `Gate: in_progress`; tôi chỉ dựa vào lần chạy cục bộ ở trên.
- `.github/workflows/release.yml`: `actions/checkout@v7`, `upload-artifact@v4`, `download-artifact@v4` đi theo tag, `setup-uv` ghim theo SHA; chuẩn chưa quy định chính sách ghim, nên không là finding. Chạy thật cần Owner cấu hình trusted publisher (evidence đã khai).
- `files.write_text` kiểm đuôi trên đường dẫn trước khi `resolve` symlink: một symlink `a.md` trong `founder/` trỏ tới `b.txt` cũng trong `founder/` sẽ ghi vào `b.txt`. Package không tạo symlink, rủi ro thấp, không có test; ghi để lane sau cân nhắc.
- `tests/conftest.py` và `tests/test_parity.py` nhập `anyio` trực tiếp trong khi nó chỉ có qua phụ thuộc bắc cầu của `mcp`/`httpx`; không là vi phạm chuẩn đã ghi, nhưng nhóm `dev` không khai.
- Evidence chưa ghi giấy phép của `mcp`, `httpx` (bảng "Dependency" của evidence-gates yêu cầu "license"); hai gói do thiết kế §5 chọn nên không chặn, nhưng nên ghi khi sửa evidence ở S1.

<promise>CHANGES_REQUESTED</promise>
