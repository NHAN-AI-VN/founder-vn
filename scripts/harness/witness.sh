#!/bin/bash
# Witness for the harness mechanisms that exist today. One command, one exit code (0 when every
# case holds, 1 otherwise). Ported from NHAN-AI-VN/nhan (scripts/harness/witness.sh at 8adef66b)
# and grown with this repository's own mechanisms; the Docker and Actions-minute machinery of the
# source has no case here because it has no mechanism here (docs/agents/kiro-harness.md).
#
#   bash scripts/harness/witness.sh               # every case must pass
#   bash scripts/harness/witness.sh --witness-red # mutate each mechanism; the cases must go red
#
# The second mode is the playbook's "a gate that cannot go red is not a gate": it removes one
# rule at a time and requires the case that guards that rule to fail. A mutation that still
# passes means the case does not test what it claims.
set -u

here=$(cd "$(dirname "$0")" && pwd)
root=$(cd "$here/../.." && pwd)
guard="$root/.kiro/hooks/guard.sh"
skill_links="$here/check-skill-links.sh"
skill_lint="$root/scripts/skill_lint.py"
hook="$root/.githooks/post-commit"
precommit="$root/.githooks/pre-commit"
runlog="$here/run-logged.sh"
gateseg="$here/gate-segment.sh"
doc_paths="$here/check-doc-paths.sh"
filter="$here/frontier.jq"
adopt_filter="$here/adopt.jq"
verify_filter="$here/verify-pick.jq"
apierr_filter="$here/api-error.jq"
openpr="$here/open-lane-pr.sh"
prbody="$here/lane-pr-body.sh"
lanecode="$here/lane-code.sh"
web_filter="$here/review-web.jq"
turn="$here/review-web-turn.sh"
prompts="$root/.kiro/prompts"
merge_filter="$here/merge.jq"
fixtures="$here/fixtures"
mode=${1:-}
failures=0
passes=0
stderr_file=$(mktemp)
trap 'rm -f "$stderr_file"' EXIT

ok()   { passes=$((passes + 1)); printf 'PASS  %s\n' "$1"; }
fail() { failures=$((failures + 1)); printf 'FAIL  %s\n' "$1"; }

# Under `--witness-red` each mutation runs only the cases of the file it mutates (WITNESS_ONLY
# names that file's override variable); every case runs when it is unset. A mutation that only an
# indirect case would catch turns GREEN and fails the run, which is the signal to widen its cases.
skip() { [ -n "${WITNESS_ONLY:-}" ] && [ "$WITNESS_ONLY" != "$1" ]; }

# A throwaway git identity for the temporary repositories the cases build.
wgit() { git -c user.name=witness -c user.email=witness@example.invalid -c commit.gpgsign=false "$@"; }

# expect_guard <name> <expected-exit> <payload> [env assignments...]
expect_guard() {
  skip GUARD && return 0
  local name=$1 want=$2 payload=$3
  shift 3
  local got
  # ${1+"$@"} instead of "$@": bash 3.2 (macOS) raises "unbound variable" for an empty "$@" under set -u.
  printf '%s' "$payload" | env ${1+"$@"} HARNESS_OWNED_PATHS_FILE="${OWNED_FILE:-$fixtures/parallel-lanes-owned.md}" bash "${GUARD:-$guard}" >/dev/null 2>"$stderr_file"
  got=$?
  if [ "$got" -eq "$want" ]; then ok "guard: $name (exit $got)"; else fail "guard: $name (want exit $want, got $got: $(head -c 160 "$stderr_file"))"; fi
}

# expect_skill_links <name> <expected-exit> <scenario>: a throwaway repository with one committed
# skill and one .kiro/skills link, bent by the scenario. Scenarios: ok, absolute (link target is
# an absolute path), dangling (no SKILL.md behind the link), uncommitted (the link is not in git),
# notlink (a directory where the link should be), none (no links at all), wrongname (the link
# points at another skill).
expect_skill_links() {
  skip SKILL_LINKS && return 0
  local name=$1 want=$2 scenario=$3 d got
  d=$(mktemp -d)
  wgit init -q "$d" && mkdir -p "$d/.agents/skills/alpha" "$d/.kiro/skills" "$d/.agents/skills/beta"
  printf -- '---\nname: alpha\n---\n# alpha\n' > "$d/.agents/skills/alpha/SKILL.md"
  printf -- '---\nname: beta\n---\n# beta\n' > "$d/.agents/skills/beta/SKILL.md"
  case "$scenario" in
    absolute)  ln -s "$d/.agents/skills/alpha" "$d/.kiro/skills/alpha" ;;
    notlink)   mkdir -p "$d/.kiro/skills/alpha" && echo x > "$d/.kiro/skills/alpha/SKILL.md" ;;
    none)      ;;
    wrongname) ln -s ../../.agents/skills/beta "$d/.kiro/skills/alpha" ;;
    *)         ln -s ../../.agents/skills/alpha "$d/.kiro/skills/alpha" ;;
  esac
  wgit -C "$d" add -A >/dev/null 2>&1
  [ "$scenario" = uncommitted ] && wgit -C "$d" rm -q --cached .kiro/skills/alpha >/dev/null 2>&1
  wgit -C "$d" commit -q --allow-empty -m one >/dev/null 2>&1
  # dangling: the SKILL.md is committed (so `tracked` holds) but gone from the working tree.
  [ "$scenario" = dangling ] && rm "$d/.agents/skills/alpha/SKILL.md"
  SKILL_LINKS_ROOT="$d" bash "${SKILL_LINKS:-$skill_links}" >/dev/null 2>"$stderr_file"; got=$?
  rm -rf "$d"
  if [ "$got" -eq "$want" ]; then ok "skill-links: $name (exit $got)"; else fail "skill-links: $name (want exit $want, got $got: $(head -c 160 "$stderr_file"))"; fi
}

# expect_skill_lint <fixture-dir> <expected-exit> [substring the findings must contain]: the
# machine half of the skill review checklist (scripts/skill_lint.py, FV-D2) over one fixture root.
expect_skill_lint() {
  skip SKILL_LINT && return 0
  local fixture=$1 want=$2 sub=${3:-} got
  python3 "${SKILL_LINT:-$skill_lint}" --root "$fixtures/skill-lint/$fixture" >/dev/null 2>"$stderr_file"; got=$?
  if [ "$got" -ne "$want" ]; then fail "skill-lint: $fixture (want exit $want, got $got: $(head -c 160 "$stderr_file"))"; return; fi
  if [ -n "$sub" ] && ! grep -qF -- "$sub" "$stderr_file"; then fail "skill-lint: $fixture (findings lack \"$sub\": $(head -c 160 "$stderr_file"))"; return; fi
  ok "skill-lint: $fixture (exit $got${sub:+, names \"$sub\"})"
}

