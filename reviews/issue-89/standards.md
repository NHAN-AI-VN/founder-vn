Commit mã đã chấm: a17cb11084c2

# Review trục Standards, issue #89, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD` (29 file) và `git log --oneline main..HEAD` (6 commit: `seam:`, 4 `slice(`, 1 `docs:`). Đối chiếu với `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (§5 và Q53), `docs/evidence/issue-89-release-0-2-0-prep.md`.

- Mã: `src/founder_vn/__init__.py` (0.1.0 thành 0.2.0) và `src/founder_vn/install.py` (đối số `uvx` thành `--from founder-vn founder-vn-mcp`). Không thêm phép tính, không ghi file mới, không thêm hằng số thuế hay ngưỡng. Installer là CLI-only theo `standards.md` (Shape of the code), nên không cần parity test.
- Test: `tests/test_front_door.py`, `tests/test_hosts.py`, 6 golden (`install_*.json`, `version.json`). Không test nào gọi mạng. Test chỉ kiểm chuỗi trong file và đầu ra của CLI.
- Skill: 6 `skills/*/SKILL.md` chỉ đổi `metadata.version` thành 0.2.0, khớp phiên bản package. `python3 scripts/skill_lint.py` cho `6 skills checked, 15 example file(s), 0 finding(s) (package version 0.2.0)`. Diff không chạm `examples/`, nên các mục còn lại của checklist skill không bị chạm.
- Tài liệu: README (bảng trạng thái và bảng host), `docs/hosts/*`, `docs/skill-conventions.md`, `docs/founder-vn-design.md`, `AGENTS.md`.

## Hình dạng vòng lặp

- (a) Commit `a746682 seam:` mang mục `## Seam` và đứng trước cả bốn commit `slice(`.
- (b) Hai commit chạm `src/` là `45b21c1` (đã chạm test golden, `test_parity`, `test_skill_lint` theo evidence) và `1e4d375` (`tests/test_hosts.py`, `tests/test_front_door.py`, 5 golden). Cả hai có dòng trong `## Lát`.
- (c) Test nằm ở seam đã khai (`founder-vn version`, `install --print-only`, text của README và host page). Không có test vào internals.
- (d) Khối `## Cổng ba đoạn` ghi `verify` GREEN ở `bb5078baa438`. Đó là commit cuối chạm mã hoặc test. `a17cb11` chỉ thêm file evidence. Cổng CI `Gate` ở `a17cb11084c2` cho `success`.
- Golden đổi (`install_*.json`, `version.json`): commit message `45b21c1` và `1e4d375` cùng mục "golden files changed" trong evidence đều giải thích lý do (đổi `uvx` args, lên 0.2.0).

## Ghi chú không chặn

- `docs/founder-vn-design.md` thêm Q53 và sửa §5. Đây là quyết định của operator (Q53 ghi rõ), kèm số đo, và đổi cùng thay đổi code theo `AGENTS.md` ("the design wins and the fix lands in the same change"). Đó không phải quyết định thiết kế mới do lane tự đặt.
- `README.md` và `src/founder_vn/__init__.py` là file một-chủ (`parallel-lanes.md`). Với `HARNESS_WIP=1` dispatcher cấp `all`, nên không vi phạm.
- Còn một chuỗi `uvx founder-vn-mcp` trong `tests/test_hosts.py:79`, dùng làm khẳng định phủ định, và trong Q53 làm ví dụ sai. Cả hai đúng ý.

## Chưa xác minh

- Không chạy lại `gate-segment.sh verify` ở sandbox này vì `.harness/gate-segments.txt` không được commit. Tôi dựa vào khối cổng trong evidence và kết quả CI `Gate` (run 45353282222, success).
- Walkthrough #19 và lệnh `uvx --from` thật trên PyPI nằm ngoài phạm vi (evidence mục `## Giới hạn` đã khai).

<promise>PASS</promise>
