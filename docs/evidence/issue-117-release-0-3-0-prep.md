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
| version | `tests/golden/version.json` (golden of `founder-vn version`), `tests/test_parity.py`, `tests/test_skill_lint.py` | `{'stdout': 'founder-vn 0.2.0\n'} != {'stdout': 'founder-vn 0.3.0\n'}` (1 failed, 105 passed) | `uv run pytest tests/ -q -k "version or golden or parity or skill_lint or package"` gave 106 passed after `uv sync --frozen --reinstall-package founder-vn` (refreshes the installed metadata that `test_package_has_single_source_version` reads) |
| lockstep witness | `tests/test_skill_lint.py::test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version` | with `skills/founder-launch/SKILL.md` set back to 0.2.0 on a scratch edit (restored, not committed): `skills/founder-launch/SKILL.md:1: metadata.version '0.2.0' differs from pyproject [project].version '0.3.0'`, 1 finding | `uv run pytest "tests/test_skill_lint.py::test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version" -q` gave `1 passed`; `python3 scripts/skill_lint.py` gave `10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.0)` |
| wave-b checklist | `tests/test_wave_b_checklist.py` (six checks over `examples/barbershop/founder/`; `test_each_check_goes_red_on_its_mutation` mutates a copy under `tmp_path`) | `present`: `AssertionError: ops.md`; `dollar`: `AssertionError: launch.md`; `disclaimer`: `AssertionError: ops.md`; `caveat`: `AssertionError: ('marketing.md', 'cận trên')`; `dated_links`: the undated `congbao.chinhphu.vn` line of `permits.md`; `after_pilot`: the bullet list gains a third line and differs from the two after-pilot lines | `uv run pytest tests/test_wave_b_checklist.py -q` gave 12 passed |

## Cổng ba đoạn

## Giới hạn

- The checks are textual: they do not prove a legal claim is correct, only that a link carries a date, the disclaimer and the panel caveat are present, and no `$` sits beside a digit.
- `business-plan.md` is pinned by its `## Chưa làm` bullets, not regenerated here; that it is compiler output is covered by the plan golden tests.
- The caveat is required in `marketing.md` and `launch.md`, the two Wave B files that quote a panel number; `permits.md` and `ops.md` quote none.
- The README and `docs/hosts/` truth tables and the Kiro walkthrough are handled in a later slice of this lane.
