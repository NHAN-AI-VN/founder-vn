# Evidence: issue #142 the package ships the permits ledger and the installer writes it

## Seam

Derived from the acceptance criteria of #142 (decision Q57, 2026-11-27); the ticket carries a `## Seam` section and this lane keeps it unchanged.

- `founder-vn install --host <host>` and its `--print-only` mode (CLI only, the installer is exempt from parity): the files the Facilitator ends up with and the plan printed. Module seam: `install.run` in `src/founder_vn/install.py`, plus `install.packaged_ledger` for the two-way lookup.
- `pyproject.toml` wheel force-include: `tests/test_install.py` pins it as it pins `skills`.
- `tests/test_install.py`, `tests/test_install_cli.py`, `tests/golden/install_*.json`: red first for the written ledger (create, update, unchanged, print-only, escape refused).
- `tests/test_permits_skill.py`, `tests/test_cfo_skill.py`, `tests/test_plan_skill.py`: red first for the one sentence.
- `tests/test_front_door.py`, `tests/test_hosts.py`: README and host pages, red first for the "fixed" wording.

Out of scope: a ledger lookup tool, moving the ledger into the skill folders, the ledger content, merging local edits, the version bump.

## Lát

No model and no network. Red and green ran with `uv run pytest <file> -q`.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| wheel ships ledger | `test_pyproject_ships_the_ledger_in_the_wheel` | `KeyError: 'permits/sources.md'` (13 failed, 31 passed with the rows below) | 44 passed |
| lookup | `test_default_ledger_is_the_repository_ledger_when_not_packaged` | `AttributeError: install.packaged_ledger` | 44 passed |
| every host, create | `test_every_host_writes_the_ledger_on_an_empty_project[5 hosts]` | `create     permits/sources.md` not in output | 44 passed |
| unchanged | `test_second_run_reports_the_ledger_unchanged` | `unchanged  permits/sources.md` not in output | 44 passed |
| update, keep others | `test_a_differing_ledger_is_updated_and_other_permits_files_are_kept` | `update     permits/sources.md` not in output | 44 passed |
| print-only | `test_print_only_plans_the_ledger_and_writes_nothing` | `create     permits/sources.md` not in output | 44 passed |
| escape | `test_ledger_through_an_escaping_symlink_is_refused` | `DID NOT RAISE InstallRefused` | 44 passed |
| CLI | `test_cli_install_writes_the_ledger_on_a_clean_project`, `test_cli_ledger_escape_exits_2` | missing line; exit code 0 instead of 2 | 44 passed |
| goldens | `test_print_only_golden[5 hosts]` | 5 failed on the new plan line once the code was in; goldens regenerated, explained in the commit message | 44 passed |
| three skill sentences | `test_says_how_to_get_an_absent_ledger_and_not_to_guess` in permits, cfo, plan tests | 3 failed with the skill edits stashed (40 passed) | 43 passed |
| README, host pages | `test_readme_truth_table_is_honest_about_release_status_and_hosts`, `test_kiro_page_has_the_clean_install_walkthrough_for_19` | 2 failed with the docs unedited | 24 passed (`tests/test_front_door.py`, `tests/test_hosts.py`) |
| design, standards | `test_design_and_standards_record_q57` | 1 failed with the docs stashed | 32 passed |

## Wheel

`unzip -l dist/founder_vn-0.3.0-py3-none-any.whl` lists `28337  founder_vn/permits/sources.md`; `unzip -p` of that member `cmp`s identical to `permits/sources.md`.

## Cổng ba đoạn

Last code commit: `823a057`. Each segment ran once at that HEAD; this evidence commit is the only commit after it.

```
static: ruff check and format clean, skill-lint 0 findings
unit:   481 passed
build:  Successfully built dist/founder_vn-0.3.0-py3-none-any.whl
verify: GREEN on 823a057b60cf18c917ed1470f3277f43f7b6a435
```

## Giới hạn

- The wheel was inspected from the checkout build; the ledger on PyPI 0.3.0 still lacks the file until the release that ships this change (version bump out of scope).
- A Facilitator's local edit of `permits/sources.md` is overwritten (reported `update`); no merge, by decision.
- Symlink escape is covered for the `permits` directory; a dangling symlink at `permits/sources.md` inside the project is written through.
- No host session was run; the CLI is tested in process.
