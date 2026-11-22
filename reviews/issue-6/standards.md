Commit mã đã chấm: 331001f15fae

# Review trục Standards, issue #6, vòng 1

Phạm vi: `git diff --stat main...HEAD` (15 file: `cfo.py`, `vnd.py`, `cli.py`, `server.py`, 5 golden, fixture, 4 file test, file bằng chứng) và `git log --oneline main..HEAD` (7 commit). Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`. `docs/adr/` không tồn tại; `skills/` và `examples/` không bị chạm nên checklist skill không áp dụng.

Máy đã chạy lại ở checkout này: `ruff check` sạch, `ruff format --check` sạch (80 file), `pytest -q` 104 passed, `skill_lint.py` 0 finding.

## Đã đạt

- Ghi file chỉ qua `files.write_text`; đọc qua `files.read_text` (`cfo.py` `_load`, `run`). Không có `open(..., "w")` nào khác.
- Tương đương CLI/MCP: cả hai gọi `cfo.run`; `tests/test_cfo_parity.py` so stdout và file giữa hai đường, 4 ca.
- Trường số thiếu thì `NumbersError` nêu tên trường; thuế suất và ngưỡng là đầu vào của `numbers.json`, không là hằng số. Fixture là dữ liệu tổng hợp. Không có mạng, không in biến `FOUNDER_LLM_*`.
- Vòng lặp: (a) `59037b4 seam:` có `## Seam`, đứng trước mọi commit `slice(`. (b) Mọi commit chạm `src/` đều chạm test và có dòng trong `## Lát`. (c) Test ở seam đã khai (`founder_vn.vnd`, `founder_vn.cfo`, CLI, MCP). (d) `GREEN on 23342b9b757b…` đúng là commit mã cuối; `331001f` chỉ chạm docs.

## Finding chặn

### S1: Lát `cfo.analyse` không có bằng chứng đỏ cho hành vi mới

- Chỗ: `docs/evidence/issue-6-cfo-unit-economics.md`, bảng `## Lát`, dòng `cfo.analyse`; commit `3024478` thêm `cfo.py` (200 dòng) cùng `tests/test_cfo.py` trong một commit.
- Sai gì: cột "Assertion while red" ghi lỗi `assert 45.0 == 45000` do một lỗi đọc số xuất hiện giữa chừng, và nói thẳng "The collection-time red (`founder_vn.cfo` absent) was not kept". Đó là đỏ của một lỗi ngẫu nhiên, không phải đỏ của hành vi mà lát tuyên bố: thuế doanh thu chỉ tính khi vượt ngưỡng, lộ `verdict_inputs`, lỗi nêu tên trường thiếu. Chưa có phép đo nào cho thấy các test này đỏ khi thiếu hành vi tương ứng (ví dụ bỏ nhánh `crosses`, hoặc bỏ kiểm tra trường bắt buộc).
- Chuẩn: `docs/agents/evidence-gates.md`, "Select validation from authoritative sources" ("A test must fail for the expected assertion before the implementation makes it pass") và bảng "Evidence by change type", dòng Behavior ("Red assertion for the intended behavior").
- Vì sao chặn: đây là lát mang phần lớn logic nghiệp vụ (thuế, hòa vốn, payback); xanh không chứng minh test bảo vệ được hành vi đó.
- Cách sửa, không viết lại lịch sử: một commit bổ sung chạy đột biến tạm trên `cfo.py` (bỏ nhánh thuế khi vượt ngưỡng; bỏ `_required` cho một trường), ghi tên test đỏ và assertion đỏ vào dòng `cfo.analyse`, hoàn tác đột biến, chạy lại `uv run pytest tests/test_cfo.py -q`, rồi chạy lại `gate-segment.sh verify` nếu commit đó chạm mã.

## Chưa xác minh

- Ba hệ số kịch bản trong `cfo.sensitivity` (giá giảm 10%, sản lượng giảm 20%, chi phí đơn vị tăng 15%) là hằng số trong mã, và test khoá đúng nhãn đó. `docs/founder-vn-design.md` không có chữ nào về chúng (grep `10%|20%|15%|sensitiv|what-if` không có kết quả). Không có thân ticket trong tay để biết ticket có quy định. Nếu ticket không quy định, đây là quyết định thiết kế chưa ghi và operator cần xác nhận. Tôi không gắn mã vì chúng là hệ số kịch bản, không phải thuế suất hay ngưỡng pháp lý.
- `_number` nhận chuỗi `"nan"`/`"inf"` qua `Decimal` rồi `float`, và `float('nan')` vượt các kiểm tra `<= 0`. Chưa chạy thử đường này nên không gắn mã.
- Workflow `Gate` ở `331001f15fae` còn `in_progress` lúc chấm; tôi chỉ dựa vào lần chạy cục bộ ở trên.
- Thân ticket #6 không có; tính đủ tiêu chí là việc của trục Spec.

<promise>CHANGES_REQUESTED</promise>
