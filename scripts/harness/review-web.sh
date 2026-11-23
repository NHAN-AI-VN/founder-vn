#!/bin/bash
# Review orchestrator (component C4 in docs/agents/kiro-harness.md; runs at the end of the Gate
# job on a pull request and in the job of .github/workflows/after-gate.yml). Deterministic: no
# model runs here. Ported from NHAN-AI-VN/nhan (scripts/harness/review-web.sh at 8adef66b)
# unchanged in logic; the message a turn receives is rendered by review-web-turn.sh, which is this
# repository's. For one lane pull request it gathers the state of the lane branch at HEAD, asks
# scripts/harness/review-web.jq for the next step, and with --apply performs it: it posts one
# `/kiro` comment per review axis (and one for the address turn) on a per-lane review issue, so a
# Kiro Web session does the model work on the lane branch and pushes (nhan M-13, M-16); it parks
# the ticket with harness:blocked when a turn answers BLOCKED, stalls, or the rounds are spent.
# Every push by a session raises real events, so the Gate runs at every HEAD and this script runs
# again; the merger (C5) reads the verdicts at HEAD as before. A pull request that conflicts with
# its target branch raises no Gate run at all (GitHub skips pull_request workflows on a
# conflicting pull request), so the sweep of after-gate.yml reaches it and this script posts the
# sync turn (D25): the session merges the target branch into the lane and pushes.
#
# Usage: scripts/harness/review-web.sh --pr N [--apply] [--repo owner/name]
#   Dry run by default: prints the gathered state and the decision, changes nothing.
#
# Credentials: GITHUB_TOKEN reads, comments on the pull request and moves labels;
# HARNESS_DISPATCH_TOKEN (the operator's fine-grained token, Issues read and write) opens the
# review issues and posts the `/kiro` comments, because Kiro Web reacts to a registered user, not
# to github-actions[bot] (M-1). Without it --apply refuses to post.
#
# Needs a git checkout of the repository (any branch) with network access to `origin`: the code
# commit and the report currency are read with git, not through the API.
set -euo pipefail
# Command substitutions run functions below; without this a failure inside `$( )` is silent (bash
# does not inherit errexit into them by default; measured on run 33944579346, M-19).
shopt -s inherit_errexit 2>/dev/null || true

here=$(cd "$(dirname "$0")" && pwd)
apply=no
pr=""
repo=${HARNESS_REPO:-}
gate_file=${HARNESS_GATE_FILE:-gate.yml}
enabled=${HARNESS_WEB_REVIEW:-on}
max_rounds=${HARNESS_MAX_ADDRESS_ROUNDS:-2}
max_attempts=${HARNESS_TURN_ATTEMPTS:-2}
# D42: 14, not 10. Two address rounds already take 8 distinct axis/round turns (3 review rounds
# of two axes, two address turns); the operator path (a commit on the lane, the park label
# removed) needs two more, and 10 refused exactly that round (lane #247, 2026-09-12).
max_turns=${HARNESS_MAX_TURNS:-14}
stale_minutes=${HARNESS_TURN_STALE_MINUTES:-120}
quiet_minutes=${HARNESS_QUIET_MINUTES:-10}
# FV-D17: a turn Kiro refused (session limit, error reply) is posted again after refused_minutes,
# at most refusals times for one code; the Gate tail waits these minutes out in its own run.
refused_minutes=${HARNESS_REFUSED_MINUTES:-5}
refusals=${HARNESS_TURN_REFUSALS:-6}
turn_label=${HARNESS_TURN_LABEL:-harness:turn}
prompts=${HARNESS_PROMPTS:-$here/../../.kiro/prompts}

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) apply=yes ;;
    --pr) shift; pr=$1 ;;
    --repo) shift; repo=$1 ;;
    -h|--help) sed -n '2,20p' "$0"; exit 0 ;;
    *) printf 'review-web.sh: unknown argument %s\n' "$1" >&2; exit 64 ;;
  esac
  shift
done
if [ -z "$pr" ]; then printf 'review-web.sh: pass --pr N\n' >&2; exit 64; fi
if [ -z "$repo" ]; then repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner); fi
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

