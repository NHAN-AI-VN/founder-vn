#!/bin/bash
# gate-segment.sh <static|unit|build|verify>: the final gate in bounded segments (D28 in nhan).
#
#   bash scripts/harness/gate-segment.sh static   # ruff check, ruff format --check, skill-lint
#   bash scripts/harness/gate-segment.sh unit     # pytest
#   bash scripts/harness/gate-segment.sh build    # uv build
#   bash scripts/harness/gate-segment.sh verify   # every segment exit 0 on the same HEAD
#
# In the Kiro sandbox one tool call has a time budget and a sub-agent that dies inside a long
# chain leaves nothing behind (nhan, lane #221). Each segment here is short, runs through
# run-logged.sh into its own log under .harness/, and appends one line to
# .harness/gate-segments.txt: <segment> <exit> <HEAD> <utc time>. `verify` reads that file and
# passes only when every segment's latest line is exit 0 and all three name the same HEAD; its
# output is what the evidence file quotes. The segments together are exactly the steps of the CI
# Gate (.github/workflows/gate.yml), in the same order; the CI Gate stays the authority.
#
# Toolchain: `uv run` for ruff and pytest (the project environment, `uv sync --frozen` first),
# `uv build` for the wheel, python3 for scripts/skill_lint.py (standard library only). A segment
# step that fails stops the segment with its own exit code.
set -u
here=$(cd "$(dirname "$0")" && pwd)
runlog=${HARNESS_RUN_LOGGED:-$here/run-logged.sh}
skill_lint=${HARNESS_SKILL_LINT:-$here/../skill_lint.py}
cd "$(git rev-parse --show-toplevel)" || exit 2
dir=${HARNESS_GATE_DIR:-.harness}
ledger="$dir/gate-segments.txt"
segments="static unit build"
seg=${1:-}

steps_of() {
  case "$1" in
    static) echo "ruff-check ruff-format skill-lint" ;;
    unit)   echo "pytest" ;;
    build)  echo "uv-build" ;;
    *) return 1 ;;
  esac
}

run_step() {
  printf '> gate %s\n' "$1"
  case "$1" in
    ruff-check)  uv run ruff check . ;;
    ruff-format) uv run ruff format --check . ;;
    skill-lint)  python3 "$skill_lint" --root . ;;
    pytest)      uv run pytest -q ;;
    uv-build)    uv build ;;
    *) printf 'gate-segment: unknown step %s\n' "$1" >&2; return 2 ;;
  esac
}

run_steps() { local s; for s in "$@"; do run_step "$s" || return $?; done; }
head_sha() { git rev-parse HEAD 2>/dev/null || echo unknown; }

record() { mkdir -p "$dir"; printf '%s %s %s %s\n' "$1" "$2" "$(head_sha)" "$(date -u +%FT%TZ)" >> "$ledger"; }

latest() { grep -E "^$1 " "$ledger" 2>/dev/null | tail -n1; }

verify() {
  local s line rc sha ref="" bad=0
  [ -f "$ledger" ] || { printf 'gate-segment verify: no %s; run the three segments first\n' "$ledger" >&2; return 1; }
  printf 'gate-segment verify: latest line per segment (%s)\n' "$ledger"
  for s in $segments; do
    line=$(latest "$s")
    if [ -z "$line" ]; then printf '  %-8s MISSING\n' "$s"; bad=1; continue; fi
    printf '  %s\n' "$line"
    rc=$(printf '%s' "$line" | awk '{print $2}'); sha=$(printf '%s' "$line" | awk '{print $3}')
    [ "$rc" = 0 ] || bad=1
    if [ -z "$ref" ]; then ref=$sha; elif [ "$sha" != "$ref" ]; then bad=1; fi
  done
  if [ "$bad" -ne 0 ]; then printf 'gate-segment verify: RED (a segment is missing, failed, or ran on a different HEAD)\n'; return 1; fi
  if [ "$ref" != "$(head_sha)" ]; then printf 'gate-segment verify: GREEN on %s (current HEAD %s differs; fine when only docs/evidence commits followed)\n' "$ref" "$(head_sha)"; else printf 'gate-segment verify: GREEN on %s\n' "$ref"; fi
  return 0
}

export -f run_step run_steps
export skill_lint
case "$seg" in
  verify) verify; exit $? ;;
  static|unit|build)
    # shellcheck disable=SC2046
    bash "$runlog" "$dir/gate-$seg.log" bash -c 'run_steps "$@"' _ $(steps_of "$seg")
    rc=$?
    record "$seg" "$rc"
    printf 'gate-segment: %s exit %s (log %s/gate-%s.log)\n' "$seg" "$rc" "$dir" "$seg"
    exit "$rc" ;;
  *) printf 'usage: gate-segment.sh <static|unit|build|verify>\n' >&2; exit 2 ;;
esac
