# Lượt sửa finding

Công việc trên nhánh này đã qua hai lượt review độc lập, **Standards** và **Spec**. Việc của lượt này là **làm `Gate` xanh và sửa những finding chặn mà hai lượt đó đã ghi ra**: không làm lại slice, không đi tìm finding mới. Lượt này được dispatch khi ít nhất một trục phát `CHANGES_REQUESTED`, **hoặc khi `Gate` đỏ ở HEAD** (khi đó có thể chưa có báo cáo nào, hoặc báo cáo đã cũ hơn commit mã); một trục `BLOCKED` không bao giờ tới đây.

Tin nhắn mở đầu cho bạn số issue `N`, nhánh đích, thư mục `reviews/issue-N/`, các lệnh gate chạy được trong môi trường này và giới hạn của nó. Đọc `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md` và `.kiro/steering/lane-implement.md` bằng đường dẫn trước khi sửa bất cứ gì.

## Finding phải sửa

`reviews/issue-N/standards.md` và `reviews/issue-N/spec.md` trong worktree. Trạng thái nhánh: `git diff --stat <đích>...HEAD` và `git log --oneline <đích>..HEAD`.

## Việc cần làm

1. `Gate` đỏ ở HEAD thì sửa nguyên nhân gốc trước, commit riêng, nêu trong message bước CI nào nó chữa; không nới test hay gate để xanh, không đổi golden file chỉ để khớp đầu ra sai. Rồi sửa từng finding chặn một, **commit riêng từng cái**, nêu trong commit message finding nào nó đóng. Lịch sử phải nói được cái gì đã đổi vì sao.
2. Một finding mà bạn xác minh được là **sai** thì không "sửa". Ghi rõ trong ledger và commit message rằng nó bị bác bỏ, kèm bằng chứng bác bỏ (dòng mã, mục tài liệu, kết quả lệnh).
3. **Ghi ledger** (khi hai báo cáo, hiện tại hay phiên bản trước, nêu mã finding nào) vào `reviews/issue-N/ledger.md`: dòng tiêu đề đầu tiên là `# Review closure ledger — #N …`, rồi đúng một dòng cho **mỗi** mã finding (`S1`, `SPEC-1`, …) xuất hiện trong hai báo cáo hiện tại **và** trong mọi phiên bản trước của hai file ấy trong lịch sử nhánh (`git log --oneline -- reviews/issue-N/standards.md reviews/issue-N/spec.md`, đọc bằng `git show <commit>:<file>`), dạng `<mã> <FIXED|DEFERRED|NOT-A-DEFECT> — <vì sao / commit nào>` (mã mở đầu dòng; một dấu `- ` hoặc `* ` trước mã được chấp nhận, ngoài ra không có gì khác trước mã). `DEFERRED` nêu lý do có tên và issue theo dõi; `NOT-A-DEFECT` nêu bằng chứng bác bỏ. Đây là luật ledger-closure của `docs/agents/evidence-gates.md`. Harness từ chối lane khi tiêu đề không nêu đúng issue này, khi thiếu một mã bất kỳ của bất kỳ vòng nào, hoặc khi có dòng mang mã mà không báo cáo nào nêu. Thư mục đã có thể chứa ledger của vòng sửa trước: **ghi lại toàn bộ file** với đủ mã của mọi vòng (giữ hoặc cập nhật dòng của vòng trước, thêm dòng của vòng này), không copy ledger của issue khác làm khuôn. Ledger đi **cùng lần push** với các commit sửa, trước bằng chứng cổng; harness coi commit chỉ chạm ledger hay hai báo cáo là commit báo cáo, còn **mọi commit khác** push sau lần push cuối mở thêm một vòng review nữa.
4. Chạy các lệnh gate như tin nhắn mở đầu chỉ dẫn (ba đoạn rồi `verify`) và xác nhận xanh, rồi push theo tin nhắn mở đầu; không mở PR mới. **Bằng chứng cổng phải đứng sau commit mã cuối cùng**: mọi commit chạm mã nguồn hay test push sau khối `## Cổng ba đoạn` của `docs/evidence/issue-N-*.md` (kể cả sửa lint, sửa một dòng) làm cổng ấy stale: chạy lại ba đoạn và `verify` tại HEAD mới, ghi lại khối cổng và một dòng `## Lát` cho commit ấy, rồi mới push lần cuối. Reviewer đọc SHA trong dòng `verify` và từ chối khi nó là tổ tiên của commit mã cuối.

Diff chỉ chạm thứ liên quan tới finding; một lượt sửa làm phình diff khiến merge tuần tự đắt hơn.

## Ràng buộc

- File một-chủ được cấp cho lane này là tập con của danh sách trong `docs/agents/parallel-lanes.md`; file trong danh sách mà không được cấp thì để nguyên, vì harness từ chối lane nếu bạn sửa, và một finding không sửa được vẫn tốt hơn một lane bị từ chối.
- Không đặt quyết định thiết kế mới để đóng một finding; finding đòi quyết định ấy là `BLOCKED`.
- Biến `FOUNDER_LLM_*` có thể có mặt trong sandbox: không in, không ghi giá trị vào bất cứ file nào.

## Tín hiệu

- `<promise>COMPLETE</promise>` khi mọi finding chặn đã được đóng hoặc bác bỏ có bằng chứng, và gate xanh.
- `<promise>BLOCKED</promise>` kèm lý do khi một finding chặn chỉ sửa được bằng file cấm, hoặc nó lộ ra một quyết định thiết kế chưa có.

Tín hiệu không kết thúc việc kiểm chứng: cổng CI chạy lại trọn ở commit cuối.
