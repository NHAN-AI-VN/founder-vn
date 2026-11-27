Commit mã đã chấm: a344811d6e2e (mã không đổi từ 7cb6894; HEAD 519bbc503abc chỉ thêm ledger)

# Review trục Spec, #143, vòng 2

Phán quyết: PASS

## Phạm vi

`git diff --stat origin/main...HEAD` (13 file) và `git log --oneline main..HEAD`. Từ vòng 1 (ffa4b0f) lane thêm commit mã `7cb6894` đã có sẵn trước vòng 1; các commit sau chỉ đổi `docs/evidence/` và `reviews/` (`git diff 7cb6894 HEAD --stat -- src tests skills` rỗng), nên mã đã chấm ở vòng 1 và vòng 2 là một. Đã chạy lại ở HEAD: `uv run pytest -q` = 492 passed; `uv run python scripts/skill_lint.py` = 0 finding. CI `Gate` run 45963777397 success.

## Đối chiếu từng criterion

| Criterion | Bằng chứng |
|---|---|
| Có answers, cùng customer/n/seed, pitch khác: từ chối, file byte-identical, CLI exit 2, stderr nêu `founder/panel/answers/`, số câu trả lời, việc cất đi | `src/founder_vn/panel.py` `_refuse_other_deal` gọi trước mọi `write_text` trong `init`; `tests/test_panel_cli.py::test_init_refuses_a_changed_pitch_over_answers` (so snapshot byte của cả `founder/`, exit 2, bốn chuỗi trong stderr) |
| Pitch cũ, seed khác hoặc n khác: từ chối | `test_init_refuses_other_seed_or_other_n_over_answers` |
| Y hệt customer, pitch, n, seed: qua, stdout `Đã chia …`, file cùng nội dung | `test_init_of_an_identical_deal_passes_over_answers` (stdout chính xác, snapshot không đổi) |
| Không có hoặc rỗng `answers/`: qua như cũ; test init cũ và golden `panel_tally` xanh | `test_init_proceeds_without_answers_or_over_an_empty_answers_folder`; `git diff` không chạm `tests/golden/`; 492 test xanh |
| Có answers mà `panel.json` hoặc `personas.json` thiếu/hỏng: từ chối cùng chỉ dẫn | 4 tham số của `test_init_refuses_when_answers_exist_and_the_panel_on_disk_is_unreadable`; guard bắt `OSError, ValueError, KeyError, TypeError` |
| Tái hiện của ticket dừng ở lệnh thứ ba, `panel check` sau đó còn P002, P003 | `test_issue_143_reproduction_stops_at_the_third_command` |
| MCP `panel_init` trả lỗi tool, test quan sát `is_error` và text, không dùng fixture `mcp_call` | `tests/test_panel_parity.py::test_panel_init_refusal_is_the_same_text_through_cli_and_mcp` chạy server stdio thật, khẳng định `is_error`, văn bản và file không đổi; `src/founder_vn/server.py` bọc `PanelError` thành `ToolError` |
| Bộ lọc resume của `panel run` không đổi | `_answer_file_problem`, `start_job`, `check`, `tally` không có trong diff; test `test_rerun_asks_only_buyers_with_a_missing_or_invalid_answer` xanh trong 492 |
| SKILL.md bước 3 có câu của mục 4, test ghim; skill_lint 0 finding; khối `## Protocol` không đổi | diff `skills/founder-consumer/SKILL.md` chỉ đổi một dòng bước 3; `tests/test_consumer_skill.py::test_step_3_tells_the_owner_…`; skill_lint chạy ở HEAD |
| Q58 trong nhật ký, mệnh đề §2 | `docs/founder-vn-design.md`: mục Q58 sau Q57 (đúng dạng Q54, nêu lý do), tiêu đề Q1–Q58, mệnh đề trong bullet fan-out; `AGENTS.md` và `tests/test_install.py` cập nhật theo |
| Bằng chứng `docs/evidence/issue-143-…md` có hàng đỏ rồi xanh | Có bảng `## Lát` kèm lệnh đỏ (9 failed, 7 passed) và lệnh xanh; khối `## Cổng ba đoạn` nay có ba lệnh, đầu ra `verify` và `GREEN on cbaa732e5f19` (hậu duệ chỉ đổi docs của mã `7cb6894`) |
| Gate xanh ở commit mã cuối (static, unit, build, verify) | CI `Gate` success; evidence ghi bốn đoạn; tôi chạy lại unit và skill_lint |

Ngoài phạm vi được giữ: không có stamp `prompt_hash` trong answer file, không có công cụ di chuyển hay xoá, không đổi `_answer_file_problem`, `check`, `tally`, `jobs/`, board, `GIVEN_NAMES`.

## Ghi nhận không chặn

- Criterion MCP nói text "bằng" stderr của CLI. Test và evidence ghi rõ text thực là tiền tố của thư viện MCP `Error executing tool panel_init: ` cộng đúng văn bản stderr của CLI (`lỗi: …`). Tiền tố do thư viện thêm khi bọc `ToolError`, lane khai là lệch (deviation) trong evidence và test ghim chuỗi chính xác. Nội dung do `panel.init` sinh là một văn bản; tôi coi criterion được đáp ứng.
- Hướng dẫn bước 3 của skill chưa có tên công cụ khác ngoài `panel_init`; không có số liệu hay khẳng định pháp lý mới nên không cần link.

## Chưa xác minh

- Không chạy mô hình thật (không có credential, ngoài phạm vi; tool dùng provider giả trong test).
- Không đối chiếu bản gốc thân ticket với issue trên GitHub ngoài văn bản trong tin nhắn lượt này.

<promise>PASS</promise>
