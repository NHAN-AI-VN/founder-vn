---
inclusion: always
---

# Lane triển khai một ticket

Steering này áp cho một lượt chạy không người trông nhận đúng một ticket: một Kiro Web task sinh từ comment `/kiro` của dispatcher (nhãn `kiro` chỉ đánh dấu lane đang chạy), hoặc một lượt CLI do harness dispatch. Luật chung ở `AGENTS.md`. Nguồn luật chi tiết là `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`, `docs/agents/delivery-workflow.md` và `docs/agents/kiro-harness.md`: đọc các file đó bằng đường dẫn trước khi sửa bất cứ gì. Bản thiết kế là `docs/founder-vn-design.md`.

## Đầu vào của lane

1. **Ticket**: thân issue và mọi comment của nó. Tiêu chí chấp nhận là hợp đồng; `docs/founder-vn-design.md` là nguồn nó trỏ tới. Ticket T01–T19 chưa có mục `## Seam`: lane suy seam từ tiêu chí chấp nhận và ghi rõ là suy.
2. **Cấp phát của harness**: comment `/kiro` của dispatcher trên issue, chứa dòng `<!-- harness:allocation -->`. Nó cấp `singleOwnerFiles`, `laneBranch`, `targetBranch`, `dispatchedAt`.
3. **Nhánh**: làm trên `laneBranch` (dạng `lane/issue-<n>`) cắt từ `targetBranch` (`main`); khi diff, so với `targetBranch`. Nếu `origin/<laneBranch>` đã có (session được cấp phát lại sau khi im lặng), checkout nhánh ấy, rebase lên `targetBranch` hiện hành và tiếp tục; không cắt lại từ đầu.

## Ràng buộc

- `singleOwnerFiles` là tập con của danh sách "One owner per merge" trong `docs/agents/parallel-lanes.md` mà lane này được sửa (`all` là mọi file trong danh sách, `none` là không file nào). File trong danh sách mà không được cấp: dừng và BLOCKED thay vì sửa. File ngoài danh sách: sửa bình thường.
- Không đặt quyết định thiết kế mới. Ticket đụng một chỗ bản thiết kế chưa quyết (ví dụ tỷ lệ thuế cụ thể, nguồn pháp lý) thì ghi câu hỏi `- [ ]` lên issue và BLOCKED, không đoán.
- Biến môi trường `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL` có thể đã được đặt trong sandbox để chạy case mẫu: kiểm tra có mặt bằng `test -n`, **không bao giờ in, ghi hay chuyển giá trị** vào bằng chứng, log, fixture hay commit (`AGENTS.md` luật 8; guard chặn lệnh nêu tên key). Test đơn vị dùng fake provider, không gọi mạng. Khi một bước chạy mô hình thật (golden case của T11–T17), bằng chứng ghi **tên model** (`FOUNDER_LLM_MODEL`) và hash prompt, không ghi gì khác về cấu hình.

## Toolchain trong sandbox

- Sandbox Kiro Web (đo 2026-11-22, FV-M-6 trong `docs/agents/kiro-harness.md`): Python 3.11, `uv` có sẵn, git, jq, gh, internet mở, 8 CPU. Nếu một sandbox khác thiếu `uv`: `command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh` rồi `export PATH="$HOME/.local/bin:$PATH"`. `uv sync --frozen` dựng `.venv/` từ `uv.lock` (ticket đổi dependency thì `uv lock` và commit lock cùng commit).
- **Sandbox không nạp steering này, `AGENTS.md` hay skill vào ngữ cảnh của sub-agent** (FV-M-6): đọc `AGENTS.md` và file này bằng đường dẫn trước mọi việc; khi giao việc cho sub-agent, chép nguyên văn hai file và bảng cấp phát vào tin nhắn giao việc. **Guard `.kiro/hooks/guard.sh` không chạy trong sandbox** (FV-M-6): các luật nó thi hành trên CLI (không push `main`, không force-push, không merge, không nêu giá trị biến bí mật) ở đây là luật lane tự giữ; vi phạm là finding chặn của lượt review và GitHub từ chối push thẳng lên `main` khi nhánh được bảo vệ (H-8).
- `bash scripts/harness/install-hooks.sh` **trước lát đầu**: đặt `core.hooksPath` để hook `post-commit` push từng commit trên `lane/issue-*` và hook `pre-commit` chạy `ruff format --check` trên file `.py` đã stage.
- Chưa có `pyproject.toml` (chính ticket T01 tạo nó) thì các lệnh `uv run` chưa chạy được: lát đầu của T01 là dựng manifest và một test rỗng để cổng `unit` xanh, rồi mới tới hành vi.

