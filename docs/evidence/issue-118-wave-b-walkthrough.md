# Evidence: issue #118 release 0.3.0 and Wave B clean-install walkthrough on Kiro CLI

Lane run by the project owner on Kiro CLI through `founder-guarded`, with `HARNESS_SINGLE_OWNER_FILES=README.md` exported in the session (the ticket is `ready-for-human`; the dispatcher skips it). The operator's allocation comment on #118 (2026-11-26T07:17:12Z) grants `README.md`, lane branch `lane/issue-118`, target `main`. The machine half #117 (T24) merged as `ca6bc9f` (PR #139): `__version__` and the ten `metadata.version` values are 0.3.0.

This file is the record that criterion 3 of #118 names, `docs/evidence/issue-<this>-wave-b-walkthrough.md`. The template #117 created as `docs/evidence/issue-#118-wave-b-walkthrough.md` is replaced by it in the slice that fills the record: the reviewer prompts, `docs/agents/evidence-gates.md` and the dispatcher look for `docs/evidence/issue-<n>-*.md`, which a `#` in the name does not match.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

1. **Clean install from the wheel, then from PyPI**: `uvx --no-cache --from <source> founder-vn --version`, `… founder-vn install --host kiro` and `… founder-vn-mcp` answering `initialize` with `serverInfo.version` `0.3.0`, in an empty folder, first with the local 0.3.0 wheel and after the `v0.3.0` release with `founder-vn` from PyPI (criterion 2). Witnessed by hand on the operator's machine; no test reaches PyPI or GitHub Actions.
2. **Protocol step 1 of a Wave B skill inside a Kiro CLI session** (`server_info` against `metadata.version` set to `1.0.0`): the only place the major-mismatch stop can be observed (criterion 4). No automated seam (spec #1: skills have no automated seam).
3. **The ten skills end to end on Kiro CLI**: Wave A, then `founder-permits`, `founder-ops`, `founder-marketing`, `founder-launch`, `founder-plan` again and `founder-vn plan --check` exit 0 (criterion 3). No automated seam; the shape of this record is pinned by a test in `tests/test_hosts.py` that replaces `test_issue_118_template_has_unticked_boxes_and_claims_no_run`.
4. **`README.md` truth table and `docs/hosts/README.md`**: asserted by `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (criterion 5).
5. **`docs/hosts/kiro.md` walkthrough section**: it says the #118 walkthrough is pending and links the template; asserted by `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` (inferred from criterion 5: a host page that still says pending after the run would contradict the README).
6. **The tracker**: every friction or defect as an issue naming the skill or tool (criterion 6), not code.
