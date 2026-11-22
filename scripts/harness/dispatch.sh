#!/bin/bash
# Frontier dispatcher (component C1 in docs/agents/kiro-harness.md). Deterministic: no model,
# no judgement. It gathers tracker state with `gh`, lets scripts/harness/frontier.jq decide, and
# applies the decision: relabel lanes that ended BLOCKED or never started, adopt a finished
# branch, then allocate and label one ticket. Ported from NHAN-AI-VN/nhan
# (scripts/harness/dispatch.sh at 8adef66b); base branch `main`, no migration timestamp.
#
# Usage: scripts/harness/dispatch.sh [--apply | --json] [--repo owner/name] [--wip N]
#   Dry run by default: prints the decision and the allocation comment, changes nothing.
#   --apply   relabels BLOCKED and stalled lanes, adopts finished branches, posts the `/kiro`
#             allocation comment, adds `kiro`.
#   --json    prints the decision alone, compact, and exits: the sweep of after-gate.yml reads it
#             to start a dispatcher run only when the decision would change something.
#   HARNESS_REPO, HARNESS_WIP and HARNESS_BASE are the environment equivalents (base: main).
#
# Two credentials on purpose. Reads, relabelling and the `kiro` label use whatever `gh` is
# logged in with (the workflow's GITHUB_TOKEN). The writes that start or resume a lane, the `/kiro`
# comment carrying the allocation and the pull request adopted for a finished branch (D24, so
# that a Gate run follows: a pull request opened with the workflow token starts none), use
# HARNESS_DISPATCH_TOKEN, a fine-grained token of the operator's own account: Kiro Web only takes
# orders from a connected person. nhan measured (M-1) that a `kiro` label added by
# github-actions[bot] starts nothing, which is what the label is for here: the harness's own
# in-flight marker; and (M-29) that a `kiro` label added by a person started TWO tasks every time,
# while a `/kiro` comment started exactly one (D13). Without the token `--apply` refuses to
# dispatch rather than marking a ticket nobody will pick up.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
apply=no
json=no
repo=${HARNESS_REPO:-}
wip=${HARNESS_WIP:-1}

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) apply=yes ;;
    --json) json=yes ;;
    --repo) shift; repo=$1 ;;
    --wip) shift; wip=$1 ;;
    -h|--help) sed -n '2,24p' "$0"; exit 0 ;;
    *) printf 'dispatch.sh: unknown argument %s\n' "$1" >&2; exit 64 ;;
  esac
  shift
done

if ! printf '%s' "$wip" | grep -Eq '^[1-9][0-9]*$'; then
  printf 'dispatch.sh: --wip must be a positive integer, got %s\n' "$wip" >&2
  exit 64
fi
if [ -z "$repo" ]; then
  repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
fi

