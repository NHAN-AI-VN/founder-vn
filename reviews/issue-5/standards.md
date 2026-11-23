Commit mã đã chấm: b0a3e6203a5f

# Review trục Standards, issue #5, vòng 1

**Phán quyết: CHANGES_REQUESTED** (hai finding chặn, cả hai sửa được trong file lane này đã chạm; không cần file một-chủ ngoài cấp phát, không lộ quyết định thiết kế mới).

## Phạm vi đã xét

`git log --oneline main..HEAD` (7 commit: `4c4c87e` seam, `e0fb19c` design, `dbfbf1a` và `811b7bf` slice, `1b951c0`, `9269c4e`, `b0a3e62` docs) và `git diff --stat main...HEAD` (5 file: `README.md`, `docs/evidence/issue-5-golden-case.md`, `docs/founder-vn-design.md`, `examples/barbershop/founder/idea.md`, `tests/test_golden_case.py`). Chuẩn đối chiếu: `AGENTS.md` (quy tắc 7, 8), `docs/agents/standards.md` (Owner-facing output, Tests, Git), `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` (Q21, Q51, §7). CI Gate ở commit này: success (theo tin nhắn mở đầu).

## Đã đạt

- Không đụng `src/`, nên không có phép tính nào lệch CLI/MCP, không đường ghi file ngoài lớp khoá, không số mặc định thay lỗi nêu tên trường; test không gọi mạng và không đọc biến `FOUNDER_LLM_*`.
- Hình dạng vòng lặp: (a) `4c4c87e` (`seam:`, có `## Seam`) đứng trước `dbfbf1a` và `811b7bf` (`slice(`); (b) không commit nào chạm `src/`, mỗi slice kèm `tests/test_golden_case.py` và có dòng trong `## Lát`; (c) test ở seam đã khai (đường dẫn và nội dung `idea.md`, README); (d) `## Cổng ba đoạn` ghi `verify GREEN on 9269c4e`, và `9269c4e` là commit cuối chạm example; `b0a3e62` chỉ chạm file bằng chứng, nên cổng không stale.
- Không golden file nào đổi. `$` cạnh chữ số: không có. Có miễn trừ trách nhiệm ở cuối `idea.md`. Không có kết quả panel nên không cần cảnh báo panel. `metadata.version` không áp dụng (diff không chạm `skills/`).
- README là file một-chủ, đã cấp phát trên #5 theo evidence; Q51 ghi vào design cùng thay đổi, đúng quy tắc "design wins".

## Finding chặn

### S1: địa điểm dưới cấp quận trong file công khai

- Chỗ: `examples/barbershop/founder/idea.md` dòng 4 ("quanh khu Phú Mỹ Hưng (Quận 7 cũ)") và dòng 6 ("Tiệm 1 ở khu Phú Mỹ Hưng (Quận 7 cũ)"); `docs/founder-vn-design.md` dòng 281 (Q51, "tại khu Phú Mỹ Hưng (Quận 7 cũ)"); `docs/evidence/issue-5-golden-case.md` dòng 50 và mục Seam, khẳng định "location at former-district level".
- Sai gì: Phú Mỹ Hưng là một khu đô thị có tên, nhỏ hơn quận. Tên khu đi kèm quy mô tiệm, giá, bán kính 1,5 km và khoảng thuê 35-40 triệu đồng nhận diện được chủ tiệm. Q51 tự nói "vị trí ghi tới cấp quận cũ" và bằng chứng nói "former-district level", nhưng văn bản ghi cấp khu. Test `test_example_is_anonymised` chỉ bắt số điện thoại, e-mail, số nhà và `$`, nên không bắt được lỗi này.
- Chuẩn: `AGENTS.md` quy tắc 8 ("No real names, locations below district level ... in fixtures, logs, examples or evidence"); `docs/agents/standards.md` mục Owner-facing output (example ẩn danh).
- Vì sao chặn: `examples/` công khai từ ngày đầu; sai chuẩn dữ liệu ẩn danh không rút lại được sau khi merge và publish.
- Cách sửa (commit bổ sung, không viết lại lịch sử): thay "khu Phú Mỹ Hưng" bằng mô tả ở cấp quận ("Quận 7 cũ, TP.HCM") ở các dòng trên, sửa Q51 và evidence cho khớp, và thêm vào `test_example_is_anonymised` một kiểm tra đỏ-rồi-xanh cho tên khu (ghi dòng đỏ vào `## Lát`), rồi chạy lại cổng ba đoạn ở commit mã cuối.

### S2: khẳng định pháp lý và thuế suất không có link chính thức, không có ngày kiểm chứng

- Chỗ: `examples/barbershop/founder/idea.md` dòng 7: "thuế thuê nhà 10%", "bảo hiểm xã hội cho người làm toàn thời gian", "thợ làm không quá 48 giờ/tuần".
- Sai gì: một tỷ lệ thuế và hai nghĩa vụ lao động xuất hiện trong ví dụ mà không có link chính thức hay ngày kiểm chứng. Cuối file lại viết "Thuế theo doanh thu và nghĩa vụ pháp lý không có trong file này", nên văn bản tự mâu thuẫn. Evidence cũng cho biết lane đã bỏ giá đối thủ vì lý do nguồn và ngày, nhưng không áp dụng cùng mức cho các khẳng định pháp lý.
- Chuẩn: `docs/agents/standards.md` mục Owner-facing output ("Every legal or numeric claim in a skill or example carries an official link and a verification date"; "Tax rates and thresholds are inputs with a source link, never constants"); checklist rà soát skill/example của lượt này.
- Vì sao chặn: thiếu một mục checklist là finding chặn; một tỷ lệ thuế cố trong ví dụ sẽ bị skill T11 đọc như đầu vào đã kiểm.
- Cách sửa: bỏ tỷ lệ "10%" và các câu nghĩa vụ pháp lý khỏi `idea.md` (để CFO/permits tra khi chạy, đúng như disclaimer đã hứa), hoặc thêm link chính thức kèm ngày kiểm chứng cho từng khẳng định. Nếu chi phí thuê nhà cần để tính, ghi là "thuế thuê nhà theo luật hiện hành, skill tra khi chạy".

## Chưa xác minh

- Tính đúng của các con số kế hoạch (giá, vốn, công suất): là ước tính của chủ dự án, evidence đã nói rõ; tôi không đối chiếu với nghiên cứu thị trường vì nó nằm ngoài repo.
- Chất lượng tiếng Việt và việc "không lọt tiếng Anh": `idea.md` là file đầu vào của chủ hộ, các từ Anh còn lại (Essential Cut, Signature Cut, app, QR, podium) là tên gói hoặc từ mượn; tôi coi là chấp nhận được, nhưng reviewer Spec có thể có ý khác.
- `scripts/skill_lint.py`, `uv run pytest`, `ruff`: không chạy lại ở lượt này; dựa vào kết quả Gate success và block `## Cổng ba đoạn`.

<promise>CHANGES_REQUESTED</promise>
