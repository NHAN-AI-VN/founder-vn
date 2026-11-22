#!/bin/bash
# Render the `/kiro` message of one review or address turn that runs as a Kiro Web session
# (component C4 in docs/agents/kiro-harness.md). The message is self-contained: the values that
# change per lane come first, then the ticket body and the CI result the session cannot fetch
# itself (the sandbox holds no GitHub credential), then the axis prompt of .kiro/prompts/<axis>.md
# verbatim, so the session reads nothing from the lane's own .kiro/ (a lane cut before a prompt
# change would carry the stale one). The last line is the marker review-web.sh reads back.
#
# Usage: review-web-turn.sh <standards|spec|address|sync> <ticket> <target> <lane-branch> <code-sha> <head-sha> <round> <prompt-dir> <ci-file> [ticket-file]
set -euo pipefail

axis=${1:-}; ticket=${2:-}; target=${3:-}; lane=${4:-}; code=${5:-}; head=${6:-}; round=${7:-}
prompt_dir=${8:-}; ci_file=${9:-}; ticket_file=${10:-}
if [ -z "$axis" ] || [ -z "$ticket" ] || [ -z "$target" ] || [ -z "$lane" ] || [ -z "$code" ] || [ -z "$head" ] || [ -z "$round" ] || [ -z "$prompt_dir" ] || [ -z "$ci_file" ]; then
  printf 'review-web-turn.sh: usage: <standards|spec|address|sync> <ticket> <target> <lane-branch> <code-sha> <head-sha> <round> <prompt-dir> <ci-file> [ticket-file]\n' >&2
  exit 64
fi
case "$axis" in
  standards|spec) prompt_file="$prompt_dir/review-$axis.md" ;;
  address) prompt_file="$prompt_dir/address-findings.md" ;;
  sync) prompt_file="$prompt_dir/sync-target.md" ;;
  *) printf 'review-web-turn.sh: unknown axis %s\n' "$axis" >&2; exit 64 ;;
esac
if [ ! -f "$prompt_file" ]; then printf 'review-web-turn.sh: prompt %s not found\n' "$prompt_file" >&2; exit 66; fi
dir="reviews/issue-$ticket"
code12=${code:0:12}; head12=${head:0:12}

checkout="Nhánh làm việc: \`$lane\`: \`git fetch origin $lane\` rồi checkout ở commit mới nhất trên \`origin\` (HEAD lúc ra lệnh: \`$head12\`; commit mã đang xét: \`$code12\`). Nhánh đích: \`$target\` (so \`git diff --stat $target...HEAD\` và \`git log --oneline $target..HEAD\`). Thư mục báo cáo: \`$dir/\`."
env_text="Môi trường này là sandbox Kiro Web trên checkout của repo (đo 2026-11-22, FV-M-6): Python 3.11, \`uv\` có sẵn, git, jq, gh, internet mở; không có Docker và không cần. Không có credential tới GitHub API ngoài push git, nên thân ticket và kết quả CI nằm ngay trong tin nhắn này, không ở file nào của repo. **Sandbox không nạp steering, AGENTS.md hay skill vào ngữ cảnh của sub-agent**: đọc \`AGENTS.md\` bằng đường dẫn trước, và nếu bạn giao việc cho sub-agent thì chép nguyên văn tin nhắn này vào tin nhắn giao việc. Guard \`.kiro/hooks/guard.sh\` không chạy ở đây; luật của nó (không push \`$target\`, không force-push, không merge, không in giá trị biến \`FOUNDER_LLM_*\`) là luật bạn tự giữ. Các file \`$dir/probe*.md\`, nếu có, là phép đo của harness, ngoài phạm vi review."
gate_text="Cổng ba đoạn (cùng các bước của CI \`Gate\`): \`bash scripts/harness/gate-segment.sh static\` (ruff check, ruff format --check, skill-lint), \`… unit\` (pytest), \`… build\` (uv build), rồi \`bash scripts/harness/gate-segment.sh verify\`; trước đó \`uv sync --frozen\` (chỉ khi \`pyproject.toml\` có) và \`bash scripts/harness/install-hooks.sh\`. Nhánh chưa có script thì \`git fetch origin $target && git show origin/$target:scripts/harness/gate-segment.sh > .harness/gate-segment.sh\` rồi chạy bản ấy."
push_rule="push lên \`origin $lane\` (bị từ chối non-fast-forward thì fetch, rebase, push lại; tuyệt đối không force-push). Không mở PR mới."

