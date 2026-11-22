# Frontier decision for the dispatcher (component C1 in docs/agents/kiro-harness.md).
#
# Pure: reads one JSON document, writes one JSON decision, touches nothing. dispatch.sh gathers
# the input from the tracker and applies the decision; scripts/harness/witness.sh replays it over
# fixtures so every rule below has a case that goes red when the rule is removed. Ported from
# NHAN-AI-VN/nhan (scripts/harness/frontier.jq at 8adef66b); the windows below carry the
# measurements they were tuned on there, labelled [tiền nhiệm] in docs/agents/kiro-harness.md
# until this repository measures its own. Two changes: the target branch is `main`, and the
# allocation carries no migration timestamp (this project has no migrations).
#
# Input
#   { wip: number,
#     now: "RFC 3339 UTC",
#     issues: [ { number, title, labels: [name], assignees: [login],
#                 subIssues: number,                   -- GitHub sub-issues under it (a spec, never a lane)
#                 blockedBy: [ { number, state } ], lastComment: string,
#                 labeledAt: "RFC 3339 UTC" | null,   -- when the `kiro` label was last added
#                 kiroAckAt: "RFC 3339 UTC" | null,    -- first comment by kiro-agent[bot]
#                 kiroAckError: boolean,               -- that comment was Kiro's error reply (D38)
#                 progressSinceDispatch: boolean,      -- the branch moved after the latest allocation (D39)
#                 lanePushedAt: "RFC 3339 UTC" | null, -- committer date at the tip of lane/issue-<n>
#                 laneBranch: boolean,                 -- lane/issue-<n> exists on origin (D35)
#                 laneEvidence: boolean } ],           -- that branch carries docs/evidence/issue-<n>-*.md (D33)
#     prs:    [ { number, headRefName, body } ] }
#
# Output
#   { reconcile: [ { number, action } ],   -- mark-blocked: lane reported BLOCKED
#                                           -- mark-stalled: `kiro` label with no Kiro reply in time
#                                           -- redispatch / mark-silent: silent lane, first / second time
#     inFlight:  [ number ],               -- lanes still running (kiro label or open PR with Closes)
#     frontier:  [ number ],               -- dispatchable tickets: lanes with a branch first (D35), then
#                                             `priority` label (D32), then ticket order
#     pick:      number | null,
#     reason:    string,
#     allocation: { singleOwnerFiles, laneBranch, targetBranch, dispatchedAt } | null }

def target_branch: "main";

def has_label($l): any(.labels[]?; . == $l);