# expect_autopush <name> <branch> <pushed|kept> [rebase] [env assignments...]
# A throwaway repository with a bare origin and the post-commit hook as its only hook: one empty
# commit on <branch>, then origin either has the branch (pushed) or does not (kept).
expect_autopush() {
  skip HOOK && return 0
  local name=$1 branch=$2 want=$3 rebase=${4:-}
  shift 3; [ $# -gt 0 ] && shift
  local d got
  d=$(mktemp -d)
  mkdir -p "$d/hooks" && cp "${HOOK:-$hook}" "$d/hooks/post-commit" && chmod +x "$d/hooks/post-commit"
  git init -q --bare "$d/origin.git"
  git init -q "$d/work" && git -C "$d/work" checkout -q -b "$branch"
  git -C "$d/work" remote add origin "$d/origin.git"
  git -C "$d/work" config core.hooksPath "$d/hooks"
  [ "$rebase" = rebase ] && mkdir -p "$d/work/.git/rebase-merge"
  env ${1+"$@"} git -C "$d/work" -c user.name=witness -c user.email=witness@example.invalid -c commit.gpgsign=false commit -q --allow-empty -m one 2>/dev/null
  if git -C "$d/origin.git" show-ref --verify -q "refs/heads/$branch"; then got=pushed; else got=kept; fi
  rm -rf "$d"
  if [ "$got" = "$want" ]; then ok "autopush: $name ($got)"; else fail "autopush: $name (want $want, got $got)"; fi
}

# expect_precommit <name> <file content> <refused|committed> [ENV=val...]: the staged-files
# ruff format check. A fake .venv/bin/ruff refuses any file containing UNFORMATTED.
expect_precommit() {
  skip PRECOMMIT && return 0
  local name=$1 content=$2 want=$3; shift 3
  local d got
  d=$(mktemp -d)
  mkdir -p "$d/hooks" "$d/work/.venv/bin" && cp "${PRECOMMIT:-$precommit}" "$d/hooks/pre-commit" && chmod +x "$d/hooks/pre-commit"
  printf '#!/bin/sh\nfor f in "$@"; do case "$f" in -*|format|check) continue;; esac; grep -q UNFORMATTED "$f" && { echo "Would reformat: $f"; exit 1; }; done; exit 0\n' > "$d/work/.venv/bin/ruff"
  chmod +x "$d/work/.venv/bin/ruff"
  git init -q "$d/work" && git -C "$d/work" checkout -q -b lane/issue-9
  git -C "$d/work" config core.hooksPath "$d/hooks"
  [ "$name" = "no ruff installed, commit stands" ] && rm -f "$d/work/.venv/bin/ruff"
  local file=a.py; [ "$name" = "a non-Python file is not checked" ] && file=a.md
  printf '%s\n' "$content" > "$d/work/$file" && git -C "$d/work" add "$file"
  if env ${1+"$@"} git -C "$d/work" -c user.name=witness -c user.email=witness@example.invalid -c commit.gpgsign=false commit -q -m one >/dev/null 2>&1; then got=committed; else got=refused; fi
  rm -rf "$d"
  if [ "$got" = "$want" ]; then ok "precommit: $name ($got)"; else fail "precommit: $name (want $want, got $got)"; fi
}

# expect_runlog <name> <want-exit> <logged|unlogged> <summary|nosummary> <command...>: the gate
# logger (D27). Runs the command through run-logged.sh into a temp log and checks the exit code,
# whether the log holds the command's output, and whether the summary repeats the pytest line.
expect_runlog() {
  skip RUNLOG && return 0
  local name=$1 want_rc=$2 want_log=$3 want_sum=$4; shift 4
  local d out rc got_log got_sum
  d=$(mktemp -d)
  out=$(bash "${RUNLOG:-$runlog}" "$d/nested/check.log" "$@" 2>/dev/null); rc=$?
  if [ -f "$d/nested/check.log" ] && grep -q 'passed in' "$d/nested/check.log"; then got_log=logged; else got_log=unlogged; fi
  if printf '%s' "$out" | sed -n '/^--- run-logged: summary/,$p' | grep -q 'passed in'; then got_sum=summary; else got_sum=nosummary; fi
  rm -rf "$d"
  if [ "$rc" -eq "$want_rc" ] && [ "$got_log" = "$want_log" ] && [ "$got_sum" = "$want_sum" ]; then ok "run-logged: $name (exit $rc, $got_log, $got_sum)"
  else fail "run-logged: $name (want exit $want_rc $want_log $want_sum, got exit $rc $got_log $got_sum)"; fi
}

# expect_gateseg <name> <want-verify-exit> <scenario>: the segmented final gate (D28). A throwaway
# repository with one commit and a fake `uv` first on PATH (prints a pytest-like line; FAKE_FAIL
# names a word of the uv command line that must exit 1). Scenarios: three (all green), fail (unit
# red), missing (build never run), moved (HEAD changes between static and the rest), docs-after
# (a commit after all three).
expect_gateseg() {
  skip GATESEG && return 0
  local name=$1 want=$2 scenario=$3
  local d rc seg out
  d=$(mktemp -d)
  mkdir -p "$d/bin"
  printf '#!/bin/bash\necho "fake uv: $*"; echo "== 1 passed in 0.01s =="; if [ -n "${FAKE_FAIL:-}" ]; then case " $* " in *" $FAKE_FAIL "*) exit 1;; esac; fi; exit 0\n' > "$d/bin/uv"
  chmod +x "$d/bin/uv"
  git init -q "$d/repo" && git -C "$d/repo" -c user.name=witness -c user.email=witness@example.invalid -c commit.gpgsign=false commit -q --allow-empty -m one
  seg_run() { (cd "$d/repo" && PATH="$d/bin:$PATH" HARNESS_RUN_LOGGED="$runlog" HARNESS_SKILL_LINT="$skill_lint" FAKE_FAIL="${2:-}" bash "${GATESEG:-$gateseg}" "$1" >/dev/null 2>&1); }
  case "$scenario" in
    three)      for seg in static unit build; do seg_run "$seg"; done ;;
    fail)       seg_run static; seg_run unit pytest; seg_run build ;;
    missing)    seg_run static; seg_run unit ;;
    moved)      seg_run static; git -C "$d/repo" -c user.name=witness -c user.email=witness@example.invalid -c commit.gpgsign=false commit -q --allow-empty -m two; seg_run unit; seg_run build ;;
    docs-after) for seg in static unit build; do seg_run "$seg"; done; git -C "$d/repo" -c user.name=witness -c user.email=witness@example.invalid -c commit.gpgsign=false commit -q --allow-empty -m docs ;;
  esac
  out=$(cd "$d/repo" && HARNESS_RUN_LOGGED="$runlog" HARNESS_SKILL_LINT="$skill_lint" bash "${GATESEG:-$gateseg}" verify 2>/dev/null); rc=$?
  local logged=yes; [ -f "$d/repo/.harness/gate-static.log" ] && grep -q 'passed in' "$d/repo/.harness/gate-static.log" || logged=no
  rm -rf "$d"
  if [ "$rc" -eq "$want" ] && [ "$logged" = yes ]; then ok "gate-segment: $name (verify exit $rc)"; else fail "gate-segment: $name (want verify exit $want, got $rc; static log $logged; $(printf '%s' "$out" | tail -n1))"; fi
}

# expect_doc_paths <name> <expected-exit> <scenario>: the rule-document path check. A throwaway
# git checkout with one doc naming paths; scenarios: present (every path exists), missing (one
# does not), placeholder (`<n>` skipped), directory (trailing slash skipped), slug (Owner/repo
# skipped), ignored (a git-ignored runtime file skipped), bare (no directory component skipped).
expect_doc_paths() {
  skip DOC_PATHS && return 0
  local name=$1 want=$2 scenario=$3 d got
  d=$(mktemp -d)
  wgit init -q "$d" && mkdir -p "$d/docs/agents" "$d/scripts"
  echo x > "$d/docs/agents/real.md"; echo x > "$d/scripts/real.sh"; printf '.harness/\n' > "$d/.gitignore"
  case "$scenario" in
    present)     printf 'See `docs/agents/real.md` and `scripts/real.sh`.\n' > "$d/RULES.md" ;;
    missing)     printf 'See `docs/agents/real.md` and `docs/agents/gone.md`.\n' > "$d/RULES.md" ;;
    placeholder) printf 'Write `docs/evidence/issue-<n>-<slug>.md` and `reviews/issue-*/x.md`.\n' > "$d/RULES.md" ;;
    directory)   printf 'ADRs go under `docs/adr/`.\n' > "$d/RULES.md" ;;
    slug)        printf 'Issues live in `NHAN-AI-VN/founder-vn`.\n' > "$d/RULES.md" ;;
    ignored)     printf 'The ledger is `.harness/gate-segments.txt`.\n' > "$d/RULES.md" ;;
    bare)        printf 'The manifest is `pyproject.toml`; the glossary `GLOSSARY.md`.\n' > "$d/RULES.md" ;;
  esac
  DOC_PATHS_ROOT="$d" bash "${DOC_PATHS:-$doc_paths}" RULES.md >/dev/null 2>"$stderr_file"; got=$?
  rm -rf "$d"
  if [ "$got" -eq "$want" ]; then ok "doc-paths: $name (exit $got)"; else fail "doc-paths: $name (want exit $want, got $got: $(head -c 160 "$stderr_file"))"; fi
}

# ---- dispatcher (C1) helpers --------------------------------------------------------------
# expect_pick <fixture> <expected pick or null>
expect_pick() {
  skip FILTER && return 0
  local fixture=$1 want=$2 got
  got=$(jq -f "${FILTER:-$filter}" "$fixtures/$fixture" 2>/dev/null | jq -r '.pick')
  if [ "$got" = "$want" ]; then ok "frontier: $fixture picks $want"; else fail "frontier: $fixture (want pick $want, got ${got:-<error>})"; fi
}

expect_reconcile() {
  skip FILTER && return 0
  local fixture=$1 want=$2 got
  got=$(jq -f "${FILTER:-$filter}" "$fixtures/$fixture" 2>/dev/null | jq -c '[.reconcile[].number]')
  if [ "$got" = "$want" ]; then ok "frontier: $fixture reconciles $want"; else fail "frontier: $fixture (want reconcile $want, got ${got:-<error>})"; fi
}

# expect_action <fixture> <issue number> <reconcile action>
expect_action() {
  skip FILTER && return 0
  local fixture=$1 number=$2 want=$3 got
  got=$(jq -f "${FILTER:-$filter}" "$fixtures/$fixture" 2>/dev/null | jq -r --argjson n "$number" '[.reconcile[] | select(.number == $n) | .action] | first // "none"')
  if [ "$got" = "$want" ]; then ok "frontier: $fixture reconciles #$number as $want"; else fail "frontier: $fixture #$number (want action $want, got ${got:-<error>})"; fi
}

