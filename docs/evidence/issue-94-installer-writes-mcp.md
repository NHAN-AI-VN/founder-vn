# Evidence: issue #94 the installer writes the MCP registration file

## Seam

Written by the operator in the ticket body (Q54, 2026-11-25); not inferred.

- `founder-vn install --host <host>` and its `--print-only` mode (CLI only, Q34; no MCP counterpart, so no parity slice): the files the Facilitator ends up with and the plan it prints. Module seam: `install.run` in `src/founder_vn/install.py`.
- `tests/test_install.py`, `tests/test_install_cli.py`, `tests/golden/install_*.json`: red first for the written registration file, the present-file case and the print-only case.
- `docs/hosts/*.md`: the host pages name the registration file (`tests/test_hosts.py`).

Out of scope: merging into an existing registration file; KiroCrew (stays print-only); the walkthrough record (#19).