case "$axis" in
  standards|spec)
    printf '/kiro Lượt review trục %s, vòng %s, cho issue #%s. %s\n\n%s\n\n' "$axis" "$round" "$ticket" "$checkout" "$env_text"
    printf 'Khác với mục "không commit" của hướng dẫn bên dưới: ở đây không có harness nào commit thay bạn. Viết báo cáo vào `%s/%s.md` (ghi đè file cũ nếu có), commit **chỉ** file đó với message `review(%s): #%s vòng %s <PASS|CHANGES_REQUESTED|BLOCKED>` rồi %s Không sửa file nào khác, không sửa mã. Dòng cuối của file báo cáo và dòng cuối câu trả lời của bạn trên issue này là cùng một tín hiệu.\n\n' \
      "$dir" "$axis" "$axis" "$ticket" "$round" "$push_rule"
    ;;
  address)
    printf '/kiro Lượt sửa, vòng %s, cho issue #%s. %s\n\n%s\n\n' "$round" "$ticket" "$checkout" "$env_text"
    printf 'Mục tiêu của lượt này, theo thứ tự: (1) `Gate` xanh ở commit bạn push: kết quả CI ở HEAD nằm dưới; run đỏ thì sửa nguyên nhân gốc, giữ nguyên độ chặt của test và gate. (2) Mọi finding chặn trong `%s/standards.md` và `%s/spec.md` được đóng trong ledger, nếu hai file ấy có ở HEAD và được viết sau commit mã `%s` (so `git log -1 --format=%%H -- <file>` với commit mã); báo cáo cũ hơn commit mã đã bị thay thế, để nguyên và không sửa theo nó. %s Mọi đoạn xanh và `verify` GREEN ở HEAD trước khi push lần cuối. Ghi ledger vào `%s/ledger.md` khi có mã finding, commit riêng từng finding hay từng nguyên nhân CI, và sau mỗi commit %s Kết thúc bằng tín hiệu ở dòng cuối câu trả lời của bạn trên issue này. CI (`Gate`) chạy trọn ở commit bạn push; harness ra lệnh review lại sau đó.\n\n' \
      "$dir" "$dir" "$code12" "$gate_text" "$dir" "$push_rule"
    ;;
  sync)
    printf '/kiro Lượt đồng bộ với `%s`, cho issue #%s. %s\n\n%s\n\n' "$target" "$ticket" "$checkout" "$env_text"
    printf 'Pull request của lane này không merge được: `%s` đã đổi sau khi nhánh được cắt và hai bên sửa cùng chỗ. GitHub không chạy `Gate` trên một pull request đang xung đột, nên không lượt review hay lượt sửa nào tới được cho tới khi nhánh lane mang `%s` hiện hành. Việc của lượt này: `git fetch origin %s` rồi `git merge origin/%s` thành **một commit merge** (không rebase, không viết lại lịch sử, không force-push: hook post-commit push commit merge như mọi commit khác), giải quyết xung đột giữ cả hai ý định như hướng dẫn bên dưới, rồi chạy cổng ba đoạn xanh ở HEAD sau merge (đỏ thì sửa nguyên nhân gốc trong commit riêng). %s Sau mỗi commit %s Kết thúc bằng tín hiệu ở dòng cuối câu trả lời của bạn trên issue này; `Gate` chạy trọn ở commit bạn push và harness đọc lại sau đó.\n\n' \
      "$target" "$target" "$target" "$target" "$gate_text" "$push_rule"
    ;;
esac

printf '## Kết quả CI của workflow `Gate` ở `%s`\n\n' "$head12"
cat "$ci_file"
printf '\n\n'
if [ -n "$ticket_file" ] && [ -f "$ticket_file" ]; then
  printf '## Thân ticket #%s (nguyên văn)\n\n' "$ticket"
  cat "$ticket_file"
  printf '\n\n'
fi
printf '## Hướng dẫn (nguyên văn `.kiro/prompts/%s` trên `%s`)\n\n---\n\n' "$(basename "$prompt_file")" "$target"
cat "$prompt_file"
printf '\n<!-- harness:turn axis=%s code=%s head=%s round=%s at=%s -->\n' "$axis" "$code" "$head" "$round" "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