def blocked_signal: (.lastComment // "") | test("<promise>BLOCKED</promise>");

# nhan M-1 (2026-09-04): Kiro acknowledged a human-added label in 7 seconds and never reacted to
# a bot-added one; a `kiro` label nobody answers would otherwise count as in flight forever.
def stalled_after: 1800;

def stalled($now):
  has_label("kiro")
  and (.kiroAckAt == null)
  and (.labeledAt != null)
  and ((($now | fromdate) - (.labeledAt | fromdate)) > stalled_after);

def closes_numbers:
  [ .prs[] | (.body // "") | [ scan("(?i)(^|\\n)[ \\t]*(?:[-*][ \\t]+)?closes[ \\t]+#([0-9]+)") | .[1] | tonumber ] ] | add // [];

# nhan M-32/M-33/M-39: an acknowledged lane with no open pull request and no push for
# silent_after leaves the in-flight set: dispatched again once (`dispatches` counts the
# allocation comments; a second `/kiro` comment resumes or restarts the session), parked as
# harness:stalled the second time. kiroAckAt is the acknowledgement of the latest allocation, so
# the clock restarts. A lane whose branch moved within the window is working, not silent: the
# pull request is the outcome, the pushes are the pulse. 60 minutes: healthy lanes there pushed
# at least every 30 minutes and a recall on a live session only adds a message to it.
def silent_after: 3600;
def silent_retries: 1;
# nhan D33/D33b/D54: a branch that already carries the evidence file is a session that reached
# its last step and may have died there; a shorter quiet window is enough, the recall reopens the
# same session and it finishes in minutes. 45 minutes: live sessions went quiet for up to 50
# minutes while running the final gate and writing the evidence; a false recall costs a session.
def evidence_quiet_after: 2700;
def window: if (.laneEvidence // false) then evidence_quiet_after else silent_after end;

def silent($now; $closes):
  has_label("kiro")
  and (.kiroAckAt != null)
  and ((($now | fromdate) - (.kiroAckAt | fromdate)) > window)
  and (.lanePushedAt == null or ((($now | fromdate) - (.lanePushedAt | fromdate)) > window))
  and (.number as $n | $closes | index($n) | not);

# nhan D39: a recall that moved the branch earns another one (sessions die around minute 60
# whatever the lane's state), up to max_dispatches; a recall that produced nothing spends the
# single plain retry.
def max_dispatches: 4;
def retry_left:
  ((.dispatches // 1) <= silent_retries)
  or ((.progressSinceDispatch // false) and (.dispatches // 1) < max_dispatches);

# nhan D38: Kiro answered the allocation with "Something went wrong while processing your
# request. Please try again." That reply sometimes still opens a session, so the lane is
# dispatched again only when no branch has appeared error_ack_after seconds after it (once, like
# a silent lane; the second time it is marked silent), instead of after the hour of silent_after.
def error_ack_after: 900;
def failed_ack($now):
  has_label("kiro") and (.kiroAckAt != null) and (.kiroAckError // false)
  and (.lanePushedAt == null)
  and ((($now | fromdate) - (.kiroAckAt | fromdate)) > error_ack_after);

# Lanes that ended BLOCKED, never started, or went silent: they leave the in-flight set and get
# relabelled (a silent lane with a retry left only loses `kiro`, so this same pass can pick it).
def reconcile:
  .now as $now | closes_numbers as $closes
  | [ .issues[]
      | if has_label("kiro") and blocked_signal then { number, action: "mark-blocked" }
        elif stalled($now) then { number, action: "mark-stalled" }
        elif failed_ack($now) then { number, action: (if retry_left then "redispatch" else "mark-silent" end) }
        elif silent($now; $closes) then { number, action: (if retry_left then "redispatch" else "mark-silent" end) }
        else empty end ];

def in_flight:
  .now as $now | closes_numbers as $closes
  | ( [ .issues[]
        | select(has_label("kiro") and (blocked_signal | not) and (stalled($now) | not) and (failed_ack($now) | not) and (silent($now; $closes) | not))
        | .number ]
      + [ .issues[] | select(.number as $n | $closes | index($n)) | .number ] )
  | unique;

def open_blockers: [ (.blockedBy // [])[] | select(.state == "open") ] | length;

# An issue with sub-issues is a spec or a map, not a ticket: #1 of this repository carries
# `ready-for-agent` and no blocker, and the first dry run of the dispatcher (2026-11-22) picked it
# ahead of T01. The tracker's own structure says what it is; no label has to be kept in step.
def is_parent: (.subIssues // 0) > 0;

def frontier:
  .now as $now | closes_numbers as $closes
  | in_flight as $inflight
  | [ .issues[]
      | select(has_label("ready-for-agent"))
      | select(has_label("ready-for-human") | not)
      | select(is_parent | not)
      | select((has_label("kiro") | not) or ((silent($now; $closes) or failed_ack($now)) and retry_left))
      | select(has_label("harness:blocked") | not)
      | select(has_label("harness:stalled") | not)
      | select(has_label("wayfinder:map") | not)
      | select((.assignees // []) | length == 0)
      | select(open_blockers == 0)
      | select(.number as $n | $inflight | index($n) | not)
      | { number, resumed: (.laneBranch // false), priority: has_label("priority") } ]
  # nhan D35: a lane that already has a branch (recalled after a silence, or unlabelled by a
  # recall while its session was merely paused) keeps its slot ahead of everything, so a
  # `priority` ticket does not open a second lane beside it and conflict with it.
  # nhan D32: then a ticket the operator labels `priority`; among equals the lowest number.
  | sort_by((if .resumed then 0 else 1 end), (if .priority then 0 else 1 end), .number)
  | map(.number);

def allocation($n):
  { singleOwnerFiles: (if .wip == 1 then "all" else "none" end),
    laneBranch: "lane/issue-\($n)",
    targetBranch: target_branch,
    dispatchedAt: .now };

. as $root
| reconcile as $reconcile
| in_flight as $inflight
| frontier as $frontier
| (if ($inflight | length) >= .wip then null else ($frontier | first) end) as $pick
| { reconcile: $reconcile,
    inFlight: $inflight,
    frontier: $frontier,
    pick: $pick,
    reason: (if ($inflight | length) >= .wip then "wip limit \(.wip) reached by \($inflight)"
             elif $pick == null then "frontier is empty"
             else "dispatch #\($pick)" end),
    allocation: (if $pick == null then null else ($root | allocation($pick)) end) }
