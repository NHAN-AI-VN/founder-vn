#!/bin/bash
# Open the lane pull request for issue <n> from the current branch, body on stdin (D26 in nhan).
#
#   bash scripts/harness/open-lane-pr.sh <n> <<'EOF'
#   ...the filled .github/PULL_REQUEST_TEMPLATE.md...
#   EOF
#
# One command for the step three nhan lane sessions died on: `gh pr create` needs GraphQL, which
# the sandbox's gh cannot reach, and a body file written through the editor tool is invisible to
# the shell. This script reads the body from the shell's own stdin and talks to GitHub through
# `gh api` (REST) only. It refuses, exit 2, unless HEAD is on lane/issue-<n> with a clean tree,
# HEAD is on origin, and the body has a line `Closes #<n>` and the line
# `<promise>COMPLETE</promise>`; a pull request already open for the branch is reported and
# reused, never duplicated. The last line of stdout is the pull request number. Each predicate
# below is one line so the witness can knock it out.
set -u

refuse() { printf 'open-lane-pr: %s\n' "$1" >&2; exit 2; }

n=${1:-}
case "$n" in ''|*[!0-9]*) refuse "usage: open-lane-pr.sh <issue-number> < body.md" ;; esac
branch="lane/issue-$n"
base=${HARNESS_BASE:-main}

repo=${GITHUB_REPOSITORY:-}
if [ -z "$repo" ]; then
  url=$(git remote get-url origin 2>/dev/null) || refuse "no origin remote"
  repo=$(printf '%s' "$url" | sed -E 's#^(https://([^@/]+@)?github\.com/|git@github\.com:|ssh://git@github\.com/)##; s#\.git$##; s#/$##')
  case "$repo" in */*) ;; *) refuse "origin is not a GitHub repository: $url" ;; esac
fi
owner=${repo%%/*}

on_lane_branch() { [ "$(git symbolic-ref --quiet --short HEAD 2>/dev/null)" = "$branch" ]; }
tree_clean()     { git diff --quiet 2>/dev/null && git diff --cached --quiet 2>/dev/null; }
on_origin()      { git fetch -q origin "refs/heads/$branch" 2>/dev/null && [ "$(git rev-parse HEAD)" = "$(git rev-parse FETCH_HEAD)" ]; }
names_closes()   { printf '%s\n' "$body" | grep -q -E "^Closes #$n[[:space:]]*\$"; }
ends_complete()  { printf '%s\n' "$body" | grep -q -F '<promise>COMPLETE</promise>'; }
open_pr_number() { gh api "repos/$repo/pulls?state=open&head=$owner:$branch&per_page=1" --jq '.[0].number // empty'; }

on_lane_branch || refuse "HEAD is on $(git symbolic-ref --quiet --short HEAD 2>/dev/null || echo 'a detached HEAD'), not $branch"
tree_clean || refuse "the working tree has uncommitted changes; commit them first"
on_origin || refuse "HEAD $(git rev-parse --short HEAD) is not on origin/$branch; push first (git push -u origin $branch)"

body=$(cat)
[ -n "$body" ] || refuse "empty body on stdin; pipe the filled pull request template in"
names_closes || refuse "the body has no line 'Closes #$n'"
ends_complete || refuse "the body lacks the line <promise>COMPLETE</promise> at the end of Outcome"

existing=$(open_pr_number 2>/dev/null) || refuse "could not list pull requests for $branch"
if [ -n "$existing" ]; then
  printf 'open-lane-pr: pull request #%s is already open for %s; nothing to do\n' "$existing" "$branch" >&2
  printf '%s\n' "$existing"
  exit 0
fi

title=${HARNESS_PR_TITLE:-}
if [ -z "$title" ]; then
  issue_title=$(gh api "repos/$repo/issues/$n" --jq '.title' 2>/dev/null) || refuse "could not read issue #$n"
  # The tickets are titled `T01 · …`; the pull request is `#<n> …`.
  title="#$n $(printf '%s' "$issue_title" | sed -E 's#^T[0-9]+ · ##')"
fi

errf=$(mktemp)
number=$(printf '%s\n' "$body" | gh api --method POST "repos/$repo/pulls" -f title="$title" -f head="$branch" -f base="$base" -F body=@- --jq '.number' 2>"$errf") || {
  err=$(head -c 300 "$errf"); rm -f "$errf"
  refuse "GitHub refused the pull request: $err"
}
rm -f "$errf"
printf 'open-lane-pr: opened pull request #%s for %s -> %s\n' "$number" "$branch" "$base" >&2
printf '%s\n' "$number"
