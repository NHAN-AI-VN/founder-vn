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
| front-door | `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (Install pending the `v0.3.0` tag, no released or verified claim for 0.3.0, Kiro row keeps the 0.2.0 phrase and adds `Wave B: pending walkthrough (#118)`, Vietnamese mirror, hosts index row; the old assertion that `pending walkthrough` is absent became "only the Kiro CLI row says it") | `assert "0.3.0" in english and "pending the `v0.3.0` tag" in english` failed (1 failed, 11 passed) | `uv run pytest tests/test_front_door.py -q` gave 12 passed |
| kiro-walkthrough | `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` (wheel name `founder_vn-0.3.0`, Wave B order permits, ops, marketing, launch, plan again, `plan --check`, mismatch step after them) and `test_issue_118_template_has_unticked_boxes_and_claims_no_run` | `AssertionError: uvx --from ./dist/founder_vn-0.3.0-py3-none-any.whl founder-vn install --host kiro` and `FileNotFoundError: docs/evidence/issue-#118-wave-b-walkthrough.md` (2 failed, 10 passed) | `uv run pytest tests/test_hosts.py -q` gave 12 passed |

## Cổng ba đoạn

Run once each, at code HEAD `5a55852` (the last code commit; this evidence commit touches no code).

- `bash scripts/harness/gate-segment.sh static`: `All checks passed!`, `252 files already formatted`, `skill-lint: 10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.0)`, exit 0.
- `bash scripts/harness/gate-segment.sh unit`: `464 passed in 30.91s`, exit 0.
- `bash scripts/harness/gate-segment.sh build`: `Successfully built dist/founder_vn-0.3.0.tar.gz` and `dist/founder_vn-0.3.0-py3-none-any.whl`, exit 0.
- `bash scripts/harness/gate-segment.sh verify`:

```
gate-segment verify: latest line per segment (.harness/gate-segments.txt)
  static 0 5a55852dc9874e3fa43489d2147e8413d3325a05 2026-11-26T06:52:46Z
  unit 0 5a55852dc9874e3fa43489d2147e8413d3325a05 2026-11-26T06:53:19Z
  build 0 5a55852dc9874e3fa43489d2147e8413d3325a05 2026-11-26T06:53:21Z
gate-segment verify: GREEN on 5a55852dc9874e3fa43489d2147e8413d3325a05
```

## Giới hạn

- The checks are textual: they do not prove a legal claim is correct, only that a link carries a date, the disclaimer and the panel caveat are present, and no `$` sits beside a digit.
- `business-plan.md` is pinned by its `## Chưa làm` bullets, not regenerated here; that it is compiler output is covered by the plan golden tests.
- The caveat is required in `marketing.md` and `launch.md`, the two Wave B files that quote a panel number; `permits.md` and `ops.md` quote none.
- No tag `v0.3.0` was created and nothing was published to PyPI: 0.2.0 stays the released version and the README says 0.3.0 is pending the `v0.3.0` tag.
- No walkthrough was executed. `docs/hosts/kiro.md` gained the Wave B steps as a script only. The record of #118 is a template, `docs/evidence/issue-#118-wave-b-walkthrough.md`, whose file name contains a literal `#` (the ticket's exact name). Its seven boxes are unticked, its record table is empty, and its criteria are copied from the body of issue #118.
- No host is verified for Wave B. The Kiro CLI row keeps "full pipeline verified on 0.2.0 (walkthrough 2026-11-25, #19)" and adds "Wave B: pending walkthrough (#118)"; the other hosts stay "not yet verified".
- The deliberate major-mismatch step is now step 9 (the Wave B step took number 7, the confirmation became 8). Its content is unchanged except that the restore version reads `0.3.0`, the version of the installed package, because `0.2.0` would be false for skills installed from a 0.3.0 build.
- Skill counts: `docs/hosts/README.md` says "the six Wave A skills" about the 0.2.0 run, which stays true. No other host page states a number of skills.

## Giải quyết review nội bộ

No self-review was run: review is the two independent turns the harness dispatches after the PR opens (lane rule).
