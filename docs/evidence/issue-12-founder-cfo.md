# Evidence: issue #12 founder-cfo skill and the first sources-ledger entries

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code: `founder_vn.cfo` (T05, issue #6) is unchanged and owned by that ticket. The seams are the shipped files.

- `permits/sources.md` (sources ledger): the first two entries, `tax_rate_on_revenue` for "cắt tóc, làm đầu, gội đầu" and `tax_free_threshold`, each with official link, Công báo number and date, article, verbatim excerpt and verification line (criterion 2, CONTRIBUTING hard rule). Checked by a ledger-shape test.
- `skills/founder-cfo/SKILL.md` (skill file): the instructions the host model follows. Seam because the Owner-terms cost questions, the lookup, the tool call, the plain-Vietnamese flag read-back and the disclaimer live only here (criteria 1, 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `founder-vn cfo --out` (existing CLI command, unchanged): produces `examples/barbershop/founder/cfo.md` from `numbers.json` (criterion 4). The golden files are checked by content tests.
- `docs/founder-vn-design.md` decision log (Q52): the combined-rate model decision the operator made for this ticket.

## Lát

## Cổng ba đoạn

## Giới hạn
