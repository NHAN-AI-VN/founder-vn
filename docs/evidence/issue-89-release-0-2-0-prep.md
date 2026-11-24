# Evidence: issue #89 release 0.2.0 prep

## Seam

Derived from the acceptance criteria (the ticket's `## Seam` was written by the operator; the list below follows it and is partly inferred).

- `founder_vn.__version__`, read through `founder-vn --version`, `founder-vn version` and the MCP tool `server_info` (existing parity tests). Criterion 1.
- `scripts/skill_lint.py` rule `rule_version_matches`: the lockstep gate between the package version and the six `metadata.version` values. Criterion 1.
- `founder-vn install --host <host> --print-only` (CLI only, Q34, no MCP counterpart, no parity slice): the `uvx` arguments in the snippets, asserted by `tests/test_hosts.py` and the `tests/golden/install_*.json` goldens. Criterion 2.
- Documentation checks in `tests/test_front_door.py` (README command, Install and Status truth tables) and `tests/test_hosts.py` (Kiro walkthrough section, #19 template). Criteria 2 to 4.
