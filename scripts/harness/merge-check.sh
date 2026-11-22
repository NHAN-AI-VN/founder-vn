#!/bin/bash
# Machine merger (component C5 in docs/agents/kiro-harness.md; runs at the end of the Gate job
# on a pull request and in the job of .github/workflows/after-gate.yml). Deterministic: no model,
# no judgement. Ported from NHAN-AI-VN/nhan (scripts/harness/merge-check.sh at 8adef66b)
# unchanged in logic; the defaults name this repository's Gate job. For one pull request, or
# every open one, it gathers what scripts/harness/merge.jq needs, prints the decision, and with
# --apply merges the pull request that satisfies every condition, comments the decision table on
# it, closes the ticket and the lane's review issues, and re-runs the dispatcher.
#
# Usage: scripts/harness/merge-check.sh (--pr N | --all) [--apply] [--repo owner/name]
#   Dry run by default. Merges are sequential: --all stops after the first merge and leaves the
#   rest to the next run, so every later merge is evaluated against the new default branch.
#
# Credentials: everything runs under the workflow's GITHUB_TOKEN. A merge made with that token
# does not raise the `issues.closed` event that would wake the dispatcher, so this script runs
# the dispatcher inline (HARNESS_DISPATCH_INLINE=1) or dispatches the frontier workflow.
set -euo pipefail

here=$(cd "$(dirname "$0")" && pwd)
apply=no
mode=""
pr=""
repo=${HARNESS_REPO:-}
operator=${HARNESS_OPERATOR:-nhannguyen89}
self=${HARNESS_MERGE_JOB:-Gate}
review_job=${HARNESS_REVIEW_JOB:-Gate}   # the orchestrator's job: its check sits where it ran
gate_file=${HARNESS_GATE_FILE:-gate.yml}
turn_label=${HARNESS_TURN_LABEL:-harness:turn}

while [ $# -gt 0 ]; do
  case "$1" in
    --apply) apply=yes ;;
    --pr) shift; mode=one; pr=$1 ;;
    --all) mode=all ;;
    --repo) shift; repo=$1 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) printf 'merge-check.sh: unknown argument %s\n' "$1" >&2; exit 64 ;;
  esac
  shift
done
if [ -z "$mode" ]; then printf 'merge-check.sh: pass --pr N or --all\n' >&2; exit 64; fi
if [ -z "$repo" ]; then repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner); fi
scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

file_at() { # $1 path, $2 sha -> content or empty
  gh api "repos/$repo/contents/$1?ref=$2" --jq '.content' 2>/dev/null | base64 -d 2>/dev/null || true
}

pr_json() { # $1 pr number -> the pull request fields merge.jq reads
  gh pr view "$1" --repo "$repo" --json number,headRefName,headRefOid,baseRefName,body,author,isDraft,mergeable,labels \
    --jq '{ number, headRef: .headRefName, headSha: .headRefOid, baseRef: .baseRefName, body: (.body // ""), author: .author.login,
            draft: .isDraft, mergeable, labels: [.labels[].name] }'
}

