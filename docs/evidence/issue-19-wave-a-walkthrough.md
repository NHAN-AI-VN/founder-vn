# Evidence: issue #19 Wave A clean-install walkthrough on Kiro CLI

Lane run by the project owner (the ticket is `ready-for-human`; the dispatcher skips it). The operator's allocation comment on #19 (2026-11-25T05:08:45Z) grants `README.md`, lane branch `lane/issue-19`, target `main`. The machine-doable half of T18 was split out to #89 (T18a, PR #90, merged 2026-11-24); this lane records the human half: the walkthrough on a real Kiro CLI, the tag and the PyPI release, the README truth table, the known-issues list.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `uvx --from founder-vn founder-vn install` for the Kiro host, run from PyPI in an empty folder, and `uvx --from founder-vn founder-vn-mcp` answering `initialize` with `serverInfo.version` `0.2.0`: the clean-install route a Facilitator uses (criteria 1 and 2). Witnessed by hand on the operator's machine; no test reaches PyPI.
- Protocol step 1 of the six skills (`server_info` against `metadata.version`) inside a Kiro CLI session: the only place "a deliberate major mismatch stops the skill with the expected message" can be observed (criterion 2). No automated seam (spec #1: skills have no automated seam).
- `README.md` truth table (Install, Status, Host) and `docs/hosts/README.md`: asserted by `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (criterion 3). The one red-then-green slice of this lane.
- The tracker: known issues of Wave B as GitHub issues (criterion 4), not code.
