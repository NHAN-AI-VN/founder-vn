Commit mã đã chấm: f2459a7a7a5f

# Review trục Spec, issue #117, vòng 1

Phạm vi: `git diff --stat origin/main...HEAD` (21 file, 7 commit). Cổng `Gate` của run 45771480069 xanh. Tôi chạy lại tại HEAD: `python3 scripts/skill_lint.py` cho `10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.0)`; `uv run pytest tests -q` cho `464 passed`; `founder-vn plan --check` trong `examples/barbershop` cho `business-plan.md khớp với các file hiện có`.

**Phán quyết: PASS.** Không có finding chặn.

## Đối chiếu từng criterion

1. **Lockstep 0.3.0**: đạt. `src/founder_vn/__init__.py` có `__version__ = "0.3.0"`; `tests/golden/version.json` là `founder-vn 0.3.0`; `tests/test_parity.py::test_cli_version_equals_mcp_server_info` (CLI và MCP `server_info`) nằm trong `pytest` của cổng unit; cả mười `skills/*/SKILL.md` có `version: "0.3.0"` (đã grep); `skill_lint` pass. Witness lockstep (`test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version`) được trích đỏ rồi xanh trong `docs/evidence/issue-117-release-0-3-0-prep.md`, hàng "lockstep witness".
2. **Wave B checklist**: đạt. `tests/test_wave_b_checklist.py` ghim `permits/ops/marketing/launch.md`: có file, không `$`, có miễn trừ, cảnh báo panel ở `marketing.md` và `launch.md` (hai file duy nhất có "panel"; `permits.md`, `ops.md` không trích số panel), mọi dòng `congbao.chinhphu.vn` trong `permits.md` có ngày, và `## Chưa làm` của `business-plan.md` đúng hai dòng. Việc `business-plan.md` là output của compiler được `tests/test_plan_example.py` (`compile_plan` và `run(check=True)`) ghim, và tôi chạy `plan --check` xanh. Mỗi check có test đột biến trên bản copy ở `tmp_path` (`test_each_check_goes_red_on_its_mutation`), nên check thật sự đỏ khi bị phá.
3. **README truth table**: đạt. Install nói 0.3.0 "pending the `v0.3.0` tag", 0.2.0 vẫn là bản đã phát hành, không có chữ released/verified cho 0.3.0. Bảng Status liệt kê mười skill kèm số ticket và artefact. Hàng Kiro CLI giữ nguyên "full pipeline verified on 0.2.0 (walkthrough 2026-11-25, #19)" và thêm "Wave B: pending walkthrough (#118)"; các host khác "not yet verified". Phần tiếng Việt phản chiếu. `docs/hosts/README.md` cùng ý. `tests/test_front_door.py` cập nhật trong cùng lát.
4. **`docs/hosts/kiro.md`**: đạt. Bước 7 mới sau bước 6 theo đúng thứ tự permits, ops, marketing, launch, plan lại, `founder-vn plan --check`; `tests/test_hosts.py` ghim thứ tự và việc bước kiểm tra major-mismatch đứng sau. `docs/evidence/issue-#118-wave-b-walkthrough.md` là template: 7 ô chưa tick, bảng record rỗng, câu "operator fills it on a real Kiro CLI", không khẳng định đã chạy; `test_issue_118_template_has_unticked_boxes_and_claims_no_run` ghim điều này.
5. **Gate và evidence**: đạt. `docs/evidence/issue-117-release-0-3-0-prep.md` có các lát đỏ rồi xanh, ba đoạn cổng, và mục "Giới hạn" nêu không tag, không publish PyPI, không chạy walkthrough, không host nào được xác nhận cho Wave B. Tên file theo ticket (`issue-<n>-release-0-3-0-prep.md`).

Giới hạn và ngoài phạm vi: không thấy thay đổi `release.yml`, không tag, không hành vi skill nào đổi (diff của `skills/` chỉ là dòng version).

## Ghi nhận, không chặn

- Bước major-mismatch giữ nội dung nhưng đánh số lại thành bước 9, và câu khôi phục đổi từ `0.2.0` sang `0.3.0`. Ticket nói "unchanged"; thay đổi này là hệ quả bắt buộc của việc bump (khôi phục về 0.2.0 sẽ sai) và evidence đã ghi lý do. Tôi coi là đúng tinh thần ticket.
- Đã sửa thêm `docs/skill-conventions.md` (ví dụ version 0.3.0), ngoài danh sách ticket nhưng cùng một lockstep, không đổi hành vi.

## Chưa xác minh

- Nội dung pháp lý và số liệu trong `permits.md`: tôi không kiểm chứng lại nguồn Công báo; ticket này chỉ yêu cầu check có link kèm ngày, và các file đó đã có từ ticket Wave B trước.
- Không có truy cập API GitHub nên không đối chiếu độc lập với ticket #118 (template chép tiêu chí từ thân #118).

<promise>PASS</promise>
