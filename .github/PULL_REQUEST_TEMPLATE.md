## Outcome

<!-- What observable outcome does this change deliver? A lane ends this section with the line <promise>COMPLETE</promise>. -->

## Ticket and source pointers

Closes #

<!-- Link the ticket and the design sections it rests on (docs/founder-vn-design.md §n, GLOSSARY.md term, docs/adr/, docs/agents/standards.md). Point to sources; do not copy them. -->

## Scope

- Included:
- Excluded:

## Evidence

| Claim | Command or measurement | Result / artifact |
| --- | --- | --- |
| | | |

For behavior changes:

- [ ] The intended assertion was witnessed red before implementation (`## Lát` in `docs/evidence/issue-<n>-<slug>.md`).
- [ ] The same targeted check is green after implementation.
- [ ] `bash scripts/harness/gate-segment.sh verify` is GREEN on the last code commit (three segments: static, unit, build), quoted in the evidence file.

If a check could not run, describe the blocker and next-best verification instead of checking it.

## Skills and examples (only when the change touches `skills/` or `examples/`)

The review checklist of `docs/founder-vn-design.md` §5, machine half in `scripts/skill_lint.py`:

- [ ] No `$`: every amount is VND in Vietnamese format (`35.000 đ`).
- [ ] No English leaks into Owner-facing output (reports, `examples/`, the simulated-buyer brief); the Owner is addressed as "anh/chị".
- [ ] Every legal or numeric claim carries an official link and a verification date.
- [ ] The disclaimer ("not financial, tax or legal advice") is present.
- [ ] The simulated-panel caveat ("mô phỏng, cận trên, không phải khách hàng thật") is present where a panel result is shown.
- [ ] `metadata.version` equals the package version; frontmatter has `name`, `description` with Vietnamese trigger phrases, `license`.

## Data

- [ ] Fixtures, logs, examples and evidence contain no credentials, no environment values, no real names and no real customer data (synthetic or anonymised only).

## Review closure

Record findings from both review axes: Standards and Spec (`reviews/issue-<n>/`).

| Finding | Resolution (`FIXED`, `DEFERRED`, `NOT-A-DEFECT`) | Evidence |
| --- | --- | --- |
| | | |

- [ ] Every accepted finding has exactly one row.
- [ ] Fixed findings were rerun with the measurement that exposed them.
- [ ] Deferred findings link to a tracked issue with an owner/trigger.

## Integration checklist

- [ ] The ticket acceptance criteria are satisfied.
- [ ] Documentation changes use pointers/deltas and update the authoritative source when needed.
- [ ] New gates were commissioned with a deliberate red violation followed by green.
- [ ] No direct push or history rewrite of the default branch is required.
