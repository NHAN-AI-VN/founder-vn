# Evidence: issue #4 pilot kit

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `pilot/consent.md`: the consent form the Owner signs; asserted by content (third-party model API, anonymised publication, 90-day deletion with opt-in to keep, withdrawal contact placeholder, Law 91/2025/QH15).
- `pilot/baseline.md`: the dated baseline form; asserted by its four fields (intended price, location, capital, open/not-open) and the date and acknowledgement lines.
- `pilot/follow-up-questions.md`: the three pre-registered questions; asserted by the definition of "changed a decision", three numbered questions, and the +14 days sender rule.
- `pilot/results-template.md`: the anonymised results table; asserted by its columns and the n = 20 descriptive caveat.
- `pilot/runbook.md`: the Facilitator runbook; asserted by the two sessions, durations, offline Wave A run, PDF over Zalo, per-participant root outside version control, 90-day deletion step.
- All of the above live in `tests/test_pilot_kit.py`, which also asserts no `$` and no phone-number or real-name shaped strings in `pilot/`.

## Lát

Red run reproduced in the address turn of round 2: `pilot/` moved out of the working tree, `uv run pytest tests/test_pilot_kit.py -q` gave `6 failed`. The test and `pilot/` landed together in `089386c`, so the original red run is not separable in git; this table records the reproduced one. Green rerun: `uv run pytest tests/test_pilot_kit.py -q` (6 passed) with `pilot/` restored.

| Test | Assertion line while red | Green rerun |
| --- | --- | --- |
| `test_consent_names_api_publication_deletion_withdrawal_and_law` | `FileNotFoundError: ... pilot/consent.md` | passed |
| `test_baseline_has_four_fields_date_and_acknowledgement` | `FileNotFoundError: ... pilot/baseline.md` | passed |
| `test_follow_up_questions_are_three_preregistered_and_sent_by_someone_else` | `FileNotFoundError: ... pilot/follow-up-questions.md` | passed |
| `test_results_template_has_columns_and_descriptive_caveat` | `FileNotFoundError: ... pilot/results-template.md` | passed |
| `test_runbook_covers_two_sessions_offline_run_pdf_root_and_deletion` | `FileNotFoundError: ... pilot/runbook.md` | passed |
| `test_pilot_kit_has_no_dollar_and_no_phone_numbers` | `assert 0 == 5` (`len(paths)` is 0 on an empty `pilot/`) | passed |

Path check: every `pilot/*.md` file and `docs/founder-vn-design.md` (section 6, `## 6. Pilot`) cited by `pilot/runbook.md` exists in the tree (`business-plan.md` is a generated artifact of the Wave A run, not a repo file).

## Cổng ba đoạn

```
static 0 089386c2f37eefa660820e7662de551195599b21 (ruff check, ruff format --check, skill-lint: 0 skill checked)
unit   0 089386c2f37eefa660820e7662de551195599b21 (51 passed)
build  0 089386c2f37eefa660820e7662de551195599b21 (founder_vn-0.1.0 built)
gate-segment verify: GREEN on 089386c2f37eefa660820e7662de551195599b21
```

The commit after that HEAD touches only this evidence file.

## Cổng sau review

Round 2 address turn, rerun on 0ddcced22fb160fdc0876072f95fb9d54393aa23 (the last commit that touches `pilot/` or the Lát table):

```
static 0 0ddcced22fb160fdc0876072f95fb9d54393aa23 (ruff check, ruff format --check, skill-lint: 0 skill checked)
unit   0 0ddcced22fb160fdc0876072f95fb9d54393aa23 (51 passed)
build  0 0ddcced22fb160fdc0876072f95fb9d54393aa23 (founder_vn-0.1.0 built)
gate-segment verify: GREEN on 0ddcced22fb160fdc0876072f95fb9d54393aa23
```

The commits after that HEAD touch only this evidence file and `reviews/issue-4/ledger.md`.

## Giới hạn

- Tests check content strings, not the quality of the Vietnamese or whether the kit works in a real session; nothing was run with a real Owner.
- The withdrawal contact is a marked placeholder (`[LIÊN HỆ RÚT LẠI: ...]`): the design names no channel. The project owner fills it before session 1.
- The four follow-up question wordings are drafted here; the design fixes the number (three) and the definition, not the text. The project owner should freeze them before recruiting.
- Law 91/2025/QH15: the rights list in `consent.md` section 5 was checked against Article 4 clause 1 in the official gazette PDF (congbao.chinhphu.vn, Công báo 971 + 972) on 2026-11-22 and carries the link and that date. That is a reading of the article text, not legal advice; a lawyer's review is still recommended before use.
- The runbook says "ngoại tuyến" for the Wave A run as the Facilitator working without the Owner; model calls still reach the third-party API.

## Giải quyết review

Review 2026-11-22-100000, five issues, all addressed in the pilot docs:

1. Sender contact path: `runbook.md` Buổi 2 step 4 hands the sender the code and the Owner's Zalo via an out-of-git contact sheet; `consent.md` section 1 tells the Owner. Sender and table recorder may be one person, never the Facilitator.
2. Re-identification: `consent.md` section 3 publishes aggregates only, no verbatim quotes, and names the small-business identifiability risk.
3. Aggregate-only: the filled per-participant table is an internal working sheet kept out of git; `pilot/` gets the blank template and aggregates (design section 6).
4. Withdrawal: `consent.md` section 6 and `runbook.md` day-90 step 4 delete the row, recompute unpublished aggregates, and state that published aggregates are not recalled.
5. Retention: the consent form is destroyed with the project folder at day 90 (or on withdrawal); the deletion log holds only the code and date and is kept. This retention rule is an assumption of this lane (the design is silent); a lawyer may require longer retention of consent evidence.

## Giải quyết review nội bộ

No self-review was run (lane rule: review is two independent turns after the pull request opens).