expect_allocation() {
  skip FILTER && return 0
  local fixture=$1 key=$2 want=$3 got
  got=$(jq -f "${FILTER:-$filter}" "$fixtures/$fixture" 2>/dev/null | jq -r ".allocation.$key")
  if [ "$got" = "$want" ]; then ok "frontier: $fixture allocation.$key = $want"; else fail "frontier: $fixture allocation.$key (want $want, got ${got:-<error>})"; fi
}

# expect_adopt <fixture> <true|false> [reason substring]: the lane adoption decision (D24)
expect_adopt() {
  skip ADOPT_FILTER && return 0
  local fixture=$1 want=$2 sub=${3:-} out got reasons
  out=$(jq -f "${ADOPT_FILTER:-$adopt_filter}" "$fixtures/$fixture" 2>/dev/null)
  got=$(jq -r '.[0].adopt' <<< "$out" 2>/dev/null); reasons=$(jq -r '.[0].reasons | join(" | ")' <<< "$out" 2>/dev/null)
  if [ "$got" != "$want" ]; then fail "adopt: $fixture (want adopt=$want, got ${got:-<error>}; reasons: ${reasons:-none})"; return; fi
  if [ -n "$sub" ] && ! printf '%s' "$reasons" | grep -qF -- "$sub"; then fail "adopt: $fixture (reasons lack \"$sub\": $reasons)"; return; fi
  ok "adopt: $fixture adopt=$want${sub:+ (reason: $sub)}"
}

# expect_verify <fixture> <true|false>: the direct read of a pick before an allocation (D47, D51)
expect_verify() {
  skip VERIFY_FILTER && return 0
  local fixture=$1 want=$2 got
  got=$(jq -f "${VERIFY_FILTER:-$verify_filter}" "$fixtures/$fixture" 2>/dev/null)
  if [ "$got" = "$want" ]; then ok "verify-pick: $fixture -> $want"; else fail "verify-pick: $fixture (want $want, got ${got:-<error>})"; fi
}

# expect_apierr <fixture> <substring>: the one-line reason read from a failed gh api body (D24b)
expect_apierr() {
  skip APIERR_FILTER && return 0
  local fixture=$1 sub=$2 out
  out=$(jq -r -f "${APIERR_FILTER:-$apierr_filter}" "$fixtures/$fixture" 2>/dev/null)
  if ! printf '%s' "$out" | grep -qF -- "$sub"; then fail "api-error: $fixture (lacks \"$sub\": ${out:-<error>})"; return; fi
  ok "api-error: $fixture -> $sub"
}

# expect_openpr <name> <opened|reused|refused> [flags...]: the lane PR opener (D26)
# A throwaway repository with a bare origin, one commit on lane/issue-9 pushed unless "unpushed",
# and a fake `gh` first on PATH that answers the three REST calls the script makes and logs the
# POST. Flags: unpushed, existing (a PR is already open), noclose, nocomplete, wrongbranch, dirty.
expect_openpr() {
  skip OPENPR && return 0
  local name=$1 want=$2; shift 2
  local d flags=" $* " body got rc out posted
  d=$(mktemp -d)
  mkdir -p "$d/bin"
  cat > "$d/bin/gh" <<'FAKE'
#!/bin/bash
# fake gh for the witness: REST only, logs the POST
case " $* " in
  *" --method POST "*) cat > "$FAKE_DIR/post-body"; printf '%s\n' "$*" > "$FAKE_DIR/post-args"; echo 77 ;;
  *"/pulls?state=open&head="*) printf '%s\n' "${FAKE_EXISTING:-}" ;;
  *"/issues/9 "*) echo 'T09 · Tiêu đề ticket' ;;
  *) echo "fake gh: unexpected call: $*" >&2; exit 1 ;;
esac
FAKE
  chmod +x "$d/bin/gh"
  git init -q --bare "$d/origin.git"
  git init -q "$d/work"
  git -C "$d/work" checkout -q -b lane/issue-9
  git -C "$d/work" remote add origin "$d/origin.git"
  wgit -C "$d/work" commit -q --allow-empty -m one
  case "$flags" in *" unpushed "*) ;; *) git -C "$d/work" push -q origin HEAD 2>/dev/null ;; esac
  # wrongbranch: the same commit sits on origin as lane/issue-9, so only the branch check can refuse
  case "$flags" in *" wrongbranch "*) git -C "$d/work" checkout -q -b main ;; esac
  case "$flags" in *" dirty "*) echo x > "$d/work/dirty.txt"; git -C "$d/work" add dirty.txt ;; esac
  body=$'## Outcome\n\nDone.\n\n<promise>COMPLETE</promise>\n\n## Ticket and source pointers\n\nCloses #9\n'
  case "$flags" in *" noclose "*) body=${body//Closes #9/Closes #8} ;; esac
  case "$flags" in *" nocomplete "*) body=${body//<promise>COMPLETE<\/promise>/} ;; esac
  local existing=""; case "$flags" in *" existing "*) existing=5 ;; esac
  out=$(cd "$d/work" && printf '%s' "$body" | PATH="$d/bin:$PATH" FAKE_DIR="$d" FAKE_EXISTING="$existing" GITHUB_REPOSITORY=o/r bash "${OPENPR:-$openpr}" 9 2>/dev/null); rc=$?
  posted=no; [ -f "$d/post-args" ] && posted=yes
  if [ "$posted" = yes ] && [ "$rc" -eq 0 ] && printf '%s' "$out" | tail -n1 | grep -qx 77 \
     && grep -q -- '-f head=lane/issue-9' "$d/post-args" && grep -q -- '-f base=main' "$d/post-args" && grep -q 'Closes #9' "$d/post-body"; then got=opened
  elif [ "$posted" = no ] && [ "$rc" -eq 0 ] && printf '%s' "$out" | tail -n1 | grep -qx 5; then got=reused
  elif [ "$posted" = no ] && [ "$rc" -eq 2 ]; then got=refused
  else got="rc=$rc posted=$posted out=$(printf '%s' "$out" | tail -n1)"; fi
  rm -rf "$d"
  if [ "$got" = "$want" ]; then ok "open-pr: $name ($got)"; else fail "open-pr: $name (want $want, got $got)"; fi
}

# expect_prbody <name>: the body rendered for an adopted lane names the ticket, promises COMPLETE
# and copies the evidence's gate block (D24)
expect_prbody() {
  skip PRBODY && return 0
  local name=$1 d out bad=""
  d=$(mktemp -d)
  printf 'src/founder_vn/x.py\ndocs/evidence/issue-9-x.md\n' > "$d/files"
  out=$(jq -r '.lanes[0].evidence.text' "$fixtures/adopt-ready.json" | bash "${PRBODY:-$prbody}" 9 "Tiêu đề" docs/evidence/issue-9-x.md 71ecd990 "$d/files" 2>/dev/null)
  rm -rf "$d"
  printf '%s\n' "$out" | grep -q -E '^Closes #9$' || bad="$bad no-Closes"
  printf '%s\n' "$out" | grep -q -F '<promise>COMPLETE</promise>' || bad="$bad no-COMPLETE"
  printf '%s\n' "$out" | grep -q -F 'GREEN on 74ac044a' || bad="$bad no-gate-block"
  printf '%s\n' "$out" | grep -q -F '`src/founder_vn/x.py`' || bad="$bad no-files"
  if [ -z "$bad" ]; then ok "lane-pr-body: $name"; else fail "lane-pr-body: $name (missing:$bad)"; fi
}

# expect_lanecode <name> <want: code|mixed|base>: a temporary lane with a code commit, a report
# commit and a ledger commit; the code commit is the one lane-code.sh must name (D40).
expect_lanecode() {
  skip LANECODE && return 0
  local name=$1 want=$2 d got base code mixed
  d=$(mktemp -d)
  git init -q "$d" && git -C "$d" checkout -q -b main
  g() { wgit -C "$d" "$@"; }
  mkdir -p "$d/reviews/issue-9" "$d/src"
  echo a > "$d/src/a.py" && g add -A && g commit -q -m base && base=$(g rev-parse HEAD)
  g checkout -q -b lane/issue-9
  case "$want" in
    base) ;;
    *) echo b > "$d/src/b.py" && g add -A && g commit -q -m "slice: b" && code=$(g rev-parse HEAD) ;;
  esac
  echo PASS > "$d/reviews/issue-9/standards.md" && g add -A && g commit -q -m "review(standards)"
  echo "# Review closure ledger — #9" > "$d/reviews/issue-9/ledger.md" && g add -A && g commit -q -m "docs: ledger"
  if [ "$want" = mixed ]; then
    echo c > "$d/src/c.py" && echo "S1 FIXED" >> "$d/reviews/issue-9/ledger.md" && g add -A && g commit -q -m "fix + ledger" && mixed=$(g rev-parse HEAD)
  fi
  got=$(cd "$d" && bash "${LANECODE:-$lanecode}" "$base" "$(g rev-parse HEAD)" reviews/issue-9 2>/dev/null)
  rm -rf "$d"
  case "$want" in code) [ "$got" = "$code" ];; mixed) [ "$got" = "$mixed" ];; base) [ "$got" = "$base" ];; esac \
    && ok "lane-code: $name" || fail "lane-code: $name (got ${got:-<error>})"
}

