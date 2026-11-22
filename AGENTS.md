# founder-vn: instructions for agents

The design is `docs/founder-vn-design.md` (what is being built, for whom, the decisions Q1–Q49 and their log); the tickets are the GitHub issues of this repository (#1 is the spec, T01–T19 its tracer bullets). When code and the design disagree, the design wins and the fix lands in the same change. Coding standards: `docs/agents/standards.md`.

## Agent skills

### Issue tracker

GitHub Issues in `NHAN-AI-VN/founder-vn`, via the `gh` CLI; a native `blocked_by` edge is the authority for a blocking edge. See `docs/agents/issue-tracker.md`.

### Triage labels

Default vocabulary: `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: one `GLOSSARY.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.

### Delivery workflow

Route feature, bug and decision work through the Matt Pocock skill flow and the ticket contract; the phase gates and who merges are decided there. See `docs/agents/delivery-workflow.md`.

### Evidence gates

A completion or review claim names the command, scope, result and artefact; every new gate is commissioned red-then-green. See `docs/agents/evidence-gates.md`.

### Parallel lanes

Before a second lane runs concurrently, read `docs/agents/parallel-lanes.md` for the work-in-progress limit, the single-owner files and the allocation rules.

### Kiro harness

How unattended work runs here: dispatcher, lane, Gate, reviewer, merger, guards, signals, and the measurements behind each claim. See `docs/agents/kiro-harness.md`.

## Rules that override tool defaults

This file is loaded on every surface, so the overrides that keep an unattended run honest live here.

1. **Skills** are the `.agents/skills/` folders linked from `.kiro/skills/`. Follow a skill from its `SKILL.md` read by path; the description in your context is a pointer, not the body. These are development tools; the product skills live in `skills/` and are never confused with them.
2. **Spec and tickets are the tracker.** Issue #1 and its sub-issues are this repository's requirements, design and task list; `.kiro/specs/` stays absent, and a plan an autonomous run writes for itself stays out of the tree.
3. **Write the question down instead of asking.** An unattended run has nobody to answer. When a ticket is insufficient, a design decision is missing, or a skill step says "ask the user": post the questions as `- [ ]` checklist items on the issue, end with `<promise>BLOCKED</promise>`, and stop. The ticked box is the approval.
4. **A lane ends at a pull request.** Work on the branch the allocation names (`lane/issue-<n>`), open the pull request with `.github/PULL_REQUEST_TEMPLATE.md` filled in and `Closes #<n>` through `bash scripts/harness/open-lane-pr.sh <n>` with the body on stdin (REST only; `gh pr create` needs GraphQL the sandbox lacks); merging belongs to the harness merger. `.kiro/hooks/guard.sh` refuses pushes to `main`, force pushes and merges, and is not the only reason to avoid them.
5. **Evidence lives in the repository**: `docs/evidence/issue-<n>-<slug>.md` per ticket, review artefacts under `reviews/issue-<n>/`. A claim that exists only in a reply is not evidence.
6. **Allocations come from the dispatcher**: the single-owner files a lane may edit are in the issue comment that begins `<!-- harness:allocation -->`. A lane that needs one of those files and has no allocation is BLOCKED.
7. **Vocabulary and identifiers**: `GLOSSARY.md` terms verbatim in code, tests, issues and commits once the glossary exists; the file names, JSON keys and skill names of `docs/founder-vn-design.md` §4 are English; Owner-facing text is Vietnamese and never carries `$`.
8. **Data and credentials**: synthetic or anonymised only. No real names, locations below district level, phone numbers or real financials in fixtures, logs, examples or evidence. `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL` may be set in the sandbox: name them, test for their presence, never print, write or forward their values; tests use the fake provider, never the network.
9. **Memory**: Kiro Web memory is per user and invisible to reviewers. A rule you want followed lives in this file, in `.kiro/steering/`, or in `docs/agents/`; a memory that contradicts them loses.

## Guarded agent on the CLI

Work through `founder-guarded` (`.kiro/agents/founder-guarded.json`): the full toolset, the project skills, and the `.kiro/hooks/guard.sh` guard. Measured 2026-11-22 on Kiro CLI: `.kiro/hooks/guard.json` fires as a PreToolUse hook and exit 2 blocks the call.

## Signals

Every unattended turn ends with exactly one signal on its own line, and the harness reads it fail-closed. An implement or address turn ends with `<promise>COMPLETE</promise>` or `<promise>BLOCKED</promise>`; a review turn ends with `<promise>PASS</promise>`, `<promise>CHANGES_REQUESTED</promise>` or `<promise>BLOCKED</promise>`. Anything else counts as not done.
