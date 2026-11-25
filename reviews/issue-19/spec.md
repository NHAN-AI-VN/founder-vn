Commit mã đã chấm: a65a6fd96e9e

# Review trục Spec, issue #19, vòng 2

**Phán quyết**: PASS

Phạm vi: `git log --oneline main..HEAD` (11 commit, thêm so với vòng 1: `9a0f538`, `0f422f3`, `8645bf8`, `a65a6fd`) và `git diff --stat main...HEAD` (README.md, docs/evidence/issue-19-wave-a-walkthrough.md, docs/hosts/README.md, docs/hosts/kiro.md, tests/test_front_door.py, tests/test_hosts.py, reviews/issue-19/*; không file mã hay skill nào đổi). Vòng 1 PASS ở `284a8ef`; vòng này kiểm lại phần đổi sau đó (`git diff 284a8ef..HEAD`): sửa S1 trong `docs/hosts/kiro.md`, một assertion mới trong `tests/test_hosts.py`, khối gate trong file bằng chứng, ledger. Không có thay đổi nào chạm hành vi hay mã.

## Đối chiếu từng criterion

1. **Clean-install walkthrough trên Kiro CLI, có ghi; lỗi chặn được sửa hoặc mở issue.** Đáp ứng. `docs/evidence/issue-19-wave-a-walkthrough.md` (bảng "Record (criterion 1)": lệnh, giờ, thời lượng, friction, issue). Ba friction mở thành #93, #94, #95. Test `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` và `test_issue_19_evidence_records_the_kiro_cli_run`. Tự chạy: `uv run pytest tests/test_hosts.py tests/test_front_door.py -q` cho 22 passed. Các test này nằm trong `tests/`, thuộc đoạn `unit` của cổng.
2. **`v0.2.0` tag, có trên PyPI, mọi skill 0.2.0, version check qua, lệch major dừng đúng thông điệp.** Đáp ứng. Tự kiểm lại: `git rev-parse 'v0.2.0^{commit}'` = `212f609c3865`; `pypi.org/pypi/founder-vn/json` trả `0.2.0`; sáu `skills/*/SKILL.md` đều `version: "0.2.0"`; `skill-lint` (đoạn `static`) 0 finding. Bản ghi bước 8 (sửa `founder-board` thành `1.0.0`, phiên Kiro CLI dừng ở bước 1 Protocol, khôi phục) vẫn nguyên. Sửa S1 làm `docs/hosts/kiro.md` nhất quán với việc 0.2.0 đã ở PyPI, có assertion cấm cụm "before the tag" (đỏ-xanh ghi trong bằng chứng).
3. **README status table: Kiro CLI full pipeline verified; host khác not yet verified.** Đáp ứng. `README.md`, `docs/hosts/README.md`; ghim bởi `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts`. Không đổi từ vòng 1.
4. **Known-issues cho Wave B mở thành issue.** Đáp ứng theo bản ghi (#93, #94, #95); xem mục "Chưa xác minh".

CI: run 45559444513 của `Gate` ở `a65a6fd96e9e` là `success` (kết quả do tin nhắn giao việc cung cấp).

## Artefact cho chủ hộ

Diff không thêm hay đổi artefact Owner-facing (không đụng `examples/`, `skills/`). Phần mới trong README và `docs/hosts/*` không có `$`. Không phát hiện tên người hay địa điểm dưới cấp quận.

## Chưa xác minh (không gắn mã, không chặn)

- Phiên Kiro CLI (bước 6.x, 8) và bước tag/publish do operator làm tay; reviewer không quan sát phiên, chỉ đối chiếu độc lập tag, PyPI, phiên bản skill.
- Sandbox không có credential tới GitHub API nên chưa mở được #93, #94, #95 để xác nhận tiêu đề và nội dung; criterion 4 dựa vào bản ghi của lane.
- "What to build" nói "ca mới" còn walkthrough dùng lại `idea.md` vàng của `examples/barbershop`; bản ghi nêu ở "Giới hạn". Bốn acceptance criterion không đòi "ca mới", nên không là finding chặn. Operator quyết nếu muốn coi là điều kiện.
- Thời lượng dựng từ mtime, đã khai trong bản ghi.

<promise>PASS</promise>
