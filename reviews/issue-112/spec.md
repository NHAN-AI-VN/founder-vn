Commit mã đã chấm: caa92fd1da54

# Review trục Spec, issue #112, vòng 1

Phạm vi: `git diff --stat main...HEAD` (10 file: README, evidence, golden `permits.md`, `business-plan.md`, `permits/sources.md`, `SKILL.md`, 4 file test) và `git log --oneline main..HEAD` (8 commit, từ seam đến evidence). Đã đọc file thật của skill, ledger, golden, evidence; chạy `uv run pytest -q` ở HEAD: 389 passed. CI `Gate` ở HEAD: success (theo tin nhắn giao việc).

**Phán quyết: PASS**

## Đối chiếu từng criterion

1. **SKILL.md**: frontmatter `name: founder-permits`, `description` có các cụm "cần giấy phép gì", "đăng ký hộ kinh doanh", "thuế hộ kinh doanh", "hóa đơn điện tử", `license: MIT`, `metadata.version: "0.2.0"` bằng `founder_vn.__version__` (src/founder_vn/__init__.py). Khối Protocol năm điểm như skill đợt A. Quy tắc "Never guess a number" có ở phần Purpose và Rules. Bằng chứng: `tests/test_permits_skill.py` (12 test, trong cổng `unit`), `scripts/skill_lint.py` trong cổng `static` (evidence ghi 7 skill, 0 finding).
2. **Cấu trúc tĩnh sáu phần**: đúng thứ tự (đăng ký hộ KD; đăng ký thuế và cách kê khai; sau khi mở cửa gồm thuế theo doanh thu dùng hai entry cũ và lời Q52, hóa đơn điện tử; ngành có điều kiện; nguồn và ngày; lưu ý và hỏi kế toán). Một câu nói đường F&B chưa có (Q56) trong skill. Golden có đủ sáu mục.
3. **Tra lại lúc chạy**: Step 3 của skill mô tả fetch lại, dùng bản chép trong sổ khi thất bại, ghi "kiểm chứng ngày X, chưa xác nhận lại hôm nay", không bỏ số, không thay bằng nguồn ngoài. Golden áp dụng đúng chữ này cạnh từng con số; evidence ghi rõ lần tra lại thực tế.
4. **`permits/sources.md`**: thêm `household_registration`, `tax_registration_declaration`, `einvoice_obligation`, `conditional_sectors`, mỗi mục có link, số Công báo và ngày, điều khoản, trích nguyên văn, dòng "Xác nhận: kiểm chứng ngày 26/11/2026 bởi operator trên bản PDF Công báo". Hai entry cũ giữ nguyên (diff chỉ xoá một câu lời dẫn nằm ngoài mọi entry, đổi "chưa kiểm chứng" thành "chưa có bản kiểm chứng"; evidence nêu rõ). `grep -c 'chưa kiểm chứng'` = 0. `tests/test_sources_ledger.py` cập nhật số link (10 văn bản) và KEYS, có test mọi entry có dòng xác nhận và không entry nào còn "chưa kiểm chứng".
5. **Golden `permits.md` và `business-plan.md`**: đọc file thật. Tiếng Việt, xưng anh/chị, tiền dạng `1.000.000.000 đ`, không có `$` cạnh chữ số (grep cả hai file), có miễn trừ trách nhiệm và dòng hỏi kế toán đúng chữ của skill, không có số panel nên không cần cảnh báo "mô phỏng, cận trên". Mọi con số pháp lý có điều khoản, link Công báo và ngày. Không có tên người hay địa điểm dưới cấp quận. `business-plan.md` do `founder-vn plan` sinh lại (+58/-1), commit `8f4c0dc` nêu lý do; `tests/test_plan_example.py` kiểm tra đầu ra compiler bằng file. Giới hạn "không có Kiro CLI, agent tự chạy trong sandbox" được ghi trong evidence như #13. Mức lệ phí ghi đúng "chưa có nguồn đã kiểm chứng", không bịa số.
6. **README**: hàng `founder-permits` thành shipped với `#112` và link `permits.md`; phần tiếng Việt nói cùng điều; `tests/test_front_door.py` chuyển hàng khỏi tập "not started".
7. **Cổng và evidence**: `docs/evidence/issue-112-founder-permits.md` có bảng lát red-rồi-green kèm thông báo lỗi thật, điểm dừng BLOCKED và câu trả lời của operator (đã hỏi gì, nhận gì, ngày kiểm chứng 26/11/2026), mục giới hạn (không Kiro CLI, không F&B, lệ phí chưa có nguồn, không đối chiếu lại PDF hôm nay). Cổng ba đoạn ghi exit 0; CI `Gate` success ở đúng commit này.

Giới hạn và điều ngoài phạm vi: không có thay đổi ở `founder-cfo`, compiler hay thư mục ví dụ thứ hai (diff không chạm `src/` hay `scripts/`); đường F&B không được viết.

## Chưa xác minh

- Nội dung pháp lý của các trích dẫn (điều khoản, ngưỡng 1 tỷ đồng, thời hạn 03 ngày làm việc) dựa vào xác nhận của operator ngày 26/11/2026 trên PDF Công báo; reviewer không có quyền đọc lại PDF để đối chiếu độc lập, và test chỉ kiểm cấu trúc và chữ.
- Nghị định 253/2026 và 296/2026 không hiện ra trong công cụ tìm kiếm Công báo lúc chạy (evidence đã nêu); trang của chúng trả HTTP 200 theo evidence, chưa tự kiểm lại.

Không có finding chặn.

<promise>PASS</promise>
