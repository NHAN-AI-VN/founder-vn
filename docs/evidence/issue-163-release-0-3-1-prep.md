# Evidence: issue #163 release 0.3.1 prep (machine half)

## Seam

Taken from the ticket's own `## Seam` (written by the operator); not inferred.

- `founder_vn.__version__`, read through `founder-vn --version`, `founder-vn version` and the MCP tool `server_info` (`tests/test_parity.py`, `tests/golden/version.json`, `tests/test_package.py`). Criterion 1.
- `scripts/skill_lint.py` lockstep rule over the ten `skills/*/SKILL.md` (`tests/test_skill_lint.py`, the four `tests/test_*_skill.py` that read `__version__`). Criterion 1.
- `README.md` and `docs/hosts/README.md` Install and version sentences (`tests/test_front_door.py`). Criterion 2.
- The `docs/hosts/kiro.md` local-wheel dry-run command (`tests/test_hosts.py`). Criterion 3.