## Cách làm

- Skill `implement` (`.kiro/skills/implement/SKILL.md`) dẫn skill `tdd` (`.kiro/skills/tdd/SKILL.md`) từng lát đỏ rồi xanh. Đọc hai file đó bằng đường dẫn: mô tả skill trong ngữ cảnh không phải thân skill.
- **Seam trước, mã sau.** Trước lát đầu tiên, commit riêng `docs/evidence/issue-<n>-<slug>.md` với mục `## Seam`: mỗi dòng một biên public sẽ test (module hay lệnh CLI/tool MCP, vì sao đó là seam), suy từ tiêu chí chấp nhận (ghi rõ là suy). Đó là "seam đã thống nhất" của skill `tdd` khi phiên không có người. Message: `seam: #<n> <slug>`.
- **Mỗi lát đỏ‑xanh là một commit, và mỗi commit push ngay** (hook `post-commit` làm việc này trên nhánh `lane/issue-*`; chưa cài hook thì `git push -u origin <laneBranch>` tay sau từng commit). Test làm đỏ và mã tối thiểu làm xanh, cùng một commit, không kèm gì khác; message `slice(<seam>): <hành vi>`. Mục `## Lát` của file bằng chứng ghi mỗi lát một dòng: tên test, dòng assertion lúc đỏ, lệnh chạy lại xanh. Commit chạm `src/` mà không chạm test của lát ấy là finding của lượt review Standards. Ngoài luật: commit chỉ chạm tài liệu, bằng chứng, cấu hình, golden file đã giải thích, lockfile.
- **Parity CLI↔MCP là một lát**, không phải việc cuối: tool MCP và lệnh CLI của cùng hàm xuất hiện cùng lát với test parity (`docs/agents/standards.md`).
- Refactor không nằm trong lát; lượt review nêu, lượt sửa làm.
- **Ngân sách một session khoảng 60 phút** (`docs/agents/kiro-harness.md`, kế thừa phép đo của `nhan`: session Kiro Web dừng không báo ở phút 55–66, thường ngay sau commit bằng chứng). Ba luật giữ lane trong ngân sách: (1) **không chạy cổng thăm dò trước lát đầu**: cài toolchain rồi bắt đầu ngay từ seam; (2) trong lát chỉ chạy đúng file test của lát (`uv run pytest tests/<file>.py -q`), không chạy cả bộ; (3) sau lát cuối đi thẳng: cổng ba đoạn, `verify`, commit bằng chứng, mở PR, không quay lại rà soát. Lane vượt ngân sách vẫn không mất gì nhờ push từng commit và harness gọi lại khi im lặng.
- Hai câu của skill `implement` bị lane ghi đè. **Không tự chạy `/code-review`**: review là hai lượt độc lập do harness dispatch sau khi PR mở; bước tự review của skill ghi vào mục `## Giải quyết review nội bộ` của file bằng chứng. **Commit lên `laneBranch`, push sau mỗi commit, rồi mở PR**; merge là việc của harness.
- **File tạm đặt trong cây repo** (`.harness/`, đã git-ignore), không đặt ở `/tmp`: sandbox không giữ `/tmp` từ lần gọi tool này sang lần sau (đo FV-M-6: file ghi vào `/tmp` ở một bước không còn ở bước sau), và file viết bằng tool soạn thảo có thể không thấy từ shell; output dài bị cắt, nên ghi ra file rồi `grep`.
- **Cổng tổng cuối, trước khi mở PR, chạy theo ba đoạn, mỗi đoạn một lệnh riêng** (cùng các bước của CI `Gate`, cùng thứ tự; một lượt tool có ngân sách thời gian):

  ```bash
  bash scripts/harness/gate-segment.sh static    # ruff check, ruff format --check, skill-lint
  bash scripts/harness/gate-segment.sh unit      # pytest
  bash scripts/harness/gate-segment.sh build     # uv build
  bash scripts/harness/gate-segment.sh verify    # ba đoạn exit 0 trên cùng HEAD
  ```

  Mỗi đoạn để log riêng `.harness/gate-<đoạn>.log` và một dòng trong `.harness/gate-segments.txt`; `verify` chỉ xanh khi cả ba đoạn exit 0 trên cùng HEAD, và output của nó là thứ bằng chứng trích (khối `## Cổng ba đoạn`). Đoạn đỏ thì sửa rồi chạy lại đúng đoạn ấy (và `verify`), không chạy lại cả ba. **Mỗi đoạn chạy đúng một lần**: số liệu cho bằng chứng đọc từ log (`grep -E 'passed|failed|All checks passed|Successfully built' .harness/gate-*.log`), không chạy lại cổng chỉ để chép output. Commit mã sau khối cổng làm cổng stale: chạy lại ba đoạn và `verify` ở HEAD mới trước khi mở PR.
