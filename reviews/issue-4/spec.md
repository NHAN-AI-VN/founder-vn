Commit mã đã chấm: 7cd567144dc3

# Review trục Spec, issue #4 (pilot kit), vòng 1

Phạm vi: `git diff --stat main...HEAD` (7 file: 5 file `pilot/*.md`, `tests/test_pilot_kit.py`, `docs/evidence/issue-4-pilot-kit.md`) và 3 commit `a2724b3`, `089386c`, `7cd5671`. Đã đọc cả năm file `pilot/` nguyên văn, đối chiếu `docs/founder-vn-design.md` §1, §6, Q40, Q41, và `AGENTS.md`.

Phán quyết: CHANGES_REQUESTED.

## Đối chiếu từng criterion

- Criterion 1 (phiếu đồng thuận): đáp ứng một phần. `pilot/consent.md` có API bên thứ ba (§2), công bố ẩn danh (§3), xóa sau 90 ngày kèm ô "đồng ý giữ" (§4, §7), liên hệ rút lại (§6, đang là placeholder), nêu Luật 91/2025/QH15 (§5), có miễn trừ trách nhiệm. Thiếu link và ngày kiểm chứng cho khẳng định pháp lý: SPEC-1.
- Criterion 2 (baseline): đáp ứng. `pilot/baseline.md` có bốn mục (giá, địa điểm đến cấp quận/huyện, vốn, mở/không mở), "Ngày ghi", mục "Xác nhận của Chủ hộ" có ngày và chữ ký hoặc tin nhắn.
- Criterion 3 (ba câu hỏi): đáp ứng định nghĩa và số lượng. `pilot/follow-up-questions.md` có đúng ba câu, định nghĩa "đổi quyết định" nguyên văn theo ticket, và quy định người khác gửi ở +14 ngày. Quy trình giao việc cho người gửi trong runbook không chạy được: SPEC-2.
- Criterion 4 (bảng kết quả): đáp ứng. `pilot/results-template.md` có đủ cột (mã, ngành, bốn mục baseline, ba câu trả lời, đổi quyết định có/không, ghi chú) và lưu ý mô tả ở n = 20.
- Criterion 5 (runbook): đáp ứng về nội dung. `pilot/runbook.md` có buổi 1 (30 phút), đợt A ngoại tuyến, buổi 2 (45–60 phút), PDF qua Zalo, thư mục dự án từng người ngoài git, bước xóa sau 90 ngày.
- Giới hạn của ticket: không có `$`; tiền ghi `35.000 đ`; không tên người hay địa điểm dưới cấp quận trong file (ví dụ P00 dùng "quận A").

Bằng chứng: `uv run pytest tests/test_pilot_kit.py -q` chạy lại ở sandbox này, 6 passed. Test nằm trong `tests/`, thuộc cổng `unit` (evidence ghi 51 passed). Các test chỉ kiểm chuỗi nội dung, không kiểm chất lượng hay tính dùng được của biểu mẫu, nên tôi đã đọc file thật.

## Finding chặn

### SPEC-1: Khẳng định pháp lý trong phiếu đồng thuận không có link và ngày kiểm chứng
Criterion 1, kèm quy tắc cứng của design §2 (CONTRIBUTING: "mọi khẳng định pháp lý cần link chính thức + ngày kiểm chứng") và checklist "xong" của design §2 / hướng dẫn trục Spec. `pilot/consent.md` §5 liệt kê quyền của Chủ hộ theo Luật 91/2025/QH15 (biết, truy cập, chỉnh sửa, yêu cầu xóa, rút lại đồng ý) mà không có link tới vbpl.vn hoặc chinhphu.vn (Q39) và không có ngày kiểm chứng. `docs/evidence/issue-4-pilot-kit.md` tự thừa nhận điều này ("not verified against vbpl.vn ... carries no verification date"). Phiếu này là văn bản Chủ hộ ký, nên khẳng định sai hay cũ gây hại trực tiếp. Sửa trong phạm vi lane: kiểm chứng điều khoản với nguồn chính thức, thêm link và ngày vào `pilot/consent.md` §5 (hoặc bỏ các quyền cụ thể chưa kiểm chứng và chỉ nêu tên luật). Độ tin cậy: confirmed.

### SPEC-2: Runbook không cho người gửi cách liên lạc với Chủ hộ
Criterion 3 ("someone other than the Facilitator sends them at +14 days") và criterion 5. `pilot/runbook.md` buổi 2 bước 4 bảo Người hỗ trợ "giao mã người tham gia, không giao tên" cho người gửi, trong khi `pilot/follow-up-questions.md` bảo người gửi gửi qua Zalo. Không có kênh nào đưa tài khoản Zalo của Chủ hộ tới người gửi, nên theo chữ của runbook người gửi không có cách gửi. Lane có thể sửa: thêm bước ghi rõ cách bàn giao liên hệ (ví dụ Chủ hộ đồng ý trong phiếu đồng thuận việc chia sẻ số Zalo với người gửi, và dữ liệu liên hệ ấy được xóa cùng thư mục ở ngày 90), hoặc cách khác mà không phá yêu cầu ẩn danh và ràng buộc "người khác gửi". Nếu chọn thêm một điều khoản vào phiếu đồng thuận, nó phải khớp §1 (dữ liệu thu thập). Độ tin cậy: likely (suy từ hai file, chưa có tài liệu nào khác trong diff nói cách bàn giao).

## Chưa xác minh / câu hỏi cho operator (không gắn mã)

- [ ] Kênh liên hệ rút lại sự đồng ý (Zalo hay email, của ai): design không nêu, `pilot/consent.md` §6 để placeholder `[LIÊN HỆ RÚT LẠI: ...]`. Ticket nói "can run session 1 tomorrow", nên phải điền trước buổi 1; runbook "Trước buổi gặp thứ nhất" bước 3 đã nhắc việc này. Tôi không coi placeholder là finding chặn vì đây là dữ kiện chỉ chủ dự án có.
- [ ] Chốt chữ ba câu hỏi: design cố định số lượng và định nghĩa, không cố định lời. Lane tự soạn lời (evidence cũng ghi vậy); chủ dự án cần xác nhận trước khi tuyển người đầu tiên, vì file tuyên bố "không đổi chữ" sau khi chốt.
- [ ] CI: tin nhắn ghi run 45006703309 "success" nhưng bước `Gate` còn `in_progress` ở thời điểm review; tôi không có credential để kiểm lại. Evidence ghi gate ba đoạn xanh ở `089386c`, commit sau chỉ đổi file evidence.
- Không có hướng dẫn cho dữ liệu của người chọn "đồng ý giữ" (Zalo, ảnh phiếu baseline); runbook chỉ nói xóa khi không giữ. Không chặn criterion nào, nêu để lane cân nhắc.

<promise>CHANGES_REQUESTED</promise>