# ---- review orchestrator (C4) helpers --------------------------------------------------------
# expect_web <fixture> <expected-action> [<expected-axes-json>]: the review orchestrator's step
expect_web() {
  skip WEB_FILTER && return 0
  local fixture=$1 want=$2 want_axes=${3:-} got got_axes
  got=$(jq -r -f "${WEB_FILTER:-$web_filter}" "$fixtures/$fixture" 2>/dev/null | jq -r '.action' 2>/dev/null || printf 'jq failed')
  if [ "$got" != "$want" ]; then fail "review-web: $fixture (want $want, got $got)"; return; fi
  if [ -n "$want_axes" ]; then
    got_axes=$(jq -c -f "${WEB_FILTER:-$web_filter}" "$fixtures/$fixture" 2>/dev/null | jq -c '.axes')
    if [ "$got_axes" != "$want_axes" ]; then fail "review-web: $fixture (want axes $want_axes, got $got_axes)"; return; fi
  fi
  ok "review-web: $fixture -> $got${want_axes:+ $want_axes}"
}

# expect_turn <axis>: the rendered `/kiro` message of one turn opens with /kiro, carries the CI
# text, the ticket body for every axis but standards, the prompt verbatim, the marker last; and
# names nothing of the source project's toolchain (npm, Docker, master).
expect_turn() {
  skip TURN && return 0
  local axis=$1 d out bad=""
  d=$(mktemp -d)
  printf 'Run 1 (https://x): success\n' > "$d/ci.md"; printf 'Thân ticket mẫu.\n' > "$d/ticket.md"
  out=$(bash "${TURN:-$turn}" "$axis" 9 main lane/issue-9 0123456789abcdef 89abcdef01234567 2 "${PROMPTS:-$prompts}" "$d/ci.md" "$d/ticket.md" 2>/dev/null) || bad="$bad exit"
  rm -rf "$d"
  printf '%s\n' "$out" | head -n1 | grep -q '^/kiro ' || bad="$bad no-/kiro-first"
  printf '%s\n' "$out" | grep -q 'Run 1 (https://x): success' || bad="$bad no-ci"
  printf '%s\n' "$out" | grep -q 'Thân ticket mẫu' || bad="$bad no-ticket"
  printf '%s\n' "$out" | grep -q '^## Tín hiệu' || bad="$bad no-prompt"
  printf '%s\n' "$out" | tail -n1 | grep -q "^<!-- harness:turn axis=$axis code=0123456789abcdef head=89abcdef01234567 round=2 at=" || bad="$bad no-marker-last"
  printf '%s\n' "$out" | grep -qiE 'npm |with-docker|master|postgres' && bad="$bad names-old-toolchain"
  printf '%s\n' "$out" | grep -q 'gate-segment.sh' || { [ "$axis" = standards ] || [ "$axis" = spec ] || bad="$bad no-gate-commands"; }
  if [ -z "$bad" ]; then ok "turn: $axis message renders"; else fail "turn: $axis message (problems:$bad)"; fi
}

# ---- merger (C5) helpers ------------------------------------------------------------------
# expect_merge <fixture> <true|false> [substring every reason list must contain]
expect_merge() {
  skip MERGE_FILTER && return 0
  local fixture=$1 want=$2 sub=${3:-} decision got reasons
  decision=$(jq -f "${MERGE_FILTER:-$merge_filter}" "$fixtures/$fixture" 2>/dev/null)
  got=$(jq -r '.merge' <<< "$decision" 2>/dev/null)
  reasons=$(jq -r '.reasons | join(" | ")' <<< "$decision" 2>/dev/null)
  if [ "$got" != "$want" ]; then fail "merge: $fixture (want merge=$want, got ${got:-<error>}; reasons: ${reasons:-none})"; return; fi
  if [ -n "$sub" ] && ! printf '%s' "$reasons" | grep -qF -- "$sub"; then fail "merge: $fixture (reasons lack \"$sub\": $reasons)"; return; fi
  ok "merge: $fixture merge=$want${sub:+ (reason: $sub)}"
}

# expect_supersede <fixture> <true|false>
expect_supersede() {
  skip MERGE_FILTER && return 0
  local fixture=$1 want=$2 got
  got=$(jq -f "${MERGE_FILTER:-$merge_filter}" "$fixtures/$fixture" 2>/dev/null | jq -r '.supersede')
  if [ "$got" = "$want" ]; then ok "merge: $fixture supersede=$want"; else fail "merge: $fixture (want supersede=$want, got ${got:-<error>})"; fi
}

