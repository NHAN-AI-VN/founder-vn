Commit mã đã chấm: 284a8efcdced

# Review trục Spec, issue #19, vòng 1

**Phán quyết**: PASS

Phạm vi: `git log --oneline main..HEAD` (6 commit: `20788c7`, `43c6553`, `e625d2b`, `d5f66dc`, `c8cfaf8`, `284a8ef`) và `git diff --stat main...HEAD` (README.md, docs/evidence/issue-19-wave-a-walkthrough.md, docs/hosts/README.md, docs/hosts/kiro.md, tests/test_front_door.py, tests/test_hosts.py; không file mã hay skill nào đổi). Điều ticket yêu cầu: bốn acceptance criterion, cộng "What to build" (từ dự án trống, cài, cấu hình mô hình, chạy sáu skill Wave A trên một ca mới tới `business-plan.md`, 0.2.0 skill và package đồng bộ).

## Đối chiếu từng criterion

1. **Clean-install walkthrough trên Kiro CLI, có ghi (lệnh, thời gian, friction); lỗi chặn được sửa hoặc mở issue.** Đáp ứng. Bằng chứng: `docs/evidence/issue-19-wave-a-walkthrough.md`, mục "Record (criterion 1)" có bảng 13 dòng (bước 1 đến 8, một dòng mỗi skill) với cột lệnh, giờ bắt đầu, thời lượng, friction, issue đã mở. Thời gian được dựng lại từ mtime file và tài liệu nói rõ điều đó ở "Giới hạn". Không có lỗi chặn; ba friction mở thành #93, #94, #95; thứ tự cfo trước pricing được sửa trong `docs/hosts/kiro.md` (`43c6553`) và có test đỏ-xanh `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19`. Test thuộc `tests/`, chạy trong đoạn `unit` của cổng (CI Gate `success` ở `284a8efcdced`; bằng chứng ghi `351 passed`).
2. **`v0.2.0` được tag và có trên PyPI; mọi skill có `metadata.version` 0.2.0; version check qua; lệch major thì skill dừng đúng thông điệp.** Đáp ứng. Đã tự kiểm: `git rev-parse v0.2.0^{commit}` = `212f609c3865` (khớp bản ghi release); `https://pypi.org/pypi/founder-vn/json` trả `version 0.2.0` với wheel và sdist; sáu `skills/*/SKILL.md` đều `version: "0.2.0"` (`scripts/skill_lint.py` trong đoạn `static` giữ chúng bằng `__version__`, "0 finding(s)"). Bước 8 trong bản ghi: sửa `founder-board` thành `1.0.0`, phiên Kiro CLI dừng ở bước 1 Protocol với câu "Tôi dừng ở bước 1 của Protocol vì phiên bản bị lệch số major…", rồi khôi phục. Protocol step 1 của skill chỉ yêu cầu "stop and tell the Facilitator to update the package or the skill" nên thông điệp này khớp; thiết kế (Q45, dòng 83) chỉ đòi dừng cảnh báo khi lệch major.
3. **README status table: Kiro CLI full pipeline verified; host khác "not yet verified".** Đáp ứng. `README.md` (bảng host: Kiro CLI "full pipeline verified on 0.2.0…", năm host còn lại "not yet verified"), phần tiếng Việt ("đã xác nhận" cho Kiro, "chưa xác nhận" cho host khác), `docs/hosts/README.md`. Được ghim bởi `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (kiểm từng host, chạy trong cổng `unit`).
4. **Danh sách known-issues cho Wave B mở thành issue.** Đáp ứng theo bản ghi: #93 (`founder-consumer` không ghi `consumer.md`), #94 (installer chỉ in `mcp.json`), #95 (`results.md` của `panel tally` thiếu dòng miễn trừ). Xem mục "Chưa xác minh" về việc kiểm tracker.

## Artefact cho chủ hộ

Diff không thêm hay đổi artefact Owner-facing nào (không đụng `examples/`, `skills/`). Bản ghi báo đã chạy checklist trên đầu ra thật của walkthrough (không `$`, miễn trừ, cảnh báo "mô phỏng, cận trên", link Công báo kèm ngày) và nói thẳng chỗ hụt (#95). Walkthrough folder nằm ngoài git; bằng chứng không trích tên đối thủ hay persona. `README.md` và `docs/hosts/*` không có `$` trong phần Owner-facing mới thêm.

## Chưa xác minh (không gắn mã, không chặn)

- Phần chạy trong phiên Kiro CLI (bước 6.x, 8) và bước tag/publish do operator thực hiện bằng tay; reviewer không quan sát phiên. Đã đối chiếu độc lập: tag, PyPI, phiên bản skill. Câu dừng ở bước 8 chỉ có dạng trích của operator, đã bị cắt.
- Sandbox này không có credential tới GitHub API nên chưa mở được #93, #94, #95 để xác nhận tiêu đề và nội dung; criterion 4 dựa vào bản ghi của lane và sự thừa nhận của operator.
- Mục "What to build" nói "ca mới", còn walkthrough dùng lại `idea.md` vàng của `examples/barbershop`. Bản ghi nêu rõ điều này ở "Giới hạn" (khảo sát đối thủ, panel 20 persona, đầu vào CFO và mọi báo cáo được tạo mới trong phiên; ca đầu tiên không phải ca vàng là P01 của T19 #20). Bốn acceptance criterion không đòi "ca mới", nên không coi là finding chặn. Nếu operator muốn coi đây là điều kiện, cần đánh dấu lại; reviewer không tự quyết.
- Thời lượng không đo bằng đồng hồ; dựng từ mtime, đã khai trong bản ghi.

<promise>PASS</promise>
