Commit mã đã chấm: a17cb11084c2

# Review trục Spec, issue #89, vòng 1

Phạm vi: `git diff --stat origin/main...HEAD` (29 file, 6 commit: seam, version, install, readme, kiro-walkthrough, evidence). Không có finding chặn.

## Đối chiếu từng criterion

1. **Version lockstep 0.2.0: đáp ứng.** `__version__ = "0.2.0"`; `uv run founder-vn --version` in `founder-vn 0.2.0`; `tests/golden/version.json` và `tests/test_parity.py` xanh (351 passed khi chạy `uv run pytest tests -q`); cả sáu `skills/*/SKILL.md` đổi sang `0.2.0`; `python3 scripts/skill_lint.py` báo `6 skills checked, ... 0 finding(s) (package version 0.2.0)`. Witness `tests/test_skill_lint.py::test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version` chạy lại: `1 passed`, và được trích trong evidence.
2. **Lệnh MCP resolve: đáp ứng.** `src/founder_vn/install.py` (JSON Kiro, TOML Codex và Grok, dòng `claude mcp add`, chữ dashboard KiroCrew), `docs/hosts/README.md`, mọi `docs/hosts/<host>.md`, README hai ngôn ngữ, design §5 và mục Q53 (tiêu đề đổi Q1-Q53; `AGENTS.md` đổi theo) đều dùng `--from founder-vn founder-vn-mcp`. Grep toàn repo không còn `uvx founder-vn-mcp` ngoài evidence lịch sử của #2 và các câu phủ định trong test. Test cập nhật: `tests/test_hosts.py`, `tests/test_front_door.py`; `tests/golden/install_*.json` tái sinh (5 file), evidence nêu lý do là đổi đối số.
3. **README truth table: đáp ứng.** Mục Install nói 0.2.0 là bản PyPI đầu tiên, 0.1.0 chưa từng phát hành, đang chờ tag `v0.2.0`, không ghi "live" hay "verified". Bảng Status liệt kê sáu skill Wave A với số ticket và golden artefact trong `examples/barbershop/founder/` (link tồn tại), bốn skill Wave B "not started". Bảng host: Kiro CLI "full pipeline: pending walkthrough (#19)", năm host còn lại "not yet verified". Mục tiếng Việt nói cùng nội dung. Không host nào bị đánh dấu verified. Test `test_readme_truth_table_is_honest_about_release_status_and_hosts` thuộc cổng `unit`.
4. **`docs/hosts/kiro.md` và template #19: đáp ứng.** Mục "Clean-install walkthrough" có lệnh đánh số từ thư mục trống đến `founder/business-plan.md`, hai biến thể cài (wheel trước tag, `uvx --from founder-vn` sau tag), chỉ ghi ba tên `FOUNDER_LLM_*` (không có giá trị), sáu skill đúng thứ tự board → competitors → consumer → pricing → cfo → plan, bước kiểm tra major mismatch (đặt `1.0.0`, chạy, mong thông báo dừng của Protocol step 1, khôi phục), và bảng ghi (step | command | started | duration | friction | issue filed). Câu thông báo dừng khớp `skills/founder-board/SKILL.md` Protocol step 1; `founder-vn plan --check` tồn tại. `docs/evidence/issue-19-wave-a-walkthrough.md`: bốn tiêu chí #19 chưa tick, bảng rỗng, ghi rõ operator điền trên Kiro CLI thật, không khẳng định đã chạy.
5. **Cổng xanh và evidence: đáp ứng.** CI `Gate` run 45353282222 success ở `a17cb11084c2`. `docs/evidence/issue-89-release-0-2-0-prep.md` có bảng lát red-then-green (assertion đỏ trích dẫn, lệnh xanh), khối cổng ba đoạn (chấm ở `bb5078b`, commit sau chỉ là evidence), và mục Giới hạn nói đủ: không tag, không publish PyPI, không chạy walkthrough, không host nào verified.

## Giới hạn và điều ticket cấm: không vượt

Không đụng `release.yml`, không tạo CHANGELOG, không đổi hành vi skill (diff skill chỉ là dòng `metadata.version`), không tag, không publish. Các thay đổi ngoài danh sách địa điểm của ticket (`AGENTS.md` Q1-Q53, `docs/skill-conventions.md` ví dụ version) là hệ quả trực tiếp của Q53 và lockstep, không phải quyết định thiết kế mới.

## Chưa xác minh

- Lệnh `uvx --from founder-vn founder-vn-mcp` chạy thật với PyPI: chưa thể kiểm (chưa có gói); đã đo bởi operator ở Q53, evidence nói rõ.
- Phần walkthrough thuộc #19, nằm ngoài ticket này.

<promise>PASS</promise>
