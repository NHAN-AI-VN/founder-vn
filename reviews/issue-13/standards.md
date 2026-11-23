Commit mã đã chấm: cada7bc77114

# Review trục Standards, issue #13, vòng 2

**Phán quyết: CHANGES_REQUESTED**

## Phạm vi đã xét

`git diff --stat main...HEAD` và `git log --stat main..HEAD` (6 commit: `b866f59` seam, `c50706a` slice, `ffdf727` evidence, `d193b6a` và `cada7bc` docs, `b139fd8` review spec). Đã đọc: `skills/founder-competitors/SKILL.md`, `skills/founder-competitors/survey-form.md`, `examples/barbershop/founder/survey-form.md`, `tests/test_competitors_skill.py`, `docs/evidence/issue-13-founder-competitors.md`. Chuẩn đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `.kiro/skills/code-review/SKILL.md`. CI Gate ở `cada7bc77114`: success (theo tin nhắn mở đầu). Tôi chạy lại `uv run python scripts/skill_lint.py`: 1 skill, 2 file ví dụ, 0 finding, phiên bản package 0.1.0.

Đạt: không đụng `src/` (không có phép tính thiếu parity, không ghi file ngoài lớp khoá, không số mặc định hay tỷ lệ hardcode); không `$` cạnh chữ số; xưng "anh/chị", đầu ra cho chủ hộ bằng tiếng Việt; `metadata.version` "0.1.0" khớp package; ví dụ có link nguồn và ngày truy cập 23/11/2026, khai rõ phương pháp bàn giấy; không lộ biến `FOUNDER_LLM_*`; commit `seam:` đứng trước commit `slice(`; test nằm ở seam đã khai (file skill, form, `install.run`); không có test gọi mạng.

## Finding chặn

### S1: cổng ba đoạn trong evidence đã stale

- Chỗ: `docs/evidence/issue-13-founder-competitors.md`, khối `## Cổng ba đoạn` ghi `Last code commit: c50706a` và `gate-segment verify: GREEN on c50706a8c96e...`.
- Sai: HEAD mã đang chấm là `cada7bc77114`. `c50706a` là tổ tiên của nó. Sau `c50706a`, `d193b6a` đã thêm file ví dụ 255 dòng vào `examples/`, và `cada7bc` phải sửa vì bước pytest của Gate đỏ (`test_example_is_anonymised`). Con số `233 passed` vì thế không còn nói gì về cây hiện tại, và cổng `static` (skill-lint nay quét thêm 2 file ví dụ) chưa được ghi lại ở SHA mới.
- Chuẩn: `docs/agents/evidence-gates.md`, mục "Where evidence lives" (`GREEN on <sha>` phải là commit mã cuối); tin nhắn mở đầu lượt: SHA là tổ tiên của commit mã cuối thì cổng đã stale.
- Chặn vì bằng chứng hoàn thành không khớp cây được giao. Sửa bằng commit bổ sung: chạy lại ba đoạn `scripts/harness/gate-segment.sh static|unit|build` rồi `verify` ở commit mã cuối (sau mọi sửa của lượt Spec), ghi SHA mới và số đếm mới. Không viết lại lịch sử.

### S2: evidence không ghi các commit sau slice và còn nêu giới hạn sai

- Chỗ: `docs/evidence/issue-13-founder-competitors.md`, mục `## Giới hạn` (dòng "Criterion 4 is not proven ... BLOCKED on the real survey") và mục `## Giải quyết review nội bộ` (tiêu đề rỗng).
- Sai: (a) hai commit `d193b6a`, `cada7bc` thêm `examples/barbershop/founder/survey-form.md` mà evidence không có dòng nào: không ghi lệnh kiểm (link, đường dẫn, `scripts/skill_lint.py`), không ghi lỗi `test_example_is_anonymised` đã đỏ rồi xanh. (b) Giới hạn nói không có phiếu khảo sát, trái với file đã nằm trong repo. (c) Mục review nội bộ để trống dù lane đã có finding được xử lý (Gate đỏ ở `d193b6a`, chữa ở `cada7bc`).
- Chuẩn: `docs/agents/evidence-gates.md`, bảng "Evidence by change type" (Documentation, skill or example: link/path validation, `skill_lint.py` green, source-pointer review) và "Where evidence lives" (mục **limits** nói đúng điều lát không chứng minh; mục `## Giải quyết review nội bộ`); `AGENTS.md`/`standards.md` (Git): commit nêu ticket, khẳng định phải có bằng chứng tái lập được.
- Chặn vì khẳng định trong evidence mâu thuẫn với nội dung diff. Sửa: cập nhật `## Giới hạn` theo trạng thái thật (và theo kết quả lượt sửa Spec về `competitors.md`), thêm dòng bằng chứng cho file ví dụ, điền mục review nội bộ.

## Chưa xác minh

- Không có bản tham chiếu T02 của đoạn `## Protocol` trong repo ở nhánh này (chỉ có một skill), nên không đối chiếu được "chép nguyên văn từ ticket T02". Văn bản khớp năm ý của `standards.md` (kiểm phiên bản, MCP trước CLI, không tự tính, không trả lời thay người mua, không viết phán quyết).
- Lượt Spec (`reviews/issue-13/spec.md`) yêu cầu sửa `SKILL.md` và thêm `examples/barbershop/founder/competitors.md`. Khi đó sẽ có thêm golden file mới và quy tắc mới trong skill; tôi chưa chấm chúng. Mỗi thay đổi cần test ở seam, cổng chạy lại ở commit cuối, và checklist skill (disclaimer, link kèm ngày kiểm chứng, không `$`) áp dụng lại.
- Chất lượng thực của các link trong file ví dụ (còn sống hay không) chưa được kiểm; tôi không tải lại các trang đó.

<promise>CHANGES_REQUESTED</promise>
