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
  mutate "lint: accept a dollar sign next to a digit" "$skill_lint" 's#^def rule_no_dollar\(.*#def rule_no_dollar(line): return True#'
  mutate "lint: accept a skill named unlike its folder" "$skill_lint" 's#^def rule_name_matches\(.*#def rule_name_matches(fm, folder): return True#'
  mutate "lint: accept an English-only description" "$skill_lint" 's#^def rule_has_vietnamese\(.*#def rule_has_vietnamese(text): return True#'
  mutate "lint: accept a skill without a license" "$skill_lint" 's#^def rule_has_license\(.*#def rule_has_license(fm): return True#'
  mutate "lint: accept a version unlike the package" "$skill_lint" 's#^def rule_version_matches\(.*#def rule_version_matches(skill, project): return True#'
  mutate "lint: accept a SKILL.md without frontmatter" "$skill_lint" 's#^        findings\.append\(f"\{rel\}:1: no frontmatter.*#        pass#'
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
