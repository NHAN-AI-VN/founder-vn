#!/bin/bash
# PreToolUse guard shared by every agent surface in this repository.
#
# Wired twice, one script: Kiro Web and the IDE run it through `.kiro/hooks/guard.json`; the
# CLI custom agent in `.kiro/agents/founder-guarded.json` runs it through its `hooks.preToolUse`
# entry, which also fails closed when this file cannot be found. Scope, blind spots and the
# measurements behind it live in docs/agents/kiro-harness.md, section "Guards". Ported from
# NHAN-AI-VN/nhan (.kiro/hooks/guard.sh at 8adef66b) with two additions: the model-provider and
# PyPI credentials this project uses, and `.pypirc` as a protected path.
#
# Hook contract: exit 0 allows the call; exit 2 blocks it and returns this script's stderr to the
# model. EVERY OTHER exit code prints a warning and ALLOWS the call, so a refusal that ends in
# exit 1 (a `set -u` error, a missing binary) is a guard that failed open. Each refusal path
# below, including internal errors, therefore goes through `refuse`, which exits 2.
#
# The guard is a string filter over the tool input, not a containment boundary. It refuses a call
# that NAMES a protected path or a forbidden command; a command that reaches the same thing
# without naming it (`cat .en*`, a script that reads the file) is not stopped.
#
# Three rules, one home for the logic:
#   1. secret paths and secret names: any tool naming `.env*`, `.pypirc`, `.aws/credentials`,
#      `.ssh/id_*`; any shell command naming a credential variable or dumping the environment
#   2. protected git operations: a shell command that pushes to main/master, force-pushes,
#      deletes a remote branch, or merges a pull request
#   3. single-owner files: a write to a path listed under "## One owner per merge" in
#      docs/agents/parallel-lanes.md that this lane was not granted through
#      HARNESS_SINGLE_OWNER_FILES (`all`, `none`, or a comma-separated list of globs; unset
#      means `none`)
set -u

refuse() {
  printf 'Refused: %s Blocked by .kiro/hooks/guard.sh.\n' "$1" >&2
  exit 2
}

if ! event=$(cat); then
  refuse "the tool input could not be read from STDIN; failing closed."
fi

# `grep -Eq` has three outcomes and all three matter: 0 match, 1 no match, 2+ malformed pattern
# or I/O error. An `if grep` reads any non-zero as "no match", so a broken pattern would fail
# open on exactly the maintenance path this file advertises. Branch on the status explicitly.
matches() {
  printf '%s' "$1" | grep -Eq "$2"
  local status=$?
  if [ "$status" -ge 2 ]; then
    refuse "guard.sh has a malformed pattern ($2); failing closed rather than passing an unmatched input."
  fi
  return "$status"
}

