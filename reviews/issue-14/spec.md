Commit mã đã chấm: c53cb77e30bc

# Review trục Spec, #14 founder-board, vòng 1

Phạm vi: `git diff --stat main...HEAD` (19 file, 8 commit từ `0fa1596` tới `c53cb77`). Đã đọc `AGENTS.md`, `docs/agents/evidence-gates.md`, mục `founder-board` và Q50 của `docs/founder-vn-design.md`, `skills/founder-board/`, `src/founder_vn/board.py`, phần đổi của `cli.py`, `server.py`, `panel.py`, ba file test, evidence và các file ví dụ.

Phán quyết: PASS. Không có finding chặn.

## Đối chiếu từng criterion

1. `board run` / `board_run` là job trên runner, ba completion độc lập, memo tiếng Việt đúng hình dạng, `job_status`, ghi model và hash prompt.
   - Mã: `board.py` (`start_job`, `_ask` chạy mỗi lens một lần gọi `llm.complete` riêng trong `ThreadPoolExecutor`; `memo_problem` ép đủ sáu trường score, vote, strong, would_kill, questions, conditions; `memo_md` in tiêu đề tiếng Việt cố định). `board.json` ghi `model` và `prompt_hash`. `panel.job_status` đọc cả job `panel` lẫn `board` (một tool poll chung, đúng Q50). CLI `board run` / `board work` và tool MCP `board_run` đều gọi `board.run`.
   - Bằng chứng: `tests/test_board.py` (nhà cung cấp giả qua HTTP; vòng đời, hình dạng memo, prompt từng lens, retry, loại sau hai lần sai, tiếp tục job, lỗi worker ghi vào job) và `tests/test_board_parity.py` (đầu ra, file và `job_status` của CLI bằng MCP). Đã chạy lại tại HEAD: `uv run pytest -q tests/test_board.py tests/test_board_parity.py tests/test_board_skill.py` được 24 passed. Cổng Gate ở `c53cb77e30bc` success (tin nhắn mở đầu). Các test nằm dưới `tests/` nên chạy trong đoạn `unit`.
   - Thiết kế: cấu hình thiếu env thì báo lỗi, không dùng mặc định; ghi qua `founder_vn.files` (chỉ `.md`/`.json`, khóa trong `founder/`). Khớp mục "Fan-out trong server".
   - Đáp ứng.
2. Văn bản lens (Offers: 100M Offers; Product: tiểu sử Isaacson; Systems: The E-Myth Revisited), quy tắc "áp dụng khung, không nói thay tác giả".
   - `board.LENSES` và `RULE` (đưa vào prompt từng lens, có test kiểm), `skills/founder-board/lenses.md` (cùng văn bản cho Facilitator, giải thích vì sao Systems thay Monopoly, khớp mục `founder-board` của thiết kế), `SKILL.md` mục Rules nhắc lại quy tắc. Memo cũng in câu "không nói thay tác giả".
   - Đáp ứng.
3. Skill: Step 0 viết hoặc dùng lại `idea.md`; brief tự đứng một mình; chair's summary giữ bất đồng, gộp điều kiện thành checklist, nêu skill trả lời từng số còn mở.
   - `SKILL.md`: Step 0 (dùng lại nếu có, hỏi từng nhóm nếu chưa, không đoán số), Step 1 (brief không phụ thuộc hội thoại hay file khác, "chưa có số liệu" thay vì bịa), Step 3 (bốn mục theo thứ tự, không lấy trung bình, danh sách `- [ ]` kèm tên lens, bảng số còn mở với skill trả lời, hai dòng miễn trừ, không đưa verdict). `scripts/skill_lint.py`: 3 skills, 9 example files, 0 finding (đã chạy lại). `tests/test_board_skill.py` kiểm các điểm này.
   - Đáp ứng.
4. Test fake-provider cho `board_run`; golden case chạy trên Kiro CLI: `board/` và `board.md` trong thư mục ví dụ; checklist review.
   - Fake-provider: `tests/test_board.py`, `tests/test_board_parity.py` (xem mục 1).
   - Golden: đọc file thật trong diff. `examples/barbershop/founder/board/` có `brief.md`, `board.json`, ba cặp `<lens>.json` / `<lens>.md`; `board.md` ở `founder/`. Tiếng Việt, xưng "anh/chị", tiền dạng `199.000 đ`, không có `$` (grep trống), có miễn trừ ở cuối `board.md` và từng memo. Bất đồng giữ mở (dải giá, vị trí rủi ro, sức khỏe vận hành), không lấy điểm trung bình, không verdict. Đối chiếu chéo: cả sáu điều kiện của ba memo có mặt trong checklist năm mục (hai điều kiện khảo sát 50 người của Offers và Product được gộp đúng vì cùng một việc, giữ nhãn `[Offers][Product]`); các câu hỏi mở đều có hàng trong bảng và đều trỏ tới skill hợp lệ hoặc "ngoài bộ công cụ". `board.md` không tự thêm số mới. Địa danh chỉ tới cấp quận ("Quận 7 cũ"), không tên người, không địa chỉ cụ thể: không vi phạm quy tắc ẩn danh.
   - Tính nhất quán máy kiểm: ba test golden trong `tests/test_board_skill.py` kiểm `<lens>.md` khớp từng byte với `board.memo_md` trên `<lens>.json`, `board.json` ghi model và hash, và cấu trúc `board.md`. Evidence `docs/evidence/issue-14-founder-board.md` có mục `## Seam`, bảng `## Lát`, khối `## Cổng ba đoạn`, bảng các bước của lượt chạy Kiro CLI, checklist review tích đủ và mục Giới hạn.
   - Đáp ứng. Phần "chạy trên Kiro CLI" dựa vào lời khai trong evidence và các file kết quả; xem mục chưa xác minh.

## Chưa xác minh

- Không thể kiểm từ sandbox rằng lượt golden thật sự chạy trên Kiro CLI với `gemini-3.5-flash-lite` như evidence khai. Bằng chứng gián tiếp nhất quán: `board.json` ghi model đó, ba memo khớp byte với bộ render của package, `board.md` tham chiếu đúng điểm và phiếu của memo. Không có dấu hiệu mâu thuẫn.
- Văn bản lens chưa đối chiếu với ba cuốn sách (evidence cũng nêu giới hạn này); ticket chỉ đòi tên nguồn và quy tắc, và thiết kế không yêu cầu hơn.
- `board.md` do mô hình của host viết ở Step 3; test chỉ ghim cấu trúc, không ghim lời văn. Đó là phạm vi test hợp lý cho một artefact tự do, không phải thiếu sót của criterion.
- Chưa xem log Gate gốc; dựa vào tin nhắn mở đầu (success) và lần chạy lại cục bộ ở trên.

<promise>PASS</promise>
