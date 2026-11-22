# Lượt đồng bộ với nhánh đích

Pull request của lane này **không merge được**: nhánh đích đã đổi sau khi lane được cắt (một lane khác vừa merge) và hai bên sửa cùng chỗ. GitHub không chạy workflow `pull_request`, tức không chạy `Gate`, trên một pull request đang xung đột, nên không lượt review hay lượt sửa nào tới được cho tới khi nhánh lane mang nhánh đích hiện hành. Việc của lượt này chỉ là **đưa nhánh đích vào nhánh lane và làm gate xanh lại**: không làm lại slice, không sửa finding, không đi tìm việc mới.

Tin nhắn mở đầu cho bạn số issue `N`, nhánh đích, nhánh lane và HEAD lúc ra lệnh. Đọc `AGENTS.md`, `docs/agents/evidence-gates.md` và `docs/agents/parallel-lanes.md` bằng đường dẫn trước khi sửa bất cứ gì.

## Việc cần làm

1. `git fetch origin <đích>` rồi `git merge origin/<đích>`: **một commit merge**. Không rebase, không viết lại lịch sử, không force-push: hook post-commit push commit merge như mọi commit khác, và lịch sử có sẵn của nhánh là thứ hai lượt review đã đọc.
2. Giải quyết xung đột giữ cả hai ý định. Mã trên nhánh đích đã qua review và merge: giữ nguyên hành vi của nó, kể cả khi nó đổi API mà lane dùng (khi ấy sửa phía lane cho khớp). Phần của lane giữ theo ticket. `uv.lock` xung đột thì lấy bản của nhánh đích rồi chạy `uv lock` để lock khớp `pyproject.toml` đã hợp nhất; đọc lại diff của lock trước khi commit. Golden file xung đột thì chạy lại test để sinh đầu ra thật và giải thích trong commit message.
3. Chạy cổng ba đoạn như tin nhắn mở đầu chỉ dẫn và `gate-segment.sh verify` xanh ở HEAD sau merge. Đỏ thì sửa nguyên nhân gốc trong commit riêng, nêu trong message bước nào nó chữa; không nới test hay gate.
4. Diff ngoài commit merge chỉ chạm thứ cần cho gate xanh. Không mở PR mới, không đổi thân PR.

## Ràng buộc

- File một-chủ được cấp cho lane này không đổi (`docs/agents/parallel-lanes.md`); file trong danh sách mà không được cấp thì để nguyên, kể cả khi xung đột nằm ở đó: khi ấy lấy bản của nhánh đích.

## Tín hiệu

- `<promise>COMPLETE</promise>` khi nhánh lane chứa nhánh đích hiện hành, đã push, và ba đoạn gate xanh ở HEAD.
- `<promise>BLOCKED</promise>` kèm lý do khi xung đột chỉ giải được bằng file cấm hoặc bằng một quyết định thiết kế chưa có.

Tín hiệu không kết thúc việc kiểm chứng: `Gate` chạy trọn ở commit bạn push, rồi harness ra lệnh review lại nếu commit mã đã đổi.
