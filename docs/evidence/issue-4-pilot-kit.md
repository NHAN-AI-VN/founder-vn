# Evidence: issue #4 pilot kit

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `pilot/consent.md`: the consent form the Owner signs; asserted by content (third-party model API, anonymised publication, 90-day deletion with opt-in to keep, withdrawal contact placeholder, Law 91/2025/QH15).
- `pilot/baseline.md`: the dated baseline form; asserted by its four fields (intended price, location, capital, open/not-open) and the date and acknowledgement lines.
- `pilot/follow-up-questions.md`: the three pre-registered questions; asserted by the definition of "changed a decision", three numbered questions, and the +14 days sender rule.
- `pilot/results-template.md`: the anonymised results table; asserted by its columns and the n = 20 descriptive caveat.
- `pilot/runbook.md`: the Facilitator runbook; asserted by the two sessions, durations, offline Wave A run, PDF over Zalo, per-participant root outside version control, 90-day deletion step.
- All of the above live in `tests/test_pilot_kit.py`, which also asserts no `$` and no phone-number or real-name shaped strings in `pilot/`.
