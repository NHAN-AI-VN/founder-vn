Commit mã đã chấm: 8105f044344d

# Review trục Spec, issue #12 (founder-cfo), vòng 1

**Phán quyết**: PASS. Cả bốn criterion của ticket được đáp ứng bằng bằng chứng đọc được trong repo. Không có finding chặn. Đã đối chiếu độc lập ở `8105f044344d`, không dựa vào báo cáo cũ (`7c6f852`, BLOCKED với SPEC-1 và SPEC-2).

Phạm vi: `git diff --stat origin/main...HEAD` (12 file: `skills/founder-cfo/SKILL.md`, `permits/sources.md`, golden `examples/barbershop/founder/{numbers.json,cfo.md}`, `tests/test_cfo_skill.py`, `tests/test_sources_ledger.py`, evidence, Q52 trong design, các file `reviews/issue-12/`) và 10 commit từ `origin/main`. `src/` không đổi (đúng, `cfo.py` thuộc T05). CI `Gate` ở `8105f044344d`: success (theo tin nhắn mở đầu). Đã chạy lại tại chỗ: `uv run python scripts/skill_lint.py` (2 skills, 4 example file, 0 finding) và `uv run pytest tests/test_cfo_skill.py tests/test_sources_ledger.py tests/test_golden_case.py -q` (27 passed). Các test này nằm trong cổng `unit`.

## Đối chiếu từng criterion

| # | Criterion | Kết quả | Bằng chứng |
|---|---|---|---|
| 1 | SKILL.md viết lại: chỉ dẫn tiếng Anh, mục protocol chung, đầu ra tiếng Việt, hỏi chi phí theo lời Owner (nguyên liệu, bao bì, phí app giao hàng, thuê mặt bằng, lương, điện nước) | Đạt | Đọc `skills/founder-cfo/SKILL.md`: mục Protocol (5 điều), Step 2 nêu đủ sáu nhóm từ ngữ, cấm hỏi "variable/fixed cost", "anh/chị", `35.000 đ`, cấm `$`. `skill_lint` xanh; test văn bản skill chạy trong `unit`. |
| 2 | Tra `tax_rate_on_revenue` theo ngành và `tax_free_threshold` kèm link chính thức và ngày kiểm chứng; ghi làm hai mục đầu của sổ nguồn theo CONTRIBUTING | Đạt | `permits/sources.md` (file mới): đúng hai mục `tax_rate_on_revenue` (7, GTGT 5% + TNCN 2%) và `tax_free_threshold` (1.000.000.000 đ), mỗi mục có link Công báo, số và ngày Công báo, điều khoản, trích đoạn, dòng "Xác nhận: kiểm chứng ngày 23/11/2026". `tests/test_sources_ledger.py` kiểm hình dạng. SKILL.md Step 3 buộc tra sổ, cấm gõ từ trí nhớ, có nhánh "chưa kiểm chứng". `numbers.json` giữ đúng hai giá trị (test golden). Phần giữa file và hai mục là bảng văn bản áp dụng làm mục lục nguồn, không phải mục khác. |
| 3 | Gọi `cfo_analyse` (MCP) hoặc `founder-vn cfo` (CLI); đọc cờ lại bằng tiếng Việt thường; câu miễn trừ | Đạt | SKILL.md Step 4 (cả hai đường gọi, what-if qua `price`/`volume`), Step 5 (đọc từng cờ, không phán quyết), Rules (câu miễn trừ cuối câu trả lời). Skill không tự tính (Protocol 3 và Rules). `cfo.md` có mục "Cảnh báo", "Lưu ý" và dòng miễn trừ cuối. |
| 4 | Chạy golden case trên Kiro CLI: `numbers.json` và `cfo.md` trong thư mục ví dụ; review checklist qua | Đạt (bằng chứng do operator ghi, xem "Chưa xác minh") | Hai file có trong `examples/barbershop/founder/`. `sha256sum` khớp bằng chứng: `cfo.md` `d426f5fb…2cd2` (81 dòng), `numbers.json` `bd39660d…029f`. `docs/evidence/issue-12-founder-cfo.md`, mục "Lượt chạy golden case trên Kiro CLI", ghi từng bước SKILL.md đã chạy, lệnh, giờ, model, hash SKILL.md. Đã tự kiểm checklist trên `cfo.md`: không `$` cạnh chữ số (regex không khớp), không tiếng Anh lọt vào phần Owner đọc (chỉ còn định danh file và số hiệu văn bản), xưng "anh/chị", mọi số pháp lý (7%, 1.000.000.000 đ, 20 triệu đồng, mốc 3 tỷ đồng, 17%) có sáu link Công báo và ngày kiểm chứng ngay trong file, miễn trừ có hai chỗ, cảnh báo panel không áp dụng (không có kết quả panel). Test golden đọc `cfo.md`: phần đầu phải bằng đúng đầu ra `cfo.run`, phần nối phải chứa mọi link của hai mục sổ nguồn. |