gather() { # $1 pr number -> JSON input for merge.jq
  local n=$1 prj checks ticket closes reports sha ref base tries=0
  prj=$(pr_json "$n")
  # GitHub recomputes mergeability for a few seconds after the base moves (the merge of another
  # pull request, M-40): UNKNOWN then is transient, and a refusal now would wait for the next
  # event, which may be hours away. Ask again a few times before deciding.
  while [ "$(jq -r '.mergeable' <<< "$prj")" = "UNKNOWN" ] && [ "$tries" -lt 4 ]; do
    tries=$((tries + 1)); sleep 5
    prj=$(pr_json "$n")
  done
  # The commit messages travel with the pull request: GitHub reads closing keywords in them at
  # the merge, wherever they stand (M-42). gh prints an error body to stdout on failure, so the
  # exit code guards the assignment.
  local commits
  if ! commits=$(gh api "repos/$repo/pulls/$n/commits?per_page=100" --jq '[.[].commit.message]' 2>/dev/null); then commits='[]'; fi
  prj=$(jq --argjson c "$commits" '. + { commits: $c }' <<< "$prj")
  sha=$(jq -r .headSha <<< "$prj")
  ref=$(jq -r .headRef <<< "$prj")
  base=$(jq -r .baseRef <<< "$prj")
  # Every check run ever made at this commit is listed, so a job that failed in an earlier run
  # and passed in a later one appears twice (measured 2026-09-05, PR #51 at 80f56dc: the gate's
  # pull_request run failed on the merge ref, a dispatched run passed); the latest per name decides.
  checks=$(gh api "repos/$repo/commits/$sha/check-runs?per_page=100" \
    --jq '[.check_runs[] | { name, status, conclusion, id }] | group_by(.name) | map(max_by(.id)) | map({ name, status, conclusion })')
  # The gate is identified by its file, as in review-web.sh: the registered display name of a
  # workflow that only exists on a lane branch is stale (M-8), and the file counts when it is at
  # HEAD or on the base branch, so a gate that never ran, or that the lane deleted, is required.
  local gate_required=false gate_runs='[]'
  if gh api "repos/$repo/contents/.github/workflows/$gate_file?ref=$sha" --jq .sha >/dev/null 2>&1 \
     || gh api "repos/$repo/contents/.github/workflows/$gate_file?ref=$base" --jq .sha >/dev/null 2>&1; then
    gate_required=true
    # REST by workflow path, so nothing depends on gh resolving a workflow name that the
    # registry may hold stale (M-8). `gh api --jq` takes no --arg: the path is interpolated.
    gate_runs=$(gh api "repos/$repo/actions/runs?head_sha=$sha&per_page=100" \
      --jq "[ .workflow_runs[] | select(.path == \".github/workflows/$gate_file\") ] | sort_by(.created_at) | map({ id, status, conclusion })" 2>/dev/null || printf '[]')
    # D31: run as the last step of the Gate job, that run is still in progress in the API; the
    # job hands its outcome over (HARNESS_GATE_SELF_RUN, HARNESS_GATE_SELF_CONCLUSION).
    if [ -n "${HARNESS_GATE_SELF_RUN:-}" ]; then
      gate_runs=$(jq --argjson id "$HARNESS_GATE_SELF_RUN" --arg c "${HARNESS_GATE_SELF_CONCLUSION:-failure}" \
        'map(if .id == $id then . + { status: "completed", conclusion: $c } else . end)' <<< "$gate_runs")
    fi
  fi
  local gate
  gate=$(jq -n --argjson r "$gate_required" --argjson runs "$gate_runs" '{ required: $r, runs: $runs }')
  # Same anchor as merge.jq (M-23): the keyword must open a line.
  closes=$(jq -r '.body | capture("(?i)(^|\\n)[ \\t]*([-*][ \\t]+)?closes[ \\t]+#(?<n>[0-9]+)") | .n' <<< "$prj" 2>/dev/null || true)
  ticket=null
  reports='{ "standards": null, "spec": null, "ledger": null }'
  if [ -n "$closes" ]; then
    local state lane
    state=$(gh api "repos/$repo/issues/$closes" --jq '.state' 2>/dev/null || echo "")
    lane=$(gh api "repos/$repo/issues/$closes/comments?per_page=100" --paginate \
      --jq '.[] | select(.body | contains("<!-- harness:allocation -->")) | .body | capture("\\| laneBranch \\| (?<b>[^ |]+) \\|") | .b' 2>/dev/null | tail -1 || true)
    if [ -n "$state" ]; then
      # The blockers of the ticket, as the dispatcher reads them (D18).
      local blockers
      if ! blockers=$(gh api "repos/$repo/issues/$closes/dependencies/blocked_by" --jq '[.[] | { number, state }]' 2>/dev/null); then blockers='[]'; fi
      ticket=$(jq -n --argjson n "$closes" --arg s "$state" --arg l "$lane" --argjson b "$blockers" \
        '{ number: $n, state: $s, laneBranch: (if $l == "" then null else $l end), blockedBy: $b }')
    fi
    # Every earlier version of the two reports in the branch history keeps its finding ids in
    # view after a later round overwrote the files.
    local earlier='[]' f c
    for f in standards spec; do
      for c in $(gh api "repos/$repo/commits?path=reviews/issue-$closes/$f.md&sha=$sha&per_page=100" --jq '.[].sha' 2>/dev/null || true); do
        [ "$c" = "$sha" ] && continue
        earlier=$(jq --arg c "$(file_at "reviews/issue-$closes/$f.md" "$c")" '. + [$c]' <<< "$earlier")
      done
    done
    # A report is current only when it was written after the last commit that touched anything
    # but the two report files and the ledger (the rule of lane-code.sh, D40): the commit list at
    # HEAD is newest first, so "after" is a smaller index. Nothing found within 100 commits reads
    # as stale.
    local shas code_sha="" cur_s=false cur_p=false rc ic
    shas=$(gh api "repos/$repo/commits?sha=$sha&per_page=100" --jq '[.[].sha]' 2>/dev/null || printf '[]')
    for c in $(jq -r '.[]' <<< "$shas"); do
      if gh api "repos/$repo/commits/$c" --jq '[.files[].filename]' 2>/dev/null \
         | jq -e --arg a "reviews/issue-$closes/standards.md" --arg b "reviews/issue-$closes/spec.md" --arg l "reviews/issue-$closes/ledger.md" 'any(.[]; . != $a and . != $b and . != $l)' >/dev/null; then
        code_sha=$c; break
      fi
    done
    ic=$(jq -r --arg s "$code_sha" 'index($s) // -1' <<< "$shas")
    for f in standards spec; do
      rc=$(gh api "repos/$repo/commits?path=reviews/issue-$closes/$f.md&sha=$sha&per_page=1" --jq '.[0].sha // empty' 2>/dev/null || true)
      local ir; ir=$(jq -r --arg s "$rc" 'index($s) // -1' <<< "$shas")
      if [ -n "$rc" ] && [ "$ir" -ge 0 ] && [ "$ic" -ge 0 ] && [ "$ir" -lt "$ic" ]; then
        if [ "$f" = standards ]; then cur_s=true; else cur_p=true; fi
      fi
    done
    # Report texts travel through files: several rounds of two reports exceed what one command-line
    # argument may hold on the runner ("jq: Argument list too long", run 33945233956).
    file_at "reviews/issue-$closes/standards.md" "$sha" > "$scratch/standards.md"
    file_at "reviews/issue-$closes/spec.md" "$sha" > "$scratch/spec.md"
    file_at "reviews/issue-$closes/ledger.md" "$sha" > "$scratch/ledger.md"
    printf '%s' "$earlier" > "$scratch/earlier.json"
    reports=$(jq -n --rawfile s "$scratch/standards.md" --rawfile p "$scratch/spec.md" --rawfile l "$scratch/ledger.md" \
                    --slurpfile e "$scratch/earlier.json" --argjson cs "$cur_s" --argjson cp "$cur_p" \
      '{ standards: (if $s == "" then null else $s end), spec: (if $p == "" then null else $p end), ledger: (if $l == "" then null else $l end), earlier: $e[0], current: { standards: $cs, spec: $cp } }')
  fi
  printf '%s' "$reports" > "$scratch/reports.json"
  jq -n --arg operator "$operator" --arg self "$self" --arg review "$review_job" --argjson pr "$prj" --argjson checks "$checks" \
        --argjson gate "$gate" --argjson ticket "$ticket" --slurpfile reports "$scratch/reports.json" \
    '{ operator: $operator, self: $self, ignore: [$review], pr: $pr, checks: $checks, gate: $gate, ticket: $ticket, reports: $reports[0] }'
  printf '%s' "$ref" > /dev/null
}

