Commit mã đã chấm: 68a9c1deb50d

# Standards review, issue #7, vòng 1 (chấm lại sau câu trả lời của operator)

Phạm vi: `git diff --stat main...HEAD` (26 file) và `git log --oneline main..HEAD` (11 commit). Kể từ lượt trước (`17a2a7f`), nhánh thêm `68a9c1d`, chỉ chạm `docs/agents/standards.md` và `reviews/issue-7/operator-answer.md`; không có mã mới, không có test mới, không có evidence mới. Đã đọc lại `AGENTS.md`, `docs/agents/standards.md` (bản sau `68a9c1d`), `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/evidence/issue-7-installer.md`, `reviews/issue-7/operator-answer.md`, `src/founder_vn/{install,cli}.py`, và design (các dòng nhắc `install`). Không có `docs/adr/` hay `CONTRIBUTING.md` cần xét. Diff không chạm `skills/` ngoài `.gitkeep`, nên checklist skill không áp dụng.

Đã chạy tại HEAD: `uv run --frozen pytest -q` được 132 passed; `uv run --frozen ruff check .` sạch.

Hình dạng vòng lặp: (a) `seam:` (`eee6595`) đứng trước mọi `slice(`, đạt. (b) Ba commit chạm `src/` (`bbe41ed`, `1fae020`, `df19a24`) đều chạm test và có dòng trong `## Lát`, đạt. (c) Test đi qua `install.run` và CLI, đúng seam đã khai, đạt. (d) `## Cổng ba đoạn` ghi `verify` GREEN ở `c124219`, là commit mã cuối; các commit sau (`0ec3879`, `68a9c1d`) chỉ chạm tài liệu, đạt.

Việc ghi ngoài `founder/` của installer trước đây bị chặn vì chuẩn cấm. Operator đã quyết và `docs/agents/standards.md` (mục "Shape of the code") nay ghi ngoại lệ với phạm vi rõ. Mã tại `install.py:97-120` (thư mục lấy từ `SKILL_FOLDERS`, từ chối đích resolve ra ngoài project bằng `InstallRefused` trước khi ghi, không xoá, `--print-only` không ghi) nằm trong phạm vi đó. Phần này không còn là finding; ledger do lượt sửa ghi.

## Finding chặn, lane sửa được

### S2: Hành vi mới không có đỏ rồi xanh (chưa được xử lý từ vòng trước)
- Chỗ: `docs/evidence/issue-7-installer.md`, mục `## Giới hạn`: "Some CLI tests (timeout note, trust note, env names, `gemini` refused, exit 2) had no witnessed red"; mục `## Lát`, dòng "CLI, snippets, goldens" ("the other CLI tests were written together with the code and have no witnessed red") và dòng "host pages" ("and 3 more reds", không nêu assertion). Test tương ứng: `tests/test_install_cli.py`, `tests/test_hosts.py`.
- Chuẩn: `docs/agents/evidence-gates.md`, "Evidence by change type" (Behavior: red assertion cho hành vi mong muốn) và "A test must fail for the expected assertion before the implementation makes it pass".
- Vì sao chặn: `68a9c1d` không đụng tới mục này; evidence vẫn tự khai thiếu đỏ. Hai khẳng định bảo vệ ràng buộc quan trọng (giá trị `FOUNDER_LLM_*` không lọt đầu ra, exit 2 khi từ chối) chưa từng được thấy đỏ nên chỉ chứng minh lệnh thoát 0.
- Cách sửa: commit bổ sung, không viết lại lịch sử. Với từng test, đột biến mã (ví dụ in giá trị `FOUNDER_LLM_API_KEY`, bỏ bắt `InstallRefused`, bỏ timeout note), ghi assertion đỏ vào `## Lát`, hoàn nguyên, chạy lại xanh, rồi chạy lại `gate-segment.sh verify` ở commit mã cuối.

### S3: cờ `--skills-dir` cho phép nguồn chọn lúc chạy, trái với ngoại lệ vừa ghi (likely)
- Chỗ: `src/founder_vn/cli.py:29` và `:50-52`; `src/founder_vn/install.py:98` (`source = Path(skills_dir) if skills_dir is not None else packaged_skills_dir()`).
- Sai gì: ngoại lệ trong chuẩn dựa trên việc tập file ghi ra "do package cố định và đã review trong repo", nên giới hạn `.md`/`.json` không cần áp dụng. Cờ công khai `--skills-dir` cho người gọi (hay một agent) trỏ nguồn vào thư mục bất kỳ, và mọi file, mọi đuôi, của thư mục đó có `SKILL.md` được ghi vào thư mục host. Với cờ này, lý do miễn giới hạn đuôi không còn đúng ở CLI. Cờ cũng không có trong design §5 hay ticket (grep `skills-dir` ở design không có kết quả) và không có test CLI ở đường mặc định đóng gói.
- Chuẩn: `docs/agents/standards.md`, mục "Shape of the code", mục ngoại lệ của installer: "the files it writes are exactly the files shipped under the package's `skills/<name>/`".
- Vì sao chặn: mã và chuẩn tự mâu thuẫn. Lane sửa được: bỏ cờ khỏi CLI (test đã có seam `install.run(..., skills_dir=...)`; test CLI cần nguồn tổng hợp thì dùng cách khác không công khai), hoặc giữ cờ nhưng khi đó phải ghi lại ngoại lệ cho nó. Cách thứ hai sửa chuẩn, nên cần operator xác nhận; chọn cách thứ nhất nếu không có xác nhận đó. Nếu operator muốn giữ cờ, đó là một quyết định thiết kế mới và lượt này chuyển thành `BLOCKED`.

## Chưa xác minh
- Run Gate 45102747034 báo `success` nhưng job `Gate` còn `in_progress` trong tin nhắn giao việc; chưa xác nhận kết quả cuối từ CI. Kết quả cục bộ ở trên là bằng chứng thay thế một phần.
- Chưa dựng wheel để xác nhận `founder_vn/skills/.gitkeep` có trong wheel; chỉ dựa vào evidence và `test_pyproject_ships_skills_in_the_wheel` (kiểm cấu hình, không kiểm wheel).
- Việc mã không cần kiểm lại sau `mkdir` (operator answer): đồng ý với lập luận cho đường dẫn tới từ `SKILL_FOLDERS`; chưa thử một thư mục host là symlink có sẵn trỏ ra ngoài project, mà `resolve()` trước `mkdir` đáng lẽ bắt được.

<promise>CHANGES_REQUESTED</promise>
