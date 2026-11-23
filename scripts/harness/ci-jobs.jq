# The job lines of the CI summary a turn message carries (review-web.sh, ci_summary). Pure: the
# response of GET /repos/{owner}/{repo}/actions/runs/{id}/jobs in, one line per job out;
# scripts/harness/witness.sh replays it over fixtures.
#
#   jq -r --arg self "<success|failure|>" -f ci-jobs.jq jobs.json
#
# $self is the outcome the Gate workflow passed in (HARNESS_GATE_SELF_CONCLUSION) when the
# orchestrator runs as the last step of that very Gate job (nhan D31), "" otherwise. While that
# step runs, the API still shows its job in_progress with no conclusion, so the message used to
# read "Gate: in_progress" under a run that said success; the reviewers of lane #7 filed it under
# "chưa xác minh" twice (FV-M-8). A job of the self-run that has not completed therefore reads
# as $self. Steps already carry their conclusions in either case, so the red ones are named.
def outcome: if $self != "" and .status != "completed" then $self else (.conclusion // .status) end;

.jobs[]
| outcome as $c
| "- \(.name): \($c)"
  + (if $c == "failure"
     then " — bước đỏ: " + ([ .steps[]? | select(.conclusion == "failure") | .name ] | join(", "))
     else "" end)
