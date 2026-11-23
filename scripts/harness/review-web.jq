# Decision of the review orchestrator (component C4 in docs/agents/kiro-harness.md): the model
# turns run as Kiro Web sessions started by `/kiro` comments on per-lane review issues; this
# filter decides, from the state of the lane branch at HEAD, which single step comes next.
#
# Pure: one JSON document in, one decision out. review-web.sh gathers the input from GitHub and
# git and applies the decision; scripts/harness/witness.sh replays it over fixtures.
#
# Input
#   { enabled: boolean,                        -- HARNESS_WEB_REVIEW switch
#     lane: { ticket, head, code, headAt, parked, mergeable },
#                                              -- head sha; code = last commit at HEAD that touched
#                                                 anything but the two report files (a report is
#                                                 only current when it was written after it);
#                                                 headAt = committer date of HEAD (null: unknown);
#                                                 parked = ticket carries harness:blocked (D30);
#                                                 mergeable = MERGEABLE | CONFLICTING | UNKNOWN
#                                                 as GitHub reports it (D25; absent: unknown)
#     gate: { required, status, conclusion },  -- latest executed Gate run at HEAD (status null: none)
#     reports: { standards: { current, signal }, spec: { current, signal } },
#     turns: [ { axis, code, round, at, refused } ],
#                                              -- /kiro comments already posted, oldest first;
#                                                 refused = Kiro answered that comment with its
#                                                 session limit or its error reply, so no session
#                                                 exists (review-turns.jq, FV-D17)
#     now: "RFC 3339 UTC",
#     limits: { rounds, attempts, turns, stale_minutes, quiet_minutes, refused_minutes, refusals } }
#
# Output
#   { action: "off" | "wait" | "post" | "done" | "address" | "sync" | "blocked" | "exhausted" | "stalled",
#     axes: [ "standards" | "spec" | "address" | "sync" ], round: number, reasons: [string] }
#
#   post      start the review axes listed in `axes` (round = address rounds so far + 1)
#   address   start the address turn (round = its ordinal): findings to close, or a red Gate at HEAD
#   sync      the pull request conflicts with its target branch: GitHub raises no Gate run for a
#             conflicting pull request, so nothing below would ever move; the sync turn merges the
#             target branch into the lane (D25), and the next push starts the gate again
#   done      both axes PASS at HEAD: nothing to start, the merger (C5) decides
#   wait      a turn is pending, or the gate at HEAD has not completed or ended without a verdict,
#             or the last turn was an address/sync turn and HEAD moved less than quiet_minutes ago
#             (D41: the fix session pushes several commits minutes apart; a docs-only push ends
#             its Gate in under a minute, and a round posted on an intermediate commit is posted
#             again on the next one, lane #247 round 4 on 2026-09-12), or Kiro refused the last
#             post of a turn less than refused_minutes ago (FV-D17: the reason says "refused", and
#             the Gate tail keeps deciding until the turn is posted again)
#   blocked   an axis answered BLOCKED: the ticket goes to harness:blocked
#   exhausted the address rounds or the turn cap are spent with findings still open; a round is
#             one distinct code commit an address turn was posted for (a turn re-posted for the
#             same code after stale_minutes is the same round, D30), and a lane whose HEAD moved
#             less than quiet_minutes ago waits instead (the session may still be pushing)
#   off       the switch is off, or the ticket is parked with harness:blocked: an operator commit
#             and the label removed resume the review (D30)
#   stalled   a turn was posted `attempts` times for this code and nothing came back, or Kiro
#             refused it `refusals` times (FV-D17)
#
# Signals are read fail-closed: PASS approves, BLOCKED parks, anything else asks for changes.

def axes: ["standards", "spec"];