# Progress goes to stderr: several functions below are read through `$( )`, and a log line on
# stdout would land in the value (run 33944579346 posted a comment to "issue #review-web: ...").
log() { printf 'review-web: %s\n' "$1" >&2; }
as_operator() { # run gh with the operator's token
  if [ -z "${HARNESS_DISPATCH_TOKEN:-}" ]; then printf 'review-web: HARNESS_DISPATCH_TOKEN is not set; cannot post as the operator\n' >&2; return 78; fi
  GH_TOKEN="$HARNESS_DISPATCH_TOKEN" gh "$@"
}

# ---- the pull request ----
prj=$(gh pr view "$pr" --repo "$repo" --json number,state,headRefName,headRefOid,baseRefName,body,isDraft,mergeable \
  --jq '{ number, state, headRef: .headRefName, head: .headRefOid, base: .baseRefName, body: (.body // ""), draft: .isDraft, mergeable }')
state=$(jq -r .state <<< "$prj"); head_ref=$(jq -r .headRef <<< "$prj"); head=$(jq -r .head <<< "$prj"); base=$(jq -r .base <<< "$prj")
if [ "$state" != OPEN ]; then log "#$pr is $state; nothing to orchestrate"; exit 0; fi
# GitHub computes mergeability lazily (UNKNOWN right after a push); a few short retries settle it,
# as in merge-check.sh. Still UNKNOWN afterwards reads as not conflicting (D25).
mergeable=$(jq -r '.mergeable // "UNKNOWN"' <<< "$prj"); tries=0
while [ "$mergeable" = UNKNOWN ] && [ "$tries" -lt 4 ]; do
  sleep 3; tries=$((tries + 1))
  mergeable=$(gh pr view "$pr" --repo "$repo" --json mergeable --jq '.mergeable // "UNKNOWN"' 2>/dev/null || printf 'UNKNOWN')
done
# The keyword counts only at the start of a line, as in merge.jq (M-23).
ticket=$(jq -r '.body | capture("(?i)(^|\\n)[ \\t]*([-*][ \\t]+)?closes[ \\t]+#(?<n>[0-9]+)") | .n' <<< "$prj" 2>/dev/null || true)
if [ -z "$ticket" ]; then log "#$pr carries no \"Closes #n\": not a lane pull request"; exit 0; fi
if [ "$(jq -r .draft <<< "$prj")" = true ]; then log "#$pr is a draft; waiting"; exit 0; fi
# Kiro Web has opened several pull requests for one label event (M-1b): only the earliest open one
# per ticket is reviewed; the merger closes the others when the ticket closes.
first=$(gh pr list --repo "$repo" --state open --json number,body \
  --jq "[ .[] | select((.body // \"\") | test(\"(?i)(^|\\\\n)[ \\\\t]*([-*][ \\\\t]+)?closes[ \\\\t]+#$ticket([^0-9]|\$)\")) | .number ] | min")
if [ -n "$first" ] && [ "$first" != "$pr" ]; then log "#$pr duplicates lane of #$first for ticket #$ticket; only the earliest is reviewed"; exit 0; fi
dir="reviews/issue-$ticket"

# ---- the branch, with git ----
git fetch -q origin "$base" "$head_ref" 2>/dev/null || git fetch -q origin "$base" "$head_ref"
if ! git cat-file -e "$head^{commit}" 2>/dev/null; then log "head $head of #$pr not reachable after fetch"; exit 65; fi
base_sha=$(git rev-parse "origin/$base")
# The code commit (lane-code.sh): the last one at HEAD that touched anything but the lane's two
# report files and its ledger. A report is current only when it was written after it, so a fix, an
# operator's answer file or a harness probe all call for a new review round; a report or a ledger
# commit never does (D40).
code=$(bash "$here/lane-code.sh" "$base_sha" "$head" "$dir")

report_state() { # $1 axis -> JSON { current, signal }
  local c current=false signal=""
  if git cat-file -e "$head:$dir/$1.md" 2>/dev/null; then
    c=$(git log -1 --format=%H "$head" -- "$dir/$1.md")
    if [ "$c" != "$code" ] && git merge-base --is-ancestor "$code" "$c" 2>/dev/null; then current=true; fi
    signal=$(git show "$head:$dir/$1.md" | awk 'NF { l = $0 } END { print l }')
  fi
  jq -n --argjson cur "$current" --arg s "$signal" '{ current: $cur, signal: $s }'
}
standards=$(report_state standards); spec=$(report_state spec)

