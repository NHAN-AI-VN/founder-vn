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

One slice, in `tests/test_pilot_kit.py` (6 tests). Run red before `pilot/` existed: 5 failed (`FileNotFoundError: ... pilot/consent.md` and the other four files), 1 passed vacuously; the vacuous test (no `$`, no phone numbers) was then given `assert len(paths) == 5` so it cannot pass on an empty folder. Rerun green: `uv run pytest tests/test_pilot_kit.py -q` (6 passed).

## Cổng ba đoạn

```
static 0 089386c2f37eefa660820e7662de551195599b21 (ruff check, ruff format --check, skill-lint: 0 skill checked)
unit   0 089386c2f37eefa660820e7662de551195599b21 (51 passed)
build  0 089386c2f37eefa660820e7662de551195599b21 (founder_vn-0.1.0 built)
gate-segment verify: GREEN on 089386c2f37eefa660820e7662de551195599b21
```

The commit after that HEAD touches only this evidence file.

## Giới hạn

- Tests check content strings, not the quality of the Vietnamese or whether the kit works in a real session; nothing was run with a real Owner.
- The withdrawal contact is a marked placeholder (`[LIÊN HỆ RÚT LẠI: ...]`): the design names no channel. The project owner fills it before session 1.
- The four follow-up question wordings are drafted here; the design fixes the number (three) and the definition, not the text. The project owner should freeze them before recruiting.
- The legal reading of Law 91/2025/QH15 (rights listed in `consent.md`) is not verified against vbpl.vn in this lane and carries no verification date; a lawyer's review is recommended before use.
- The runbook says "ngoại tuyến" for the Wave A run as the Facilitator working without the Owner; model calls still reach the third-party API.

## Giải quyết review nội bộ

No self-review was run (lane rule: review is two independent turns after the pull request opens).
