#!/bin/bash
# Every backticked path with a directory component in AGENTS.md and .kiro/steering/*.md must
# exist in the checkout. A rule that points at a file that is not there sends an unattended
# lane looking for it (nhan: four agents once pointed at a prompt path the CLI resolved
# elsewhere). Skipped on purpose: placeholders (`<n>`, `*`), directories (trailing `/`),
# paths git ignores (runtime files such as .harness/gate-segments.txt), and bare file names
# without a directory (pyproject.toml, GLOSSARY.md: named before they exist by design).
#
#   bash scripts/harness/check-doc-paths.sh [file...]      # default: AGENTS.md .kiro/steering/*.md
#   DOC_PATHS_ROOT=<dir> bash scripts/harness/check-doc-paths.sh   # another checkout (witness)
set -u
root=${DOC_PATHS_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}
cd "$root" || exit 2
if [ $# -gt 0 ]; then docs=("$@"); else docs=(AGENTS.md .kiro/steering/*.md); fi

is_placeholder() { case "$1" in *'<'*|*'*'*|*'…'*) return 0 ;; esac; return 1; }
is_directory_ref() { case "$1" in */) return 0 ;; esac; return 1; }
# `Owner/repo` slugs (NHAN-AI-VN/founder-vn): the first segment carries an upper-case letter,
# which no directory of this repository does.
is_repo_slug() { case "${1%%/*}" in *[[:upper:]]*) return 0 ;; esac; return 1; }
is_ignored() { git check-ignore -q -- "$1" 2>/dev/null; }
exists() { [ -e "$1" ]; }

bad=0
checked=0
for doc in "${docs[@]}"; do
  [ -f "$doc" ] || { printf 'check-doc-paths: %s not found\n' "$doc" >&2; bad=1; continue; }
  # A path: backticked, has a slash, starts with a letter or a dot, no spaces. The sed keeps the
  # text between the backticks only.
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    is_placeholder "$p" && continue
    is_directory_ref "$p" && continue
    is_repo_slug "$p" && continue
    is_ignored "$p" && continue
    checked=$((checked + 1))
    if ! exists "$p"; then printf 'check-doc-paths: %s names %s, which does not exist\n' "$doc" "$p" >&2; bad=1; fi
  done < <(grep -oE '`[.A-Za-z0-9_][^` ]*/[^` ]*`' "$doc" | sed -E 's/^`//; s/`$//' | sort -u)
done
[ "$bad" -eq 0 ] && printf 'check-doc-paths: %s path(s) in %s file(s) exist\n' "$checked" "${#docs[@]}"
exit "$bad"