# ---- the gate at HEAD (by file and path, M-8; executed runs only, M-10) ----
gate_required=false; gate_run='{}'
if git cat-file -e "$head:.github/workflows/$gate_file" 2>/dev/null || git cat-file -e "origin/$base:.github/workflows/$gate_file" 2>/dev/null; then
  gate_required=true
  gate_run=$(gh api "repos/$repo/actions/runs?head_sha=$head&per_page=100" \
    --jq "[ .workflow_runs[] | select(.path == \".github/workflows/$gate_file\") | select(.conclusion != \"action_required\") ] | sort_by(.created_at) | last // {} | { id, status, conclusion, url: .html_url }" 2>/dev/null || printf '{}')
fi
# D31: this script may run as the last step of the Gate job itself; that run is still in progress
# in the API, so its outcome comes from the job (HARNESS_GATE_SELF_RUN = its id,
# HARNESS_GATE_SELF_CONCLUSION = success | failure). Any other run is read as before.
if [ -n "${HARNESS_GATE_SELF_RUN:-}" ] && [ "$(jq -r '.id // empty' <<< "$gate_run")" = "$HARNESS_GATE_SELF_RUN" ]; then
  gate_run=$(jq --arg c "${HARNESS_GATE_SELF_CONCLUSION:-failure}" '. + { status: "completed", conclusion: $c }' <<< "$gate_run")
fi
gate=$(jq -n --argjson r "$gate_required" --argjson run "$gate_run" '{ required: $r, status: ($run.status // null), conclusion: ($run.conclusion // null), id: ($run.id // null), url: ($run.url // null) }')

# ---- the review issues and the turns already posted ----
issues=$(gh api "repos/$repo/issues?labels=$turn_label&state=open&per_page=100" --paginate --jq '[ .[] | select(.pull_request == null) | { number, title } ]' 2>/dev/null || printf '[]')
issue_of() { # $1 axis -> issue number or empty
  jq -r --arg t "$(issue_title "$1")" '.[] | select(.title == $t) | .number' <<< "$issues" | head -1
}
issue_title() { # $1 axis
  case "$1" in
    standards) printf 'Review #%s — Standards' "$ticket" ;;
    spec) printf 'Review #%s — Spec' "$ticket" ;;
    # The sync turn (D25) is posted on the address issue: the same session that fixes the lane.
    address|sync) printf 'Review #%s — Address' "$ticket" ;;
  esac
}
turns='[]'
for axis in standards spec address; do
  n=$(issue_of "$axis")
  [ -n "$n" ] || continue
  # review-turns.jq reads the turns and, for each, Kiro's first reply: its session limit or its
  # error reply means no session exists and the turn is `refused` (FV-D17).
  comments=$(gh api "repos/$repo/issues/$n/comments?per_page=100" --paginate \
    --jq '[ .[] | { login: .user.login, created_at, body } ]' 2>/dev/null | jq -s 'add // []' 2>/dev/null) || comments='[]'
  t=$(jq -f "$here/review-turns.jq" <<< "$comments" 2>/dev/null) || t='[]'
  turns=$(jq --argjson t "$t" '. + $t' <<< "$turns")
done
turns=$(jq 'sort_by(.at)' <<< "$turns")

