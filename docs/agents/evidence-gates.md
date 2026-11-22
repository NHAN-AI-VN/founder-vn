# Evidence gates

How coding agents prove work in this repository. Ported from `NHAN-AI-VN/nhan` (`docs/agents/evidence-gates.md` at `8adef66b`); the commands are this repository's (`docs/agents/standards.md`, toolchain).

## Three operating rules

1. **Red before trust:** a new gate is not trusted until a deliberate violation makes it fail for the expected reason.
2. **One source, pointers elsewhere:** duplicated rules require an automated synchronization check; prefer eliminating the copy.
3. **Reproducible evidence:** a completion claim names the command, input scope, result, and relevant artifact. Self-declaration is not evidence.

## Commission a new gate

For a validation, lint rule, CI check, document guard, hook, or measurement script:

1. Define the claim, scope, command, expected failure, and known blind spots.
2. Add the smallest fixture or mutation that violates the claim.
3. Run the real command in the place where it will block work; confirm it is red for the intended assertion.
4. Revert or fix the violation and rerun the same command; confirm green.
5. Attach the command at the earliest useful enforcement point and retain a regression test for the failure mode.
6. Record evidence in the pull request or issue. Do not preserve secrets, environment values, personal data, or real customer values in fixtures or logs.

A green result without the witnessed-red step proves only that the command exited successfully, not that it guards the stated behavior. The harness's own gates follow the same rule: `scripts/harness/witness.sh --witness-red` mutates each mechanism and requires its case to go red.

## Select validation from authoritative sources

- Use the gate commands of `docs/agents/standards.md` (CI: `.github/workflows/gate.yml`; sandbox: `scripts/harness/gate-segment.sh`).
- Run targeted tests for changed behavior (`uv run pytest <file>`), then the smallest applicable lint, format, build check.
- A missing test runner or command is a named gap to track; it is not permission to claim that tests passed.
- A test must fail for the expected assertion before the implementation makes it pass.
- Do not retry nondeterministic checks until green. Diagnose the flake or record the failure.

For documentation-only changes, validate links, referenced paths, structured files, and rendered structure as applicable. A raw-text check does not prove that Markdown or a generated artifact renders correctly.

## Evidence by change type

| Change | Minimum evidence |
| --- | --- |
| Behavior | Red assertion for the intended behavior, green targeted test, and the three gate segments |
| Bug fix | A command that reproduces the bug before the fix plus a permanent regression test after it |
| New or changed gate | Witnessed red mutation, restored green run, scope/blind-spot statement |
| Documentation, skill or example | Link/path validation, `scripts/skill_lint.py` green, the review checklist of `.github/PULL_REQUEST_TEMPLATE.md`, source-pointer review |
| Dependency | Purpose tied to a ticket, license, exact pinned version in `uv.lock` in the same commit |
| Golden file | The diff of the golden file read and explained in the commit message; a golden file never changes silently |

## Where evidence lives

- A lane writes `docs/evidence/issue-<n>-<slug>.md`: command, scope, result, artifact, and a **limits** section stating what the slice does not prove. It opens with `## Seam` (the public boundaries under test, committed before any slice; derived from the acceptance criteria and marked as derived when the ticket has no `## Seam` section) and carries a `## Lát` table with one row per red-green slice: test name, the assertion line while red, the green rerun. It closes with the `## Cổng ba đoạn` block: the three `gate-segment.sh` commands and the output of `gate-segment.sh verify`, whose `GREEN on <sha>` must name the last code commit.
- The implement skill's own review step is the lane's internal review: findings and how they were handled go into the `## Giải quyết review nội bộ` section of the evidence file, not into `reviews/`.
- A slice that adds or changes a gate adds a witness case (`scripts/harness/witness.sh` for harness mechanisms; a test under `tests/` for package gates) that mutates the mechanism and requires the corresponding check to go red.
- Review turns write `reviews/issue-<n>/standards.md` and `reviews/issue-<n>/spec.md`; an address turn writes `reviews/issue-<n>/ledger.md`. These are committed on the lane branch so a reader of the pull request can check the ledger's claims rather than trust them.

## Review closure ledger

The two review axes return Standards (`S1`, `S2`, …) and Spec (`SPEC-1`, …) findings. Close every accepted finding with one row:

| Finding | Resolution | Evidence |
| --- | --- | --- |
| Identifier and concise statement | `FIXED`, `DEFERRED`, or `NOT-A-DEFECT` | Exact command/result, tracked issue, or source citation |

Closure rules:

- `FIXED`: rerun the measurement that exposed the finding, not only a broad gate that was already green.
- `DEFERRED`: create or link a tracked issue with owner/trigger and blocking relationship where applicable.
- `NOT-A-DEFECT`: cite code or an authoritative source that disproves the finding.
- The number of ledger rows must equal the number of accepted findings. Reconcile duplicates explicitly.

In an unattended lane the ledger is the file `reviews/issue-<n>/ledger.md`, written by the address turn; the merger reads it only when the two reports, current or an earlier version, name finding identifiers: its first heading names the issue, and it holds exactly one line per finding identifier that appears in the two current reports or in any earlier version of those two files in the branch history, in the form `<id> <FIXED|DEFERRED|NOT-A-DEFECT> — <evidence>` (a leading `- ` or `* ` is accepted). The merger refuses a pull request whose ledger misses an identifier or carries one the reports never named. The pull request's closure table points at that file rather than restating it.

## Pull-request evidence

Use `.github/PULL_REQUEST_TEMPLATE.md`. Paste concise command results or link to durable CI artifacts; never paste credentials, environment values, personal data, or real customer records. If a required check cannot run, state the blocker and the next-best check rather than marking it complete.

A change is complete only when its ticket acceptance is met, applicable validation is green, review findings are reconciled, and no decision of the design has been bypassed.