Giới hạn và điều ngoài phạm vi: `src/founder_vn/cfo.py` không đổi. Việc phần giới hạn thuế do skill nối vào `cfo.md` (Step 6) là hệ quả của Q52 (`docs/founder-vn-design.md`, mục Q52 do operator quyết), nên không tính là quyết định tự đặt của lane; ticket tách tỷ lệ thuế và thêm cờ mốc 3 tỷ đồng được ghi là ticket mới. Không có tên người hay địa điểm dưới cấp quận trong `examples/barbershop/`; tên case ghi rõ là tên gọi tạm. Không file một-chủ nào bị chạm (`pyproject.toml`, `uv.lock`, `README.md`, `src/founder_vn/__init__.py` không đổi).

Hai finding cũ đã được đóng, đã kiểm lại ở mã:
- Cũ SPEC-1 (`cfo.md` nêu số pháp lý không kèm link và ngày): Step 6 của SKILL.md giờ buộc chép tên văn bản, link, ngày và dòng "Xác nhận" từ sổ nguồn và mở bằng dòng đính chính mục "Lưu ý". `cfo.md` hiện có đủ sáu link và ngày. Hai test mới (`tests/test_cfo_skill.py`) giữ điều này và có bước đỏ ghi trong evidence.
- Cũ SPEC-2 (chưa chạy trên Kiro CLI): đã có lượt chạy ghi trong evidence, và câu hỏi cũ cho operator đã được trả lời trong `reviews/issue-12/operator-answer.md` (không hoãn, đóng ngay). Cả hai có dòng trong `reviews/issue-12/ledger.md`.

## Finding chặn

Không có.

## Chưa xác minh

- Lượt chạy Kiro CLI là tự ghi của operator: phiên không có transcript trong repo. Tôi kiểm được hash của hai file ra và sự nhất quán giữa các bước, không kiểm được rằng một phiên Kiro CLI thật đã sinh ra chúng. Evidence tự nêu các giới hạn: đọc skill bằng đường dẫn thay vì slash command sau `install`; một model, một host; Step 2 không có hỏi đáp thật (Owner trả lời "giữ nguyên"); đường MCP không chạy; phần chép nguồn ở Step 6 do một đoạn script làm, nên chưa chứng minh model tự chép đúng.
- Nội dung pháp lý của hai mục sổ nguồn (số điều, trích đoạn, 7% và 1 tỷ đồng, các văn bản 2026): không fetch Công báo ở lượt này; tin theo ghi "kiểm chứng ngày 23/11/2026 bởi operator". Sổ nguồn tự ghi không rà thông tư của Bộ Tài chính và hai ưu đãi tạm thời chưa kiểm chứng, nên không đưa vào mô hình.
- Hành vi của model (hỏi chi phí đúng từ ngữ, đọc cờ đúng) chỉ có bằng chứng ở dạng văn bản skill và test đọc văn bản, không có phép đo hành vi.
- Mục "Lưu ý" do công cụ in vẫn nói thuế suất và ngưỡng là "số anh/chị nhập"; phần nối đính chính ngay sau. Không phải finding vì sửa công cụ thuộc T05 và Q52 đã ghi nhận.

<promise>PASS</promise>
