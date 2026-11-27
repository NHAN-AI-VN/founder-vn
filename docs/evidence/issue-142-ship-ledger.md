# Evidence: issue #142 the package ships the permits ledger and the installer writes it

## Seam

Derived from the acceptance criteria of #142 (decision Q57, 2026-11-27); the ticket carries a `## Seam` section and this lane keeps it unchanged.

- `founder-vn install --host <host>` and its `--print-only` mode (CLI only, the installer is exempt from parity): the files the Facilitator ends up with and the plan printed. Module seam: `install.run` in `src/founder_vn/install.py`, plus `install.packaged_ledger` for the two-way lookup.
- `pyproject.toml` wheel force-include: `tests/test_install.py` pins it as it pins `skills`.
- `tests/test_install.py`, `tests/test_install_cli.py`, `tests/golden/install_*.json`: red first for the written ledger (create, update, unchanged, print-only, escape refused).
- `tests/test_permits_skill.py`, `tests/test_cfo_skill.py`, `tests/test_plan_skill.py`: red first for the one sentence.
- `tests/test_front_door.py`, `tests/test_hosts.py`: README and host pages, red first for the "fixed" wording.

Out of scope: a ledger lookup tool, moving the ledger into the skill folders, the ledger content, merging local edits, the version bump.
