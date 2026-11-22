# Merge decision for the machine merger (component C5 in docs/agents/kiro-harness.md).
#
# Pure: one JSON document in, one decision out. merge-check.sh gathers the input from GitHub and
# applies the decision; scripts/harness/witness.sh replays it over fixtures so every condition has
# a case that goes red when the condition is removed.
#
# Input
#   { operator: "login",                     -- the account allowed to label a harness PR
#     self: "job name",                      -- this workflow's own check run, ignored
#     ignore: [ "job name" ],                -- other harness job checks to ignore (the review
#                                               job: its outcome is the reports at HEAD, and its
#                                               check sits on the commit it started from)
#     pr: { number, headRef, headSha, body, author, draft, mergeable, labels: [name],
#           commits: [message] },             -- the commit messages of the pull request (M-42)
#     checks: [ { name, status, conclusion } ],           -- check runs at headSha
#     gate: { required, runs: [ { status, conclusion } ] }, -- Gate workflow runs at headSha, oldest first
#     ticket: { number, state, laneBranch,               -- the issue named by "Closes #n" ...
#               blockedBy: [ { number, state } ] } | null, -- ... and the issues it is blocked by (D18)
#     reports: { standards, spec, ledger,             -- file contents at headSha, or null
#                earlier: [string],                    -- earlier versions of the two reports
#                                                          (branch history: a round overwrites them)
#                current: { standards, spec } } }      -- written after the last commit that touched
#                                                          anything but the two report files (absent: true)
#
# Output
#   { kind: "lane" | "harness" | "none", ticket: number | null, merge: boolean, reasons: [string] }
#
# The four conditions of "Who merges" in docs/agents/delivery-workflow.md are the lane branch;
# the harness branch is decision D9 (docs/agents/kiro-harness.md §9).

def has_label($l): any(.pr.labels[]?; . == $l);

