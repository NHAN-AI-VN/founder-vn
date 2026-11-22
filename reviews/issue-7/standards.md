Commit mã đã chấm: 0ec387988ab9

# Standards review, issue #7, vòng 1

Phạm vi: `git diff --stat main...HEAD` (22 file) và 6 commit mã (`eee6595` seam, `bbe41ed`, `1fae020`, `df19a24`, `45c3ca8`, `c124219` slice) cộng `0ec3879` (evidence). Đã đọc `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/founder-vn-design.md` §5, `docs/evidence/issue-7-installer.md`, `src/founder_vn/{install,cli,files}.py`, `tests/test_install*.py`. Không có `docs/adr/`, không có `CONTRIBUTING.md` cần xét. Diff không chạm `skills/` ngoài `.gitkeep`, nên checklist skill không áp dụng.

Đã chạy lại tại HEAD: `uv run --frozen pytest -q` được 132 passed; `ruff check` sạch. Đã kiểm tay: không có `$` cạnh chữ số trong `docs/hosts/*`; test không gọi mạng; biến `FOUNDER_LLM_*` chỉ được nêu tên, test khẳng định giá trị không lọt vào đầu ra.

Hình dạng vòng lặp: (a) `seam:` đứng trước mọi `slice(`, đạt. (b) Mọi commit chạm `src/` (`bbe41ed`, `1fae020`, `df19a24`) cũng chạm test và có dòng trong `## Lát`, đạt. (c) Test đi qua `install.run` và CLI, đúng seam đã khai, đạt. (d) `## Cổng ba đoạn` ghi `verify` GREEN ở `c124219`, là commit slice cuối; `0ec3879` chỉ chạm evidence, đạt. Parity: seam khai `install` chỉ có ở CLI, và design §5 chỉ nêu lệnh CLI, nên không coi là finding.

## Finding chặn

### S1: `install.py` ghi file ngoài lớp khoá đường dẫn, và chuẩn không có ngoại lệ cho việc đó
- Chỗ: `src/founder_vn/install.py:104-111` (`target.parent.mkdir(...)`, `target.write_bytes(data)`), `docs/evidence/issue-7-installer.md` mục `## Seam`, dòng "Writes".
- Sai gì: installer tự mở file để ghi dưới `.kiro/skills`, `.grok/skills`, `.claude/skills`, `.agents/skills`, bằng kiểm tra riêng (`is_relative_to` một lần, trước `mkdir`, không kiểm lại sau khi tạo thư mục như `files.write_text` làm). Nó cũng chép mọi đuôi file trong `skills/<name>/`, không giới hạn `.md`/`.json`.
- Chuẩn: `docs/agents/standards.md`, mục "Shape of the code": "Every file the package writes goes through the path-locked layer ... only `.md` and `.json` written ... No other code path opens a file for writing."
- Vì sao chặn: design §5 yêu cầu lệnh sao chép skill vào thư mục host, nên ghi ngoài `founder/` là bắt buộc. Nhưng chuẩn hiện ghi cấm, và diff tự khai ngoại lệ trong file evidence, không trong chuẩn hay design. Một lane không tự đặt ngoại lệ cho luật "không có đường ghi nào khác". Cần quyết định: sửa chuẩn (`docs/agents/standards.md`, file một-chủ ngoài cấp phát của lane) hoặc đổi design. Lane này không sửa được bằng file của mình, nên là BLOCKED. Sau khi có quyết định, mã nên có phần kiểm lại sau `mkdir` và phạm vi đuôi file theo đúng ngoại lệ được ghi.

## Finding chặn, lane sửa được

### S2: Hành vi mới không có đỏ rồi xanh
- Chỗ: `docs/evidence/issue-7-installer.md`, mục `## Giới hạn`: "Some CLI tests (timeout note, trust note, env names, `gemini` refused, exit 2) had no witnessed red". Dòng `## Lát` của slice host pages ghi "and 3 more reds" không nêu assertion; các test tương ứng ở `tests/test_install_cli.py:28-60`, `tests/test_hosts.py`.
- Chuẩn: `docs/agents/evidence-gates.md`, "Evidence by change type" (Behavior: red assertion cho hành vi mong muốn) và "A test must fail for the expected assertion before the implementation makes it pass".
- Vì sao chặn: test viết cùng mã chưa từng đỏ chỉ chứng minh lệnh thoát 0. Có hai khẳng định bảo vệ ràng buộc quan trọng: giá trị biến môi trường không lọt đầu ra, và exit 2 khi từ chối.
- Cách sửa: commit bổ sung, không viết lại lịch sử. Với mỗi test, đột biến mã (ví dụ in giá trị `FOUNDER_LLM_API_KEY`, bỏ bắt `InstallRefused`), ghi assertion đỏ vào `## Lát`, hoàn nguyên, chạy lại xanh, rồi chạy lại `gate-segment.sh verify` ở commit mã cuối.

## Chưa xác minh
- Run Gate 45048917567 báo `success` nhưng job `Gate` còn `in_progress` trong tin nhắn giao việc; không xác nhận được kết quả cuối từ CI. Kết quả cục bộ ở trên là bằng chứng thay thế một phần.
- Chưa dựng wheel để xác nhận `founder_vn/skills/.gitkeep` có trong wheel; chỉ dựa vào evidence và test `test_pyproject_ships_skills_in_the_wheel` (kiểm cấu hình, không kiểm wheel).
- Golden `install_*.json` sinh từ mã rồi đọc lại; commit `df19a24` nêu goldens mới nhưng chỉ nêu chúng là "first output", chưa nói nội dung. Coi là chấp nhận được vì là golden mới, không đổi golden cũ.

## Câu hỏi cho operator
- [ ] Installer ghi vào thư mục skill của host (ngoài `founder/`) là ngoại lệ chính thức của luật "chỉ lớp khoá đường dẫn được ghi" ở `docs/agents/standards.md`? Nếu có, ngoại lệ gồm phạm vi thư mục và đuôi file nào, và chuẩn được sửa ở lane nào?

<promise>BLOCKED</promise>
