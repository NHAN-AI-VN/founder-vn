Commit mã đã chấm: e7ec97e9d86e

# Review trục Spec: #118, vòng 1

Phạm vi: `git diff --stat main...HEAD` (7 file: `README.md`, `docs/hosts/README.md`, `docs/hosts/kiro.md`, `docs/evidence/issue-118-wave-b-walkthrough.md` thay cho template `issue-#118-...`, `tests/test_front_door.py`, `tests/test_hosts.py`) và 8 commit của `main..HEAD`. Gate của CI ở `e7ec97e9d86e`: success. Tôi không chạy lại test; không quan sát phiên Kiro CLI hay PyPI, chỉ đọc bản ghi.

## Đối chiếu từng criterion

| # | Criterion | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | Comment cấp phát | Đáp ứng (chưa xác minh được ở đây) | Bản ghi nêu comment 2026-11-26T07:17:12Z; tôi không có credential tới tracker. |
| 2 | Dry run wheel, tag `v0.3.0`, Build xanh, Publish được duyệt, `uvx` ra `founder-vn 0.3.0` | Đáp ứng | Bảng "Release record": run 45776129259, sha256 wheel/sdist của dry run trùng bản trên PyPI, `founder-vn 0.3.0` từ PyPI. Ngoài repo (PyPI, Actions), nên nằm trong mục "chưa xác minh". |
| 3 | Walkthrough Kiro CLI, ghi vào `docs/evidence/issue-118-wave-b-walkthrough.md` | Đáp ứng, có ghi lệch kịch bản | Bảng bản ghi có lệnh, giờ bắt đầu, thời lượng (dựng lại từ mtime, nói rõ), friction, issue (#142, #143, #144); chỉ ghi tên mô hình; `plan --check` exit 0. Ca là golden idea, ticket cho phép. |
| 4 | Major mismatch vẫn dừng skill | **Chưa đáp ứng** | Xem SPEC-1. |
| 5 | README, `docs/hosts/README.md`, `tests/test_front_door.py`, áp bằng `HARNESS_SINGLE_OWNER_FILES=README.md` | Đáp ứng về chữ, xem SPEC-1 về độ trung thực | Diff README (Install 0.3.0, tag 2026-11-26; hàng Kiro CLI đúng câu ticket) và host index; test cập nhật, Gate xanh. |
| 6 | Mỗi friction/defect thành issue; defect chặn được sửa hoặc nêu trước khi đóng | Đáp ứng | #142, #143, #144; #142 chặn số liệu pháp lý, nêu tên cạnh tuyên bố "verified" trong README. Nội dung issue chưa đọc được. |
| 7 | PR qua `open-lane-pr.sh` | Chưa đến bước; harness mở sau review | Bản ghi nói PR mở sau khi commit bản ghi. |

Artefact cho chủ hộ: diff không chứa `cfo.md`, `pricing.md` hay `examples/` mới. Bản ghi chỉ trích nội dung trong phiên, ngoài git. Tôi không đánh giá nội dung đó.

## Finding chặn

### SPEC-1: Criterion 4 (major mismatch dừng skill) chưa được quan sát trên 0.3.0, nhưng ticket vẫn được coi là đủ

- Criterion: "The deliberate major mismatch still stops a skill (one Wave B skill set to `1.0.0`, run, stop message quoted, restored)".
- Thiếu gì: bản ghi tự ghi `[ ] ... skipped by the operator ("bỏ qua")`, "Criterion 4 is not met", bước 9 "not run". Phần "Major-mismatch check" chỉ đưa sha256 của khối `## Protocol` trùng nhau giữa 10 skill và 0.2.0. Chính bản ghi nói đó không phải quan sát, vì một lần chạy skill là mô hình làm theo văn bản. Không có test nào chạy điều này, đúng như ticket nói ("the steps #19 showed a sandbox lane cannot do").
- Vì sao chặn: criterion là điều kiện của ticket. Một lời "bỏ qua" trong phiên chat không sửa được ticket. Cổng chứng cứ coi criterion chỉ được đáp ứng bằng bằng chứng thật, không bằng lời tuyên bố hay suy luận. Hệ quả đi tiếp: hàng Kiro CLI trong README và `docs/hosts/README.md` nói "full pipeline incl. Wave B verified on 0.3.0" trong khi một phần của việc xác minh bị bỏ. README có chú thích "major-mismatch stop ... not rerun on 0.3.0", nhưng `docs/hosts/README.md` ghi "verified end to end on 0.3.0" mà không có chú thích đó.
- Lane không tự sửa được: cần một phiên Kiro CLI thật do operator chạy (đặt `metadata.version: "1.0.0"` ở một skill Wave B, chạy, trích thông báo dừng, khôi phục). Operator cũng có thể sửa criterion 4 trên ticket. Cả hai đều là quyết định hoặc việc của operator, nên đây là BLOCKED chứ không phải CHANGES_REQUESTED.

## Câu hỏi cho operator

- [ ] Criterion 4: operator chạy kiểm tra major mismatch trên 0.3.0 (một skill Wave B đặt `1.0.0`, trích thông báo dừng, khôi phục, ghi vào mục "Major-mismatch check" và tick criterion 4 trong bản ghi), hay sửa ticket #118 để bỏ/hoãn criterion 4 (kèm issue theo dõi)?
- [ ] Nếu criterion 4 được hoãn: có đồng ý hàng Kiro CLI của `docs/hosts/README.md` nêu rõ "major-mismatch stop chưa chạy lại trên 0.3.0" như README gốc đã làm không? (Đây là sửa văn bản của lane sau khi có quyết định, không phải việc của vòng này.)

## Chưa xác minh

- Comment cấp phát trên #118, nội dung issue #142 #143 #144 và trạng thái nhãn của chúng (không có credential tới tracker).
- Release run 45776129259, các sha256 trên PyPI, tag `v0.3.0` và môi trường `pypi`: bản ghi không kiểm tra lại được từ sandbox này. Tôi dùng `git` và đọc diff; PyPI mở nhưng tôi không truy vấn, vì vòng này chấm bản ghi chứ không chấm lại bản phát hành.
- Các số đo walkthrough (giờ, thời lượng) dựng lại từ mtime, như bản ghi tự nhận.
- Chất lượng artefact của walkthrough (`cfo.md`, `pricing.md`, ...) nằm ngoài git; mục "Review-checklist walk" tự ghi vài lỗi (#142, #144) và tôi không đọc được file gốc.

<promise>BLOCKED</promise>
