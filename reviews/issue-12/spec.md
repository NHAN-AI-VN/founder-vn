Commit mã đã chấm: e15e2e730dea

# Review trục Spec, issue #12 (founder-cfo), vòng 1

**Phán quyết**: BLOCKED. Tiêu chí 4 của ticket chưa đáp ứng và lane không tự đóng được; thêm một finding chặn mà lane sửa được (SPEC-1).

Phạm vi: `git diff --stat origin/main...HEAD` (8 file: SKILL.md, `permits/sources.md`, golden `numbers.json` và `cfo.md`, hai file test, evidence, Q52 trong design) và 6 commit từ `origin/main`. CI `Gate` ở `e15e2e730dea`: success. Đã chạy lại tại chỗ: `uv run python scripts/skill_lint.py` (0 finding) và `uv run pytest tests/test_cfo_skill.py tests/test_sources_ledger.py` (19 passed, gồm test golden vì chúng nằm trong hai file này).

## Đối chiếu từng criterion

| # | Criterion | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | SKILL.md viết lại: chỉ dẫn tiếng Anh, mục protocol chung, đầu ra tiếng Việt, hỏi chi phí theo lời Owner (nguyên liệu, bao bì, phí app giao hàng, thuê mặt bằng, lương, điện nước) | Đạt | Đọc `skills/founder-cfo/SKILL.md`: mục Protocol, Step 2 nêu đủ sáu nhóm từ ngữ, "anh/chị", `35.000 đ`, cấm `$`. `skill_lint` xanh; `tests/test_cfo_skill.py` chạy trong cổng `unit`. |
| 2 | Tra `tax_rate_on_revenue` theo ngành và `tax_free_threshold` kèm link chính thức và ngày kiểm chứng; ghi làm hai mục đầu của sổ nguồn theo CONTRIBUTING | Đạt phần sổ nguồn, chưa đạt phần báo cáo (xem SPEC-1) | `permits/sources.md` mới, đúng hai mục đó đứng đầu, mỗi mục có link Công báo, số Công báo, điều khoản, trích đoạn, "kiểm chứng ngày 23/11/2026". `tests/test_sources_ledger.py` kiểm hình dạng. SKILL.md Step 3 buộc tra sổ, không gõ từ trí nhớ, và có nhánh "chưa kiểm chứng". |
| 3 | Gọi `cfo_analyse` (MCP) hoặc `founder-vn cfo` (CLI); đọc cờ lại bằng tiếng Việt thường; câu miễn trừ "không phải tư vấn tài chính hay thuế" | Đạt | SKILL.md Step 4 và 5, mục Rules (câu miễn trừ cuối câu trả lời), `cfo.md` có mục "Cảnh báo" và "Lưu ý". Skill không tự tính số. |
| 4 | Chạy golden case trên Kiro CLI: `numbers.json` và `cfo.md` trong thư mục ví dụ; review checklist đã qua | **Chưa đạt** | Hai file có trong `examples/barbershop/founder/`, nhưng do lane viết `numbers.json` và chạy `founder-vn cfo --out`, không phải một phiên Kiro CLI chạy `/founder-cfo`. `docs/evidence/issue-12-founder-cfo.md` mục "Giới hạn" tự nhận tiêu chí này chưa đóng và review checklist mới kiểm phần máy. Xem SPEC-2. |

Giới hạn và điều ngoài phạm vi: `src/founder_vn/cfo.py` không đổi (đúng, thuộc T05). Quyết định giữ mô hình thuế gộp được ghi là Q52 do operator quyết, nên không tính là quyết định tự đặt của lane. Không có `$`, không có tên người hay địa điểm dưới cấp quận trong `examples/`.

## Finding chặn

### SPEC-1: `cfo.md` nêu khẳng định pháp lý và con số luật mà không có link và ngày kiểm chứng ngay trong báo cáo

Criterion 2 và đầu ra "mọi số đều lần được về input Owner kiểm được". Trong `examples/barbershop/founder/cfo.md`:
- Mục "Lưu ý" (do công cụ in) vẫn nói thuế suất và ngưỡng "là số anh/chị nhập" và Owner phải tự đối chiếu. Với skill này hai số đến từ sổ nguồn, nên câu đó sai về nguồn gốc. Evidence ghi nhận điểm này nhưng để nguyên.
- Mục "Giới hạn của phần thuế" (phần skill nối) đưa ra các khẳng định pháp lý (20 triệu đồng, mốc 3 tỷ đồng, thuế suất 17%) và chỉ trỏ chung tới `permits/sources.md`. Không có link Công báo nào và không có ngày kiểm chứng trong file mà Owner đọc. Dòng "Doanh thu năm 1 ... Ngưỡng miễn thuế: 1.000.000.000 đ; thuế suất trên doanh thu: 7%" cũng không kèm văn bản căn cứ.

Vì sao chặn: ticket nói "a sourced sector tax rate and threshold ... every number traced to an input the Owner can check". Owner nhận `cfo.md` chứ không đọc `permits/sources.md`; số pháp lý không có link và ngày trong artefact là chưa lần được. Lane sửa được bằng cách đổi Step 6 của SKILL.md (và golden `cfo.md`, test tương ứng) để phần nối có tên văn bản, link và ngày kiểm chứng lấy từ mục sổ nguồn (không gõ từ trí nhớ), và nối thêm một dòng đính chính "Lưu ý" ghi hai số này lấy từ sổ nguồn. Không cần sửa `cfo.py`.

### SPEC-2: Tiêu chí 4, golden case chưa chạy trên Kiro CLI và checklist chưa qua

Criterion 4 đòi `/founder-cfo` chạy trên Kiro CLI sinh ra hai file, và review checklist đạt. Bằng chứng hiện có là test đọc văn bản chỉ dẫn (evidence tự ghi: "không kiểm hành vi của mô hình") cộng file do lane viết tay và công cụ sinh. Một criterion được đáp ứng bằng lời hứa làm sau thì chưa được đáp ứng. Lane không chạm được: nó cần một phiên Kiro CLI của operator và commit evidence riêng. Do đó trục Spec không thể PASS chừng nào chưa có phiên đó.

## Câu hỏi cho operator

- [ ] Tiêu chí 4 (chạy trên Kiro CLI, checklist qua) có được hoãn khỏi PR này sang một commit evidence sau (như evidence đề xuất, "trước T18"), hay PR này chỉ merge sau khi operator chạy `/founder-cfo` trên Kiro CLI và ghi kết quả vào `docs/evidence/issue-12-founder-cfo.md`? Design chưa quyết việc hoãn một acceptance criterion; lane không tự quyết.

## Chưa xác minh

- Nội dung pháp lý của hai mục sổ nguồn (số điều, trích đoạn, giá trị 7% và 1 tỷ đồng): không có quyền fetch Công báo ở lượt này; tin theo ghi "kiểm chứng ngày 23/11/2026 bởi operator". Không rà thông tư của Bộ Tài chính (sổ nguồn tự ghi).
- Lệnh `founder-vn cfo ... --out` chạy lại bằng tay trong sandbox trả mã 2 do tôi dùng đường dẫn `--out` tuyệt đối ngoài thư mục; không dùng làm bằng chứng. Việc golden `cfo.md` bắt đầu bằng đúng đầu ra công cụ dựa vào test golden đã chạy (xanh).
- Phần kiểm hành vi của mô hình (có hỏi chi phí đúng từ ngữ, có đọc cờ đúng không) chưa có bằng chứng nào ngoài văn bản skill.

<promise>BLOCKED</promise>
