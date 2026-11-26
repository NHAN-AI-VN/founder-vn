# Evidence: issue #118 Wave B clean-install walkthrough (template)

This file is a template. The operator fills it on a real Kiro CLI, following the section
"Clean-install walkthrough" of [docs/hosts/kiro.md](../hosts/kiro.md). No walkthrough has been
recorded here yet, and nothing in this file claims a run happened. The `#` in the file name is
literal: it is the name the ticket gives.

## Acceptance criteria of #118

The criteria are copied from the ticket (read from issue #118); the first is the allocation comment.

- [ ] Allocation comment written by the operator on #118 (`<!-- harness:allocation -->`, `singleOwnerFiles: README.md`, `laneBranch: lane/issue-118`).
- [ ] Dry run on the local 0.3.0 wheel in an empty folder (install, MCP `initialize`), then tag `v0.3.0` on the merge commit of the machine half, `release.yml` Build green, `Publish to PyPI` approved by the operator on environment `pypi`, `uvx --no-cache --from founder-vn founder-vn --version` gives `founder-vn 0.3.0`.
- [ ] Clean-install walkthrough on Kiro CLI following `docs/hosts/kiro.md` (Wave A, then permits, ops, marketing, launch, plan recompile, `plan --check` exit 0), recorded in this file (commands, started, duration, friction, issue filed; model name only; no secret values; no case content beyond the golden).
- [ ] The deliberate major mismatch still stops a skill (one Wave B skill set to `1.0.0`, run, stop message quoted, restored).
- [ ] README says 0.3.0 is released (tag date) and the Kiro CLI host row says the full pipeline including Wave B is verified on 0.3.0 (walkthrough date, #118); `docs/hosts/README.md` likewise; `tests/test_front_door.py` updated.
- [ ] Every friction or defect filed as an issue naming the skill or tool; blocking defects fixed (0.3.1) or filed before closing.
- [ ] PR from `lane/issue-118` with `Closes #118` through `scripts/harness/open-lane-pr.sh`.

## Record

The operator fills this table on a real Kiro CLI. Walkthrough times can be reconstructed from file
modification times if no stopwatch was kept; say so in the record.

| step | command | started | duration | friction | issue filed |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
