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

## Release record (criterion 2)

Done on 2026-11-26 from the operator's machine (macOS, uv 0.11.24); times UTC. The MCP `initialize` check is a scratch helper under `.harness/` (git-ignored): it sends `initialize` with protocol `2025-06-18` over stdio, reads the first response line, sends `notifications/initialized` and closes stdin.

| Step | Command or measurement | Result |
| --- | --- | --- |
| Commit to tag | `gh api repos/NHAN-AI-VN/founder-vn/pulls/139`; `git rev-parse <sha>^{tree}` for the merge commit and the pull request head | merge commit `ca6bc9f`, merged 2026-11-26T06:58:59Z; its tree `4766b11` equals the tree of the head `f68b73c`, whose `Gate` run 45771836554 concluded success (the merger's push to `main` starts no run) |
| Build | `uv build` at `ca6bc9f` | `founder_vn-0.3.0-py3-none-any.whl` sha256 `6c9628c9623cae47…`, `founder_vn-0.3.0.tar.gz` sha256 `6ab79f449993adf7…` |
| Dry run on the local wheel, empty folder (07:25:54Z) | `uvx --no-cache --from <repo>/dist/founder_vn-0.3.0-py3-none-any.whl founder-vn --version`; `… founder-vn install --host kiro`; MCP `initialize` to `… founder-vn-mcp` | `founder-vn 0.3.0`; 13 `create` lines: twelve skill files in ten skill folders and `.kiro/settings/mcp.json` with `["--from", "founder-vn", "founder-vn-mcp"]`; `grep -h -E '^ +version:' .kiro/skills/*/SKILL.md \| sort \| uniq -c` gives `10   version: "0.3.0"`; `serverInfo {"name": "founder-vn", "version": "0.3.0"}`, protocol `2025-06-18`, stderr empty, exit 0 |
| PyPI before the tag | `curl -s https://pypi.org/pypi/founder-vn/json` | `version 0.2.0`; releases `0.2.0` only |
| Tag (07:32:50Z) | `git tag -a v0.3.0 ca6bc9f -m "founder-vn 0.3.0" && git push origin v0.3.0`, after the operator's go-ahead in the session | tag object `23e0bb2` pointing at `ca6bc9f` |
| Release run 45776129259 | `gh api repos/NHAN-AI-VN/founder-vn/actions/runs/45776129259/jobs` | `Build` success, 07:32:54Z to 07:33:03Z (tag equals `v0.3.0`, `uv build`, artefact uploaded); `Publish to PyPI` waiting on environment `pypi`, required reviewer `nhannguyen89` |
| Approval (07:34:54Z) | `gh api --method POST repos/NHAN-AI-VN/founder-vn/actions/runs/45776129259/pending_deployments` with `state=approved`, run by the lane with the operator's `gh` account on the operator's instruction in the session ("approve theo đề xuất") | `Publish to PyPI` success, 07:34:55Z to 07:35:12Z |
| On PyPI | `curl -s https://pypi.org/pypi/founder-vn/0.3.0/json` | `founder_vn-0.3.0-py3-none-any.whl` sha256 `6c9628c9623cae47…` uploaded 07:35:08Z and `founder_vn-0.3.0.tar.gz` sha256 `6ab79f449993adf7…` uploaded 07:35:09Z: byte-identical to the build of the dry run; the project JSON gave `version 0.3.0` at 07:35:53Z |
| From PyPI, empty folder (07:36:00Z) | `uvx --no-cache --from founder-vn founder-vn --version`; `uvx --no-cache --from founder-vn founder-vn install --host kiro`; MCP `initialize` to `uvx --no-cache --from founder-vn founder-vn-mcp` | `founder-vn 0.3.0`; the same 13 `create` lines; `10   version: "0.3.0"`; `serverInfo {"name": "founder-vn", "version": "0.3.0"}`, protocol `2025-06-18`, stderr empty, exit 0 |
