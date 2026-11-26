# Evidence: issue #117 release 0.3.0 prep

## Seam

Derived from the acceptance criteria (the ticket's `## Seam` follows the list below and is partly inferred).

- `founder_vn.__version__`, read through `founder-vn --version`, `founder-vn version` and the MCP tool `server_info` (existing parity tests). Criterion 1.
- `scripts/skill_lint.py` rule `rule_version_matches`: the lockstep gate between the package version and the ten `metadata.version` values. Criterion 1.
- The Wave B checklist test `tests/test_wave_b_checklist.py` over `examples/barbershop/founder/` (`permits.md`, `ops.md`, `marketing.md`, `launch.md`, and `business-plan.md` as compiler output). Criterion 2.
- README, `docs/hosts/` truth tables through `tests/test_front_door.py`, and the Kiro walkthrough through `tests/test_hosts.py`. Criteria 3 and 4.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|

## Cổng ba đoạn

## Giới hạn
