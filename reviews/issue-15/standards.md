Commit mã đã chấm: f456a55d18d9

# Review trục Standards, issue #15, vòng 1

Phán quyết: **PASS**. Không có finding chặn.

## Phạm vi đã xét

`git diff --stat main...HEAD` (22 file, +1788/-19) và `git log --oneline main..HEAD` (17 commit). Đã đọc toàn bộ `src/founder_vn/llm.py`, `src/founder_vn/panel.py` (chỉ comment), `scripts/bakeoff.py`, `tests/conftest.py`, `tests/test_llm.py`, `docs/bakeoff/*`, `README.md`, `docs/hosts/*` và `docs/evidence/issue-15-model-bakeoff.md`. Đối chiếu với `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `CONTRIBUTING.md`, `docs/founder-vn-design.md` (Q42, bảng ticket) và `.kiro/skills/code-review/SKILL.md`. Không ADR nào bị chạm. Chạy lại ở HEAD: `pytest tests/test_bakeoff.py tests/test_llm.py tests/test_panel_run.py` 31 passed; `ruff check` sạch; `ruff format --check` sạch (153 file); `scripts/skill_lint.py` 0 finding.

## Các mục chuẩn đã kiểm

- Mạng trong test: mọi test mới dùng fake provider trên 127.0.0.1; `price_source` trong test là `example.invalid`. Không gọi mạng thật.
- Biến môi trường: không có giá trị `FOUNDER_LLM_*` trong `results.json`, `replies.md`, `scores.json` hay evidence (chỉ tên mô hình và prompt hash). Test khẳng định đầu ra không chứa endpoint hay khoá.
- Số mặc định thay cho lỗi: `load_models`, `load_scores`, `load_customer`, `load_pitch` báo lỗi nêu tên trường. Giá token nằm trong `models.json` với `price_source` và `price_verified` bắt buộc, không phải hằng trong mã. Không có tỷ lệ thuế hay ngưỡng pháp lý.
- Một client OpenAI-compatible: `complete_with_usage` nằm trong `llm.py`, `complete` bọc nó; body vẫn chỉ `model` + `messages` (test khẳng định).
- Ghi file: package không ghi thêm đường nào. Xem ghi chú 1.
- Parity CLI/MCP: không có phép tính mới cho Owner. Xem ghi chú 1.
- Skill/example: diff không chạm `skills/` hay `examples/`; checklist skill không áp dụng. Không có `$` cạnh chữ số trong `docs/bakeoff`, `README.md`, `docs/hosts`. Dữ liệu persona tổng hợp, địa danh ở mức quận cũ.
- Golden file: không golden file nào đổi (`results.json` và `replies.md` là dữ liệu đo, có commit giải thích).
- Tên và mã: `ask`, `summarise`, `render`, `load_*` làm đúng điều tên nói. `GIVEN_NAMES` chỉ thêm comment `⏳`, hành vi không đổi.

## Hình dạng vòng lặp

- (a) `27c2893 seam: #15 model-bakeoff` mang mục `## Seam` và đứng trước mọi commit `slice(`. Đạt.
- (b) `dc7228c` chạm `src/founder_vn/llm.py` cùng `tests/test_llm.py` và có dòng "llm usage" trong `## Lát`. `6df0a51` chạm `src/` mà không có test: chỉ thêm comment, thuộc ngoại lệ "documentation" của `docs/agents/standards.md` (Git). Các slice còn lại (`bakeoff`, `bakeoff-inputs`, `bakeoff-docs`) đều có test cùng commit và dòng trong `## Lát`. Đạt.
- (c) Test ở seam đã khai (`llm.complete_with_usage`, `bakeoff.run/main/load_*/render`, các tài liệu `docs/bakeoff/`), không với tới hàm nội bộ `_`. Đạt.
- (d) Khối `## Cổng ba đoạn` ghi `gate-segment verify: GREEN on 0c223496d00b…`. Commit mã cuối là `0c22349` (`tests/conftest.py`); `f456a55` chỉ đổi file evidence, nên cổng không stale. Đạt.

Bằng chứng đỏ rồi xanh có đủ cho hành vi mới. Hai test pass ngay lần đầu (retry, render) được ghi rõ kèm phép đột biến làm chúng đỏ. Flake `test_buyers_are_asked_in_waves_of_ten_concurrent_calls` được chẩn đoán (backlog 5 của socketserver), không chạy lại cho tới khi xanh.

## Ghi chú không chặn

1. `scripts/bakeoff.py` ghi `results.json` và `replies.md` bằng `write_text` vào thư mục do dòng lệnh chỉ định, và không có cặp CLI/MCP. `docs/agents/standards.md` viết "every file the package writes" và "no other code path opens a file for writing"; script nằm ngoài package, cạnh `skill_lint.py`, và đường dẫn do người vận hành chọn chứ không do mô hình. Tôi đọc chuẩn theo phạm vi ấy nên không coi là vi phạm. Lời khai nằm ở evidence ("Stated for the Standards review"), chưa ở `standards.md`. Đề nghị (không bắt buộc cho PASS): một PR riêng thêm một dòng vào `standards.md` về phạm vi của hai quy tắc này với `scripts/`, như đã làm cho installer.
2. Comment `⏳` ở `panel.GIVEN_NAMES` chuyển quyết định giới tính của persona cho T15. Không đổi hành vi, đúng phạm vi.

## Chưa xác minh

- Việc comment cấp phát `singleOwnerFiles: README.md` (2026-11-24) có tồn tại hay không: sandbox này không có quyền đọc GitHub API, và evidence tự khai. Cần merger hoặc operator đối chiếu trên issue #15. `README.md` là file một-chủ; nếu comment không có, đó là finding `BLOCKED`.
- Kết quả chạy thật trên Gemini (`results.json`, `scores.json`) do chủ dự án chạy trong shell riêng; tôi không tái hiện được và không xét độ đúng của số đo, chỉ xét hình dạng, chuẩn dữ liệu và việc không lộ cấu hình.
- Khối `## Cổng ba đoạn` đọc từ `.harness/gate-*.log` của worktree máy khác; `gate-segment.sh verify` không chạy lại được ở đây (không có `.harness/gate-segments.txt`). Phía CI, `Gate` run 45323530825 ở `f456a55d18d9` báo success.

<promise>PASS</promise>
