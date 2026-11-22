#!/bin/bash
# Point this checkout's git hooks at .githooks/ (post-commit autopush of lane branches, D23;
# pre-commit ruff format check). nhan did this from npm's `prepare` script; a Python project has
# no such hook, so a lane runs this once before its first slice (the steering says so) and an
# operator runs it once per clone. Idempotent; prints what it set.
#
#   bash scripts/harness/install-hooks.sh
set -u
top=$(git rev-parse --show-toplevel 2>/dev/null) || { printf 'install-hooks: not inside a git checkout\n' >&2; exit 2; }
cd "$top" || exit 2
[ -d .githooks ] || { printf 'install-hooks: no .githooks/ directory in %s\n' "$top" >&2; exit 2; }
chmod +x .githooks/* 2>/dev/null || true
git config core.hooksPath .githooks
printf 'install-hooks: core.hooksPath = %s (hooks: %s)\n' "$(git config core.hooksPath)" "$(ls .githooks | tr '\n' ' ')"
