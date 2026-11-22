#!/usr/bin/env bash
# The code commit of a lane: the last commit between the target and HEAD that touched anything but
# the review lane's own files under reviews/issue-N/ (the two reports and the closure ledger). A
# report is current only when it was written after this commit, so a fix, an operator's answer
# file or a harness probe all call for a new review round, while a report or a ledger commit never
# does (D40: the merger reads the ledger at HEAD itself; an address session that pushed its ledger
# minutes after its fixes used to open a second, identical round). Prints the commit, or the
# merge-base when the branch holds nothing but reports.
# Usage: lane-code.sh <base sha> <head sha> <reviews/issue-N>
set -euo pipefail
base=$1; head=$2; dir=$3
ledger=":(exclude)$dir/ledger.md"
code=$(git log -1 --format=%H "$base..$head" -- . ":(exclude)$dir/standards.md" ":(exclude)$dir/spec.md" $ledger 2>/dev/null || true)
[ -n "$code" ] || code=$(git merge-base "$base" "$head")
printf '%s\n' "$code"
