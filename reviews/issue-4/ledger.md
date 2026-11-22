# Review closure ledger — #4 pilot kit
S1 FIXED — consent.md section 5 now cites Điều 4 khoản 1 of Law 91/2025/QH15, links the official Công báo Chính phủ page and gives verification date 2026-11-22 (checked against the gazette PDF, CB 971+972); commit "docs: #4 close S1 and SPEC-1" (see `git log --grep 'close S1'`), rerun `uv run pytest tests/test_pilot_kit.py -q` 6 passed.
S2 FIXED — evidence `## Lát` is a six-row table with red assertion lines from a reproduced red run (pilot/ moved away: 6 failed) and green rerun, plus a path check; commit "docs: #4 close S2" (0ddcced).
SPEC-1 FIXED — same change as S1 (consent.md section 5: link, article, verification date); commit "docs: #4 close S1 and SPEC-1".
SPEC-2 FIXED — sender contact path added before this round in 8687a06: runbook.md Buổi 2 step 4 hands the sender the participant code and Zalo via an out-of-git contact sheet destroyed after use, and consent.md section 1 tells the Owner; verified by reading both files at HEAD.
