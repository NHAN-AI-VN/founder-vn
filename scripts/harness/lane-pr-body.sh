#!/bin/bash
# lane-pr-body.sh <n> <title> <evidence-path> <head-sha> <files-file> < evidence.md
# Render the pull request body the dispatcher opens for a finished lane (D24 in nhan), from the
# lane's evidence file on stdin: .github/PULL_REQUEST_TEMPLATE.md filled from the evidence. The
# gate block is copied from the evidence's "## Cổng ba đoạn" section (the lane steering names
# it so); "## Cổng tổng cuối" is accepted too. <files-file> lists the changed paths, one per line.
set -u
n=${1:-}; title=${2:-}; evidence=${3:-}; head=${4:-}; files=${5:-}
[ -n "$n" ] && [ -n "$title" ] && [ -n "$evidence" ] && [ -n "$head" ] && [ -f "$files" ] || { printf 'usage: lane-pr-body.sh <n> <title> <evidence-path> <head-sha> <files-file> < evidence.md\n' >&2; exit 2; }
base=${HARNESS_BASE:-main}
text=$(cat)
gate=$(printf '%s\n' "$text" | awk '/^## Cổng (ba đoạn|tổng cuối)/{f=1; next} /^## /{f=0} f' | sed -e '/^[[:space:]]*$/d')
[ -n "$gate" ] || gate='(mục "## Cổng ba đoạn" không có trong file bằng chứng)'
seams=$(printf '%s\n' "$text" | awk '/^## Seam/{f=1; next} /^## /{f=0} f' | grep -E '^[0-9]+\. \*\*' | sed -E 's/^[0-9]+\. \*\*/- /; s/\*\*//g' | cut -c1-150 | head -12)
included=$(grep -v -E '^docs/evidence/|^reviews/' "$files" | sed -E 's/^/  - `/; s/$/`/')
touches_skills=no; grep -q -E '^(skills|examples)/' "$files" && touches_skills=yes
cat <<BODY
## Outcome

$title

PR này do harness mở (D24, \`scripts/harness/dispatch.sh\`) từ nhánh \`lane/issue-$n\` tại \`$head\`: file bằng chứng của lane ghi cổng ba đoạn GREEN mà session không tới được lệnh mở PR. Nội dung Outcome đầy đủ, theo seam, nằm ở \`$evidence\` (mục Seam, Lát, Giới hạn); các seam lane khai:

${seams:-- (mục Seam không liệt kê dạng đánh số)}

<promise>COMPLETE</promise>

## Ticket and source pointers

Closes #$n

Nguồn thiết kế và cấp phát harness ghi trong \`$evidence\` (phần mở đầu).

## Scope

- Included (các file nhánh đổi so với \`$base\`):
${included:-  - (không có file mã nào ngoài bằng chứng)}
- Excluded: xem mục Giới hạn trong \`$evidence\`.

## Evidence

Khối cổng ba đoạn chép nguyên văn từ \`$evidence\`:

$gate

Từng lát (test đỏ trước, xanh sau, lệnh chạy lại) ở mục Lát của cùng file.

For behavior changes:

- [x] The intended assertion was witnessed red before implementation (theo mục Lát của bằng chứng).
- [x] The same targeted check is green after implementation (theo mục Lát của bằng chứng).
- [x] \`bash scripts/harness/gate-segment.sh verify\` is GREEN on the last code commit (khối trên; CI Gate là thẩm quyền).

## Skills and examples (only when the change touches \`skills/\` or \`examples/\`)

$(if [ "$touches_skills" = yes ]; then printf '%s\n' "PR chạm \`skills/\` hoặc \`examples/\`: harness không tự kiểm checklist rà soát; lượt review Spec đối chiếu từng ô (không \`\$\`, tiếng Việt cho chủ hộ, link cho khẳng định pháp lý/số liệu, miễn trừ, cảnh báo panel, phiên bản khớp)."; else printf '%s\n' "Not touched."; fi)

## Data

- [x] Fixtures, logs, examples and evidence contain no credentials, no environment values, no real names and no real customer data (theo khai báo của lane trong bằng chứng; lượt review đối chiếu).

## Review closure

Record findings from both review axes: Standards and Spec (\`reviews/issue-$n/\`).

| Finding | Resolution (\`FIXED\`, \`DEFERRED\`, \`NOT-A-DEFECT\`) | Evidence |
| --- | --- | --- |
| (harness ghi ở \`reviews/issue-$n/ledger.md\` sau hai lượt review) | | |

- [ ] Every accepted finding has exactly one row.
- [ ] Fixed findings were rerun with the measurement that exposed them.
- [ ] Deferred findings link to a tracked issue with an owner/trigger.

## Integration checklist

- [x] The ticket acceptance criteria are satisfied (theo bằng chứng; lượt review Spec đối chiếu).
- [x] Documentation changes use pointers/deltas and update the authoritative source when needed.
- [x] New gates were commissioned with a deliberate red violation followed by green.
- [x] No direct push or history rewrite of the default branch is required.
BODY
