# Trả lời của operator — review #16, vòng 2

Trả lời cho `reviews/issue-16/spec.md` (BLOCKED, commit mã đã chấm `1bfb3a3f1686`), finding SPEC-2 và câu hỏi "cho operator" trong đó. File này không phải báo cáo review; nó là đầu vào cho vòng review kế. Lượt Standards vòng 2 đã PASS ở cùng commit mã; S1 và SPEC-1 của vòng 1 đã đóng bằng lượt sửa (`0fcbe00`, `3aa6fdc`).

## Câu hỏi: chấp nhận golden case chạy bằng CLI gói, hay đòi một phiên Kiro CLI thật

- [x] **Chấp nhận golden case chạy bằng CLI gói `founder-vn` theo `SKILL.md` cho criterion 5.** Dòng criterion 5 trên ticket #16 được sửa cho khớp trong cùng lúc với commit này (thân issue, ghi ngày sửa và nguyên văn cũ); mã, test và các file ví dụ giữ như ở `3aa6fdc`.
- [ ] ~~Yêu cầu một phiên Kiro CLI thật với `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite`, chạy lại và đối chiếu `consumer.md`, `panel/`.~~ Không chọn.

## Căn cứ

- **Ticket này không thêm mã, lệnh CLI hay tool MCP nào.** Bốn tool panel (`panel_init`, `panel_run`, `job_status`, `panel_tally`) đã được T08 (#11) kiểm bằng golden file và test parity trong cổng `unit`. Phần của T15 là văn bản skill và các file ví dụ; `tests/test_consumer_skill.py` (13 test, chạy trong cổng `unit`) đọc văn bản skill và kiểm `customer.json` qua `panel.validate_customer`, các luật của `pitch.md`, số đếm của `panel/` và tính ẩn danh của ví dụ.
- **Điều golden case hiện có chứng minh:** các file sinh ra bằng cách làm theo `skills/founder-consumer/SKILL.md` từng bước; panel chạy trên model tham chiếu `gemini-3.5-flash-lite` (`docs/bakeoff/models.json`, khoá `"reference"`), ghi trong `examples/barbershop/founder/panel/panel.json` cùng hash prompt `7602aad4…c71c6`, seed 837740, `n` 20, `excluded` 0; 20 câu trả lời đều từ model, không câu nào do agent viết thay (bằng chứng, mục Giới hạn); checklist `docs/review-checklist.md` qua trên `consumer.md`, `pitch.md`, `customer.json`; reviewer Spec vòng 2 đối chiếu số trong `consumer.md` với `panel/results.md` và `results.json` và xác nhận criterion 1 đến 4.
- **Điều nó không chứng minh, và ai chứng minh thay:** một phiên Kiro CLI làm theo skill (xác nhận profile với chủ hộ, không trả lời thay buyer, đọc lại năm điểm). Spec #1 (dòng "Skills have no automated seam. Acceptance is manual and recorded: a full pipeline run on the golden case on Kiro CLI, Claude Code and Codex, plus the review checklist") và `docs/founder-vn-design.md` (mục kiểm chứng host: "pipeline đầy đủ trên case mẫu chỉ ở Kiro CLI, Claude Code, Codex", "kiểm chứng liên tục khi đổi mã chỉ trên Kiro + Claude Code") đặt lần chạy đó ở mức pipeline, không ở từng ticket skill. Trong hàng đợi, T18 (#19) là nơi ấy: "From an empty Kiro project, a Facilitator installs founder-vn, configures the model, and runs the six Wave A skills on a new case all the way to `business-plan.md`", criterion "Clean-install walkthrough executed on Kiro CLI and recorded (commands, time taken, friction); blocking defects fixed or filed". Phiên Kiro CLI của `founder-consumer` được chứng kiến ở đó, trên một case mới, cùng với năm skill còn lại.
- **Vì sao không chạy lại tại máy operator như #12 và #14:** hai lane đó đóng cùng nửa criterion bằng một lần chạy Kiro CLI của operator vì chúng kiểm những điều chỉ phiên thật mới lộ (phần nối sổ nguồn của `cfo.md`; ba memo và bản tổng kết của chủ toạ). Ở T15, phần "model trả lời" đã chạy trên model tham chiếu và nằm trong `panel/`; phần còn lại là hội thoại skill với chủ hộ, thứ T18 kiểm trên cả sáu skill liền mạch. Chạy riêng một lần nữa ở đây lặp lại việc của T18 mà không thêm bằng chứng nào T18 không có.
- Không có quyết định thiết kế mới: `docs/founder-vn-design.md` không đổi. Điều đổi là dòng criterion 5 của một ticket, do operator sửa trên ticket ấy.

## Dòng criterion 5 mới trên #16

> Golden case produced by following `SKILL.md` step by step, with the panel run through the package CLI (`founder-vn panel init` / `run` / `status` or `work` / `tally`) on the reference model, model name and prompt hash recorded in `panel/panel.json`: `customer.json`, `pitch.md` and `panel/` in the example directory (personas anonymised); review checklist passed. The Kiro CLI session of this skill is verified by the T18 (#19) clean-install walkthrough. *(Amended 2026-11-24 by the operator, answering SPEC-2 of review round 2. Original wording: "Golden case run on Kiro CLI with the reference model: `customer.json`, `pitch.md` and `panel/` in the example directory (personas anonymised); review checklist passed.")*

## Hệ quả cho bằng chứng

`docs/evidence/issue-16-founder-consumer.md`, mục Giới hạn, dòng đầu đổi từ "criterion 5 is not claimed as met" sang: criterion 5 (bản sửa) được đáp ứng bởi golden case hiện có; điều chưa chứng minh (phiên Kiro CLI tuân theo skill) ghi là giới hạn và trỏ tới T18 (#19). Mã, test, file ví dụ và khối cổng (`verify` GREEN trên `f72f9ab`, commit mã cuối `3aa6fdc`) không đổi.

## Ledger

`reviews/issue-16/ledger.md` được ghi lại toàn bộ trong cùng commit này: S1, SPEC-1 (đóng bằng lượt sửa vòng 1) và SPEC-2 (đóng bằng quyết định này) là ba mã finding của mọi vòng tới nay, và merger đòi ledger cho mọi mã từng được nêu (FV-D18). Lượt sửa, nếu có vòng sau, ghi lại toàn bộ file với đủ mã của mọi vòng.
