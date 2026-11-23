Commit mã đã chấm: 61c236555191

# Review trục Standards, issue #8, vòng 1

Phán quyết: CHANGES_REQUESTED (một finding chặn, S1, lane tự sửa được bằng commit bổ sung).

## Phạm vi đã xét

`git diff --stat main...HEAD`: 9 file (`src/founder_vn/pricing.py`, `cli.py`, `server.py`, `tests/test_pricing_cli.py`, `tests/test_pricing_parity.py`, hai golden, một fixture, `docs/evidence/issue-8-pricing-psm.md`), 7 commit (`seam:` rồi 5 `slice(`, rồi `docs(evidence)`). Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Shape of the code, Tests, Owner-facing output, Git), `docs/agents/evidence-gates.md` (bảng "Evidence by change type", "Where evidence lives"), `docs/agents/parallel-lanes.md`.

Đã chạy lại ở HEAD: `ruff check` sạch, `ruff format --check` sạch, `pytest -q` 143 passed, `scripts/skill_lint.py` 0 finding. Diff không chạm `skills/` hay `examples/` nên checklist skill không áp dụng.

Đạt: mọi ghi file đi qua `files.write_text`, đọc qua `files.read_text`; không file một-chủ nào bị sửa (không đụng `pyproject.toml`, `uv.lock`, `README.md`, `__init__.py`); `pricing.run` là một hàm duy nhất sau CLI `pricing` và MCP `pricing_psm`, có parity test cho báo cáo, `--json`, `--out`; không có `$` cạnh chữ số, báo cáo xưng "anh/chị", có cảnh báo panel mô phỏng; không có gọi mạng hay LLM; thiếu `answers` là lỗi nêu tên trường, không có số mặc định; không có tỷ lệ thuế; không in giá trị biến `FOUNDER_LLM_*`; fixture là dữ liệu tổng hợp. Hình dạng vòng lặp: (a) `seam:` d268160 có `## Seam` và đứng trước mọi `slice(`; (b) mọi commit chạm `src/` cũng chạm test và có dòng trong `## Lát`; (c) test đi qua CLI và MCP, tức là seam đã khai; (d) `## Cổng ba đoạn` ghi `GREEN on 7a489011…`, đúng commit mã cuối (61c2365 chỉ sửa tài liệu).

## Finding chặn

### S1: Ba hành vi mới không có bằng chứng đỏ rồi xanh

Chỗ: `docs/evidence/issue-8-pricing-psm.md`, dòng thứ tư của bảng `## Lát`; mã ở `src/founder_vn/pricing.py` (`analyse`: `raise PricingInputError("thiếu trường 'answers'")`; `run`: nhánh `out`) và `src/founder_vn/cli.py` (`except (pricing.PricingInputError, files.PathRefused)` → exit 2); test ở `tests/test_pricing_cli.py` (`test_out_outside_root_is_refused`, `test_missing_answers_exits_2_naming_the_field`).

Sai gì: mã của refusal đường dẫn, của lỗi thiếu trường và của `--out` đã vào từ slice đầu (3bba197), còn test của chúng đến sau ở 82d8040 (commit chỉ có test, không có `src/`). Bằng chứng tự khai "These passed on first run". Lane có chạy một đột biến, nhưng chỉ cho `test_out_writes_pricing_md_under_founder` (thay `files.write_text` bằng ghi trực tiếp). Hai test còn lại, cái bảo vệ ranh giới ghi file và cái bảo vệ "thiếu trường nêu tên trường, không đặt mặc định", chưa từng được thấy đỏ. Một test xanh ngay lần chạy đầu chưa chứng minh nó bảo vệ hành vi đó. Ngoài ra đột biến của `--out` chỉ chứng minh đường ghi đi qua layer, không chứng minh `..` bị từ chối.

Chuẩn: `docs/agents/evidence-gates.md` ("A test must fail for the expected assertion before the implementation makes it pass"; bảng "Behavior": "Red assertion for the intended behavior"; `## Lát` cần "the assertion line while red" cho từng slice) và `docs/agents/standards.md` §Git (một commit `slice(` mang test và mã cùng nhau).

Vì sao chặn: hai hành vi này là hai quy tắc của chuẩn (path-locked layer, lỗi nêu tên trường). Thiếu đỏ thì không phân biệt được test có canh chúng hay chỉ chạy xanh.

Cách sửa (commit bổ sung, không viết lại lịch sử, không cần chạm file cấm): với mỗi test, làm một đột biến tạm thời trong `src/` rồi chạy `uv run pytest tests/test_pricing_cli.py -q` thấy đỏ đúng assertion, hoàn nguyên (`git diff src` rỗng), chạy lại xanh. Gợi ý: (1) bỏ `files.PathRefused` khỏi `except` trong `cli.py` hoặc cho `--out` ghi thẳng bằng `Path.write_text` với `..`; (2) thay `raise PricingInputError("thiếu trường 'answers'")` bằng `spec = {"answers": []}`. Ghi assertion đỏ thật vào dòng `## Lát` tương ứng (tách thành dòng riêng cho mỗi test) và chạy lại `gate-segment.sh verify`; vì commit chỉ sửa tài liệu, SHA mã cuối vẫn là 7a48901 và cổng không stale.

## Chưa xác minh (không gắn mã)

- Hằng số `MIN_VALID_ANSWERS = 8` trong `pricing.py`: chuẩn nói "thresholds are inputs with a source link, never constants". Thân ticket #8 không có trong sandbox và `docs/founder-vn-design.md` không nêu số 8 (grep không thấy). Nếu ticket ghi 8 là tiêu chí chấp nhận thì đây là ngưỡng đã được quyết và hằng số có tên là đủ; nếu không, đây là quyết định thiết kế chưa có và operator cần chốt. Spec axis nên đối chiếu với ticket.
- Hợp đồng file đầu vào (`answers`, `competitor_prices`) do lane tự đặt vì design không định nghĩa; evidence đã nêu trong `## Giới hạn`, nhưng nên có người xác nhận trước khi ticket panel sau này dựa vào.
- Đường lỗi qua MCP: `pricing_psm` không bắt `PricingInputError`/`PathRefused`, và parity test chỉ phủ đường thành công. Tôi chưa so với cách `cfo_analyse` xử lý lỗi, nên không kết luận có lệch hay không.
- Công thức Van Westendorp chỉ được kiểm bằng một phép tính tay và một golden (lane đã khai trong `## Giới hạn`); không so với cài đặt ngoài.
- Job `Gate` còn `in_progress` lúc chấm; cổng CI chạy lại trọn ở commit cuối.

<promise>CHANGES_REQUESTED</promise>