def signal($r): ($r.signal // "");
def verdict($r):
  if signal($r) == "<promise>PASS</promise>" then "pass"
  elif signal($r) == "<promise>BLOCKED</promise>" then "blocked"
  else "changes" end;

def minutes_since($in; $t): (($in.now | fromdate) - ($t | fromdate)) / 60;

# A refused post (FV-D17) opened no session and did no work: it counts toward neither the
# address rounds nor the turn cap, so the post that replaces it carries the same round number.
def served_turns($in): [ $in.turns[] | select((.refused // false) | not) ];
def address_rounds($in): [ served_turns($in)[] | select(.axis == "address") | .code ] | unique | length;

# D33: the turn cap counts distinct (axis, round) pairs: a turn re-posted for the same round (a
# stale re-post, D30; the pair posted for two commits thirty seconds apart, M-46, lane #334) is
# the same work; and a lane that already reads PASS/PASS at HEAD has nothing left to cap.
def axis_round: "\(.axis)/\(.round // 0)";
def turn_rounds($in): [ served_turns($in)[] | axis_round ] | unique | length;
def done_at_head($in):
  ($in.reports.standards.current // false) and ($in.reports.spec.current // false)
  and verdict($in.reports.standards) == "pass" and verdict($in.reports.spec) == "pass";

# HEAD moved less than quiet_minutes ago: the session may still be pushing (lane #228, M-49).
def settling($in): ($in.lane.headAt != null) and (minutes_since($in; $in.lane.headAt) < ($in.limits.quiet_minutes // 10));

# The last turn posted was an address or sync turn: its session answers with several pushes
# (fix commits, evidence, ledger), so a review round starts only once HEAD has been quiet.
def after_address($in): ([ $in.turns[] | select(.axis == "address" or .axis == "sync") ] | length) > 0 and (([ $in.turns[] ] | max_by(.at) | .axis) as $a | $a == "address" or $a == "sync");

# The address rounds are spent: park, unless the branch is still settling.
def spent($in; $why):
  if settling($in) then
    { action: "wait", axes: [], round: address_rounds($in),
      reasons: ["\($in.limits.rounds) address rounds spent but HEAD moved \(minutes_since($in; $in.lane.headAt) | floor) min ago: waiting for the branch to settle"] }
  else
    { action: "exhausted", axes: [], round: address_rounds($in), reasons: [$why] }
  end;

# One axis (or the address turn) that has no fresh result yet is in one of four states.
# FV-D17: a turn Kiro refused (its session limit or its error reply, review-turns.jq) opened no
# session, so it is never pending: it reads "refused" until refused_minutes have passed since the
# post, then "post" again. Refused posts do not count toward `attempts` (that cap is for a session
# that started and went silent), and `refusals` caps how many posts Kiro may refuse for one code
# before the turn reads as stalled and the lane is parked.
def turns_of($in; $axis): [ $in.turns[] | select(.axis == $axis and .code == $in.lane.code) ];
def refused_minutes($in): ($in.limits.refused_minutes // 5);
def attempt_state($in; $axis):
  turns_of($in; $axis) as $t
  | [ $t[] | select(.refused // false) ] as $refused
  | [ $t[] | select((.refused // false) | not) ] as $served
  | if ($t | length) == 0 then "post"
    elif ($t[-1].refused // false) then
      if minutes_since($in; $t[-1].at) < refused_minutes($in) then "refused"
      elif ($refused | length) >= ($in.limits.refusals // 6) then "stalled"
      else "post" end
    elif minutes_since($in; $t[-1].at) < $in.limits.stale_minutes then "pending"
    elif ($served | length) >= $in.limits.attempts then "stalled"
    else "post" end;

# The reasons the states above are reported with. "refused" is load-bearing: the Gate tail keeps
# deciding while a reason carries it (gate.yml, FV-D17), as it does for "settling" (FV-D15).
def waiting($in; $axis; $state):
  if $state == "refused" then
    "\($axis) turn refused by Kiro at \($in.lane.code[0:12]) (session limit or error reply, \((refused_minutes($in) - (minutes_since($in; (turns_of($in; $axis) | last).at) | floor)) | tostring) min before it is posted again)"
  else "\($axis) turn pending at \($in.lane.code[0:12])" end;
def stalled_reason($in; $axis):
  (turns_of($in; $axis) | last) as $t
  | if ($t.refused // false) then "Kiro refused \([ turns_of($in; $axis)[] | select(.refused // false) ] | length) posts of the \($axis) turn at \($in.lane.code[0:12]) (session limit or error reply)"
    else "no \(if $axis == "address" then "commit" elif $axis == "sync" then "push" else "\($axis) report" end) after \($in.limits.attempts) \($axis) turns at \($in.lane.code[0:12])" end;

def decision:
  . as $in
  | $in.lane.code[0:12] as $code
  | if ($in.enabled | not) then { action: "off", axes: [], round: 0, reasons: ["HARNESS_WEB_REVIEW is off"] }
    elif ($in.lane.parked // false) then
      { action: "off", axes: [], round: address_rounds($in),
        reasons: ["ticket parked with harness:blocked: an operator commit on the lane and the label removed resume the review"] }
    elif turn_rounds($in) >= $in.limits.turns and (done_at_head($in) | not) then
      { action: "exhausted", axes: [], round: address_rounds($in), reasons: ["turn cap \($in.limits.turns) reached (\(turn_rounds($in)) distinct axis/round turns)"] }
    elif ($in.lane.mergeable // "") == "CONFLICTING" then
      # No pull_request run exists for a conflicting pull request (lane #219, M-47; PR #337 after
      # #338 merged, 2026-09-11), so the gate branch below would wait forever: the sync turn goes
      # first, on the address issue, and is retried like any other turn.
      attempt_state($in; "sync") as $s
      | if $s == "pending" or $s == "refused" then
          { action: "wait", axes: ["sync"], round: address_rounds($in), reasons: [waiting($in; "sync"; $s)] }
        elif $s == "stalled" then
          { action: "stalled", axes: ["sync"], round: address_rounds($in),
            reasons: [stalled_reason($in; "sync")] }
        else
          { action: "sync", axes: ["sync"], round: address_rounds($in),
            reasons: ["pull request conflicts with its target branch: no Gate runs until the lane carries the target"] }
        end
    elif $in.gate.required and $in.gate.status != "completed" then
      { action: "wait", axes: [], round: address_rounds($in),
        reasons: [ (if $in.gate.status == null then "Gate has not run at HEAD" else "Gate at HEAD is \($in.gate.status)" end) ] }
    elif $in.gate.required and $in.gate.conclusion != "success" then
      # A red Gate at HEAD has an actor before any verdict: the address turn fixes the code, even
      # when both reports already say PASS (otherwise nobody moves and the merger refuses forever).
      # Review turns already posted for this code finish first, so their findings join that turn.
      # A run that ended without a verdict (cancelled, timed out) waits for a rerun or the next push.
      if $in.gate.conclusion != "failure" then
        { action: "wait", axes: [], round: address_rounds($in),
          reasons: ["Gate at HEAD concluded \($in.gate.conclusion): a rerun or the next push continues"] }
      else
        [ axes[] | . as $a | select(((($in.reports[$a].current // false) | not) and (attempt_state($in; $a) | . == "pending" or . == "refused"))) ] as $pending
        | attempt_state($in; "address") as $s
        | if $s == "pending" or $s == "refused" then
            { action: "wait", axes: ["address"], round: address_rounds($in), reasons: [waiting($in; "address"; $s)] }
          elif $s == "stalled" then
            { action: "stalled", axes: ["address"], round: address_rounds($in),
              reasons: [stalled_reason($in; "address")] }
          elif ($pending | length) > 0 then
            { action: "wait", axes: $pending, round: address_rounds($in),
              reasons: [ $pending[] | . as $a | "Gate at HEAD is red; \(waiting($in; $a; attempt_state($in; $a))) joins the address turn" ] }
          elif address_rounds($in) >= $in.limits.rounds then
            spent($in; "Gate at HEAD is red after \($in.limits.rounds) address rounds")
          else
            { action: "address", axes: ["address"], round: (address_rounds($in) + 1),
              reasons: ["Gate at HEAD concluded failure"] }
          end
      end
    else
      [ axes[] | . as $a | select(($in.reports[$a].current // false) | not) ] as $missing
      | if ($missing | length) > 0 then
          [ $missing[] | . as $a | { axis: $a, state: attempt_state($in; $a) } ] as $states
          | [ $states[] | select(.state == "post") | .axis ] as $to_post
          | [ $states[] | select(.state == "stalled") | .axis ] as $stalled
          | [ $states[] | select(.state == "pending" or .state == "refused") | .axis ] as $pending
          | if ($stalled | length) > 0 then
              { action: "stalled", axes: $stalled, round: (address_rounds($in) + 1),
                reasons: [ $stalled[] | stalled_reason($in; .) ] }
            elif ($to_post | length) > 0 and after_address($in) and settling($in) then
              { action: "wait", axes: $to_post, round: (address_rounds($in) + 1),
                reasons: ["HEAD moved \(minutes_since($in; $in.lane.headAt) | floor) min ago after an address turn: settling before round \(address_rounds($in) + 1)"] }
            elif ($to_post | length) > 0 then
              { action: "post", axes: $to_post, round: (address_rounds($in) + 1),
                reasons: [ $to_post[] | "\(.) report missing or older than \($code)" ] }
            else
              { action: "wait", axes: $pending, round: (address_rounds($in) + 1),
                reasons: [ $states[] | select(.state == "pending" or .state == "refused") | waiting($in; .axis; .state) ] }
            end
        else
          [ axes[] | . as $a | verdict($in.reports[$a]) ] as $v
          | [ axes[] | . as $a | select(verdict($in.reports[$a]) == "blocked") ] as $blocked
          | [ axes[] | . as $a | select(verdict($in.reports[$a]) == "changes") ] as $changes
          | if ($v | all(. == "pass")) then
              { action: "done", axes: [], round: address_rounds($in), reasons: ["standards and spec PASS at HEAD"] }
            elif ($blocked | length) > 0 then
              { action: "blocked", axes: $blocked, round: address_rounds($in), reasons: [ $blocked[] | "\(.) answered BLOCKED" ] }
            else
              attempt_state($in; "address") as $s
              | if $s == "pending" or $s == "refused" then
                  { action: "wait", axes: ["address"], round: address_rounds($in), reasons: [waiting($in; "address"; $s)] }
                elif $s == "stalled" then
                  { action: "stalled", axes: ["address"], round: address_rounds($in),
                    reasons: [stalled_reason($in; "address")] }
                elif address_rounds($in) >= $in.limits.rounds then
                  spent($in; "\($in.limits.rounds) address rounds spent, findings still open")
                else
                  { action: "address", axes: ["address"], round: (address_rounds($in) + 1),
                    reasons: [ $changes[] | "\(.) asks for changes" ] }
                end
            end
        end
    end;

decision
