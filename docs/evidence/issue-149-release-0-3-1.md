# Evidence: issue #149 release 0.3.1, the sources ledger ships with the package

Lane run by the project owner's Kiro CLI session through `founder-guarded`, on the operator's instruction in the session ("thực hiện thay tôi #149"); the ticket is `ready-for-human`, so the dispatcher skips it and the operator's allocation comment on #149 (2026-11-27) grants `README.md`, lane branch `lane/issue-149`, target `main`. The machine half #163 merged as `c5c5ef7` (PR #164, 2026-11-27T09:34:42Z): `__version__` and the ten `metadata.version` values are 0.3.1, the front door says 0.3.1 is pending the `v0.3.1` tag.

`HARNESS_SINGLE_OWNER_FILES` is not exported in this session, so `.kiro/hooks/guard.sh` refuses the editor tools on `README.md` (probed before the first slice on `pyproject.toml`, refused as expected); the front-door slice left `.harness/readme-149.patch` (built by a scratch script from exact-match replacements, `git apply --check` clean) and the operator applied it by hand before the slice was committed, as the #118 lane did for its last slice. Shell reads of the file were not refused; no shell write was attempted.

## Seam

Derived from the acceptance criteria and the five steps of #149 (the ticket has no `## Seam` section); every line is inferred.