run_cases() {
  # ---- guard rule 1: secret paths and names ----
  expect_guard "read .env is refused"                      2 '{"tool_name":"fs_read","tool_input":{"path":".env"}}'
  expect_guard "read nested .env.local is refused"         2 '{"tool_name":"fs_read","tool_input":{"path":"examples/quan-com/.env.local"}}'
  expect_guard "read .env.example is allowed"              0 '{"tool_name":"fs_read","tool_input":{"path":".env.example"}}'
  expect_guard "read ~/.pypirc is refused"                 2 '{"tool_name":"fs_read","tool_input":{"path":"/Users/x/.pypirc"}}'
  expect_guard "cat ~/.aws/credentials is refused"         2 '{"tool_name":"execute_bash","tool_input":{"command":"cat ~/.aws/credentials"}}'
  expect_guard "read an ordinary file is allowed"          0 '{"tool_name":"fs_read","tool_input":{"path":"docs/founder-vn-design.md"}}'
  expect_guard "write whose CONTENT mentions .env is allowed" 0 '{"tool_name":"fs_write","tool_input":{"path":".gitignore","content":".venv/\n.env\n.env.*\n"}}'
  expect_guard "echo of a credential variable is refused"  2 '{"tool_name":"execute_bash","tool_input":{"command":"echo $KIRO_API_KEY | base64"}}'
  expect_guard "echo of FOUNDER_LLM_API_KEY is refused"    2 '{"tool_name":"execute_bash","tool_input":{"command":"echo $FOUNDER_LLM_API_KEY"}}'
  expect_guard "echo of PYPI_TOKEN is refused"             2 '{"tool_name":"execute_bash","tool_input":{"command":"curl -u __token__:$PYPI_TOKEN https://upload.pypi.org"}}'
  expect_guard "naming FOUNDER_LLM_MODEL is allowed"       0 '{"tool_name":"execute_bash","tool_input":{"command":"test -n \"$FOUNDER_LLM_MODEL\" && echo model set"}}'
  expect_guard "printenv is refused"                       2 '{"tool_name":"execute_bash","tool_input":{"command":"printenv"}}'
  expect_guard "env alone is refused"                      2 '{"tool_name":"execute_bash","tool_input":{"command":"env | sort"}}'
  expect_guard "unknown schema naming .env falls back to refusal" 2 '{"kind":"mystery","args":["cat",".env"]}'
  # ---- guard rule 2: protected git operations ----
  expect_guard "push to lane branch is allowed"            0 '{"tool_name":"execute_bash","tool_input":{"command":"git push -u origin lane/issue-1"}}'
  expect_guard "push to main is refused"                   2 '{"tool_name":"execute_bash","tool_input":{"command":"git push origin main"}}'
  expect_guard "push to master is refused"                 2 '{"tool_name":"execute_bash","tool_input":{"command":"git push origin master"}}'
  expect_guard "push HEAD:main refspec is refused"         2 '{"tool_name":"execute_bash","tool_input":{"command":"git push origin HEAD:main"}}'
  expect_guard "force push is refused"                     2 '{"tool_name":"execute_bash","tool_input":{"command":"git push --force origin lane/issue-1"}}'
  expect_guard "remote branch delete is refused"           2 '{"tool_name":"execute_bash","tool_input":{"command":"git push origin :lane/issue-1"}}'
  expect_guard "deleting main locally is refused"          2 '{"tool_name":"execute_bash","tool_input":{"command":"git branch -D main"}}'
  expect_guard "gh pr merge is refused"                    2 '{"tool_name":"execute_bash","tool_input":{"command":"gh pr merge 40 --merge"}}'
  expect_guard "merge via REST is refused"                 2 '{"tool_name":"execute_bash","tool_input":{"command":"gh api -X PUT repos/o/r/pulls/40/merge"}}'
  expect_guard "git log is allowed"                        0 '{"tool_name":"execute_bash","tool_input":{"command":"git log --oneline main..HEAD"}}'
  expect_guard "doc write mentioning gh pr merge is allowed" 0 '{"tool_name":"fs_write","tool_input":{"path":"docs/agents/x.md","content":"The merger runs gh pr merge when all four conditions hold."}}'
  expect_guard "shell payload without command key still scanned" 2 '{"tool_name":"execute_bash","tool_input":{"cmdline":"git push origin main"}}'
  # ---- guard rule 3: single-owner files ----
  expect_guard "one-owner README with no grant is refused" 2 '{"tool_name":"fs_write","tool_input":{"path":"README.md","content":"x"}}'
  expect_guard "one-owner pyproject with no grant is refused" 2 '{"tool_name":"fs_write","tool_input":{"path":"pyproject.toml","content":"x"}}'
  expect_guard "one-owner README with grant all is allowed" 0 '{"tool_name":"fs_write","tool_input":{"path":"README.md","content":"x"}}' HARNESS_SINGLE_OWNER_FILES=all
  expect_guard "one-owner README with exact grant is allowed" 0 '{"tool_name":"fs_write","tool_input":{"path":"README.md","content":"x"}}' HARNESS_SINGLE_OWNER_FILES=README.md
  expect_guard "one-owner glob entry is refused without grant" 2 '{"tool_name":"fs_write","tool_input":{"path":"tests/golden/cfo.txt","content":"x"}}' HARNESS_SINGLE_OWNER_FILES=README.md
  expect_guard "file outside the list is allowed"          0 '{"tool_name":"fs_write","tool_input":{"path":"src/founder_vn/cfo.py","content":"x"}}'
  expect_guard "absolute path is normalised against PWD"   2 "{\"tool_name\":\"fs_write\",\"tool_input\":{\"path\":\"$PWD/README.md\",\"content\":\"x\"}}"
  # ---- committed skill links (FV-D6) ----
  expect_skill_links "relative link to a committed skill holds"   0 ok
  expect_skill_links "absolute link target is refused"            1 absolute
  expect_skill_links "link to a missing SKILL.md is refused"      1 dangling
  expect_skill_links "link not committed is refused"              1 uncommitted
  expect_skill_links "a directory instead of a link is refused"   1 notlink
  expect_skill_links "no links at all is refused"                 1 none
  expect_skill_links "link to another skill's folder is refused"  1 wrongname
  # ---- skill-lint (FV-D2): the machine half of the review checklist ----
  expect_skill_lint "ok"                  0
  expect_skill_lint "empty"               0
  expect_skill_lint "missing-frontmatter" 1 "no frontmatter"
  expect_skill_lint "name-mismatch"       1 "expected 'founder-cfo'"
  expect_skill_lint "no-vietnamese"       1 "no Vietnamese trigger phrase"
  expect_skill_lint "no-license"          1 "license missing"
  expect_skill_lint "version-mismatch"    1 "differs from pyproject"
  expect_skill_lint "dollar"              1 "SKILL.md:21:"
  expect_skill_lint "examples-dollar"     1 "cfo.md:3:"
  # ---- post-commit autopush (D23) ----
  expect_autopush "commit on a lane branch is pushed"        lane/issue-9 pushed
  expect_autopush "commit on main stays local"               main         kept
  expect_autopush "commit on a harness branch stays local"   harness/x    kept
  expect_autopush "commit during a rebase stays local"       lane/issue-9 kept rebase
  expect_autopush "HARNESS_AUTOPUSH=0 keeps the commit local" lane/issue-9 kept "" HARNESS_AUTOPUSH=0
  # ---- pre-commit ruff format check ----
  expect_precommit "unformatted staged file is refused"       "UNFORMATTED" refused
  expect_precommit "formatted staged file is committed"      "fine"        committed
  expect_precommit "HARNESS_PRECOMMIT=0 commits anyway"      "UNFORMATTED" committed HARNESS_PRECOMMIT=0
  expect_precommit "no ruff installed, commit stands"        "UNFORMATTED" committed
  expect_precommit "a non-Python file is not checked"        "UNFORMATTED" committed
  # ---- gate logger (D27) ----
  expect_runlog "green gate: log kept, summary printed, exit 0" 0 logged summary sh -c 'echo "== 3 passed in 0.12s =="; echo noise'
  expect_runlog "red gate keeps its own exit code"              3 logged summary sh -c 'echo "== 1 failed, 2 passed in 0.12s =="; exit 3'
  expect_runlog "stderr is logged too"                          0 logged summary sh -c 'echo "== 2 passed in 0.05s ==" >&2'
  # ---- segmented final gate (D28) ----
  expect_gateseg "three green segments verify GREEN"             0 three
  expect_gateseg "a red segment keeps its exit code, verify RED" 1 fail
  expect_gateseg "a segment never run is RED"                    1 missing
  expect_gateseg "segments on different HEADs are RED"           1 moved
  expect_gateseg "a docs commit after the segments stays GREEN"  0 docs-after
  # ---- rule documents name real paths ----
  expect_doc_paths "every named path exists"                 0 present
  expect_doc_paths "a missing path is refused"               1 missing
  expect_doc_paths "a placeholder path is skipped"           0 placeholder
  expect_doc_paths "a directory reference is skipped"        0 directory
  expect_doc_paths "an Owner/repo slug is skipped"           0 slug
  expect_doc_paths "a git-ignored runtime file is skipped"   0 ignored
  expect_doc_paths "a bare file name is skipped"             0 bare
  # ---- frontier (C1) ----
  expect_pick "frontier-basic.json" 1
  # The spec issue (#1 here) has sub-issues and the ready-for-agent label: a parent is never a lane.
  expect_pick "frontier-spec-parent.json" 2
  expect_pick "frontier-priority.json" 4
  expect_pick "frontier-resumed-vs-priority.json" 1
  expect_action "frontier-ack-error.json" 12 redispatch
  expect_pick "frontier-ack-error.json" 12
  expect_action "frontier-ack-error-fresh.json" 12 none
  expect_pick "frontier-ack-error-fresh.json" null
  expect_action "frontier-ack-error-pushing.json" 12 none
  expect_pick "frontier-ack-error-pushing.json" null
  expect_action "frontier-evidence-quiet.json" 12 redispatch
  expect_pick "frontier-evidence-quiet.json" 12
  expect_action "frontier-evidence-fresh.json" 12 none
  expect_pick "frontier-evidence-fresh.json" null
  expect_pick "frontier-mentions-closes.json" 1
  expect_pick "frontier-blocked.json" 3
  expect_pick "frontier-wip-full.json" null
  expect_pick "frontier-pr-in-flight.json" null
  expect_pick "frontier-human-and-map.json" 5
  expect_reconcile "frontier-blocked-signal.json" "[7]"
  expect_pick "frontier-blocked-signal.json" 8
  expect_reconcile "frontier-stalled.json" "[9]"
  expect_pick "frontier-stalled.json" 10
  expect_reconcile "frontier-acked.json" "[]"
  expect_pick "frontier-acked.json" null
  expect_reconcile "frontier-fresh-label.json" "[]"
  expect_pick "frontier-fresh-label.json" null
  expect_reconcile "frontier-silent.json" "[12]"
  expect_action "frontier-silent.json" 12 redispatch
  expect_pick "frontier-silent.json" 12
  # silent_after is 60 minutes: 45 minutes without a branch is a working lane, 105 is a silent one.
  expect_reconcile "frontier-silent-45min.json" "[]"
  expect_pick "frontier-silent-45min.json" null
  expect_reconcile "frontier-silent-105min.json" "[12]"
  expect_action "frontier-silent-105min.json" 12 redispatch
  # A branch that moved within silent_after is a working lane; an old push is not.
  expect_reconcile "frontier-silent-pushing.json" "[]"
  expect_pick "frontier-silent-pushing.json" null
  expect_action "frontier-silent-old-push.json" 12 redispatch
  expect_reconcile "frontier-silent-again.json" "[12]"
  expect_action "frontier-silent-again.json" 12 mark-silent
  expect_action "frontier-silent-again-progress.json" 12 redispatch
  expect_pick "frontier-silent-again-progress.json" 12
  expect_action "frontier-silent-again-exhausted.json" 12 mark-silent
  expect_pick "frontier-silent-again.json" 13
  expect_reconcile "frontier-silent-pr.json" "[]"
  expect_pick "frontier-silent-pr.json" null
  expect_allocation "frontier-basic.json" singleOwnerFiles all
  expect_allocation "frontier-basic.json" laneBranch lane/issue-1
  expect_allocation "frontier-basic.json" targetBranch main
  # ---- lane adoption (D24) ----
  expect_adopt "adopt-ready.json"       true
  expect_adopt "adopt-open-pr.json"     false "already open"
  expect_adopt "adopt-fresh-push.json"  false "wait 600 s of quiet"
  expect_adopt "adopt-no-evidence.json" false "no evidence file"
  expect_adopt "adopt-not-green.json"   false "does not record"
  expect_adopt "adopt-no-branch.json"   false "no branch"
  expect_adopt "adopt-not-ahead.json"   false "no commit beyond the base"
  expect_prbody "body names the ticket, promises COMPLETE, copies the gate block and the files"
  expect_apierr "api-error-refs.json"  "not all refs are readable"
  expect_apierr "api-error-field.json" "head invalid"
  # ---- verify-pick.jq: the direct read of a pick before an allocation (D47, D51) ----
  expect_verify "verify-pick-clean.json" true
  expect_verify "verify-pick-recalled.json" true
  expect_verify "verify-pick-recalled-other.json" false
  expect_verify "verify-pick-stale-kiro.json" false
  expect_verify "verify-pick-closed.json" false
  # ---- lane PR opener (D26) ----
  expect_openpr "pushed lane with a complete body opens the PR" opened
  expect_openpr "a PR already open for the branch is reused"    reused  existing
  expect_openpr "HEAD not on origin is refused"                 refused unpushed
  expect_openpr "body without Closes #<n> is refused"           refused noclose
  expect_openpr "body without the COMPLETE promise is refused"  refused nocomplete
  expect_openpr "HEAD on another branch is refused"             refused wrongbranch
  expect_openpr "uncommitted changes are refused"               refused dirty
  # ---- the code commit of a lane (D40): reports and the ledger are not code ----
  expect_lanecode "a report and a ledger after the last slice do not move the code commit" code
  expect_lanecode "a commit that touches the ledger and a source file is code"             mixed
  expect_lanecode "nothing but reports since the target: the merge-base"                   base
  # ---- review orchestrator (C4) ----
  expect_web "review-web-fresh.json" post '["standards","spec"]'
  expect_web "review-web-off.json" off
  expect_web "review-web-gate-running.json" wait
  expect_web "review-web-gate-none.json" wait
  expect_web "review-web-no-gate-file.json" post '["standards","spec"]'
  expect_web "review-web-pending.json" wait
  expect_web "review-web-half.json" post '["spec"]'
  expect_web "review-web-half-pending.json" wait
  expect_web "review-web-stale-repost.json" post '["standards","spec"]'
  expect_web "review-web-stalled.json" stalled
  expect_web "review-web-old-code-turns.json" post '["standards","spec"]'
  expect_web "review-web-pass.json" done
  expect_web "review-web-stale-pass.json" post '["standards"]'
  expect_web "review-web-changes.json" address '["address"]'
  expect_web "review-web-no-signal.json" address
  expect_web "review-web-address-pending.json" wait
  expect_web "review-web-address-stalled.json" stalled
  expect_web "review-web-blocked.json" blocked '["spec"]'
  expect_web "review-web-exhausted.json" exhausted
  expect_web "review-web-turn-cap.json" exhausted
  expect_web "review-web-gate-red.json" address '["address"]'
  expect_web "review-web-gate-red-reviews-pending.json" wait '["standards","spec"]'
  expect_web "review-web-gate-red-pass.json" address '["address"]'
  expect_web "review-web-gate-red-address-pending.json" wait
  expect_web "review-web-gate-cancelled.json" wait
  expect_web "review-web-gate-red-exhausted.json" exhausted
  expect_web "review-web-repost-same-code.json" address '["address"]'
  expect_web "review-web-exhausted-settling.json" wait
  expect_web "review-web-parked.json" off
  expect_web "review-web-conflicting.json" sync '["sync"]'
  expect_web "review-web-conflicting-pending.json" wait '["sync"]'
  expect_web "review-web-conflicting-stalled.json" stalled '["sync"]'
  expect_web "review-web-conflict-cleared.json" address '["address"]'
  expect_web "review-web-pass-over-cap.json" done
  expect_web "review-web-post-after-address-settling.json" wait '["standards","spec"]'
  expect_web "review-web-post-after-address-quiet.json" post '["standards","spec"]'
  expect_web "review-web-post-fresh-lane-settling.json" post '["standards","spec"]'
  expect_web "review-web-turn-cap-duplicates.json" post '["standards","spec"]'
  # ---- the /kiro message of a turn ----
  expect_turn standards
  expect_turn spec
  expect_turn address
  expect_turn sync
  # ---- merger (C5) ----
  expect_merge "merge-lane-pass.json" true
  expect_merge "merge-lane-findings-ledger.json" true
  # Ledger lines may open with a list marker, as report headings and bullets may (D22).
  expect_merge "merge-lane-bullet-ledger.json" true
  expect_merge "merge-lane-ledger-gap.json" false "ledger misses S2"
  expect_merge "merge-lane-ledger-gap.json" false "never named: SPEC-9"
  expect_merge "merge-lane-ledger-wrong-title.json" false "ledger title does not name #4"
  expect_merge "merge-lane-own-ledger.json" true
  expect_merge "merge-lane-not-passed.json" false "standards verdict is <promise>CHANGES_REQUESTED</promise>"
  expect_merge "merge-lane-wrong-branch.json" false "not the allocated lane branch"
  expect_merge "merge-lane-failing-check.json" false "failing checks: gate=failure"
  expect_merge "merge-lane-no-reports.json" false "standards.md is missing"
  expect_merge "merge-harness-label.json" true
  # A harness pull request still in draft (PR #21 while this harness was being built) waits.
  expect_merge "merge-harness-draft.json" false "pull request is a draft"
  # GitHub acts on a closing keyword wherever it stands (nhan M-42).
  expect_merge "merge-harness-mentions-closes.json" false "must not close an issue"
  expect_merge "merge-harness-closing-commit.json" false "closes #32: a harness pull request must not close an issue"
  expect_merge "merge-harness-closing-body.json" false "closes #7: a harness pull request must not close an issue"
  expect_merge "merge-lane-foreign-closes.json" false "closes #12, not this lane's ticket #3"
  expect_merge "merge-lane-blocked.json" false "issue #3 is blocked by open #2"
  expect_merge "merge-lane-blockers-closed.json" true
  expect_merge "merge-harness-wrong-author.json" false "is not the operator"
  expect_merge "merge-plain-pr.json" false "neither a lane pull request"
  expect_merge "merge-lane-gate-missing.json" false "Gate has not run at this commit"
  expect_merge "merge-lane-gate-failed.json" false "Gate concluded failure"
  expect_merge "merge-lane-gate-green.json" true
  expect_merge "merge-lane-gate-parked.json" true
  expect_merge "merge-lane-rounds.json" true
  # Earlier rounds' ids keep demanding a ledger even when the current reports name none (nhan M-28).
  expect_merge "merge-lane-rounds-ledger-missing.json" false "findings S1 recorded but reviews/issue-3/ledger.md is missing"
  expect_merge "merge-lane-ledger-missing.json" false "ledger.md is missing"
  expect_merge "merge-lane-review-check.json" true
  expect_merge "merge-lane-stale-report.json" false "spec report predates the last code commit"
  expect_merge "merge-lane-ticket-closed.json" false "issue #3 is closed"
  expect_supersede "merge-lane-ticket-closed.json" true
  expect_supersede "merge-lane-pass.json" false
}