render_comment() { # $1 decision json, $2 pr
  jq -r --arg n "$2" '"<!-- harness:merge -->\n## Merger máy: quyết định cho #\($n)\n\nLoại: `\(.kind)`" + (if .ticket then " · ticket #\(.ticket)" else "" end) + "\n\n" +
    (if .merge then "Mọi điều kiện của `docs/agents/delivery-workflow.md` \"Who merges\" đều đúng ở HEAD này; merge tuần tự bởi `scripts/harness/merge-check.sh`."
     else "Chưa merge. Điều kiện chưa đạt:\n\n" + ([.reasons[] | "- \(.)"] | join("\n")) end)' <<< "$1"
}

decide_one() { # $1 pr number -> prints decision, returns 0 when merged
  local n=$1 input decision
  input=$(gather "$n")
  decision=$(jq -f "$here/merge.jq" <<< "$input")
  printf '#%s: %s\n' "$n" "$(jq -c '{kind, ticket, merge, supersede, reasons}' <<< "$decision")"
  if [ "$apply" != yes ]; then return 1; fi
  if [ "$(jq -r .supersede <<< "$decision")" = true ]; then
    local t
    t=$(jq -r .ticket <<< "$decision")
    printf '<!-- harness:merge -->\nTicket #%s đã đóng, nên PR này không còn merge được và merger đóng nó. Nếu công việc ở đây vẫn cần, mở lại ticket hoặc tạo ticket mới rồi mở PR trỏ tới đó.\n' "$t" \
      | gh api --method POST "repos/$repo/issues/$n/comments" -F body=@- >/dev/null
    gh pr close "$n" --repo "$repo" >/dev/null
    printf 'closed #%s: ticket #%s is not open\n' "$n" "$t"
    return 1
  fi
  if [ "$(jq -r .merge <<< "$decision")" != true ]; then return 1; fi
  local title
  title=$(gh pr view "$n" --repo "$repo" --json title --jq .title)
  render_comment "$decision" "$n" | gh api --method POST "repos/$repo/issues/$n/comments" -F body=@- >/dev/null
  # D55: the merge call itself can fail (GitHub answered 500/502 for minutes on 2026-09-13; PR #463
  # printed "merged" and stayed open). Nothing below may run on a pull request that is not merged:
  # closing the ticket would turn the open lane pull request into "the pull request of a closed
  # ticket", and the next sweep would supersede it. The exit code and a fresh read of the pull
  # request state both have to say merged; otherwise the next sweep decides again and retries.
  local rc=0 state
  gh pr merge "$n" --repo "$repo" --merge --subject "$title (#$n)" || rc=$?
  state=$(gh pr view "$n" --repo "$repo" --json state --jq .state 2>/dev/null || printf unknown)
  if [ "$rc" -ne 0 ] || [ "$state" != MERGED ]; then
    printf 'merge of #%s failed (gh pr merge exit %s, state %s): nothing closed, the next sweep retries (D55)\n' "$n" "$rc" "$state" >&2
    return 1
  fi
  printf 'merged #%s\n' "$n"
  # GitHub does not close the "Closes #n" ticket when the merge is made with GITHUB_TOKEN
  # (measured 2026-09-05: PR #51 merged at 04:45:54Z, issue #3 still open six minutes later,
  # M-22), so the merger closes it, and drops `kiro` so nothing reads the closed ticket as a
  # lane in flight. The lane's review issues (C4) have served too: closed, without a comment
  # (a comment would wake their sessions, M-17).
  local t i
  t=$(jq -r '.ticket // empty' <<< "$decision")
  if [ -n "$t" ]; then
    gh api --method PATCH "repos/$repo/issues/$t" -f state=closed -f state_reason=completed >/dev/null && printf 'closed ticket #%s\n' "$t"
    gh api --method DELETE "repos/$repo/issues/$t/labels/kiro" >/dev/null 2>&1 || true
    for i in $(gh api "repos/$repo/issues?labels=$turn_label&state=open&per_page=100" --jq ".[] | select(.pull_request == null) | select(.title | startswith(\"Review #$t \")) | .number" 2>/dev/null || true); do
      gh api --method PATCH "repos/$repo/issues/$i" -f state=closed >/dev/null && printf 'closed review issue #%s\n' "$i"
    done
  fi
  # D31: with HARNESS_DISPATCH_INLINE=1 the dispatcher runs here, in the same job (a
  # workflow_dispatch run is one more billed minute for thirty seconds of work, M-50).
  if [ "${HARNESS_DISPATCH_INLINE:-0}" = 1 ]; then
    bash "$here/dispatch.sh" --apply --repo "$repo" || printf 'warning: the dispatcher failed after merging #%s\n' "$n" >&2
  else
    gh workflow run frontier-dispatch.yml --repo "$repo" -f apply=true >/dev/null 2>&1 || \
      printf 'warning: could not re-run the dispatcher after merging #%s\n' "$n" >&2
  fi
  # Another open pull request may be ready as well (M-40): this run merges one, and the next run
  # evaluates the rest against the new default branch. No event wakes that next run (the other
  # pull request's Gate has already completed), so wake it here; a run that merges nothing wakes
  # nothing, which bounds the chain by the number of ready pull requests.
  if [ "$(gh pr list --repo "$repo" --state open --json number --jq 'length' 2>/dev/null || printf 0)" -gt 0 ]; then
    gh workflow run after-gate.yml --repo "$repo" -f apply=true >/dev/null 2>&1 || \
      printf 'warning: could not re-run the merger for the remaining pull requests\n' >&2
  fi
  return 0
}

if [ "$mode" = one ]; then
  decide_one "$pr" || true
else
  for n in $(gh pr list --repo "$repo" --state open --json number --jq '.[].number' | sort -n); do
    if decide_one "$n"; then break; fi
  done
fi
[ "$apply" = yes ] || printf '(dry run: nothing merged; pass --apply to act)\n'
