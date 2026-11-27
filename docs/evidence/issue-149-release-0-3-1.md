# Evidence: issue #149 release 0.3.1, the sources ledger ships with the package

Lane run by the project owner's Kiro CLI session through `founder-guarded`, on the operator's instruction in the session ("thực hiện thay tôi #149"); the ticket is `ready-for-human`, so the dispatcher skips it and the operator's allocation comment on #149 (2026-11-27) grants `README.md`, lane branch `lane/issue-149`, target `main`. The machine half #163 merged as `c5c5ef7` (PR #164, 2026-11-27T09:34:42Z): `__version__` and the ten `metadata.version` values are 0.3.1, the front door says 0.3.1 is pending the `v0.3.1` tag.

`HARNESS_SINGLE_OWNER_FILES` is not exported in this session, so `.kiro/hooks/guard.sh` refuses the editor tools on `README.md` (probed before the first slice on `pyproject.toml`, refused as expected); the front-door slice leaves a patch under `.harness/` for the operator to apply by hand, as the #118 lane did.

## Seam

Derived from the acceptance criteria and the five steps of #149 (the ticket has no `## Seam` section); every line is inferred.

1. **The release itself**: tag `v0.3.1` on `c5c5ef7`, `release.yml` Build, `Publish to PyPI` approved on environment `pypi`; `curl -s https://pypi.org/pypi/founder-vn/json` gives version 0.3.1 and the PyPI wheel's sha256 equals the local `uv build` at the same commit (criterion 1). Witnessed by hand from the operator's machine; no test reaches PyPI or GitHub Actions.
2. **Clean install from PyPI in an empty folder outside every git tree**: `uvx --no-cache --from founder-vn founder-vn --version`, `… founder-vn install --host kiro` writing 14 `create` lines including `permits/sources.md`, the written ledger byte-identical to `src/founder_vn/permits/sources.md` at the tagged commit, `unzip -l` of the PyPI wheel listing `founder_vn/permits/sources.md`, MCP `initialize` answering `serverInfo.version` 0.3.1 (criterion 2). Witnessed by hand; the in-process half of the same behaviour is `tests/test_install.py` and `tests/test_install_cli.py` (#142).
3. **`founder-permits` and `founder-cfo` on the clean install with the golden `idea.md`**: `permits.md` passes `check_permits_links_dated` of `tests/test_wave_b_checklist.py` and `cfo.md` carries the "Giới hạn của phần thuế" section and passes the legal-claim check of `tests/test_wave_a_checklist.py` (criterion 3). Run in a nested non-interactive Kiro CLI session from the clean-install folder; only file names, the kind of result and the model name are recorded, the folder stays outside git.
4. **The front door**: `README.md`, `docs/hosts/README.md` and `docs/hosts/kiro.md` say 0.3.1 is the current release and #142 is fixed in it; asserted by `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` and `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` (criterion 4), red first.

Out of scope: any skill behaviour, `release.yml`, the ledger content, #20 and #113.