now=$(date -u +%Y-%m-%dT%H:%M:%SZ)
# When HEAD was committed (the session may still be pushing) and whether the ticket is parked (D30).
head_at=$(TZ=UTC git log -1 --date=format-local:%Y-%m-%dT%H:%M:%SZ --format=%cd "$head" 2>/dev/null || true)
parked=$(gh api "repos/$repo/issues/$ticket" --jq '[ .labels[].name ] | index("harness:blocked") != null' 2>/dev/null || printf 'false')
input=$(jq -n --argjson enabled "$([ "$enabled" = on ] && echo true || echo false)" --argjson ticket "$ticket" --arg head "$head" --arg code "$code" \
  --argjson gate "$gate" --argjson standards "$standards" --argjson spec "$spec" --argjson turns "$turns" --arg now "$now" \
  --argjson rounds "$max_rounds" --argjson attempts "$max_attempts" --argjson maxturns "$max_turns" --argjson stale "$stale_minutes" \
  --arg headAt "$head_at" --argjson parked "$parked" --argjson quiet "$quiet_minutes" --arg mergeable "$mergeable" \
  --argjson refusedmin "$refused_minutes" --argjson refusals "$refusals" \
  '{ enabled: $enabled, lane: { ticket: $ticket, head: $head, code: $code, headAt: (if $headAt == "" then null else $headAt end), parked: $parked, mergeable: $mergeable },
     gate: { required: $gate.required, status: $gate.status, conclusion: $gate.conclusion },
     reports: { standards: $standards, spec: $spec }, turns: $turns, now: $now,
     limits: { rounds: $rounds, attempts: $attempts, turns: $maxturns, stale_minutes: $stale, quiet_minutes: $quiet, refused_minutes: $refusedmin, refusals: $refusals } }')
