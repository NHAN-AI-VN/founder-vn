#!/bin/bash
# run-logged.sh <log> <command...>: run the command with stdout and stderr copied into <log>,
# print the gate summary lines at the end, exit with the command's own code (D27 in nhan,
# kept here as is).
#
#   bash scripts/harness/run-logged.sh .harness/gate-unit.log uv run pytest -q
#
# gate-segment.sh wraps every segment in this, so one gate run leaves its whole output in a file
# inside the repository tree, where the Kiro sandbox keeps it from one tool call to the next
# (/tmp does not survive, and a tool call truncates long output). The evidence file is filled
# from the log; the gate is not rerun to read its own summary.
set -u
log=${1:-}
[ -n "$log" ] && [ $# -ge 2 ] || { printf 'usage: run-logged.sh <log> <command...>\n' >&2; exit 2; }
shift
mkdir -p "$(dirname "$log")"
"$@" 2>&1 | tee "$log"
rc=${PIPESTATUS[0]}
printf '\n--- run-logged: summary (full output in %s, %s lines) ---\n' "$log" "$(wc -l < "$log" | tr -d ' ')"
# The lines worth quoting in an evidence file: the step markers gate-segment.sh prints, pytest's
# closing line, ruff's verdicts, uv build's result and skill-lint's count.
grep -E '^> gate |[0-9]+ (passed|failed|error|errors|skipped|xfailed)|no tests ran|All checks passed|Found [0-9]+ error|already formatted|Would reformat|Successfully built|skill-lint:' "$log" | sed -E 's/^ +//'
printf 'exit %s\n' "$rc"
exit "$rc"
