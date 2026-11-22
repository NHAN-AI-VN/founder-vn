# verify-pick.jq: is the dispatcher's pick still dispatchable on a direct read of the issue?
# (D47, D51; scripts/harness/dispatch.sh --apply runs it before every allocation)
#
#   Input:  { pick: number,
#             live: { state: "open" | "closed", labels: [string] },   the single-issue GET
#             reconcile: [ { number, action } ] }                      the same decision's reconcile
#   Output: true | false
#
# The listing the frontier decides on is eventually consistent (D47): a ticket the merger just
# closed, or one another sweep just labelled `kiro`, is dropped here. A pick the same decision
# recalls (`redispatch`: the lane went silent without a pull request) still carries `kiro` on the
# direct read, because the apply section removes the label right before the new allocation; that
# label is expected, not stale (D51: #255 dropped, #256 dispatched beside it, 18:28Z 2026-09-12).
def open: .live.state == "open";
def clean: (.live.labels | index("kiro")) == null;
def recalled: .pick as $p | any((.reconcile // [])[]; .number == $p and .action == "redispatch");
open and (clean or recalled)