# `capture` yields nothing on no match, and an empty stream would silence the whole decision;
# collecting into an array turns "no match" into null.
# The keyword counts only at the start of a line (a list marker allowed): a description that
# quotes "Closes #3" mid-sentence is prose (measured 2026-09-05: the merger read harness PR #69
# as a lane of the closed ticket #3 and closed it, M-23).
def closes_or_null: [ (.pr.body // "") | capture("(?i)(^|\\n)[ \\t]*([-*][ \\t]+)?closes[ \\t]+#(?<n>[0-9]+)") | .n | tonumber ] | first // null;
def closes: closes_or_null;

def kind:
  if closes_or_null != null then "lane"
  elif has_label("harness:auto-merge") then "harness"
  else "none" end;

def signal($report): ($report // "") | split("\n") | map(select(length > 0)) | last // "";

# Line anchors are spelled (^|\n) rather than (?m)^ so the rule does not depend on which
# multiline convention the regex engine applies.
def finding_ids($report):
  [ ($report // "") | match("(^|\\n)(?:#{1,6}[ \\t]+|-[ \\t]+)(S[0-9]+|SPEC-[0-9]+)\\b"; "g") | .captures[1].string ]
  | unique;

# A ledger line may start with a list marker, as a report heading or bullet may in finding_ids
# (lane #216 wrote `- S1 FIXED — …` and was refused for it, D22); the id still opens the line.
def ledger_ids($ledger):
  [ ($ledger // "") | match("(^|\\n)(?:[-*][ \\t]+)?(S[0-9]+|SPEC-[0-9]+)[ \\t]+(FIXED|DEFERRED|NOT-A-DEFECT)\\b"; "g") | .captures[1].string ];

def ledger_title_names($ledger; $n):
  (($ledger // "") | split("\n") | map(select(length > 0)) | first // "")
  | test("^#[ \\t]+Review closure ledger[ \\t]+[—-][ \\t]+#\($n)\\b");

def bad_conclusion: ["failure", "cancelled", "timed_out", "action_required", "stale", "startup_failure"];

# The gate condition of "Who merges": when the gate workflow file (.github/workflows/gate.yml)
# is at HEAD or on the base branch, the latest run of that file at HEAD must be completed and
# successful. A head with no gate run at all is not green; a push made with GITHUB_TOKEN raises
# no event, so the review lane dispatches the gate. merge-check.sh finds the file and its runs.
# A run whose conclusion is action_required never executed: GitHub creates one for the
# pull_request event a harness push raises and parks it for approval (measured 2026-09-04 at
# b6f1521 of lane #3, four seconds after the run the lane had dispatched). It says nothing
# about the code, so the latest executed run decides.
def executed_runs: [ (.gate.runs // [])[] | select(.conclusion != "action_required") ];

def gate_reasons:
  (.gate // { required: false, runs: [] }) as $g
  | if ($g.required | not) then []
    else ( executed_runs | last ) as $run
      | [ (if $run == null then "Gate has not run at this commit" else empty end),
          (if $run != null and $run.status != "completed" then "Gate is still running at this commit" else empty end),
          (if $run != null and $run.status == "completed" and $run.conclusion != "success" then "Gate concluded \($run.conclusion // "unknown") at this commit" else empty end) ]
    end;

def own_checks: [ .self ] + (.ignore // []);

def common_reasons:
  own_checks as $own
  | gate_reasons
  + [ (if .pr.draft then "pull request is a draft" else empty end),
      (if .pr.mergeable != "MERGEABLE" then "mergeable state is \(.pr.mergeable // "unknown")" else empty end),
      ( [ .checks[]? | select(.name as $n | $own | index($n) | not) | select(.status != "completed") | .name ]
        | if length > 0 then "checks still running: \(join(", "))" else empty end ),
      ( [ .checks[]? | select(.name as $n | $own | index($n) | not) | select(.status == "completed") | select(.conclusion as $c | bad_conclusion | index($c)) | "\(.name)=\(.conclusion)" ]
        | if length > 0 then "failing checks: \(join(", "))" else empty end ) ];

# GitHub closes an issue when a closing keyword and "#n" reach the default branch in a commit
# message or in the description of a merged pull request, wherever they stand: mid-sentence, in
# backticks, in a quoted example (measured 2026-09-07: commit 8ed4b0b of harness PR #188 quoted
# `Closes #32` in prose; at the merge GitHub closed ticket #32, the merger then superseded lane
# PR #186 as the pull request of a closed ticket, and the dispatcher, with #32 gone from the
# in-flight set and from the open blockers of #33, dispatched #33 over a default branch without
# #32, nhan M-42). So a harness pull request carries no such reference at all, and a lane pull request
# names no issue but its own ticket (D18). The keyword list and the shape are GitHub's.
def closing_refs($text):
  [ ($text // "") | match("(?i)\\b(close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\\b:?[ \\t]+(?:[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)?#([0-9]+)"; "g")
    | .captures[1].string | tonumber ]
  | unique;
def closing_texts: [ (.pr.body // "") ] + (.pr.commits // []);
def closes_others($own): [ closing_texts[] | closing_refs(.)[] | select(. != $own) ] | unique;
def closes_others_text($own): closes_others($own) | map(tostring) | join(", #");

# The dispatcher only hands out a ticket whose blockers are closed; the merger asks again at the
# merge, when a blocker may have been reopened, or the ticket dispatched by mistake (M-42).
def open_blockers: [ (.ticket.blockedBy // [])[] | select(.state == "open") | .number ];

# Finding ids come from the latest reports and from every earlier round's report: a later round
# overwrites standards.md and spec.md, and the ledger must still account for what the earlier
# rounds found (measured 2026-09-04 on lane #3, round 2). A report also has to be current: written
# after the last commit that touched anything but the two report files, the rule the review
# orchestrator (review-web.jq) uses to start a round, so both components read one state.
def lane_reasons:
  closes as $n
  | .reports as $r
  | (finding_ids($r.standards) + finding_ids($r.spec) + ([ ($r.earlier // [])[] | finding_ids(.) ] | add // []) | unique) as $ids
  | [ (if .ticket == null then "issue #\($n) not found" else empty end),
      (if .ticket != null and .ticket.state != "open" then "issue #\($n) is \(.ticket.state)" else empty end),
      (if .ticket != null and .ticket.laneBranch == null then "issue #\($n) has no harness allocation" else empty end),
      (if .ticket != null and .ticket.laneBranch != null and .ticket.laneBranch != .pr.headRef then "head \(.pr.headRef) is not the allocated lane branch \(.ticket.laneBranch)" else empty end),
      (if (open_blockers | length) > 0 then "issue #\($n) is blocked by open #\(open_blockers | map(tostring) | join(", #"))" else empty end),
      (if (closes_others($n) | length) > 0 then "a commit or the description closes #\(closes_others_text($n)), not this lane's ticket #\($n)" else empty end),
      (if ($r.standards // "") == "" then "reviews/issue-\($n)/standards.md is missing or empty" else empty end),
      (if ($r.spec // "") == "" then "reviews/issue-\($n)/spec.md is missing or empty" else empty end),
      (if ($r.standards // "") != "" and signal($r.standards) != "<promise>PASS</promise>" then "standards verdict is \(signal($r.standards))" else empty end),
      (if ($r.spec // "") != "" and signal($r.spec) != "<promise>PASS</promise>" then "spec verdict is \(signal($r.spec))" else empty end),
      (if $r.current.standards == false then "standards report predates the last code commit" else empty end),
      (if $r.current.spec == false then "spec report predates the last code commit" else empty end),
      (if ($ids | length) > 0 and ($r.ledger // "") == "" then "findings \($ids | join(", ")) recorded but reviews/issue-\($n)/ledger.md is missing" else empty end),
      # The ledger is read only for findings the harness reviews named. A lane may keep another
      # record at this path (the implement skill's own review step did on lane #8, M-28); while no
      # report, current or earlier, carries an identifier, the merger neither reads nor rejects it.
      (if ($ids | length) > 0 and ($r.ledger // "") != "" then
         ( (if (ledger_title_names($r.ledger; $n) | not) then "ledger title does not name #\($n)" else empty end),
           ( (ledger_ids($r.ledger)) as $l
             | ( ($ids - $l) as $missing | if ($missing | length) > 0 then "ledger misses \($missing | join(", "))" else empty end ),
               ( ($l - $ids) as $extra | if ($extra | length) > 0 then "ledger carries ids the reports never named: \($extra | join(", "))" else empty end ),
               ( ($l | length) as $count | if $count != ($l | unique | length) then "ledger has a duplicated id" else empty end ) ) )
       else empty end) ];

def harness_reasons:
  [ (if .pr.author != .operator then "author \(.pr.author) is not the operator \(.operator)" else empty end),
    (if (closes_others(null) | length) > 0 then "a commit or the description closes #\(closes_others_text(null)): a harness pull request must not close an issue (GitHub reads the keyword anywhere)" else empty end) ];

# A lane pull request whose ticket is already closed can never merge (the ticket closed through
# another pull request, or by hand); the merger closes it instead of leaving it open forever.
# Measured 2026-09-04: Kiro Web started several sessions for one label event.
def superseded: kind == "lane" and .ticket != null and .ticket.state != "open";

kind as $kind
| (if $kind == "lane" then (common_reasons + lane_reasons)
   elif $kind == "harness" then (common_reasons + harness_reasons)
   else ["neither a lane pull request (Closes #n) nor a harness pull request (harness:auto-merge)"] end) as $reasons
| { kind: $kind,
    ticket: (if $kind == "lane" then closes else null end),
    merge: ($kind != "none" and ($reasons | length) == 0),
    supersede: superseded,
    reasons: $reasons }
