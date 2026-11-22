#!/bin/bash
# Every entry of .kiro/skills/ that is committed must be a relative symlink to a committed
# .agents/skills/<name>/SKILL.md, and must not point outside the repository (FV-D6 in
# docs/agents/kiro-harness.md). The upstream founder-* and the ID8Labs skills are git-ignored by
# name, so they are not checked: a lane's sandbox checkout never sees them.
#
#   bash scripts/harness/check-skill-links.sh            # exit 0 when every link holds
#   SKILL_LINKS_ROOT=<dir> bash scripts/harness/check-skill-links.sh   # another checkout (witness)
set -u
root=${SKILL_LINKS_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}
cd "$root" || exit 2
bad=0
count=0

tracked() { git ls-files --error-unmatch -- "$1" >/dev/null 2>&1; }

for link in .kiro/skills/*; do
  [ -e "$link" ] || [ -L "$link" ] || continue
  name=$(basename "$link")
  # Ignored entries (founder-*, ID8Labs) are outside the contract.
  if git check-ignore -q -- "$link"; then continue; fi
  count=$((count + 1))
  if [ ! -L "$link" ]; then
    printf 'check-skill-links: %s is not a symlink\n' "$link" >&2; bad=1; continue
  fi
  target=$(readlink "$link")
  case "$target" in
    /*) printf 'check-skill-links: %s points to an absolute path (%s)\n' "$link" "$target" >&2; bad=1; continue ;;
  esac
  if [ "$target" != "../../.agents/skills/$name" ]; then
    printf 'check-skill-links: %s points to %s, expected ../../.agents/skills/%s\n' "$link" "$target" "$name" >&2; bad=1; continue
  fi
  if [ ! -f ".agents/skills/$name/SKILL.md" ]; then
    printf 'check-skill-links: %s has no .agents/skills/%s/SKILL.md\n' "$link" "$name" >&2; bad=1; continue
  fi
  if ! tracked ".agents/skills/$name/SKILL.md"; then
    printf 'check-skill-links: .agents/skills/%s/SKILL.md is not committed\n' "$name" >&2; bad=1; continue
  fi
  if ! tracked "$link"; then
    printf 'check-skill-links: %s is not committed\n' "$link" >&2; bad=1; continue
  fi
done

if [ "$count" -eq 0 ]; then printf 'check-skill-links: no committed skill links under .kiro/skills\n' >&2; exit 1; fi
if [ "$bad" -ne 0 ]; then exit 1; fi
printf 'check-skill-links: %s links hold\n' "$count"
exit 0