1. **The release itself**: tag `v0.3.1` on `c5c5ef7`, `release.yml` Build, `Publish to PyPI` approved on environment `pypi`; `curl -s https://pypi.org/pypi/founder-vn/json` gives version 0.3.1 and the PyPI wheel's sha256 equals the local `uv build` at the same commit (criterion 1). Witnessed by hand from the operator's machine; no test reaches PyPI or GitHub Actions.
2. **Clean install from PyPI in an empty folder outside every git tree**: `uvx --no-cache --from founder-vn founder-vn --version`, `… founder-vn install --host kiro` writing 14 `create` lines including `permits/sources.md`, the written ledger byte-identical to `src/founder_vn/permits/sources.md` at the tagged commit, `unzip -l` of the PyPI wheel listing `founder_vn/permits/sources.md`, MCP `initialize` answering `serverInfo.version` 0.3.1 (criterion 2). Witnessed by hand; the in-process half of the same behaviour is `tests/test_install.py` and `tests/test_install_cli.py` (#142).
3. **`founder-permits` and `founder-cfo` on the clean install with the golden `idea.md`**: `permits.md` passes `check_permits_links_dated` of `tests/test_wave_b_checklist.py` and `cfo.md` carries the "Giới hạn của phần thuế" section and passes the legal-claim check of `tests/test_wave_a_checklist.py` (criterion 3). Run in a nested non-interactive Kiro CLI session from the clean-install folder; only file names, the kind of result and the model name are recorded, the folder stays outside git.
4. **The front door**: `README.md`, `docs/hosts/README.md` and `docs/hosts/kiro.md` say 0.3.1 is the current release and #142 is fixed in it; asserted by `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` and `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` (criterion 4), red first.

Out of scope: any skill behaviour, `release.yml`, the ledger content, #20 and #113.

## Acceptance criteria of #149

Copied from the ticket.

- [x] `curl -s https://pypi.org/pypi/founder-vn/json` gives version 0.3.1 (09:57:06Z on 2026-11-27, after a CDN lag: the same call at 09:56:26Z still said 0.3.0 while the release JSON already listed the files); the PyPI wheel's sha256 `3df5d062…a2142` equals the local build's (release record below).
- [x] The clean install from PyPI writes `permits/sources.md`, byte-identical to `permits/sources.md` at the tagged commit (`cmp` against `git show v0.3.1:permits/sources.md`; clean-install record below).
- [x] `permits.md` and `cfo.md` from the clean-install run pass the two legal-claim checks named in step 4: `check_permits_links_dated` PASS on `permits.md` (21 Công báo links, 21 dated), the legal-claim check PASS on `cfo.md` with the "Giới hạn của phần thuế" section present (re-run record below, 2026-11-28).
- [x] The front door says 0.3.1 is current and names #142 as fixed; `tests/test_front_door.py` and `tests/test_hosts.py` pin it: slice `67218ff` (Lát below).

## Release record (criterion 1)

Done on 2026-11-27 from the operator's machine (macOS, uv 0.11.x, gh 2.98.0); times UTC. The MCP `initialize` check is a scratch helper under `.harness/` (git-ignored): it sends `initialize` with protocol `2025-06-18` over stdio, reads the first response line, sends `notifications/initialized` and closes stdin.

| Step | Command or measurement | Result |
| --- | --- | --- |
| Commit to tag | `gh api repos/NHAN-AI-VN/founder-vn/pulls/164`; `git rev-parse <sha>^{tree}` for the merge commit and the pull request head | merge commit `c5c5ef7`, merged 2026-11-27T09:34:42Z; its tree `61006f2` equals the tree of the head `58e3c92`, whose `Gate` run 45974713020 concluded success (the merger's push to `main` starts no run: zero runs at `c5c5ef7`) |
| Build | `uv build` in a detached worktree at `c5c5ef7` (`.harness/build-c5c5ef7`, so the lane's own commits are not in the sdist) | `founder_vn-0.3.1-py3-none-any.whl` sha256 `3df5d062da868e65…a2142`, `founder_vn-0.3.1.tar.gz` sha256 `cad8522106976dda…ce452`; `unzip -l` lists `28337  founder_vn/permits/sources.md`, `cmp` identical to `permits/sources.md` at `c5c5ef7` (sha256 `87054ae4…`) |
| Dry run on the local wheel, empty folder outside git (09:52:01Z) | `uvx --no-cache --from <wheel> founder-vn --version`; `… founder-vn install --host kiro`; MCP `initialize` to `… founder-vn-mcp` | `founder-vn 0.3.1`; **14 `create` lines**: twelve skill files in ten skill folders, `permits/sources.md`, `.kiro/settings/mcp.json` (`["--from", "founder-vn", "founder-vn-mcp"]`); the written ledger `cmp`s identical to the repository's; `grep -h -E '^ +version:' .kiro/skills/*/SKILL.md \| sort \| uniq -c` gives `10   version: "0.3.1"`; `serverInfo {"name": "founder-vn", "version": "0.3.1"}`, protocol `2025-06-18`, exit 0 (stderr holds only uvx's own install lines) |
| PyPI before the tag | `curl -s https://pypi.org/pypi/founder-vn/json` | `version 0.3.0`; releases `0.2.0, 0.3.0`; tags on origin `v0.2.0`, `v0.3.0` |
| Tag (09:54:56Z) | `git tag -a v0.3.1 c5c5ef7 -m "founder-vn 0.3.1" && git push origin v0.3.1`, after the operator's go-ahead in the session ("go") | tag object `bb5ee92` pointing at `c5c5ef7` |
| Release run 45977671164 | `gh api repos/NHAN-AI-VN/founder-vn/actions/runs/45977671164/jobs` | `Build` success, 09:55:03Z to 09:55:13Z (tag equals `v0.3.1`, `uv build`, artefact uploaded); `Publish to PyPI` waiting on environment `pypi` (id 28354158075), required reviewer `nhannguyen89` |
| Approval (09:55:31Z) | `gh api --method POST …/actions/runs/45977671164/pending_deployments` with `environment_ids[]=28354158075`, `state=approved`, run by the lane with the operator's `gh` account on the operator's go-ahead; `…/approvals` afterwards | `approved by nhannguyen89`; `Publish to PyPI` success, 09:55:35Z to 09:55:56Z |
| On PyPI | `curl -s https://pypi.org/pypi/founder-vn/0.3.1/json` | `founder_vn-0.3.1-py3-none-any.whl` sha256 `3df5d062da868e65…a2142` uploaded 09:55:52Z and `founder_vn-0.3.1.tar.gz` sha256 `cad8522106976dda…ce452` uploaded 09:55:53Z: byte-identical to the local build; the project JSON gave `version 0.3.1`, releases `0.2.0, 0.3.0, 0.3.1`, at 09:57:06Z |

## Clean install from PyPI (criterion 2)

Folder `~/Documents/Research/founder-release-149/clean-install`, outside every git tree (`git rev-parse --show-toplevel` fails in it), 2026-11-27.

| Step | Command or measurement | Result |
| --- | --- | --- |
| Version (09:56:49Z) | `uvx --no-cache --from founder-vn founder-vn --version` | `founder-vn 0.3.1` |
| Install | `uvx --no-cache --from founder-vn founder-vn install --host kiro` | **14 `create` lines**, the same set as the dry run, `permits/sources.md` among them |
| Ledger identity | `git show v0.3.1:permits/sources.md \| cmp - permits/sources.md` | identical (the ledger lives at `permits/sources.md` in the repository and is force-included into the wheel as `founder_vn/permits/sources.md`) |
| Skills | `grep -h -E '^ +version:' .kiro/skills/*/SKILL.md \| sort \| uniq -c` | `10   version: "0.3.1"` |
| PyPI wheel | downloaded from the URL in the release JSON; `shasum -a 256`; `unzip -l`; `unzip -p … founder_vn/permits/sources.md \| cmp - permits/sources.md` | sha256 prefix `3df5d062da868e65`; lists `28337  founder_vn/permits/sources.md`; identical to the installed ledger |
| MCP (09:57:06Z) | `initialize` to `uvx --no-cache --from founder-vn founder-vn-mcp` | `serverInfo {"name": "founder-vn", "version": "0.3.1"}`, protocol `2025-06-18`, exit 0 |

## Re-run of the two steps #142 broke (criterion 3)

Run on 2026-11-28 in the clean-install folder above (package `founder-vn` 0.3.1 from PyPI through the installed `.kiro/settings/mcp.json`; the installer's `permits/sources.md` in place), with the golden `idea.md` copied from `examples/barbershop/founder/idea.md` at `v0.3.1` (sha256 prefix `f8565562`). Each skill ran in a nested non-interactive Kiro CLI 2.37.1 session this lane started from that folder (`kiro-cli chat --no-interactive --trust-workspace --trust-all-tools --model <model> "<prompt>"`), the lane standing in for the Facilitator and the prompt carrying the Owner's answers in advance (one individual, services). Only the model name is recorded. Times UTC, from `date -u` lines the lane wrote to a `times.txt` outside git and from file modification times. The outputs stay in that folder; only file names and the kind of result are recorded here.

| Step | Command or measurement | Result |
| --- | --- | --- |
| `founder-permits`, attempt 1 (2026-11-27, 10:00:49Z) | model `claude-opus-5.5`; the prompt bounded nothing | killed after 20 min by the time limit of the lane's own tool call, still inside Step 3 (re-check at run time: scripts under `/tmp` fetching Công báo pages); no `permits.md` |
| `founder-permits`, attempt 2 (10:01:27Z to 10:21:50Z) | model `claude-opus-5.5`; the prompt bounded Step 3 to about 3 minutes, one curl per link | the session ended by itself at about 20 min with no final message and no `permits.md`, after about ten tool calls (task list, one curl loop, three analysis commands over the answers), each model turn taking 2 to 6 minutes; the end reason is not recorded |
| `founder-permits`, attempt 3 (10:23:27Z to 10:46:39Z; `permits.md` written 10:45Z) | model `claude-fable-5.1`; the Facilitator's bound on Step 3: one shell command, one `curl -m 8` per link, 90 s in all, no PDF download; then write the file | `server_info` called first (`SERVER_INFO=founder-vn 0.3.1` as the reply's last line); `founder/permits.md` (34 087 bytes) with the six headings in the skill's order; **21 `congbao.chinhphu.vn` links, 21 of them on a line with a `dd/mm/yyyy` verification date**; the registration fee written as "chưa có nguồn đã kiểm chứng" (5 lines, as the skill prescribes: the ledger holds no fee amount); the run-time re-check did not confirm the pages in the bound, so 13 lines carry "kiểm chứng ngày X, chưa xác nhận lại hôm nay" and no figure was dropped; no `$` next to a digit; "anh/chị" 16 times; `check_permits_links_dated` of `tests/test_wave_b_checklist.py` **PASS** (scratch runner `.harness/check-149.py`, git-ignored, importing the check function from the test module) |
| `founder-cfo` (10:47:15Z to about 10:48Z) | model `claude-fable-5.1`; `founder/numbers.json` placed first, byte-identical to the golden (sha256 prefix `bd39660d`); the prompt: keep every figure, do Step 3 from the ledger, Step 4 through MCP, Steps 5 and 6 | `@founder-vn/server_info` then `@founder-vn/cfo_analyse` (once each); `founder/numbers.json` unchanged (the ledger's `tax_rate_on_revenue` 7 and `tax_free_threshold` 1 000 000 000 equal the golden's); `founder/cfo.md` (7 397 bytes) with the tool's six sections and the appended **"Giới hạn của phần thuế"**, **4 `congbao.chinhphu.vn` links, 4 of them dated**; "không phải tư vấn" twice; no `$`; the legal-claim check of `tests/test_wave_a_checklist.py` (the `LEGAL` regex matches; a Công báo link and a date are present) **PASS**; `SERVER_INFO=founder-vn 0.3.1` |

What this shows: on a clean install of 0.3.1 the two skills find `permits/sources.md` where 0.3.0 found nothing (#118 rows 6.4 and 7.1), and every legal figure they write carries the ledger's link and date. The deviations from the skills' own steps are the Facilitator's bound on Step 3 of `founder-permits` (attempt 3) and the Owner's answers given in the prompt instead of in conversation; both are recorded, neither changes a skill file.

## Lát

One red-green slice; the release and the re-run are hand-witnessed records, not slices.

| Test | Assertion line while red | Green rerun |
| --- | --- | --- |
| `test_readme_truth_table_is_honest_about_release_status_and_hosts` and `test_readme_names_purpose_audience_hosts_and_both_install_routes` (README Install: "0.3.1 (Wave B, ten skills; ships the source ledger, #142) is the current PyPI release", `v0.3.1`, 2026-11-27, the #149 record linked, "0.3.0 (`v0.3.0`) was tagged on 2026-11-26" kept, "A clean install of 0.3.1 writes `permits/sources.md` (#142 fixed in 0.3.1)", no "pending the `v0", no "The repository is at 0.3.1", both routes "released, 0.3.1 on PyPI" and none "released, 0.3.0"; the `founder-permits` row "#142 fixed in 0.3.1; 0.3.0 on PyPI lacked it"; the Kiro CLI row keeps "verified on 0.3.0 (walkthrough 2026-11-26, #118)" and adds "on a clean install of 0.3.1 the installer writes the source ledger and `founder-permits` and `founder-cfo` re-run with sourced figures (2026-11-28, #149; #142 fixed)" with no "verified on 0.3.1"; the hosts index: "the current release is `v0.3.1`, published 2026-11-27", the #149 record linked, no "first release that ships"; Vietnamese: "Bản hiện hành trên PyPI là 0.3.1", `v0.3.1`, 27/11/2026, no "đang chờ tag", no "Kho mã đang ở 0.3.1", the permits and Kiro clauses, `#142` exactly twice) and `test_kiro_page_has_the_clean_install_walkthrough_for_19` (the page says `` `v0.3.1` (published 2026-11-27) is the current release `` and no longer says it of `v0.3.0`, links `../evidence/issue-149-release-0-3-1.md`, says "re-run on a clean install of 0.3.1 on 2026-11-28" and "lacked `permits/sources.md` (#142)", no "From the first release that") | `AssertionError: assert '0.3.1 (Wave B, ten skills; ships the source ledger, #142) is the current PyPI release' in '# founder-vn…'` and ``AssertionError: assert '`v0.3.1` (published 2026-11-27) is the current release' in '# Kiro: registering the founder-vn MCP server…'`` (2 failed, 25 passed, `uv run pytest tests/test_front_door.py tests/test_hosts.py -q`, log `.harness/red-149-front-door.log`) | `uv run pytest tests/test_front_door.py tests/test_hosts.py -q`: 27 passed (commit `67218ff`). On the way to green: a first wording of the Kiro page named `founder-cfo` in the paragraph above the step list and broke the test's order check ("founder-pricing reads cfo.md, so founder-cfo runs first"), so the paragraph says "the permits checklist (step 7.1) and the CFO step (step 6.4)" instead; and the README's "Version 0.3.0 was tagged" dropped the `v0.3.0` literal the test wants in the English half, so it reads "Version 0.3.0 (`v0.3.0`) was tagged on 2026-11-26". The README text went through `.harness/README.149.md` and the patch, verified against the whole test module before the operator applied it |

## Cổng ba đoạn

Run at the last code commit `67218ff` (the front-door slice); the commit after it touches only this evidence file. Counts read from `.harness/gate-*.log`; `static` and `build` ran once. `unit` ran twice: the first run was red on stale `.venv` metadata (`tests/test_package.py::test_package_has_single_source_version`, `assert '0.3.0' == '0.3.1'`: the environment had been synced before #163 merged), fixed by `uv sync --frozen --reinstall-package founder-vn` as #117 and #118 recorded, then rerun alone.

```
bash scripts/harness/gate-segment.sh static   # All checks passed!; 326 files already formatted; skill-lint: 10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.1)
bash scripts/harness/gate-segment.sh unit     # 502 passed in 22.73s (after the metadata refresh; first run 1 failed, 501 passed)
bash scripts/harness/gate-segment.sh build    # Successfully built dist/founder_vn-0.3.1.tar.gz and dist/founder_vn-0.3.1-py3-none-any.whl
bash scripts/harness/gate-segment.sh verify
gate-segment verify: latest line per segment (.harness/gate-segments.txt)
  static 0 67218ff8bd2b4d53b352aa1715466eb567735315 2026-11-28T12:30:05Z
  unit 0 67218ff8bd2b4d53b352aa1715466eb567735315 2026-11-28T12:31:14Z
  build 0 67218ff8bd2b4d53b352aa1715466eb567735315 2026-11-28T12:31:22Z
gate-segment verify: GREEN on 67218ff8bd2b4d53b352aa1715466eb567735315
```

## Giới hạn

- The release (tag, Build, approval, PyPI) and the clean install are hand-witnessed from the operator's machine with the operator's `gh` account; no test reaches PyPI or GitHub Actions. The tag push and the approval were run by this lane on the operator's single go-ahead ("go") given after the pre-flight table, not one go-ahead per action.
- The re-run covers `founder-permits` and `founder-cfo` only, on the golden `idea.md`, each in one nested non-interactive session with the Owner's answers written into the prompt. It is not a walkthrough of the ten skills and the front door does not say 0.3.1 is verified end to end; the "verified on 0.3.0 (walkthrough 2026-11-26, #118)" claim stands as the latest full run.
- Two `founder-permits` attempts with `claude-opus-5.5` produced no file within 20 minutes; the file came from `claude-fable-5.1` with the Facilitator's bound on Step 3. The run-time re-check of Step 3 confirmed none of the Công báo pages inside that bound, so `permits.md` says "chưa xác nhận lại hôm nay" on 13 lines; the figures and dates are the ledger's, which the operator verified for #112 and #142. The 20-minute end of attempt 2 has no recorded cause (no final message in the transcript; the Kiro CLI log of that session was not identified).
- The content of `permits.md` and `cfo.md` was not reviewed line by line against `docs/review-checklist.md` beyond the two named checks, the `$` check and the disclaimer count; the outputs stay outside git and are not committed as a second example (design §5, Q56).
- `README.md` was edited by the operator applying the lane's patch, so the slice commit `67218ff` carries an edit this session's guard would have refused through the editor tools; the allocation comment grants the file. The guard's rule 3 does not inspect shell commands, and this lane did not use that gap to write the file.
- `cfo-end` in `times.txt` was written when the lane next polled (10:50:42Z); `cfo.md`'s modification time (10:48Z) is the closer end mark.

## Giải quyết review nội bộ

The implement skill's own review step, run by the lane over the diff `main..lane/issue-149` before opening the pull request (the harness dispatches the two independent review turns after it):

- Standards: the slice commit touches three docs and two test files, no `src/`; `ruff` and `skill_lint` green in the `static` segment; identifiers English, Owner-facing text none (the README's Vietnamese section is Facilitator-facing and carries no `$`). No finding.
- Spec: the four criteria of #149 are ticked above with the command and result each; the front door claims only what ran (the re-run, not a walkthrough). One question was weighed and settled here: whether the Kiro CLI row should say "verified on 0.3.1". It does not, because design §5 reserves "verified" for a witnessed host run of the pipeline, and the ticket's step 4 asks for two skills. No finding.