decision=$(jq -f "$here/review-web.jq" <<< "$input")
log "#$pr (ticket #$ticket, $head_ref): head ${head:0:12}, code ${code:0:12}, gate $(jq -r '"\(.status // "none")/\(.conclusion // "-")"' <<< "$gate"), standards $(jq -r '"\(.current)/\(.signal)"' <<< "$standards"), spec $(jq -r '"\(.current)/\(.signal)"' <<< "$spec"), turns $(jq length <<< "$turns") ($(jq '[ .[] | select(.refused) ] | length' <<< "$turns") refused), head at ${head_at:-?}, parked $parked, mergeable $mergeable"
log "decision: $(jq -c . <<< "$decision")"
[ -z "${HARNESS_DECISION_FILE:-}" ] || printf '%s\n' "$decision" > "$HARNESS_DECISION_FILE"
action=$(jq -r .action <<< "$decision")
if [ "$apply" != yes ]; then log "(dry run: nothing posted; pass --apply to act)"; exit 0; fi
if [ -z "${HARNESS_DISPATCH_TOKEN:-}" ] && [ "$action" != wait ] && [ "$action" != off ] && [ "$action" != done ]; then
  printf 'review-web: HARNESS_DISPATCH_TOKEN is not set; refusing to act as the operator\n' >&2; exit 78
fi

# ---- apply ----
ci_summary() { # -> text for the message
  if [ "$gate_required" != true ]; then printf 'Repo chưa có workflow `%s`: không có kết quả CI ở HEAD; đừng kết luận gì từ việc đó.' "$gate_file"; return; fi
  local id st cc url self=""
  id=$(jq -r '.id // empty' <<< "$gate"); st=$(jq -r '.status // empty' <<< "$gate"); cc=$(jq -r '.conclusion // empty' <<< "$gate"); url=$(jq -r '.url // empty' <<< "$gate")
  if [ -z "$id" ]; then printf 'Chưa có run `Gate` nào ở HEAD này.'; return; fi
  # D31 again, for the job lines (FV-M-8): when this script is the tail of the Gate job itself, the
  # API still shows that job in_progress, and the message used to carry "Gate: in_progress" under
  # a run that said success; the reviewers of lane #7 filed it under "chưa xác minh" twice. The job
  # of the self-run reads as the outcome the workflow passed in (ci-jobs.jq), and its log, which
  # gh refuses to read before the run completes, is replaced by the gate commands of the sandbox.
  if [ -n "${HARNESS_GATE_SELF_RUN:-}" ] && [ "$id" = "$HARNESS_GATE_SELF_RUN" ]; then self=${HARNESS_GATE_SELF_CONCLUSION:-failure}; fi
  printf 'Run %s (%s): %s' "$id" "$url" "${cc:-$st}"
  gh api "repos/$repo/actions/runs/$id/jobs?per_page=100" 2>/dev/null | jq -r --arg self "$self" -f "$here/ci-jobs.jq" 2>/dev/null | sed '1s/^/\n/' || true
  if [ -n "$self" ]; then printf '\n\nKết quả của job `Gate` ở trên là của chính run này: bước đuôi của nó đang ghi tin nhắn này, nên API còn báo `in_progress`; `%s` là kết luận của các bước trước đó.' "$self"; fi
  # The session holds no GitHub credential, so the tail of the failed steps' log travels in the
  # message (colour codes, job/step prefixes and timestamps stripped; capped to keep the comment small).
  if [ "$cc" = failure ]; then
    if [ -n "$self" ]; then
      printf '\n\nLog của run này chưa đọc được khi nó còn chạy. Chạy lại `bash scripts/harness/gate-segment.sh static`, rồi `unit`, rồi `build` trong sandbox: cùng lệnh, cùng thứ tự với CI, lỗi của bước đỏ hiện ở đó.\n'
    else
      printf '\nTrích cuối log các bước đỏ (tối đa 80 dòng):\n\n```text\n'
      gh run view "$id" --repo "$repo" --log-failed 2>/dev/null \
        | perl -pe 's/\e\[[0-9;]*[A-Za-z]//g; s/\^\[\[[0-9;]*[A-Za-z]//g; s/^[^\t]*\t[^\t]*\t//; s/^\d{4}-\d\d-\d\dT[\d:.]+Z //' \
        | grep -vE '^[[:space:]]*$' | tail -80 | cut -c1-240 || true
      printf '```\n'
    fi
  fi
}
pr_comment() { # $1 body (stdin when -) -> posts on the pull request as the workflow
  gh api --method POST "repos/$repo/issues/$pr/comments" -F body=@- >/dev/null
}
pr_has_marker() { # $1 marker -> 0 when a comment on the pull request carries it
  # `gh api --jq` takes no --arg (measured 2026-09-04), so the marker is matched with grep.
  gh api "repos/$repo/issues/$pr/comments?per_page=100" --paginate --jq '.[].body' 2>/dev/null | grep -qF -- "$1"
}
ensure_issue() { # $1 axis -> issue number (opened as the operator when missing)
  local n title
  n=$(issue_of "$1")
  if [ -n "$n" ]; then printf '%s' "$n"; return; fi
  title=$(issue_title "$1")
  n=$(as_operator api --method POST "repos/$repo/issues" -f title="$title" -f "labels[]=$turn_label" \
    -f body="$(printf 'Issue kỹ thuật của harness cho lane của ticket #%s (PR #%s), không phải ticket sản phẩm; dispatcher bỏ qua vì không có nhãn `ready-for-agent`. Mỗi comment `/kiro` ở đây là một lượt do `scripts/harness/review-web.sh` ra lệnh; session Kiro Web làm việc trên nhánh `%s` và push lên đó. Merger đóng issue này khi PR lane merge. Quy tắc ở `docs/agents/kiro-harness.md` (C4).' "$ticket" "$pr" "$head_ref")" --jq .number)
  issues=$(jq --argjson n "$n" --arg t "$title" '. + [{ number: $n, title: $t }]' <<< "$issues")
  log "opened issue #$n ($title)"
  printf '%s' "$n"
}
post_turn() { # $1 axis, $2 round
  local n body ci_file ticket_file=""
  n=$(ensure_issue "$1")
  ci_file="$scratch/ci.md"; ci_summary > "$ci_file"
  if [ "$1" != standards ]; then
    ticket_file="$scratch/ticket.md"
    gh api "repos/$repo/issues/$ticket" --jq '.body // ""' > "$ticket_file"
  fi
  body="$scratch/turn-$1.md"
  bash "$here/review-web-turn.sh" "$1" "$ticket" "$base" "$head_ref" "$code" "$head" "$2" "$prompts" "$ci_file" $ticket_file > "$body"
  local id
  id=$(as_operator api --method POST "repos/$repo/issues/$n/comments" -F body=@"$body" --jq .id)
  if [ -z "$id" ]; then printf 'review-web: posting the %s turn on issue #%s failed\n' "$1" "$n" >&2; return 70; fi
  log "posted $1 turn (round $2, code ${code:0:12}) on issue #$n (comment $id)"
  printf '#%s' "$n"
}
park() { # $1 heading, $2 explanation -> one comment per code on the pull request; ticket parked
  local marker="<!-- harness:review-web park=$code -->"
  if ! pr_has_marker "$marker"; then
    printf '%s\n## Review lane cho #%s (ticket #%s): %s\n\nCommit mã đang xét: `%s`, HEAD `%s`.\n\n%s\n\n%s\n' "$marker" "$pr" "$ticket" "$1" "${code:0:12}" "${head:0:12}" \
      "$(jq -r '[.reasons[] | "- \(.)"] | join("\n")' <<< "$decision")" "$2" | pr_comment
  fi
  # harness:blocked replaces kiro (lifecycle, docs/agents/kiro-harness.md §2): Kiro Web reacts to
  # activity on an issue that still carries `kiro` (M-1c).
  gh api --method POST "repos/$repo/issues/$ticket/labels" -f 'labels[]=harness:blocked' >/dev/null
  gh api --method DELETE "repos/$repo/issues/$ticket/labels/kiro" >/dev/null 2>&1 || true
  log "ticket #$ticket parked with harness:blocked ($1)"
}

case "$action" in
  post|address|sync)
    round=$(jq -r .round <<< "$decision"); posted=""
    for axis in $(jq -r '.axes[]' <<< "$decision"); do posted="$posted $(post_turn "$axis" "$round")"; done
    printf '<!-- harness:review-web turn code=%s -->\nHarness ra lệnh lượt **%s** (vòng %s) cho commit mã `%s` trên issue review%s. Session Kiro Web push kết quả lên `%s`; harness đọc lại ở lần chạy sau.\n' \
      "$code" "$(jq -r '.axes | join(", ")' <<< "$decision")" "$round" "${code:0:12}" "$posted" "$head_ref" | pr_comment
    ;;
  done)
    marker="<!-- harness:review-web done=$head -->"
    if ! pr_has_marker "$marker"; then
      printf '%s\n## Review lane cho #%s (ticket #%s): PASS/PASS\n\nHai trục PASS ở HEAD `%s` (commit mã `%s`), sau %s vòng sửa. Merger máy quyết định phần còn lại (Gate ở HEAD, ledger).\n' \
        "$marker" "$pr" "$ticket" "${head:0:12}" "${code:0:12}" "$(jq -r .round <<< "$decision")" | pr_comment
      log "PASS/PASS at ${head:0:12}: noted on #$pr"
    else
      log "PASS/PASS at ${head:0:12}: already noted"
    fi
    ;;
  blocked)
    park "BLOCKED" "Câu hỏi \`- [ ]\` nằm trong báo cáo ở \`$dir/\` tại HEAD. Operator trả lời **bằng một commit trên nhánh lane** (file trả lời trong \`$dir/\`, hoặc sửa thẳng) rồi gỡ nhãn \`harness:blocked\` trên ticket; commit ấy dời commit mã nên harness ra lệnh vòng review mới." ;;
  exhausted)
    park "hết vòng sửa" "Còn finding chặn sau $max_rounds vòng sửa (điểm dừng theo thiết kế). Operator sửa hoặc bác bỏ bằng commit trên nhánh lane rồi gỡ nhãn \`harness:blocked\`; commit ấy dời commit mã nên harness ra lệnh vòng review mới." ;;
  stalled)
    if jq -e '.reasons | any(test("refused"))' <<< "$decision" >/dev/null 2>&1; then
      park "Kiro từ chối mở session" "Kiro Web trả lời $refusals lần ra lệnh bằng giới hạn session (\"You've reached your session limit\", trần 10 cloud session song song theo tài liệu) hay lỗi (\"Something went wrong\"), mỗi lần cách nhau ít nhất $refused_minutes phút, nên không có session nào làm lượt này (FV-D17). Kiểm tra và dừng các session còn chạy ở app.kiro.dev; sau đó commit bất kỳ trên nhánh lane và gỡ nhãn \`harness:blocked\` để harness ra lệnh lại."
    else
      park "lượt không trả lời" "Session Kiro Web không push gì sau $max_attempts lần ra lệnh (mỗi lần chờ $stale_minutes phút). Kiểm tra session ở app.kiro.dev; sau đó commit bất kỳ trên nhánh lane và gỡ nhãn \`harness:blocked\` để harness ra lệnh lại."
    fi ;;
  wait|off)
    log "nothing to post ($action)" ;;
  *)
    printf 'review-web.sh: unknown action %s\n' "$action" >&2; exit 70 ;;
esac
