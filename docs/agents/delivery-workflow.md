# Coding-agent delivery workflow

This document connects the repository's way of working to the installed Matt Pocock skills. It defines routing and phase transitions; it does not replace the design, the glossary, or the issue tracker configuration. Ported from `NHAN-AI-VN/nhan` (`docs/agents/delivery-workflow.md` at `8adef66b`).

## Read before choosing a route

- Domain language and durable decisions: `docs/agents/domain.md`.
- What is being built and why: `docs/founder-vn-design.md`; coding standards: `docs/agents/standards.md`.
- Issue operations and labels: `docs/agents/issue-tracker.md` and `docs/agents/triage-labels.md`.
- How unattended lanes run: `docs/agents/kiro-harness.md`.

Use source pointers in generated artifacts. Copying a rule into a spec or ticket creates a second source that can drift.

## Route the work

| Starting situation | Route | Handoff point |
| --- | --- | --- |
| A scoped idea in this repository | `/grill-with-docs` | Continue to `/to-spec` or direct `/implement` according to size |
| A huge effort whose route is still unclear | `/wayfinder` | When decisions make the route clear, continue to `/to-spec`; do not jump from the map to implementation |
| A question that needs runnable code or visible UI | `/handoff` → fresh prototype workspace/session → `/prototype` → `/handoff` back | Fold the measured answer into the source conversation and spec |
| A raw external bug or feature request | `/triage` | Implement only after the issue becomes agent-ready |
| A hard, intermittent, or regression bug | `/diagnosing-bugs` | Produce a tight red feedback loop and regression test before implementation |
| A concrete, already-scoped behavior | `/tdd` directly, or `/implement` when a ticket exists | Finish with validation and review |

Tickets created by `/to-tickets` (T01–T19 under issue #1) are already agent-ready. Do not send them through `/triage`.

## Main flow for multi-session work

1. **Sharpen:** run `/grill-with-docs` in the working repository. Resolve decisions in conversation; update `GLOSSARY.md` or ADRs only when their own rules require it.
2. **Answer runnable unknowns:** use the prototype detour above. Keep prototype code as evidence, not production code.
3. **Specify:** run `/to-spec`. The spec must point to design sections, glossary terms and measured research instead of reproducing them.
4. **Decompose:** run `/to-tickets`. Create tracer-bullet tickets with explicit blocking edges. Keep this context intact until ticket publication is complete.
5. **Implement:** start a fresh context for each unblocked ticket and run `/implement`; it drives `/tdd` one red-green slice at a time. In an unattended lane the loop is visible in git: the lane commits its `## Seam` list first, then one commit per slice carrying the test and the code (rules in `.kiro/steering/lane-implement.md`; the Standards review checks the shape).
6. **Review:** run `/code-review` against a fixed merge base. Close both axes: Standards and Spec.
7. **Integrate:** use the pull-request template and the repository's Git safety policy. Never push directly to the default branch.

Steps 5 and 6 run unattended as the implement lane and the review turns, described in `docs/agents/kiro-harness.md`. An unattended step keeps every human decision of its skill by writing it down as a `- [ ]` question instead of answering it.

For genuinely single-session work, continue from grilling to `/implement` in the same context. At phase boundaries, prefer continuing when the current evidence is still useful; use `/clear` between independent implementation tickets, `/handoff` for portability, and `/compact` only when context pressure requires it.

## Spec and ticket contract

A buildable spec or ticket contains:

- **Source pointers:** paths plus section, glossary term, or design decision (`Q<n>`). It does not mint new decisions.
- **Outcome:** externally observable behavior or decision result.
- **Scope:** included and explicitly excluded work.
- **Acceptance:** independently verifiable examples or measurements.
- **Blocking edges:** issue numbers or named evidence gates that must close first, as native `blocked_by` edges.
- **Affected seams:** public module/API boundary to change; avoid prescribing internals unless the design does. In this repository's ticket bodies this is a `## Seam` section; T01–T19 were published without it, and the lane derives the seams from the acceptance criteria and says so in its evidence file.
- **Validation:** the command or measurement that will prove completion.

A ticket is `ready-for-agent` only when these fields are sufficient for a fresh agent and all blockers are closed. Otherwise use `needs-info`, `ready-for-human`, or retain the explicit blocking edge.

## Phase gates

| Transition | Required evidence |
| --- | --- |
| Grilling → spec | Open questions have an owner or explicit deferred condition; terminology and durable decisions are recorded at their existing source; runnable unknowns have measured answers or named prototype work |
| Spec → tickets | Source pointers, scope, acceptance, seams, and blocking edges are explicit; decomposition preserves end-to-end tracer bullets |
| Ticket → implementation | The ticket is unblocked and agent-ready; the proposed slice does not assume an unresolved design or legal decision |
| Implementation → review | Seams declared before the first slice and one commit per slice with its test (unattended lanes); changed behavior has witnessed red-then-green evidence where applicable; the three gate segments are green at the last code commit; affected source artifacts are synchronized by pointer/delta |
| Review → integration | Standards and Spec reviews are complete; every accepted finding is fixed, deferred to a tracked issue, or rejected with evidence; the Gate has rerun at the final commit |

Detailed evidence rules are in `docs/agents/evidence-gates.md`.

## Who merges

**The merger is a deterministic workflow, never an agent** (decision FV-D1 in `docs/agents/kiro-harness.md`, inherited from `nhan` D1). A lane pull request is merged by the merger step (`scripts/harness/merge-check.sh`, decision in `scripts/harness/merge.jq`, run at the end of the `Gate` job and in `after-gate.yml`) only when all of these hold at the exact head commit:

1. the latest `Gate` run of `.github/workflows/gate.yml` at that commit has completed and concluded `success` (no run at all is not green);
2. `reviews/issue-<n>/standards.md` and `reviews/issue-<n>/spec.md` exist, are non-empty, were written after the last code commit, and their last line is `<promise>PASS</promise>`;
3. when any report, current or earlier, named finding identifiers, `reviews/issue-<n>/ledger.md` covers every identifier with exactly one line (`docs/agents/evidence-gates.md`, review closure ledger);
4. the pull request body carries `Closes #<n>` for the ticket the dispatcher allocated and no other closing keyword, the head branch is `lane/issue-<n>`, the ticket is open and has no open blocker.

Merges stay sequential: one pull request per run, evaluated against `main` as it is after the previous merge. The workflow holds the only credential that merges; no agent turn has one. The decision table is posted on the pull request either way.

A pull request with no lane behind it (harness configuration, documentation, protocol fixes) is merged by the same workflow when: the operator's account authored it, the operator put the label `harness:auto-merge` on it, no failing or pending check sits at its head, and its body and commits carry no closing keyword. The label is the operator's approval, written where the merger can read it. The pull request that introduced the harness (`harness/bootstrap`) is merged by hand, because the merger cannot merge itself (FV-D4).

## Source-control boundary

Use one focused branch per implementation ticket, named `lane/issue-<n>` when the harness dispatches it, `harness/<topic>` for harness changes. Preserve hooks, never rewrite shared history, and never push directly to `main`.
