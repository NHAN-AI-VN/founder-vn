# Evidence: issue #89 release 0.2.0 prep

## Seam

Derived from the acceptance criteria (the ticket's `## Seam` was written by the operator; the list below follows it and is partly inferred).

- `founder_vn.__version__`, read through `founder-vn --version`, `founder-vn version` and the MCP tool `server_info` (existing parity tests). Criterion 1.
- `scripts/skill_lint.py` rule `rule_version_matches`: the lockstep gate between the package version and the six `metadata.version` values. Criterion 1.
- `founder-vn install --host <host> --print-only` (CLI only, Q34, no MCP counterpart, no parity slice): the `uvx` arguments in the snippets, asserted by `tests/test_hosts.py` and the `tests/golden/install_*.json` goldens. Criterion 2.
- Documentation checks in `tests/test_front_door.py` (README command, Install and Status truth tables) and `tests/test_hosts.py` (Kiro walkthrough section, #19 template). Criteria 2 to 4.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| version | `tests/golden/version.json` (golden of `founder-vn version`), `tests/test_parity.py`, `tests/test_skill_lint.py` | `{'stdout': 'founder-vn 0.1.0\n'} != {'stdout': 'founder-vn 0.2.0\n'}` | `uv run pytest tests/ -q -k "version or golden or parity or skill_lint or package"` (72 passed after `uv sync --frozen --reinstall-package founder-vn`, which refreshes the installed metadata that `test_package_has_single_source_version` reads) |
| lockstep witness | `tests/test_skill_lint.py::test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version` | n/a (existing gate, run to show it still bites at 0.2.0) | `uv run pytest "tests/test_skill_lint.py::test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version" -q` gave `1 passed`; `python3 scripts/skill_lint.py` gave `6 skills checked, 15 example file(s), 0 finding(s) (package version 0.2.0)` |
| uvx `--from` | `tests/test_hosts.py::test_kiro_mcp_json_registers_the_console_script`, `test_every_host_page_starts_the_server_with_uvx_from_the_package`, `tests/test_front_door.py::test_readme_names_purpose_audience_hosts_and_both_install_routes`, `tests/test_install_cli.py` goldens | 3 failed in the three files, then 5 install goldens failed after the source change (`install_<host>.json` differ in the `uvx` arguments) | `uv run pytest tests/test_hosts.py tests/test_front_door.py tests/test_install_cli.py tests/test_install.py -q` gave 41 passed |
| README truth table | `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` | `assert '0.2.0 is the first PyPI release' in '# founder-vn ...'` | `uv run pytest tests/test_front_door.py -q` gave 12 passed |
| Kiro walkthrough and #19 template | `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19`, `test_issue_19_template_has_unticked_boxes_and_claims_no_run` | `assert '## Clean-install walkthrough' in '# Kiro: registering ...'` and `FileNotFoundError: ... issue-19-wave-a-walkthrough.md` | `uv run pytest tests/test_hosts.py -q` gave 10 passed |

The golden files `tests/golden/install_*.json` and `tests/golden/version.json` changed because the `uvx` arguments changed (`--from founder-vn founder-vn-mcp`, Q53) and because the version is now 0.2.0.

## Cổng ba đoạn

```
gate-segment verify: latest line per segment (.harness/gate-segments.txt)
  static 0 bb5078baa438d5886805da1aeb9c4c3d4cc40280
  unit 0 bb5078baa438d5886805da1aeb9c4c3d4cc40280
  build 0 bb5078baa438d5886805da1aeb9c4c3d4cc40280
gate-segment verify: GREEN on bb5078baa438d5886805da1aeb9c4c3d4cc40280
```

From the logs: `All checks passed!` (static, with skill-lint 0 findings), `351 passed` (unit), `Successfully built dist/founder_vn-0.2.0-py3-none-any.whl` (build). This evidence commit follows the gate block, so the gate was run again on the final HEAD before the pull request was opened.

## Giới hạn

- No tag: `v0.2.0` is not created and `release.yml` is untouched.
- No PyPI publish: the first PyPI release is still to come; the README says it is pending the tag.
- No walkthrough executed: `docs/hosts/kiro.md` and `docs/evidence/issue-19-wave-a-walkthrough.md` are a procedure and an empty template for the operator on a real Kiro CLI.
- No host verified: the README marks Kiro CLI "full pipeline: pending walkthrough (#19)" and every other host "not yet verified".
- The `uvx --from` form was measured by the operator on 2026-11-24 (Q53); this lane asserts the strings in snippets, pages and goldens, not a live `uvx` run against PyPI.
