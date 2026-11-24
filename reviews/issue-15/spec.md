Commit mã đã chấm: f456a55d18d9

# Review trục Spec, issue #15, vòng 1

**Phán quyết: PASS.** Không có finding chặn.

Phạm vi: `git diff --stat main...HEAD` (22 file) và `git log --oneline main..HEAD`. Đã đọc `docs/bakeoff/*`, `README.md`, `docs/hosts/*`, `docs/evidence/issue-15-model-bakeoff.md`, `scripts/bakeoff.py` và test liên quan. Đã chạy `uv run pytest -q tests/test_bakeoff.py tests/test_llm.py`: 15 passed. `tests/test_bakeoff.py` nằm trong `uv run pytest -q` của cổng Gate (`.github/workflows/gate.yml:88`), và Gate xanh ở commit này.

## Đối chiếu từng criterion

1. **5 persona từ hồ sơ khách của case mẫu, 3 mô hình qua client OpenAI-compatible, so trên giọng Việt, trung thực, tỉ lệ JSON hợp lệ, độ trễ, chi phí mỗi người mua: đáp ứng.**
   - `docs/bakeoff/customer.json` rút từ đoạn "Cho ai" của `examples/barbershop/founder/idea.md`. `scripts/bakeoff.py` chia persona bằng `founder_vn.panel.deal`, hỏi bằng brief của chính panel, và kiểm JSON như panel.
   - `docs/bakeoff/results.json` có 3 mô hình, 5 cuộc gọi mỗi mô hình, với `json_valid_rate`, `mean_seconds`, `mean_cost_usd_per_buyer`, token. Số trong bảng `docs/bakeoff/README.md` khớp `results.json`: 3.1 là 5/5, 1,57 s, 0,000447 USD; 3.5 là 5/5, 1,40 s, 0,000632 USD.
   - `replies.md` có cả hai bên. `scores.json` có điểm giọng và trung thực (3/3 so với 4/4) kèm ghi chú theo từng persona.
   - `gemini-3.8-flash` trả 0/5 ở hai lần chạy (503, timeout, 429), được ghi là không đánh giá được, không bịa số. Ticket yêu cầu chạy và so ba mô hình; mô hình thứ ba thất bại được ghi trung thực nên không coi là thiếu.
   - Giá có nguồn và ngày kiểm (`price_verified` 2026-11-24).
2. **Mô hình tham chiếu ghi trong README và docs host; `FOUNDER_LLM_MODEL` gợi ý đặt cạnh các biến môi trường: đáp ứng.**
   - `README.md` có mục "Model" mới và một dòng trong phần tiếng Việt.
   - `docs/hosts/README.md` và đủ sáu trang host (claude, codex, gemini, grok, kiro, kirocrew) đều nêu `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite` ngay cạnh đoạn nói về ba biến `FOUNDER_LLM_*`. `models.json` có `reference`.
3. **Ghi chú ngắn trong docs: đã thử gì, chọn gì, vì sao; nêu panel chỉ so sánh được giữa các host khi dùng mô hình này: đáp ứng.**
   - `docs/bakeoff/README.md` có các mục "Chosen", "What was tried", "Why this one", "Limits", kèm bản tóm tắt tiếng Việt. Câu "comparable across hosts ... only when every run uses this model" in đậm, và có bản tiếng Việt.
   - Không có `$` hay tiền VND sai định dạng trong artefact này (giá ghi USD, đúng bản chất giá API).

Không có hành vi vượt phạm vi: thay đổi ở `src/founder_vn/llm.py` (`complete_with_usage`), `panel.py` (chỉ comment) và `tests/conftest.py` đều phục vụ bake-off hoặc sửa test flaky có ghi lý do, không đổi hành vi panel. Không có artefact chủ hộ trong diff, và không có dữ liệu cá nhân thật (persona do `deal` sinh).

## Chưa xác minh (không gắn mã, không chặn)

- Quyết định chọn của chủ dự án và việc giá được dán vào session lane (2026-11-24) chỉ có trong lời văn của file. Review này không có cách đối chiếu phiên ngoài repo.
- Ticket cần "phán đoán giọng Việt của chủ dự án"; điểm giọng và trung thực do một model làm giám khảo mù (A/B), chủ dự án chọn sau khi đọc `replies.md`. File ghi rõ giới hạn này. Nếu operator muốn chủ dự án tự chấm cột giọng, đó là quyết định của operator.
- Tên model `gemini-3.x` và giá không kiểm được độc lập từ sandbox này; chỉ tin vào `results.json` do script ghi.
- Mẫu nhỏ (5 buyer, một lượt chạy mỗi mô hình); README đã tự nêu "không phải benchmark".

<promise>PASS</promise>
