# Trả lời của operator — review #7, vòng 1

Trả lời cho `reviews/issue-7/standards.md` (BLOCKED, commit mã đã chấm `0ec387988ab9`), mục "Câu hỏi cho operator". File này không phải báo cáo review; nó là đầu vào cho vòng review kế và cho lượt sửa.

## S1: installer ghi ngoài lớp khoá đường dẫn

- [x] Có, là ngoại lệ chính thức của luật "chỉ lớp khoá đường dẫn được ghi". Ghi vào `docs/agents/standards.md`, mục "Shape of the code", trong cùng commit này trên nhánh lane (PR #40). Design §5 không đổi: nó đã yêu cầu lệnh sao chép skill vào thư mục của host.

Phạm vi ngoại lệ, như đã ghi trong chuẩn:

- Thư mục: `<project>/<thư mục skill của host>/<skill>/…`, thư mục host lấy từ bảng `install.SKILL_FOLDERS` (`.kiro/skills`, `.grok/skills`, `.claude/skills`, `.agents/skills`). Không ghi chỗ nào khác.
- File: đúng tập file đi theo package dưới `skills/<name>/` (thư mục có `SKILL.md`), mọi đuôi file. Không giới hạn `.md`/`.json`: giới hạn đuôi của lớp khoá đường dẫn bảo vệ trước đường dẫn do mô hình chọn lúc chạy; ở đây tập file do package cố định và đã được review trong repo.
- Giữ nguyên các từ chối của lớp khoá: đích resolve ra ngoài project (`..`, symlink) → `InstallRefused`, exit 2, trước khi ghi gì; không xoá; `--print-only` không ghi.
- Kiểm lại sau `mkdir` như `files.write_text`: không yêu cầu. Phép kiểm chạy trên đường dẫn đã resolve trước `mkdir`; thư mục `mkdir` vừa tạo không thể là symlink, nên phép kiểm ấy đã bao phủ. Phép kiểm lại trong `files.py` nhắm vào đường dẫn do mô hình chọn lúc chạy, điều không xảy ra ở installer.
- CLI-only: chuẩn ghi rõ installer không có MCP tool (chạy trước khi server được đăng ký) nên luật parity không áp dụng cho nó; khớp mục "Parity decision" của `docs/evidence/issue-7-installer.md`.

Mã hiện tại (`src/founder_vn/install.py`, `_copy_skills`) nằm trong phạm vi trên; S1 không cần đổi mã. Chuẩn được sửa ở lane này, không ở lane khác.

## S2: hành vi mới không có đỏ rồi xanh

Thuộc lane, không cần quyết định của operator. Lượt sửa làm theo "Cách sửa" trong báo cáo: với từng test (giá trị biến môi trường không lọt đầu ra, exit 2 khi từ chối, timeout note, trust note, `gemini` bị từ chối) đột biến mã để chứng kiến assertion đỏ, ghi vào `## Lát`, hoàn nguyên, chạy lại xanh, rồi chạy lại cổng ba đoạn và `verify` ở commit mã cuối; commit bổ sung, không viết lại lịch sử.

## Ledger

Lượt sửa ghi `reviews/issue-7/ledger.md` cho mọi mã của mọi vòng. Gợi ý cho S1: `S1 FIXED — ngoại lệ ghi vào docs/agents/standards.md bởi commit của operator trên nhánh lane; mã không đổi`.
