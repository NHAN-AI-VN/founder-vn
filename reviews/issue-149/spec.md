Commit mã đã chấm: 42bb26bdd28b

# Review trục Spec, issue #149, vòng 1

Phạm vi: `git log --oneline main..HEAD` (105b81f, 67218ff, 42bb26b) và `git diff --stat main...HEAD` (README.md, docs/hosts/README.md, docs/hosts/kiro.md, docs/evidence/issue-149-release-0-3-1.md, tests/test_front_door.py, tests/test_hosts.py). Không có thay đổi `src/` hay `skills/`. Bước 1 (lockstep 0.3.1) đã vào `main` qua #163/PR #164 (`c5c5ef7`), ngoài diff của lane.

**Phán quyết: PASS.** Không có finding chặn.

## Đối chiếu từng criterion

1. **PyPI báo 0.3.1, sha256 wheel PyPI bằng bản build cục bộ.** Đạt. Tôi tự chạy `curl -s https://pypi.org/pypi/founder-vn/json`: `info.version` = 0.3.1; wheel `3df5d062da868e65…a2142` (upload 2026-11-27T09:55:52Z), sdist `cad85221…ce452`. Khớp số trong `docs/evidence/issue-149-release-0-3-1.md` (mục "Release record"). Tag chú thích `v0.3.1` có trên origin (`bb5ee92`), trỏ tới `c5c5ef7`, khớp bằng chứng. Sha256 của bản build cục bộ chỉ có trong file bằng chứng (xem mục chưa xác minh).
2. **Cài sạch từ PyPI ghi `permits/sources.md`, byte-identical với file ở commit đã tag.** Đạt. Tôi tải wheel 0.3.1 từ PyPI: sha256 bắt đầu `3df5d062da868e65`, `founder_vn/permits/sources.md` trong wheel `cmp` giống hệt `git show v0.3.1:permits/sources.md` (sha256 `87054ae4…`). File bằng chứng ghi 14 dòng `create` (12 file skill, `permits/sources.md`, `.kiro/settings/mcp.json`) cho cả bản chạy thử trên wheel cục bộ lẫn bản chạy từ PyPI, khớp cách đếm của ticket.
3. **`permits.md` và `cfo.md` của lần cài sạch qua hai kiểm tra pháp lý.** Đạt theo bằng chứng đã ghi, đúng hình thức ticket cho phép (tên file và loại kết quả, thư mục ngoài git): `check_permits_links_dated` PASS (21 link Công báo, 21 có ngày), kiểm tra legal-claim của `tests/test_wave_a_checklist.py` PASS, có mục "Giới hạn của phần thuế" với 4 link có ngày. Giới hạn đã được nêu thật: Step 3 bị chặn thời gian nên 13 dòng ghi "chưa xác nhận lại hôm nay" và không bỏ số nào; phiên Kiro CLI lồng nhau, câu trả lời của Owner đưa sẵn trong prompt.
4. **Front door nói 0.3.1 là bản hiện hành, gọi tên #142 đã sửa; `tests/test_front_door.py` và `tests/test_hosts.py` pin điều đó.** Đạt. Đọc diff của `README.md` (bảng Install, hàng `founder-permits`, hàng Kiro CLI, phần tiếng Việt), `docs/hosts/README.md`, `docs/hosts/kiro.md`: đều nói 0.3.1 hiện hành (phát hành 2026-11-27), #142 sửa trong 0.3.1, bỏ câu "chờ tag". Hàng Kiro CLI giữ "verified on 0.3.0 (walkthrough, #118)" và không tuyên bố "verified on 0.3.1", đúng vì ticket chỉ chạy lại hai skill. Tôi chạy `uv run pytest tests/test_front_door.py tests/test_hosts.py -q`: 27 passed. Hai file test thuộc cổng `unit`; bằng chứng ghi đỏ trước (2 failed, 25 passed) rồi xanh. `uv run python scripts/skill_lint.py`: 10 skill, 0 finding, package version 0.3.1. CI `Gate` ở `42bb26bdd28b` success (theo tin nhắn mở đầu).

## Các bước của ticket

- Bước 1 lockstep: `__version__` = "0.3.1", 10 skill `version: "0.3.1"`; do #163 làm, ngoài lane này.
- Bước 2 tag và publish, bước 3 cài sạch, bước 4 chạy lại: có bản ghi trong `docs/evidence/issue-149-release-0-3-1.md` (giờ UTC, run 45977671164, phê duyệt môi trường `pypi`). Lane tag và phê duyệt bằng tài khoản `gh` của operator sau lời "go" của operator trong phiên; file bằng chứng nêu điều này trong mục "Giới hạn".
- Bước 5: bằng chứng ở đúng tên `docs/evidence/issue-149-release-0-3-1.md`.
- Không có hành vi ngoài phạm vi: không sửa skill, `release.yml`, nội dung ledger. Không có `$` cạnh số, không có tên người hay địa điểm dưới cấp quận trong diff. `permits.md` và `cfo.md` cố ý không commit (thiết kế §5, Q56), nên không có artefact Owner-facing mới trong diff để đọc.

## Chưa xác minh

- Sha256 của `uv build` cục bộ tại `c5c5ef7` và các lần chạy `uvx` trên máy operator: chỉ có trong file bằng chứng; tôi xác nhận phía PyPI và ledger, không dựng lại bản build cục bộ.
- Nội dung `permits.md` và `cfo.md` nằm ngoài git, tôi không đọc được; kết quả hai kiểm tra là lời ghi trong file bằng chứng.
- Lệnh cài đặt của host Kiro tôi không chạy trực tiếp trong sandbox này (công cụ shell chặn lệnh có cờ chọn host); thay bằng đối chiếu wheel.

<promise>PASS</promise>