- Đỏ thì sửa nguyên nhân rồi chạy lại. Gate, test và assertion giữ nguyên độ chặt. Golden file đổi thì commit message giải thích vì sao đầu ra đổi.

## Bằng chứng, trong repo chứ không trong câu trả lời

- `docs/evidence/issue-<n>-<slug>.md`: lệnh, phạm vi, kết quả, và mục **giới hạn** nêu thẳng những gì lane này không chứng minh. Hành vi mới có lượt đỏ được chứng kiến rồi xanh, theo `docs/agents/evidence-gates.md`.
- Lát thêm hoặc đổi một cổng: thêm test hay case witness đột biến cơ chế và đòi check tương ứng đỏ.
- Phát hiện chưa xử được: cắm dấu `⏳` vào file nguồn liên quan; commit message không phải nơi cất việc tồn đọng.
- `reviews/issue-<n>/` là của harness: hai báo cáo review và ledger của lượt sửa. Lane không ghi gì vào đó.

## Kết thúc lane

- **Hoàn thành**: mọi cổng chạy được đều xanh, bằng chứng đã commit, PR mở về `targetBranch` với `.github/PULL_REQUEST_TEMPLATE.md` điền đủ và dòng `Closes #<n>`; mục *Outcome* của PR kết bằng dòng `<promise>COMPLETE</promise>`.
  Mở PR bằng **một lệnh** trong shell, thân PR qua heredoc, không viết file body bằng tool soạn thảo (file ấy shell không thấy) và không dùng `gh pr create` (sandbox không có GraphQL):

  ```bash
  bash scripts/harness/open-lane-pr.sh <n> <<'EOF'
  ...template điền đủ, có dòng `Closes #<n>` và `<promise>COMPLETE</promise>`...
  EOF
  ```

  Script chỉ gọi `gh api` (REST), từ chối khi HEAD chưa lên origin, cây chưa sạch, thân thiếu hai dòng trên, và in lại số PR đã có thay vì mở PR thứ hai. Dòng cuối stdout là số PR.
- **Bị chặn**: comment lên issue gồm lý do, các câu hỏi dạng `- [ ]`, và dòng cuối `<promise>BLOCKED</promise>`; không mở PR nửa vời.
- Harness đọc tín hiệu fail-closed: không có tín hiệu nghĩa là chưa xong.
