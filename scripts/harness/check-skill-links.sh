#!/bin/bash
# Every entry of .kiro/skills/ that is committed must be a relative symlink to a committed
# .agents/skills/<name>/SKILL.md, and must not point outside the repository (FV-D6 in
# docs/agents/kiro-harness.md). The upstream founder-* and the ID8Labs skills are git-ignored by
# name, so they are not checked: a lane's sandbox checkout never sees them.
#
#   bash scripts/harness/check-skill-links.sh                        # exit 0 when every link holds
#   SKILL_LINKS_ROOT=<dir> bash scripts/harness/check-skill-links.sh # another checkout (witness)
#
# One predicate per rule so scripts/harness/witness.sh can mutate each and require a red case.
# An absolute target, or a directory where the link should be, is refused by expected_target
# (neither equals the relative path); the first two messages below only name the cause.
set -u
root=${SKILL_LINKS_ROOT:-$(cd "$(dirname "$0")/../.." && pwd)}
cd "$root" || exit 2

expected_target() { [ "$1" = "../../.agents/skills/$2" ]; }
has_skill() { [ -f ".agents/skills/$1/SKILL.md" ]; }
tracked() { git ls-files --error-unmatch -- "$1" >/dev/null 2>&1; }

bad=0
count=0
for link in .kiro/skills/*; do
  [ -e "$link" ] || [ -L "$link" ] || continue
  name=$(basename "$link")
  # Ignored entries (founder-*, ID8Labs) are outside the contract.
  if git check-ignore -q -- "$link"; then continue; fi
  count=$((count + 1))
  target=$(readlink "$link" 2>/dev/null || true)
  if ! expected_target "$target" "$name"; then
    if [ ! -L "$link" ]; then printf 'check-skill-links: %s is not a symlink\n' "$link" >&2
    else printf 'check-skill-links: %s points to %s, expected ../../.agents/skills/%s\n' "$link" "$target" "$name" >&2; fi
    bad=1; continue
  fi
  if ! has_skill "$name"; then printf 'check-skill-links: %s has no .agents/skills/%s/SKILL.md in the working tree\n' "$link" "$name" >&2; bad=1; continue; fi
  if ! tracked ".agents/skills/$name/SKILL.md"; then printf 'check-skill-links: .agents/skills/%s/SKILL.md is not committed\n' "$name" >&2; bad=1; continue; fi
  if ! tracked "$link"; then printf 'check-skill-links: %s is not committed\n' "$link" >&2; bad=1; continue; fi
done

if [ "$count" -eq 0 ]; then printf 'check-skill-links: no committed skill links under .kiro/skills\n' >&2; exit 1; fi
if [ "$bad" -ne 0 ]; then exit 1; fi
printf 'check-skill-links: %s links hold\n' "$count"
exit 0
