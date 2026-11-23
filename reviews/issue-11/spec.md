Commit mã đã chấm: 573cedf8a2fb

# Review trục Spec, issue #11, vòng 1

Phạm vi: `git diff --stat main...HEAD` (10 file, 11 commit từ `9b64cf5` tới `573cedf`). Đã chạy `uv run pytest -q` ở HEAD: 219 passed (cổng `unit`). Gate CI ở HEAD: success.

**Phán quyết: PASS.** Không có finding chặn.

## Đối chiếu từng criterion

1. **Client cấu hình bằng `FOUNDER_LLM_*`, chưa cấu hình thì báo lỗi, không dùng `response_format`/`seed`/`temperature`.** Đạt. `src/founder_vn/llm.py`: `load_config` đọc ba biến, `NotConfigured` nêu tên biến thiếu và hướng dẫn cài đặt, không có nhà cung cấp mặc định; request chỉ có `model` và `messages`. Bằng chứng: `tests/test_llm.py` (3 test, gồm kiểm body request), `test_start_job_unconfigured_is_an_error_with_setup_and_writes_no_job`, `test_run_unconfigured_exits_2_...` trong `tests/test_panel_cli.py`.
2. **Brief tiếng Việt từ persona và pitch; hash của template + persona + pitch ghi vào `panel.json`, truyền sang `results.json`.** Đạt. `panel.BRIEF_TEMPLATE`, `brief`, `prompt_hash` (SHA-256 của template, JSON persona, pitch); `start_job` ghi `mode`, `model`, `prompt_hash` vào `panel.json`; `run_tally` đã chuyển sang `results.json` (`panel.py` dòng 422 đến 424). Bằng chứng: `test_brief_is_vietnamese_...`, `test_prompt_hash_covers_template_personas_and_pitch`, `test_job_lifecycle_answers_land_and_model_and_hash_reach_results`.
3. **`panel run` trả job id ngay; `job_status` trả done/pending/failed/excluded và lỗi cuối; answers ghi dần; chạy lại chỉ hỏi buyer thiếu hoặc không hợp lệ.** Đạt. CLI chạy tiến trình tách rời (`panel work`), MCP chạy thread của server; `execute` ghi job và answer sau từng buyer; `start_job` chọn `targets` bằng `_answer_file_problem`. Bằng chứng: `test_run_returns_a_job_id_at_once_...`, `test_job_lifecycle_...`, `test_rerun_asks_only_buyers_with_a_missing_or_invalid_answer`.
4. **Đợt 10 gọi đồng thời; timeout mỗi lời gọi; retry có backoff; buyer sai hai lần bị loại và đếm; package không viết answer thay buyer.** Đạt. `WAVE = 10`, `ThreadPoolExecutor(max_workers=WAVE)`, `llm.TIMEOUT = 90`, `ATTEMPTS = 3` với backoff gấp đôi, `MAX_INVALID = 2`; `_ask` chỉ ghi answer đã qua `extract_answer`. Bằng chứng: `test_buyers_are_asked_in_waves_of_ten_concurrent_calls` (provider đếm đồng thời, 25 buyer), `test_buyer_invalid_twice_is_excluded_and_nothing_is_written_for_them` (cũng kiểm `results.json` có `excluded`), `test_5xx_is_retried_with_backoff_then_succeeds`, `test_5xx_for_good_is_failed_...`, `test_timeout_is_a_failed_buyer_not_a_hang`.
5. **Trích JSON lỏng (object đầu tiên), dùng lại luật kiểm của tally.** Đạt. `extract_answer` dùng `raw_decode` từ dấu `{` đầu tiên rồi gọi `answer_problem` (hàm tally dùng). Bằng chứng: `test_extract_takes_the_first_json_object_in_prose`, `test_extract_reports_the_problem_instead_of_guessing`, `test_prose_wrapped_json_is_filed`.
6. **Test với fake provider: hợp lệ, JSON bọc văn xuôi, JSON sai, timeout, 5xx; vòng đời và số đếm; parity MCP cho hình dạng phản hồi `panel_run` / `job_status`.** Đạt. Các test nêu trên chạy trong `pytest` của cổng `unit` và dùng `fake_provider` trên 127.0.0.1. Parity: `tests/test_panel_parity.py::test_panel_run_and_job_status_cli_equals_mcp_seed_7` chạy CLI thật và MCP stdio thật, so văn bản run và status (sau khi thay job id) cùng tập file.

## Ghi chú, không chặn

- Thiết kế (`docs/founder-vn-design.md` §2) viết `panel_status`, ticket viết `job_status`; mã theo ticket và ghi rõ trong `docs/evidence/issue-11-panel-run.md`. Dòng thiết kế để operator sửa.
- Hành vi lane tự đặt nhưng nằm trong phạm vi criterion: `failed` (lỗi gọi sau 3 lần) tách khỏi `excluded` (sai hai lần); trạng thái job ở `founder/panel/jobs/`; lệnh ẩn `panel work`. Không vượt giới hạn nào của ticket.

## Chưa xác minh

- Chưa gọi mô hình thật; tương thích định dạng của từng nhà cung cấp ngoài `choices[0].message.content` chưa chứng minh (lane đã tự nêu ở mục Giới hạn).
- Hai job chạy đồng thời trên cùng panel sẽ hỏi lặp buyer; ticket không cấm và không yêu cầu.

<promise>PASS</promise>
