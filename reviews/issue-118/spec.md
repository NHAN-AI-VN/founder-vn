Commit mã đã chấm: 6925fe575468

# Review trục Spec: #118, vòng 1 (lượt sau SPEC-1)

Phạm vi: `git diff --stat origin/main...HEAD` (README.md, docs/hosts/README.md, docs/hosts/kiro.md, docs/evidence/issue-118-wave-b-walkthrough.md thay template `issue-#118-...`, tests/test_front_door.py, tests/test_hosts.py, cùng file review) và `git log --oneline origin/main..HEAD` (14 commit, gồm 2424508, ea77918, 6925fe5 sau báo cáo BLOCKED bb4a728). Gate của CI ở `6925fe575468`: success (run 45955604010, từ tin nhắn mở đầu). Tôi chạy lại `uv run pytest tests/test_front_door.py tests/test_hosts.py -q`: 24 passed. Tôi không quan sát phiên Kiro CLI, PyPI hay GitHub Actions; những phần ấy đọc từ bản ghi.

## Đối chiếu từng criterion

1. Comment cấp phát: bản ghi trích comment 2026-11-26T07:17:12Z (`README.md`, `lane/issue-118`, `main`). Không có credential tới tracker nên tôi không đọc được comment (xem "Chưa xác minh").
2. Dry run, tag, publish, `uvx --no-cache`: mục "Release record" có lệnh, giờ UTC, sha256 của wheel/sdist trên PyPI trùng bản build dry run, run 45776129259, `founder-vn 0.3.0`. Bằng chứng là bản ghi của operator; không test nào chạm PyPI (đúng bản chất ticket). Đã đáp ứng theo bản ghi.
3. Walkthrough Kiro CLI: `docs/evidence/issue-118-wave-b-walkthrough.md` có bảng bước với lệnh, giờ bắt đầu, thời lượng, friction, issue (#142, #143, #144), nêu rõ giờ dựng lại từ mtime, chỉ ghi tên model, ý tưởng là golden, không nội dung ca ngoài golden, `plan --check` exit 0. Test `test_issue_118_evidence_records_the_kiro_cli_run` ghim hình dạng bản ghi và chạy trong cổng `unit`. Đã đáp ứng.
4. Major mismatch (SPEC-1 của vòng trước): đã đóng. Bản ghi mục "Major-mismatch check" quan sát trên 0.3.0 ngày 2026-11-27: `founder-launch` đặt `1.0.0`, `server_info` trả `founder-vn 0.3.0`, skill dừng ở Protocol step 1, không ghi file, trích nguyên văn thông báo dừng, khôi phục sha256 `e8908d4ec871…` bằng `skills/founder-launch/SKILL.md` ở `ca6bc9f`. Lần chạy 1 bị từ chối tool nên bản ghi tự nhận không phải quan sát; lần 2 mới là quan sát. Giới hạn đã ghi (session lồng, `--trust-all-tools`, khoá ghi do lane đặt, không chạy lại skill sau khôi phục) không làm mất điều ticket đòi: một skill Wave B ở `1.0.0`, chạy, trích thông báo, khôi phục. Đã đáp ứng.
5. README, `docs/hosts/README.md`, `tests/test_front_door.py`: README Install nói 0.3.0 là bản hiện hành, tag `v0.3.0` ngày 2026-11-26; hàng Kiro CLI ghi đúng cụm "full pipeline incl. Wave B verified on 0.3.0 (walkthrough 2026-11-26, #118)" kèm #142 và mismatch trên 0.3.0; `docs/hosts/README.md` tương tự; bản tiếng Việt cập nhật; test sửa tương ứng và xanh. README sửa bằng `HARNESS_SINGLE_OWNER_FILES=README.md` và một patch tay (ea77918), cả hai đường ticket cho phép; README nằm trong cấp phát. Đã đáp ứng.
6. Friction thành issue: #142, #143, #144, #148, mỗi cái nêu tên skill hoặc tool. #142 chặn cho số liệu pháp lý đã kiểm chứng; ticket cho phép "sửa (0.3.1) hoặc nêu issue trước khi đóng", và README nêu #142 cạnh khẳng định "verified". Đã đáp ứng.
7. PR qua `open-lane-pr.sh`: chưa mở theo thiết kế của lane (bản ghi để ô này trống đến sau review); không phải finding.

## Ngoài phạm vi ticket
Không thấy hành vi vượt phạm vi: không sửa mã, không file ngoài README và docs/test liên quan. Đổi tên file template `issue-#118-...` thành `issue-118-...` được giải thích (tên có `#` không khớp `docs/evidence/issue-<n>-*.md`) và khớp tên criterion 3 đòi.

## Chưa xác minh (không gắn mã)
- Comment cấp phát trên #118 và thân các issue #142/#143/#144/#148 tồn tại đúng như bản ghi: không có credential tới tracker.
- Các số liệu release (run 45776129259, hash PyPI, giờ) và nội dung phiên Kiro CLI: chỉ đọc bản ghi của operator.
- Thông báo dừng bằng tiếng Anh (#148) lệch với lần #19 bằng tiếng Việt; ticket không yêu cầu ngôn ngữ, nên không chặn. Operator xử lý #148.

<promise>PASS</promise>