# Print the string value of every occurrence of JSON key $1 in the tool input, one per line,
# JSON escapes left as they are. Tool schemas differ between surfaces, so the keys are listed
# rather than assumed; the fallbacks below cover an input that carries none of them.
extract() {
  local re='"KEY"[[:space:]]*:[[:space:]]*"([^"\\]|\\.)*"'
  re=${re//KEY/$1}
  printf '%s' "$event" | grep -oE "$re" | sed -E 's/^"[^"]+"[[:space:]]*:[[:space:]]*"//; s/"$//'
  return 0
}

paths=$(for key in path file_path filePath paths directory cwd; do extract "$key"; done)
commands=$(for key in command cmd script; do extract "$key"; done)

# ---- 1. secret paths and secret names -----------------------------------------------------
# Extended regular expressions matched against the extracted paths and commands, or against the
# whole input when neither could be extracted. `.env.example` is a template and is filtered out
# first so it stays speakable.
PROTECTED_PATHS=(
  '\.env(\.[A-Za-z0-9_-]+)?'
  '\.pypirc'
  '\.aws/credentials'
  '\.ssh/id_[A-Za-z0-9_]+'
)
if [ "${#PROTECTED_PATHS[@]}" -eq 0 ]; then
  refuse "guard.sh has an empty PROTECTED_PATHS list; failing closed."
fi
if [ -n "$paths$commands" ]; then
  scope=$(printf '%s\n%s' "$paths" "$commands")
else
  scope=$event
fi
scope=$(printf '%s' "$scope" | sed -e 's/\.env\.example//g')
for pattern in "${PROTECTED_PATHS[@]}"; do
  if matches "$scope" "${pattern}([^A-Za-z0-9._-]|\$)"; then
    refuse "this tool call names a protected secret path (${pattern//\\/}). Ask the user to read it themselves if the value is genuinely needed."
  fi
done

# FOUNDER_LLM_API_KEY is the model-provider key the package reads (docs/founder-vn-design.md §2);
# the PyPI names are what `uv publish` and twine read. They may be SET in the sandbox; a lane
# never prints, writes or forwards them.
SECRET_NAMES='(KIRO_API_KEY|GITHUB_TOKEN|GH_TOKEN|AWS_SECRET_ACCESS_KEY|AWS_SESSION_TOKEN|NPM_TOKEN|FOUNDER_LLM_API_KEY|PYPI_TOKEN|PYPI_API_TOKEN|UV_PUBLISH_TOKEN|TWINE_PASSWORD)'
ENV_DUMP='((^|[^A-Za-z0-9_-])printenv([^A-Za-z0-9_-]|$)|(^|[;&|][[:space:]]*)env[[:space:]]*(\||;|&|$))'
if [ -n "$commands" ]; then
  if matches "$commands" "$SECRET_NAMES"; then
    refuse "this shell command names a credential variable. Credentials stay in the environment and are never echoed, written, or sent."
  fi
  if matches "$commands" "$ENV_DUMP"; then
    refuse "this shell command dumps the environment, which holds credentials. Read the one variable you need by name instead."
  fi
fi

# ---- 2. protected git operations ----------------------------------------------------------
# Applied to extracted shell commands. When no command key was found but the input names a
# shell-like tool, the whole input is scanned instead; a doc that merely mentions these
# commands goes through a write tool, which this branch does not reach.
GIT_FORBIDDEN=(
  'git[[:space:]]+push([[:space:]]+[^[:space:];&|]+)*[[:space:]]+(origin[[:space:]]+)?((refs/heads/)?(master|main)|[^[:space:]:]*:(refs/heads/)?(master|main))([^A-Za-z0-9_./-]|$)'
  'git[[:space:]]+push([[:space:]]+[^[:space:];&|]+)*[[:space:]]+(-f|--force|--force-with-lease|--force-if-includes|-d|--delete|--mirror)([^A-Za-z0-9_-]|$)'
  'git[[:space:]]+push([[:space:]]+[^[:space:];&|]+)*[[:space:]]+:[^[:space:]]'
  'git[[:space:]]+branch[[:space:]]+(-D|-d|--delete)[[:space:]]+(master|main)([^A-Za-z0-9_./-]|$)'
  'gh[[:space:]]+pr[[:space:]]+merge'
  'pulls/[0-9]+/merge'
)
git_scope=$commands
if [ -z "$git_scope" ] && matches "$event" '"(tool_name|toolName|name|tool)"[[:space:]]*:[[:space:]]*"[^"]*(bash|shell)'; then
  git_scope=$event
fi
if [ -n "$git_scope" ]; then
  for pattern in "${GIT_FORBIDDEN[@]}"; do
    if matches "$git_scope" "$pattern"; then
      refuse "this shell command pushes to the default branch, rewrites or deletes a shared branch, or merges a pull request. A lane ends at a pull request from its own branch; the merger is the harness."
    fi
  done
fi

# ---- 3. single-owner files ----------------------------------------------------------------
# The list is read from the "## One owner per merge" section of docs/agents/parallel-lanes.md:
# every bullet that opens with a backticked path, up to the next "## " heading, exactly as the
# lane allocator reads it. HARNESS_OWNED_PATHS_FILE overrides the file for the witness tests.
owned_file=${HARNESS_OWNED_PATHS_FILE:-docs/agents/parallel-lanes.md}
owned=''
if [ -f "$owned_file" ]; then
  owned=$(awk '/^## One owner per merge/{f=1; next} /^## /{f=0} f && /^- `/{sub(/^- `/, ""); sub(/`.*/, ""); print}' "$owned_file")
fi
grants=${HARNESS_SINGLE_OWNER_FILES:-none}
if [ -n "$owned" ] && [ -n "$paths" ] && [ "$grants" != "all" ]; then
  while IFS= read -r raw; do
    [ -z "$raw" ] && continue
    p=${raw#"$PWD"/}
    p=${p#./}
    while IFS= read -r pattern; do
      [ -z "$pattern" ] && continue
      # shellcheck disable=SC2254
      case "$p" in
        $pattern)
          granted=no
          if [ "$grants" != "none" ]; then
            IFS=',' read -ra grant_list <<< "$grants"
            for g in "${grant_list[@]}"; do
              g=$(printf '%s' "$g" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
              [ -z "$g" ] && continue
              # shellcheck disable=SC2254
              case "$p" in
                $g) granted=yes ;;
              esac
            done
          fi
          if [ "$granted" = no ]; then
            refuse "$p is a single-owner file (docs/agents/parallel-lanes.md) that this lane was not allocated. Report BLOCKED instead of editing it."
          fi
          ;;
      esac
    done <<< "$owned"
  done <<< "$paths"
fi

exit 0
