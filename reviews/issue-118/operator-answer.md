# Trả lời của operator — review #118, vòng 1

Trả lời cho `reviews/issue-118/spec.md` (BLOCKED, commit mã đã chấm `e7ec97e9d86e`), mục "Câu hỏi cho operator". File này không phải báo cáo review; nó là đầu vào cho vòng review kế. Lượt Standards vòng 1 đã PASS ở cùng commit mã.

## SPEC-1: criterion 4 (major mismatch dừng skill) chưa được quan sát trên 0.3.0

- [x] Operator chọn **chạy kiểm tra**, không hoãn. Ngày 2026-11-27, trong session Kiro CLI của operator (`founder-guarded`), lane đặt `.kiro/skills/founder-launch/SKILL.md` của thư mục walkthrough thành `version: "1.0.0"`, chạy `founder-launch` trong một session Kiro CLI lồng (`kiro-cli chat --no-interactive --trust-workspace --trust-all-tools --model claude-opus-5.5 "founder-launch"`, `founder/` khoá ghi bằng `chmod a-w` trong lúc chạy). Skill dừng ở Protocol step 1 sau khi `server_info` trả `founder-vn 0.3.0`, không ghi file; stop message trích nguyên văn; file khôi phục byte-identical (sha256 `e8908d4ec871…`, bằng `skills/founder-launch/SKILL.md` ở `ca6bc9f`); `founder/` không đổi (86 file, nội dung, mtime, mode). Ghi ở mục "Major-mismatch check (criterion 4)" của `docs/evidence/issue-118-wave-b-walkthrough.md`; criterion 4 đã tick (commit `2424508`).
- [ ] Hoãn criterion 4 và sửa ticket: không chọn.
- [x] Câu hỏi thứ hai (chú thích "chưa chạy lại trên 0.3.0" cho `docs/hosts/README.md`) không còn áp dụng: hàng Kiro CLI của `README.md` nay ghi "major-mismatch stop observed on 0.2.0 (#19) and on 0.3.0 (2026-11-27, #118)" (commit `ea77918`; patch `.harness/readme-criterion4.patch` do operator apply tay vì guard từ chối session sửa file một-chủ khi `HARNESS_SINGLE_OWNER_FILES` không được export, cùng khe hở #5 và #19 đã ghi), và `docs/hosts/kiro.md` dòng 45 nói bước 9 chạy trên 0.2.0 (#19) và 0.3.0 (#118).

Friction của lần chạy: stop message bằng tiếng Anh, trong khi lần #19 trên 0.2.0 là tiếng Việt; khối `## Protocol` chung của mười skill không quy định ngôn ngữ → issue #148 (`needs-triage`, ba phương án cho operator). Lượt đầu với `--trust-tools=fs_read,@founder-vn/server_info` không phải quan sát: Kiro CLI 2.37.1 không nhận dạng `@server/tool` trong `--trust-tools` nên từ chối mọi tool cần duyệt; đó là giới hạn của Kiro CLI, không phải của skill hay tool founder-vn, ghi trong bản ghi, không lập issue. Giới hạn của cách quan sát (session lồng, không tương tác, `--trust-all-tools`, khoá ghi là của lane, không chạy lại skill sau khôi phục) ghi ở mục Giới hạn của bản ghi.

## Ledger

`reviews/issue-118/ledger.md` được ghi trong cùng commit này: SPEC-1 là mã finding duy nhất của mọi vòng tới nay, nó đóng bằng việc operator làm chứ không bằng lượt sửa của harness, và merger đòi ledger cho mọi mã từng được nêu (kể cả trong phiên bản báo cáo trước) nên không thể để trống. Lượt sửa, nếu có vòng sau, ghi lại toàn bộ file với đủ mã của mọi vòng.