# ---- gather ------------------------------------------------------------------------------
issues=$(gh api "repos/$repo/issues?state=open&per_page=100" --paginate \
  --jq '[.[] | select(.pull_request == null)
          | { number, title, labels: [.labels[].name], assignees: [.assignees[].login],
              subIssues: (.sub_issues_summary.total // 0) }]' \
  | jq -s 'add // []')

# What was gathered, on stderr: a run that reports "frontier is empty" must say what it read.
printf 'gathered %s open issues, %s labelled ready-for-agent\n' \
  "$(jq 'length' <<< "$issues")" "$(jq '[.[] | select(any(.labels[]; . == "ready-for-agent"))] | length' <<< "$issues")" >&2

# Native blocking edges for every candidate.
for n in $(jq -r '.[] | select(any(.labels[]; . == "ready-for-agent")) | .number' <<< "$issues"); do
  blocked=$(gh api "repos/$repo/issues/$n/dependencies/blocked_by" --jq '[.[] | { number, state }]')
  issues=$(jq --argjson n "$n" --argjson b "$blocked" \
    'map(if .number == $n then . + { blockedBy: $b } else . end)' <<< "$issues")
done

# For every lane in flight: the last comment (BLOCKED signal), when `kiro` was last added, how
# many allocation comments the dispatcher has posted, whether Kiro acknowledged the latest one
# (the first kiro-agent[bot] comment after it; the first one at all when the lane was labelled by
# hand), and when the lane branch last moved (no branch yet: null).
for n in $(jq -r '.[] | select(any(.labels[]; . == "kiro")) | .number' <<< "$issues"); do
  comments=$(gh api "repos/$repo/issues/$n/comments?per_page=100" --paginate \
    --jq '[.[] | { login: .user.login, created_at, body }]' | jq -s 'add // []')
  # D53: the signal is read from the last comment that is not Kiro's own. A lane posts its BLOCKED
  # report with the operator's token, and Kiro Web answers that comment within seconds with
  # "Taking a look…", so the very last comment hid the signal and the lane was never relabelled.
  last=$(jq -r '[ .[] | select(.login != "kiro-agent[bot]") ] | (last // {}) | .body // ""' <<< "$comments" | tail -n 40)
  dispatches=$(jq '[.[] | select(.body | contains("<!-- harness:allocation -->"))] | length' <<< "$comments")
  alloc_last=$(jq -r '[.[] | select(.body | contains("<!-- harness:allocation -->")) | .created_at] | last // ""' <<< "$comments")
  ack=$(jq -r --arg a "$alloc_last" '[.[] | select(.login == "kiro-agent[bot]" and .created_at > $a) | .created_at] | first // ""' <<< "$comments")
  # D38: Kiro's first reply can be an error ("Something went wrong while processing your request.
  # Please try again.") that opens no session; the dispatcher re-posts at once.
  ack_error=$(jq -r --arg a "$alloc_last" '[.[] | select(.login == "kiro-agent[bot]" and .created_at > $a) | .body] | first // "" | test("Something went wrong")' <<< "$comments")
  labeled=$(gh api "repos/$repo/issues/$n/timeline?per_page=100" --paginate \
    --jq '[.[] | select(.event == "labeled" and .label.name == "kiro") | .created_at] | last // ""' | grep -v '^$' | tail -1 || true)
  # gh prints the 404 body on stdout, so the assignment is guarded by the exit code, not the output.
  if ! pushed=$(gh api "repos/$repo/branches/lane/issue-$n" --jq '.commit.commit.committer.date // ""' 2>/dev/null); then pushed=""; fi
  # D39: did the latest allocation produce commits? A recall that moved the branch earns another.
  progress=false; if [ -n "$pushed" ] && [ -n "$alloc_last" ] && [ "$pushed" \> "$alloc_last" ]; then progress=true; fi
  issues=$(jq --argjson n "$n" --arg c "$last" --arg ack "$ack" --arg labeled "$labeled" --arg pushed "$pushed" --argjson d "$dispatches" --argjson err "$ack_error" --argjson prog "$progress" \
    'map(if .number == $n
         then . + { lastComment: $c,
                    dispatches: $d,
                    kiroAckAt: (if $ack == "" then null else $ack end),
                    kiroAckError: $err,
                    progressSinceDispatch: $prog,
                    labeledAt: (if $labeled == "" then null else $labeled end),
                    lanePushedAt: (if $pushed == "" then null else $pushed end) }
         else . end)' <<< "$issues")
done

prs=$(gh api "repos/$repo/pulls?state=open&per_page=100" --paginate \
  --jq '[.[] | { number, headRefName: .head.ref, body: (.body // "") }]' | jq -s 'add // []')

now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
base=${HARNESS_BASE:-main}

# D35: which candidates already have a lane branch. A recalled lane, or one a recall unlabelled
# while its session was merely paused, keeps its slot ahead of `priority` tickets.
lane_branches=$(gh api "repos/$repo/branches?per_page=100" --paginate --jq '[ .[] | .name | select(startswith("lane/issue-")) ]' 2>/dev/null | jq -s 'add // []')
issues=$(jq --argjson b "$lane_branches" 'map(. + { laneBranch: (("lane/issue-\(.number)") as $x | ($b | index($x)) != null) })' <<< "$issues")

# ---- adopt (D24) -------------------------------------------------------------------------
# For every lane in flight: is the branch finished and abandoned? scripts/harness/adopt.jq says
# yes when the branch is quiet, ahead of the base, has no pull request, and its evidence file
# records `gate-segment.sh verify` GREEN (D28). Then the dispatcher opens the pull request itself
# (below, under --apply) instead of waiting silent_after for a recall.
lanes='[]'
for n in $(jq -r '.[] | select(.labels | index("kiro")) | .number' <<< "$issues"); do
  br="lane/issue-$n"
  if ! cmp=$(gh api "repos/$repo/compare/$base...$br" 2>/dev/null); then cmp='{}'; fi
  pushed=$(jq -r '.commits[-1].commit.committer.date // ""' <<< "$cmp")
  head_sha=$(jq -r '.commits[-1].sha // ""' <<< "$cmp")
  ahead=$(jq '.ahead_by // 0' <<< "$cmp")
  files=$(jq -c '[.files[]?.filename]' <<< "$cmp")
  open_pr=$(jq --arg b "$br" '[.[] | select(.headRefName == $b) | .number] | first // null' <<< "$prs")
  ev_path=""; ev_text=""
  if [ -n "$pushed" ]; then
    ev_path=$(gh api "repos/$repo/contents/docs/evidence?ref=$br" --jq ".[] | select(.name | test(\"^issue-$n-.*\\\\.md\$\")) | .path" 2>/dev/null | head -1 || true)
    [ -n "$ev_path" ] && ev_text=$(gh api "repos/$repo/contents/$ev_path?ref=$br" --jq .content 2>/dev/null | base64 -d 2>/dev/null || true)
  fi
  lanes=$(jq --argjson n "$n" --arg b "$br" --arg p "$pushed" --arg h "$head_sha" --argjson a "$ahead" --argjson pr "$open_pr" --argjson f "$files" --arg ep "$ev_path" --arg et "$ev_text" \
    '. + [{ number: $n, branch: $b, pushedAt: (if $p == "" then null else $p end), headSha: (if $h == "" then null else $h end),
            ahead: $a, openPr: $pr, files: $f, evidence: (if $ep == "" then null else { path: $ep, text: $et } end) }]' <<< "$lanes")
done
adopt=$(jq -n --argjson lanes "$lanes" --arg now "$now" '{ lanes: $lanes, now: $now }' | jq -f "$here/adopt.jq")
adoptable=$(jq -c '[.[] | select(.adopt) | .number]' <<< "$adopt")
# D33: a lane whose branch already carries its evidence file is silent after a shorter quiet
# window (frontier.jq, evidence_quiet_after).
issues=$(jq --argjson lanes "$lanes" 'map(. as $i | . + { laneEvidence: any($lanes[]; .number == $i.number and .evidence != null) })' <<< "$issues")
if [ "$(jq 'length' <<< "$adopt")" -gt 0 ]; then
  printf 'adopt: %s\n' "$(jq -c '[.[] | { number, adopt, reasons }]' <<< "$adopt")" >&2
fi

input=$(jq -n --argjson issues "$issues" --argjson prs "$prs" --arg now "$now" --argjson wip "$wip" \
  '{ issues: $issues, prs: $prs, now: $now, wip: $wip }')

# ---- decide ------------------------------------------------------------------------------
decide() { jq -f "$here/frontier.jq" <<< "$input" | jq --argjson a "$adoptable" '. + { adopt: $a }'; }
decision=$(decide)

# D47: the listing above is eventually consistent (a ticket the merger just closed may still be
# listed as open). Before acting, read the pick itself (a single-issue GET is consistent): closed
# or already `kiro` drops it from the input and the frontier decides again, at most three times;
# a failed read dispatches nothing this run (the next sweep decides afresh) rather than the next
# ticket in line. A dry run keeps the listing's decision: nothing acts on it.
if [ "$apply" = yes ]; then
  for attempt in 1 2 3 4; do
    pick=$(jq -r '.pick // empty' <<< "$decision")
    [ -n "$pick" ] || break
    if [ "$attempt" = 4 ]; then
      printf 'dispatch.sh: three picks in a row were not dispatchable: dispatching nothing this run (D47)\n' >&2
      decision=$(jq '. + { pick: null, allocation: null, reason: "three picks were not dispatchable on a direct read (D47)" }' <<< "$decision")
      break
    fi
    live=$(gh api "repos/$repo/issues/$pick" --jq '{ state, labels: [ .labels[].name ] }' 2>/dev/null || printf '')
    if [ -z "$live" ]; then
      printf 'dispatch.sh: could not read #%s directly: dispatching nothing this run (D47)\n' "$pick" >&2
      decision=$(jq '. + { pick: null, allocation: null, reason: "direct read of the pick failed (D47)" }' <<< "$decision")
      break
    fi
    # D51: a pick this same decision recalls (reconcile `redispatch`) still carries `kiro` on the
    # direct read, because the apply section below removes the label right before the new
    # allocation; that label is expected, not a stale listing.
    dispatchable=$(jq -n --argjson pick "$pick" --argjson live "$live" --argjson d "$decision" \
      '{ pick: $pick, live: $live, reconcile: ($d.reconcile // []) }' | jq -f "$here/verify-pick.jq")
    if [ "$dispatchable" = true ]; then break; fi
    printf 'dispatch.sh: #%s is not dispatchable on a direct read (%s): dropped, deciding again (D47, attempt %s)\n' "$pick" "$(jq -c . <<< "$live")" "$attempt" >&2
    issues=$(jq --argjson n "$pick" '[ .[] | select(.number != $n) ]' <<< "$issues")
    input=$(jq --argjson issues "$issues" '.issues = $issues' <<< "$input")
    decision=$(decide)
  done
fi
if [ "$json" = yes ]; then jq -c . <<< "$decision"; exit 0; fi
printf '%s\n' "$decision"

render_allocation() {
  jq -r '.allocation
    | "/kiro Nhận ticket này: làm theo `.kiro/steering/lane-implement.md`; đầu vào là thân issue và cấp phát bên dưới.\n\n<!-- harness:allocation -->\n## Cấp phát của harness cho lane này\n\n| Khoá | Giá trị |\n|---|---|\n| singleOwnerFiles | \(.singleOwnerFiles) |\n| laneBranch | \(.laneBranch) |\n| targetBranch | \(.targetBranch) |\n| dispatchedAt | \(.dispatchedAt) |\n\nLane đọc `.kiro/steering/lane-implement.md` để biết cách dùng các giá trị này; ý nghĩa từng khoá ở `docs/agents/kiro-harness.md` mục 3. Comment này do `scripts/harness/dispatch.sh` ghi."' \
    <<< "$decision"
}

pick=$(jq -r '.pick // empty' <<< "$decision")
if [ -n "$pick" ]; then
  printf '\n--- allocation comment for #%s ---\n' "$pick"
  render_allocation
fi

# ---- dispatch-token preflight ------------------------------------------------------------
# Runs on every invocation, dry run included, so an expired or mis-scoped token is reported
# while the frontier is still empty rather than on the first real dispatch.
token_user=""
if [ -n "${HARNESS_DISPATCH_TOKEN:-}" ]; then
  if token_user=$(GH_TOKEN="$HARNESS_DISPATCH_TOKEN" gh api user --jq '.login' 2>/dev/null) && [ -n "$token_user" ]; then
    printf '\ndispatch token: authenticates as %s\n' "$token_user"
  else
    token_user=""
    printf '\ndispatch token: HARNESS_DISPATCH_TOKEN is set but GitHub rejected it (expired, revoked, or wrong scope)\n' >&2
  fi
else
  printf '\ndispatch token: HARNESS_DISPATCH_TOKEN is not set; --apply will refuse to dispatch\n'
fi

# ---- apply -------------------------------------------------------------------------------
if [ "$apply" != yes ]; then
  printf '\n(dry run: nothing changed; pass --apply to act)\n'
  exit 0
fi

# REST rather than `gh issue edit`, so the same calls work under a fine-grained token.
remove_label() { gh api --method DELETE "repos/$repo/issues/$1/labels/$2" >/dev/null 2>&1 || true; }
add_label()    { gh api --method POST "repos/$repo/issues/$1/labels" -f "labels[]=$2" >/dev/null; }
comment()      { gh api --method POST "repos/$repo/issues/$1/comments" -F body=@- >/dev/null; }

# Adoption first (D24): a lane whose pull request is opened here is in flight again, so the
# frontier is decided once more with that pull request before any recall below.
adopted=0
for n in $(jq -r '.[]' <<< "$adoptable"); do
  if [ -z "$token_user" ]; then
    printf 'dispatch.sh: not adopting #%s: no usable HARNESS_DISPATCH_TOKEN (a pull request opened with the workflow token starts no Gate run)\n' "$n" >&2
    continue
  fi
  lane=$(jq --argjson n "$n" '.[] | select(.number == $n)' <<< "$lanes")
  br=$(jq -r '.branch' <<< "$lane"); head_sha=$(jq -r '.headSha' <<< "$lane"); ev_path=$(jq -r '.evidence.path' <<< "$lane")
  title=$(jq -r --argjson n "$n" '.[] | select(.number == $n) | .title' <<< "$issues" | sed -E 's#^T[0-9]+ · ##')
  files_file=$(mktemp); jq -r '.files[]' <<< "$lane" > "$files_file"
  body_file=$(mktemp)
  jq -r '.evidence.text' <<< "$lane" | bash "$here/lane-pr-body.sh" "$n" "$title" "$ev_path" "${head_sha:0:8}" "$files_file" > "$body_file"
  rm -f "$files_file"
  if pr=$(GH_TOKEN="$HARNESS_DISPATCH_TOKEN" gh api --method POST "repos/$repo/pulls" -f title="#$n $title" -f head="$br" -f base="$base" -F body=@"$body_file" --jq '.number' 2>"$body_file.err"); then
    printf 'adopted #%s: opened pull request #%s from %s at %s (evidence %s)\n' "$n" "$pr" "$br" "${head_sha:0:8}" "$ev_path"
    prs=$(jq --argjson pr "$pr" --arg b "$br" '. + [{ number: $pr, headRefName: $b, body: "Closes #\($b | ltrimstr("lane/issue-"))" }]' <<< "$prs")
    adopted=$((adopted + 1))
  else
    # On a non-2xx status `gh api` prints the response body on stdout (now in $pr) and one summary
    # line on stderr; the body carries the reason (D24b).
    reason=$(jq -r -f "$here/api-error.jq" <<< "$pr" 2>/dev/null || true)
    [ -z "$reason" ] && reason=$(head -c 300 "$body_file.err")
    printf 'dispatch.sh: could not open the pull request for #%s: %s (the dispatch token needs Pull requests: write and Contents: read for D24)\n' "$n" "$reason" >&2
  fi
  rm -f "$body_file" "$body_file.err"
done
if [ "$adopted" -gt 0 ]; then
  input=$(jq -n --argjson issues "$issues" --argjson prs "$prs" --arg now "$now" --argjson wip "$wip" '{ issues: $issues, prs: $prs, now: $now, wip: $wip }')
  decision=$(jq -f "$here/frontier.jq" <<< "$input")
  pick=$(jq -r '.pick // empty' <<< "$decision")
  printf 'frontier decided again after adoption: %s\n' "$(jq -c '{ pick, reconcile }' <<< "$decision")"
fi

for n in $(jq -r '.reconcile[] | select(.action == "mark-blocked") | .number' <<< "$decision"); do
  remove_label "$n" kiro
  add_label "$n" harness:blocked
  printf 'relabelled #%s: kiro -> harness:blocked\n' "$n"
done

# The stall and silence windows have one home, frontier.jq; read them from there rather than restating them.
stall_seconds=$(sed -nE 's/^def stalled_after: ([0-9]+);.*/\1/p' "$here/frontier.jq")
silent_seconds=$(sed -nE 's/^def silent_after: ([0-9]+);.*/\1/p' "$here/frontier.jq")
for n in $(jq -r '.reconcile[] | select(.action == "mark-stalled") | .number' <<< "$decision"); do
  remove_label "$n" kiro
  add_label "$n" harness:stalled
  printf 'Harness: nhãn `kiro` đã gắn nhưng không có phản hồi nào từ `kiro-agent[bot]` sau %s phút, nên dispatcher đổi sang `harness:stalled` để ticket không bị đếm là đang chạy. Operator kiểm tra kết nối Kiro Web (repo có trong Settings > Agent > GitHub, credential dispatcher còn hạn) rồi gỡ nhãn để dispatcher thử lại.\n' \
    "$((stall_seconds / 60))" | comment "$n"
  printf 'relabelled #%s: kiro -> harness:stalled\n' "$n"
done

# A lane Kiro acknowledged and then left without a pull request: `kiro` comes off so the pick
# below can dispatch it again (a second `/kiro` comment resumes or restarts the session)…
for n in $(jq -r '.reconcile[] | select(.action == "redispatch") | .number' <<< "$decision"); do
  remove_label "$n" kiro
  printf 'relabelled #%s: kiro removed (no pull request %s minutes after Kiro acknowledged; eligible again)\n' "$n" "$((silent_seconds / 60))"
done
# …and the second silence parks it for the operator.
for n in $(jq -r '.reconcile[] | select(.action == "mark-silent") | .number' <<< "$decision"); do
  remove_label "$n" kiro
  add_label "$n" harness:stalled
  printf 'Harness: `kiro-agent[bot]` đã nhận ticket nhưng sau %s phút không có PR, nhánh hay comment kết thúc, và lần gọi lại cũng im lặng như vậy, nên dispatcher đổi sang `harness:stalled` để ticket không bị đếm là đang chạy. Operator xem session Kiro Web (link trong comment "Taking a look"), rồi gỡ nhãn để dispatcher thử lại.\n' \
    "$((silent_seconds / 60))" | comment "$n"
  printf 'relabelled #%s: kiro -> harness:stalled (silent twice)\n' "$n"
done

if [ -n "$pick" ]; then
  if [ -z "$token_user" ]; then
    printf 'dispatch.sh: refusing to dispatch #%s: no usable HARNESS_DISPATCH_TOKEN (see the preflight line above). Kiro Web only takes a `/kiro` comment from a connected person, so posting it with the workflow token would mark a ticket nobody picks up.\n' "$pick" >&2
    exit 78
  fi
  render_allocation | GH_TOKEN="$HARNESS_DISPATCH_TOKEN" comment "$pick"
  # Workflow token on purpose: Kiro ignores a bot-added label (nhan M-1), the comment above is the
  # one order; the label only marks the lane in flight for this dispatcher and the merger.
  add_label "$pick" kiro
  printf 'dispatched #%s\n' "$pick"
fi