if [ "$mode" = "--witness-red" ]; then
  # Each mutation removes one mechanism; the run must then contain at least one FAIL.
  run_mutation() {
    local label=$1 target=$2 expr=$3 tmp
    tmp=$(mktemp)
    sed -E "$expr" "$target" > "$tmp"
    local out
    if [ "$target" = "$guard" ]; then
      out=$(GUARD="$tmp" WITNESS_ONLY=GUARD run_cases 2>/dev/null)
    elif [ "$target" = "$skill_links" ]; then
      out=$(SKILL_LINKS="$tmp" WITNESS_ONLY=SKILL_LINKS run_cases 2>/dev/null)
    elif [ "$target" = "$skill_lint" ]; then
      out=$(SKILL_LINT="$tmp" WITNESS_ONLY=SKILL_LINT run_cases 2>/dev/null)
    elif [ "$target" = "$hook" ]; then
      out=$(HOOK="$tmp" WITNESS_ONLY=HOOK run_cases 2>/dev/null)
    elif [ "$target" = "$precommit" ]; then
      out=$(PRECOMMIT="$tmp" WITNESS_ONLY=PRECOMMIT run_cases 2>/dev/null)
    elif [ "$target" = "$runlog" ]; then
      out=$(RUNLOG="$tmp" WITNESS_ONLY=RUNLOG run_cases 2>/dev/null)
    elif [ "$target" = "$gateseg" ]; then
      out=$(GATESEG="$tmp" WITNESS_ONLY=GATESEG run_cases 2>/dev/null)
    elif [ "$target" = "$doc_paths" ]; then
      out=$(DOC_PATHS="$tmp" WITNESS_ONLY=DOC_PATHS run_cases 2>/dev/null)
    elif [ "$target" = "$filter" ]; then
      out=$(FILTER="$tmp" WITNESS_ONLY=FILTER run_cases 2>/dev/null)
    elif [ "$target" = "$adopt_filter" ]; then
      out=$(ADOPT_FILTER="$tmp" WITNESS_ONLY=ADOPT_FILTER run_cases 2>/dev/null)
    elif [ "$target" = "$verify_filter" ]; then
      out=$(VERIFY_FILTER="$tmp" WITNESS_ONLY=VERIFY_FILTER run_cases 2>/dev/null)
    elif [ "$target" = "$apierr_filter" ]; then
      out=$(APIERR_FILTER="$tmp" WITNESS_ONLY=APIERR_FILTER run_cases 2>/dev/null)
    elif [ "$target" = "$openpr" ]; then
      out=$(OPENPR="$tmp" WITNESS_ONLY=OPENPR run_cases 2>/dev/null)
    elif [ "$target" = "$prbody" ]; then
      out=$(PRBODY="$tmp" WITNESS_ONLY=PRBODY run_cases 2>/dev/null)
    elif [ "$target" = "$lanecode" ]; then
      out=$(LANECODE="$tmp" WITNESS_ONLY=LANECODE run_cases 2>/dev/null)
    elif [ "$target" = "$web_filter" ]; then
      out=$(WEB_FILTER="$tmp" WITNESS_ONLY=WEB_FILTER run_cases 2>/dev/null)
    elif [ "$target" = "$turn" ]; then
      out=$(TURN="$tmp" WITNESS_ONLY=TURN run_cases 2>/dev/null)
    elif [ "$target" = "$merge_filter" ]; then
      out=$(MERGE_FILTER="$tmp" WITNESS_ONLY=MERGE_FILTER run_cases 2>/dev/null)
    else
      printf 'witness: no case family for %s\n' "$target" >&2
      out="FAIL no family"
      out=""
    fi
    rm -f "$tmp"
    if printf '%s' "$out" | grep -q '^FAIL'; then
      printf 'RED   mutation "%s" turned %s case(s) red\n' "$label" "$(printf '%s' "$out" | grep -c '^FAIL')"
    else
      printf 'GREEN mutation "%s" changed nothing: the cases do not guard it\n' "$label"
    fi
  }
  red_mutations() {
  # sed -E: every escaped character below is an ERE metacharacter, so the escape means "literal".
  mutate "drop the .env pattern"                 "$guard"  "s#'\\\\\\.env\\(#'\\\\.never-matches(#"
  mutate "drop the .pypirc pattern"              "$guard"  "s#'\\\\\\.pypirc'#'\\\\.never-matches'#"
  mutate "drop the push-to-main pattern"         "$guard"  "s#\\(master\\|main\\)#(never-a-branch)#g"
  mutate "forget the FOUNDER_LLM_API_KEY name"   "$guard"  "s#\\|FOUNDER_LLM_API_KEY##"
  mutate "forget the PyPI token names"           "$guard"  "s#\\|PYPI_TOKEN\\|PYPI_API_TOKEN##"
  mutate "drop the environment dump rule"        "$guard"  "s#matches \"\\\$commands\" \"\\\$ENV_DUMP\"#false#"
  mutate "drop the single-owner refusal"         "$guard"  "s#refuse \"\\\$p is a single-owner#true \"#"
  mutate "accept a link to another skill or an absolute one" "$skill_links" 's#^expected_target\(\) .*#expected_target() { true; }#'
  mutate "accept a link to a missing SKILL.md"   "$skill_links" 's#^has_skill\(\) .*#has_skill() { true; }#'
  mutate "accept an uncommitted link or skill"   "$skill_links" 's#^tracked\(\) .*#tracked() { true; }#'
  mutate "accept a checkout with no links"       "$skill_links" 's#if \[ "\$count" -eq 0 \]; then#if false; then#'
  mutate "lint: accept a dollar sign next to a digit" "$skill_lint" 's#^    return DOLLAR\.search\(line\) is None#    return True#'
  mutate "lint: accept a skill named unlike its folder" "$skill_lint" 's#^    return fm\.get\("name"\) == folder#    return True#'
  mutate "lint: accept an English-only description" "$skill_lint" 's#^    return VIETNAMESE\.search\(text or ""\) is not None#    return True#'
  mutate "lint: accept a skill without a license" "$skill_lint" 's#^    return bool\(fm\.get\("license"\)\)#    return True#'
  mutate "lint: accept a version unlike the package" "$skill_lint" 's#^    return project is None or skill == project#    return True#'
  mutate "lint: accept a SKILL.md without frontmatter" "$skill_lint" 's#^        findings\.append\(f"\{rel\}:1: no frontmatter.*#        pass#'
  mutate "never push a lane branch"          "$hook"   's#lane/issue-\*\) ;;#never/*) ;;#'
  mutate "push from inside a rebase"         "$hook"   's#-d "\$gitdir/rebase-merge"#-d "$gitdir/never-a-dir"#'
  mutate "drop the HARNESS_AUTOPUSH switch"  "$hook"   's#HARNESS_AUTOPUSH:-1#HARNESS_AUTOPUSH_NEVER:-1#'
  mutate "commit unformatted code"            "$precommit" 's#^  exit 1$#  exit 0#'
  mutate "drop the HARNESS_PRECOMMIT switch"  "$precommit" 's#HARNESS_PRECOMMIT:-1#HARNESS_PRECOMMIT_NEVER:-1#'
  mutate "swallow the gate's exit code"         "$runlog" 's#^exit "\$rc"#exit 0#'
  mutate "run the gate without keeping a log"   "$runlog" 's#\| tee "\$log"#| cat#'
  mutate "print no summary"                     "$runlog" 's#^grep -E .*#true#'
  mutate "record every segment as exit 0"       "$gateseg" 's#^    record "\$seg" "\$rc"#    record "$seg" 0#'
  mutate "verify ignores a failed segment"      "$gateseg" 's#\[ "\$rc" = 0 \] \|\| bad=1#true#'
  mutate "verify ignores a missing segment"     "$gateseg" 's#bad=1; continue; fi#continue; fi#'
  mutate "verify ignores a moved HEAD"          "$gateseg" 's#elif \[ "\$sha" != "\$ref" \]; then bad=1; fi#fi#'
  mutate "doc-paths: accept a missing path"     "$doc_paths" 's#^exists\(\) .*#exists() { true; }#'
  # ---- frontier (C1) ----
  mutate "ignore open blockers"             "$filter" "s#select\\(open_blockers == 0\\)#select(true)#"
  mutate "ignore the priority label"        "$filter" 's#priority: has_label\("priority"\)#priority: false#'
  mutate "read a quoted closing keyword"    "$filter" 's#\(\^\|\\\\n\)\[ \\\\t\]\*#(?:)#'
  mutate "ignore the wip limit"             "$filter" "s#>= \\.wip#>= 999#g"
  mutate "ignore the BLOCKED signal"        "$filter" "s#test\\(\"<promise>BLOCKED</promise>\"\\)#false#"
  mutate "ignore the stall timeout"         "$filter" "s#> stalled_after#> 999999999#"
  mutate "ignore the silence timeout"       "$filter" "s#> window#> 999999999#"
  mutate "wait an hour for a lane that wrote its evidence" "$filter" 's#then evidence_quiet_after else#then silent_after else#'
  mutate "trust an error reply as an acknowledgement" "$filter" 's#\(\.kiroAckError // false\)#false#'
  mutate "redispatch on an error reply before the session had time" "$filter" 's#> error_ack_after#> -1#'
  mutate "redispatch on an error reply while the branch moves" "$filter" 's#and \(\.lanePushedAt == null\)#and true#'
  mutate "let a priority ticket jump a resumed lane" "$filter" 's#resumed: \(\.laneBranch // false\)#resumed: false#'
  mutate "stretch the silence window to 120 minutes" "$filter" "s#silent_after: 3600#silent_after: 7200#"
  mutate "retry a silent lane forever"      "$filter" "s#<= silent_retries#<= 999#"
  mutate "recall a productive lane forever" "$filter" 's#< max_dispatches#< 999#'
  mutate "ignore progress since the last dispatch" "$filter" 's#\(\.progressSinceDispatch // false\)#false#'
  mutate "count a silent lane in flight"    "$filter" "s#and \\(silent\\(\\\$now; \\\$closes\\) \\| not\\)#and true#"
  mutate "ignore a lane that still pushes"  "$filter" 's#\.lanePushedAt == null or#true or#'
  mutate "dispatch a ready-for-human ticket" "$filter" 's#select\(has_label\("ready-for-human"\) \| not\)#select(true)#'
  mutate "dispatch the spec issue as a lane" "$filter" 's#^def is_parent: .*#def is_parent: false;#'
  mutate "allocate onto master"             "$filter" 's#^def target_branch: "main";#def target_branch: "master";#'
  # ---- lane adoption (D24) ----
  mutate "adopt a lane that already has a pull request" "$adopt_filter" 's#if \.openPr != null#if false#'
  mutate "adopt a branch that just moved"        "$adopt_filter" 's#< quiet_after#< -1#'
  mutate "adopt without an evidence file"        "$adopt_filter" 's#if \.evidence == null#if false#'
  mutate "adopt without the green verdict"       "$adopt_filter" 's#green \| not\)#false)#'
  mutate "adopt a branch that has not moved past the base" "$adopt_filter" 's#\(\.ahead // 0\) == 0#false#'
  mutate "open the harness pull request without Closes" "$prbody" 's#^Closes \#\$n$#Đóng \#$n#'
  mutate "hide the reason of a failed API call"   "$apierr_filter" 's#\.errors\[\]\?#.never[]?#'
  # ---- verify-pick (D47, D51) ----
  mutate "drop a recalled pick because it still carries kiro" "$verify_filter" 's#^def recalled: .*#def recalled: false;#'
  mutate "dispatch a ticket that already carries kiro" "$verify_filter" 's#^def clean: .*#def clean: true;#'
  mutate "dispatch a closed ticket"                    "$verify_filter" 's#^def open: .*#def open: true;#'
  # ---- lane PR opener (D26) ----
  mutate "open a PR from an unpushed HEAD"      "$openpr" 's#^on_origin\(\) .*#on_origin() { true; }#'
  mutate "open a PR without Closes"             "$openpr" 's#^names_closes\(\) .*#names_closes() { true; }#'
  mutate "open a PR without the COMPLETE promise" "$openpr" 's#^ends_complete\(\) .*#ends_complete() { true; }#'
  mutate "open a second PR for the same branch" "$openpr" 's#^open_pr_number\(\) .*#open_pr_number() { :; }#'
  mutate "open a PR from any branch"            "$openpr" 's#^on_lane_branch\(\) .*#on_lane_branch() { true; }#'
  mutate "open a PR over a dirty tree"          "$openpr" 's#^tree_clean\(\) .*#tree_clean() { true; }#'
  mutate "open a PR against master"             "$openpr" 's#^base=\$\{HARNESS_BASE:-main\}#base=master#'
  # ---- the code commit of a lane (D40) ----
  mutate "count a ledger commit as code"       "$lanecode" 's#^ledger=.*#ledger=#'
  # ---- review orchestrator (C4) ----
  mutate "ignore the gate entirely"          "$web_filter" 's#\$in\.gate\.required and#false and#g'
  mutate "treat a stale report as current"   "$web_filter" 's#\(\$in\.reports\[\$a\]\.current // false\) \| not#false#'
  mutate "repost a pending turn"             "$web_filter" 's#then "pending"#then "post"#'
  mutate "never stall a turn"                "$web_filter" 's#then "stalled"#then "post"#'
  mutate "ignore the address round cap"      "$web_filter" 's#address_rounds\(\$in\) >= \$in\.limits\.rounds#false#'
  mutate "read BLOCKED as changes"           "$web_filter" 's#then "blocked"#then "changes"#'
  mutate "read any verdict as PASS"          "$web_filter" 's#then "pass"#then "pass" elif true then "pass"#'
  mutate "ignore the switch"                 "$web_filter" 's#\(\$in\.enabled \| not\)#false#'
  mutate "ignore the turn cap"               "$web_filter" 's#>= \$in\.limits\.turns#>= 999999#'
  mutate "review code with a red gate"       "$web_filter" 's#\$in\.gate\.conclusion != "success"#false#'
  mutate "address a gate without a verdict"  "$web_filter" 's#\$in\.gate\.conclusion != "failure"#false#'
  mutate "count a re-posted turn as a new round" "$web_filter" 's#\| \.code \] \| unique \| length#] | length#'
  mutate "park a lane that is still pushing"  "$web_filter" 's#if settling\(\$in\) then#if false then#'
  mutate "review a parked ticket"            "$web_filter" 's#\(\$in\.lane\.parked // false\)#false#'
  mutate "review a conflicting pull request" "$web_filter" 's#== "CONFLICTING"#== "never"#'
  mutate "park a finished lane at the turn cap" "$web_filter" 's#and \(done_at_head\(\$in\) \| not\)#and true#'
  mutate "count a re-posted round toward the turn cap" "$web_filter" 's#\| axis_round \] \| unique \| length#] | length#'
  mutate "post a review round while the fix session may still be pushing" "$web_filter" 's#^def after_address\(\$in\): .*#def after_address($in): false;#'
  # ---- the /kiro message of a turn ----
  mutate "post a turn without the marker"    "$turn" 's#^printf .\\n<!-- harness:turn .*#true#'
  mutate "post a turn without the prompt"    "$turn" 's#^cat "\$prompt_file"#true#'
  # ---- merger (C5) ----
  mutate "merge a quoted closing keyword"    "$merge_filter" 's#\(\^\|\\\\n\)\[ \\\\t\]\*#(?:)#'
  mutate "accept any review verdict"        "$merge_filter" "s#!= \"<promise>PASS</promise>\"#!= \"never\"#g"
  mutate "drop the ledger requirement"      "$merge_filter" "s#if \\(\\\$ids \\| length\\) > 0#if false#g"
  mutate "ignore the ledger title"          "$merge_filter" 's#ledger_title_names(\$r\.ledger; \$n) | not#false#g'
  mutate "refuse a ledger line that opens with a list marker" "$merge_filter" 's#(?:\[-\*\]\[ \\\\t\]+)?(S\[0-9\]+|SPEC-\[0-9\]+)\[ \\\\t\]+(FIXED#(S[0-9]+|SPEC-[0-9]+)[ \\\\t]+(FIXED#'
  mutate "ignore the allocated lane branch" "$merge_filter" "s#\\.ticket\\.laneBranch != \\.pr\\.headRef#false#"
  mutate "ignore failing checks"            "$merge_filter" "s#bad_conclusion \\| index\\(\\\$c\\)#false#"
  mutate "ignore the harness PR author"     "$merge_filter" "s#\\.pr\\.author != \\.operator#false#"
  mutate "never supersede a closed ticket"  "$merge_filter" "s#\\.ticket\\.state != \"open\";#false;#"
  mutate "ignore the Gate requirement"      "$merge_filter" "s#if \\(\\\$g\\.required \\| not\\) then \\[\\]#if true then []#"
  mutate "count parked gate runs as results" "$merge_filter" 's#select\(\.conclusion != "action_required"\)#select(true)#'
  mutate "forget earlier rounds' findings"   "$merge_filter" 's#\(\$r\.earlier // \[\]\)#[]#'
  mutate "accept a stale report"             "$merge_filter" 's#\$r\.current\.(standards|spec) == false#false#g'
  mutate "let a pull request close an issue"  "$merge_filter" 's#close\|closes\|closed\|fix\|fixes\|fixed\|resolve\|resolves\|resolved#never-a-keyword#'
  mutate "read closing keywords in the description only" "$merge_filter" 's#\+ \(\.pr\.commits // \[\]\)#+ []#'
  mutate "read closing keywords in commits only" "$merge_filter" 's#\[ \(\.pr\.body // ""\) \]#[]#'
  mutate "let a lane close another issue"     "$merge_filter" 's#select\(\. != \$own\)#select(false)#'
  mutate "ignore open blockers of the ticket" "$merge_filter" 's#select\(\.state == "open"\) \| \.number#select(false) | .number#'
  mutate "merge a draft pull request"         "$merge_filter" 's#if \.pr\.draft then#if false then#'
  }
  # The mutations run in parallel. Each `mutate` line above is numbered in order; this script
  # re-runs itself once per number with WITNESS_MUTATION set, and that child runs the one mutation
  # (its own temp files, its own stderr file). The parent counts the RED and GREEN lines: fewer
  # RED lines than mutations (a child that crashed, or a GREEN one) fails the run. WITNESS_JOBS
  # sets the parallelism (default: the machine's processors).
  mutation_n=0
  if [ -n "${WITNESS_MUTATION:-}" ]; then
    mutate() { mutation_n=$((mutation_n + 1)); [ "$mutation_n" = "$WITNESS_MUTATION" ] && run_mutation "$@"; true; }
    red_mutations
    exit 0
  fi
  mutate() { mutation_n=$((mutation_n + 1)); }
  red_mutations
  total=$mutation_n
  jobs=${WITNESS_JOBS:-$(getconf _NPROCESSORS_ONLN 2>/dev/null || printf 2)}
  out=$(seq 1 "$total" | xargs -P "$jobs" -I{} env WITNESS_MUTATION={} bash "$0" --witness-red)
  printf '%s\n' "$out"
  caught=$(printf '%s\n' "$out" | grep -c '^RED   mutation' || true)
  missed=$(printf '%s\n' "$out" | grep -c '^GREEN mutation' || true)
  if [ "$missed" -gt 0 ] || [ "$caught" -ne "$total" ]; then
    printf '\n%s of %s mutation(s) were not caught\n' "$((total - caught))" "$total"; exit 1
  fi
  printf '\nevery mutation was caught (%s, %s at a time)\n' "$total" "$jobs"
  exit 0
fi

run_cases
printf '\n%s passed, %s failed\n' "$passes" "$failures"
[ "$failures" -eq 0 ]
