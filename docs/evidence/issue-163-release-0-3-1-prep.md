# Evidence: issue #163 release 0.3.1 prep (machine half)

## Seam

Taken from the ticket's own `## Seam` (written by the operator); not inferred.

- `founder_vn.__version__`, read through `founder-vn --version`, `founder-vn version` and the MCP tool `server_info` (`tests/test_parity.py`, `tests/golden/version.json`, `tests/test_package.py`). Criterion 1.
- `scripts/skill_lint.py` lockstep rule over the ten `skills/*/SKILL.md` (`tests/test_skill_lint.py`, the four `tests/test_*_skill.py` that read `__version__`). Criterion 1.
- `README.md` and `docs/hosts/README.md` Install and version sentences (`tests/test_front_door.py`). Criterion 2.
- The `docs/hosts/kiro.md` local-wheel dry-run command (`tests/test_hosts.py`). Criterion 3.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| version | `tests/golden/version.json` (golden of `founder-vn version`), `tests/test_parity.py`, `tests/test_skill_lint.py`, `tests/test_package.py` | `{'stdout': 'founder-vn 0.3.0\n'} != {'stdout': 'founder-vn 0.3.1\n'}` (1 failed, 111 passed) | `uv run pytest tests/ -q -k "version or golden or parity or skill_lint or package"` gave 112 passed after `uv sync --frozen --reinstall-package founder-vn` (refreshes the installed metadata that `tests/test_package.py` reads). The golden changed only because the version string changed. |
| lockstep witness | `tests/test_skill_lint.py::test_skill_lint_refuses_a_skill_version_that_differs_from_a_dynamic_package_version` | with `skills/founder-launch/SKILL.md` set back to 0.3.0 on a scratch edit (restored, not committed): `skills/founder-launch/SKILL.md:1: metadata.version '0.3.0' differs from pyproject [project].version '0.3.1'`, 1 finding | the test gave `1 passed`; after the restore `python3 scripts/skill_lint.py` gave `10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.1)` |
| front-door | `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (negative assertions narrowed to the 0.3.0 tag; positive pins for the English, Vietnamese and hosts index pending sentences) | `AssertionError: assert 'The repository is at 0.3.1, pending the `v0.3.1` tag (#149).' in '# founder-vn ...'` (1 failed, 13 passed) | `uv run pytest tests/test_front_door.py -q` gave 14 passed |
| kiro-walkthrough | `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` | `AssertionError: uvx --from ./dist/founder_vn-0.3.1-py3-none-any.whl founder-vn install --host kiro` (1 failed, 12 passed) | `uv run pytest tests/test_hosts.py -q` gave 13 passed |

`uv.lock` has no `version` line under `name = "founder-vn"` and did not change. The `args` example of step 3 in `docs/hosts/kiro.md` names the same wheel and moved to 0.3.1 with the dry-run command. The `founder-vn 0.3.0` output lines in `tests/test_hosts.py` record the 2026-11-26/27 walkthrough and stay.

## Cổng ba đoạn

Run once each, at code HEAD `fab92e0` (this evidence commit touches no code).

- `static`: `All checks passed!`, `273 files already formatted`, `skill-lint: 10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.1)`, exit 0.
- `unit`: `502 passed in 29.99s`, exit 0.
- `build`: `Successfully built dist/founder_vn-0.3.1.tar.gz` and `dist/founder_vn-0.3.1-py3-none-any.whl`, exit 0.
- `verify`:

```
gate-segment verify: latest line per segment (.harness/gate-segments.txt)
  static 0 fab92e060de025c70e5bd36fbbb4cb9866973715 2026-11-27T09:28:26Z
  unit 0 fab92e060de025c70e5bd36fbbb4cb9866973715 2026-11-27T09:28:57Z
  build 0 fab92e060de025c70e5bd36fbbb4cb9866973715 2026-11-27T09:28:58Z
gate-segment verify: GREEN on fab92e060de025c70e5bd36fbbb4cb9866973715
```

## Giới hạn

- No tag `v0.3.1` was created and nothing was published to PyPI: 0.3.0 stays the current release and the front door says 0.3.1 is pending the `v0.3.1` tag (#149).
- No clean install from PyPI or from the 0.3.1 wheel was run; the wheel was only built by the gate.
- No skill was run on 0.3.1.
- No host is verified on 0.3.1; the host tables keep their 0.3.0 and 0.2.0 claims.
- The #142 and #118 sentences are unchanged: #149 step 5 rewrites them after the publish.

## Giải quyết review nội bộ

No self-review was run: review is the two independent turns the harness dispatches after the PR opens (lane rule).
