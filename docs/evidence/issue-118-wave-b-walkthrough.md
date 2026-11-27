# Evidence: issue #118 release 0.3.0 and Wave B clean-install walkthrough on Kiro CLI

Lane run by the project owner on Kiro CLI through `founder-guarded`, with `HARNESS_SINGLE_OWNER_FILES=README.md` exported in the session (the ticket is `ready-for-human`; the dispatcher skips it). The operator's allocation comment on #118 (2026-11-26T07:17:12Z) grants `README.md`, lane branch `lane/issue-118`, target `main`. The machine half #117 (T24) merged as `ca6bc9f` (PR #139): `__version__` and the ten `metadata.version` values are 0.3.0.

This file is the record that criterion 3 of #118 names, `docs/evidence/issue-<this>-wave-b-walkthrough.md`. The template #117 created as `docs/evidence/issue-#118-wave-b-walkthrough.md` is replaced by it in the slice that fills the record: the reviewer prompts, `docs/agents/evidence-gates.md` and the dispatcher look for `docs/evidence/issue-<n>-*.md`, which a `#` in the name does not match.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

1. **Clean install from the wheel, then from PyPI**: `uvx --no-cache --from <source> founder-vn --version`, `… founder-vn install --host kiro` and `… founder-vn-mcp` answering `initialize` with `serverInfo.version` `0.3.0`, in an empty folder, first with the local 0.3.0 wheel and after the `v0.3.0` release with `founder-vn` from PyPI (criterion 2). Witnessed by hand on the operator's machine; no test reaches PyPI or GitHub Actions.
2. **Protocol step 1 of a Wave B skill inside a Kiro CLI session** (`server_info` against `metadata.version` set to `1.0.0`): the only place the major-mismatch stop can be observed (criterion 4). No automated seam (spec #1: skills have no automated seam).
3. **The ten skills end to end on Kiro CLI**: Wave A, then `founder-permits`, `founder-ops`, `founder-marketing`, `founder-launch`, `founder-plan` again and `founder-vn plan --check` exit 0 (criterion 3). No automated seam; the shape of this record is pinned by a test in `tests/test_hosts.py` that replaces `test_issue_118_template_has_unticked_boxes_and_claims_no_run`.
4. **`README.md` truth table and `docs/hosts/README.md`**: asserted by `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (criterion 5).
5. **`docs/hosts/kiro.md` walkthrough section**: it says the #118 walkthrough is pending and links the template; asserted by `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19` (inferred from criterion 5: a host page that still says pending after the run would contradict the README).
6. **The tracker**: every friction or defect as an issue naming the skill or tool (criterion 6), not code.

## Acceptance criteria of #118

Copied from the ticket; the first is the allocation comment.

- [x] Allocation comment written by the operator on #118 (`<!-- harness:allocation -->`, `singleOwnerFiles: README.md`, `laneBranch: lane/issue-118`): comment of 2026-11-26T07:17:12Z.
- [x] Dry run on the local 0.3.0 wheel in an empty folder (install, MCP `initialize`), then tag `v0.3.0` on the merge commit of the machine half, `release.yml` Build green, `Publish to PyPI` approved by the operator on environment `pypi`, `uvx --no-cache --from founder-vn founder-vn --version` gives `founder-vn 0.3.0`: release record below.
- [x] Clean-install walkthrough on Kiro CLI following `docs/hosts/kiro.md` (Wave A, then permits, ops, marketing, launch, plan recompile, `plan --check` exit 0), recorded in this file: record below, with the deviations it names.
- [x] The deliberate major mismatch still stops a skill (one Wave B skill set to `1.0.0`, run, stop message quoted, restored): observed on 0.3.0 on 2026-11-27: `founder-launch` at `1.0.0` stopped at Protocol step 1 after `server_info` answered 0.3.0, in a nested non-interactive Kiro CLI session this lane started from the walkthrough folder, and the file was restored byte-identical ("Major-mismatch check" below). The 2026-11-26 session had not run it.
- [x] README says 0.3.0 is released (tag date) and the Kiro CLI host row says the full pipeline including Wave B is verified on 0.3.0 (walkthrough date, #118); `docs/hosts/README.md` likewise; `tests/test_front_door.py` updated: slices `eb4e2ed` and `eb8585d`, with known defect #142 named next to the claim (operator's decision).
- [x] Every friction or defect filed as an issue naming the skill or tool; blocking defects fixed (0.3.1) or filed before closing: #142, #143, #144 from the walkthrough and #148 from the major-mismatch check (all `needs-triage`); #142 is blocking for verified legal figures and is filed, not fixed (operator's decision).
- [ ] PR from `lane/issue-118` with `Closes #118` through `scripts/harness/open-lane-pr.sh`: the pull request is opened after this record is committed.

## Release record (criterion 2)

Done on 2026-11-26 from the operator's machine (macOS, uv 0.11.24); times UTC. The MCP `initialize` check is a scratch helper under `.harness/` (git-ignored): it sends `initialize` with protocol `2025-06-18` over stdio, reads the first response line, sends `notifications/initialized` and closes stdin.

| Step | Command or measurement | Result |
| --- | --- | --- |
| Commit to tag | `gh api repos/NHAN-AI-VN/founder-vn/pulls/139`; `git rev-parse <sha>^{tree}` for the merge commit and the pull request head | merge commit `ca6bc9f`, merged 2026-11-26T06:58:59Z; its tree `4766b11` equals the tree of the head `f68b73c`, whose `Gate` run 45771836554 concluded success (the merger's push to `main` starts no run) |
| Build | `uv build` at `ca6bc9f` | `founder_vn-0.3.0-py3-none-any.whl` sha256 `6c9628c9623cae47…`, `founder_vn-0.3.0.tar.gz` sha256 `6ab79f449993adf7…` |
| Dry run on the local wheel, empty folder (07:25:54Z) | `uvx --no-cache --from <repo>/dist/founder_vn-0.3.0-py3-none-any.whl founder-vn --version`; `… founder-vn install --host kiro`; MCP `initialize` to `… founder-vn-mcp` | `founder-vn 0.3.0`; 13 `create` lines: twelve skill files in ten skill folders and `.kiro/settings/mcp.json` with `["--from", "founder-vn", "founder-vn-mcp"]`; `grep -h -E '^ +version:' .kiro/skills/*/SKILL.md \| sort \| uniq -c` gives `10   version: "0.3.0"`; `serverInfo {"name": "founder-vn", "version": "0.3.0"}`, protocol `2025-06-18`, stderr empty, exit 0 |
| PyPI before the tag | `curl -s https://pypi.org/pypi/founder-vn/json` | `version 0.2.0`; releases `0.2.0` only |
| Tag (07:32:50Z) | `git tag -a v0.3.0 ca6bc9f -m "founder-vn 0.3.0" && git push origin v0.3.0`, after the operator's go-ahead in the session | tag object `23e0bb2` pointing at `ca6bc9f` |
| Release run 45776129259 | `gh api repos/NHAN-AI-VN/founder-vn/actions/runs/45776129259/jobs` | `Build` success, 07:32:54Z to 07:33:03Z (tag equals `v0.3.0`, `uv build`, artefact uploaded); `Publish to PyPI` waiting on environment `pypi`, required reviewer `nhannguyen89` |
| Approval (07:34:54Z) | `gh api --method POST repos/NHAN-AI-VN/founder-vn/actions/runs/45776129259/pending_deployments` with `state=approved`, run by the lane with the operator's `gh` account on the operator's instruction in the session ("approve theo đề xuất") | `Publish to PyPI` success, 07:34:55Z to 07:35:12Z |
| On PyPI | `curl -s https://pypi.org/pypi/founder-vn/0.3.0/json` | `founder_vn-0.3.0-py3-none-any.whl` sha256 `6c9628c9623cae47…` uploaded 07:35:08Z and `founder_vn-0.3.0.tar.gz` sha256 `6ab79f449993adf7…` uploaded 07:35:09Z: byte-identical to the build of the dry run; the project JSON gave `version 0.3.0` at 07:35:53Z |
| From PyPI, empty folder (07:36:00Z) | `uvx --no-cache --from founder-vn founder-vn --version`; `uvx --no-cache --from founder-vn founder-vn install --host kiro`; MCP `initialize` to `uvx --no-cache --from founder-vn founder-vn-mcp` | `founder-vn 0.3.0`; the same 13 `create` lines; `10   version: "0.3.0"`; `serverInfo {"name": "founder-vn", "version": "0.3.0"}`, protocol `2025-06-18`, stderr empty, exit 0 |

## Record (criterion 3)

Operator: the project owner, acting as Facilitator and as Owner. Host: Kiro CLI 2.37.1 on macOS, in the folder `~/Documents/Research/founder-walkthrough-118`, outside every git tree (`git rev-parse --show-toplevel` fails in it and in its parent). The session's model, named by the operator: `claude-opus-5.5` (only the name is recorded). Package: `founder-vn` 0.3.0 from PyPI. Panel and board model: `gemini-3.5-flash-lite`, recorded by `founder/board/board.json` and `founder/panel/results.json` with a `prompt_hash`; n = 20 buyers; the three board lenses. Date: 2026-11-26; times are local (UTC+7).

The operator kept no stopwatch: `started` and `duration` are read from the modification times of the files each step wrote (`stat -f '%Sm'` in the walkthrough folder), so a step's duration includes the Owner's own work and any break between the previous file and its own. Asked afterwards for friction the files would not show and about the three long gaps (steps 7.2 and 7.4 and the extra row), the operator answered "ok" and named none; the gaps are recorded as measured, with no cause. Asked whether they had requested `offer.md` and `brand.md` and whether `founder-plan` ran after Wave A, the operator answered "yes".

| step | command | started | duration | friction | issue filed |
|---|---|---|---|---|---|
| 1 | `mkdir founder-walkthrough-118 && cd founder-walkthrough-118` (under `~/Documents/Research`) | before 14:42 | no file trace | none | |
| 2 | `uvx --from founder-vn founder-vn install --host kiro` | 14:42 | seconds: the ten skill folders and `.kiro/settings/mcp.json` all written at 14:42:20 | none; the registration is written by the installer (Q54), the hand-made file of #19 (#94) is gone | |
| 3 | check `.kiro/settings/mcp.json` | 14:42 | written by step 2 | none | |
| 4 | export the three `FOUNDER_LLM_*` names in the shell that starts Kiro CLI | before the session | no file trace | none reported; the MCP server inherited the variables (the board and the panel ran) | |
| 5 | `mkdir founder && cp …/examples/barbershop/founder/idea.md founder/`; `kiro-cli chat` | 14:44 (`idea.md` 14:44:34) | | the golden idea, byte-identical to `examples/barbershop/founder/idea.md` (see limits) | |
| 6.1 | `founder-board` | after 14:44 | 34 min to `board.md` 15:18:41; `board/brief.md` 15:10:52, `board_run` from 15:11:10 to 15:11:15 (5 s for three lenses) | none reported | |
| 6.2 | `founder-competitors` | 15:18 | 37 min to `competitors.md` 15:55:36, most of it the Owner's desk survey (filled form 15:54:00, two price-board images 15:44:55); the skill's own output took about 2 min | a new desk survey by the Owner, not the golden form | |
| 6.3 | `founder-consumer` | 15:56 | 11 min to `consumer.md` 16:06:25: `customer.json` 15:58:43; first panel, n = 20, from 16:00:22 to 16:01:27 (three jobs: one buyer answered on the retry); the Owner changed the pitch; the session set the first run aside as `panel-lan-1/`, `pitch-lan-1.md` and `consumer-lan-1.md` (16:04:29); second panel from 16:04:42 to 16:05:19 (one job, 20 answers in 22 s) | without the set-aside, `panel init` would have kept the first run's answers and the second run would have asked nobody | #143 |
| 6.4 | `founder-cfo` | 16:06 | 16 min; `numbers.json` 16:20:25, `cfo.md` 16:22:22 | no `permits/sources.md` in the project. At the Owner's request ("đặt giả định và tiếp tục") the session set the cost inputs as its own assumptions, labelled as such in `cfo.md`; it took the tax rate from the model's memory (marked "chưa kiểm chứng") and the threshold from a provincial tax office's PDF summary; no "Giới hạn của phần thuế" section | #142 |
| 6.5 | `founder-pricing` | 16:22 | 19 min; `pricing_input.json` 16:35:01, `pricing.md` 16:41:15 | repeats the unverified tax rate without a Công báo link | #142 |
| 6.6 | `founder-plan` | after 16:41 | no file trace: the run of step 7.5 overwrote `business-plan.md` and `summary.md`; the operator confirms it ran | none reported | |
| 7.1 | `founder-permits` | after 16:41 | 22 min to `permits.md` 17:03:10 (includes step 6.6) | no ledger: every figure and date is "chưa có nguồn đã kiểm chứng", and the file tells the Facilitator to put `permits/sources.md` into the project; the "ngành có điều kiện" line has no verification date | #142 |
| 7.2 | `founder-ops` | 17:03 | 1 h 50 min to `ops.md` 18:53:25 | none reported; the gap has no recorded cause | |
| 7.3 | `founder-marketing` | 18:53 | 12 min to `marketing.md` 19:05:24 | none reported | |
| 7.4 | `founder-launch` | 19:05 | 1 h 8 min to `launch.md` 20:13:11 | none reported; the gap has no recorded cause | |
| extra | `founder-offer` and `founder-brand`, at the Owner's request (not in the script) | 20:13 | 59 min to `brand.md` 21:12:25 and `offer.md` 21:13:24 | 0.3.0 ships neither skill: the session fetched the English upstream skills from `github.com/Jakeschincariol/founder-skill` (commit `fd9385b`) and adapted them; each file says so in its first lines | #144 |
| 7.5 | `founder-plan` again | 21:13 | `summary.md` 21:13:37, `business-plan.md` 21:13:43 | the plan compiles offer and brand as sections ("Đề xuất giá trị", "Thương hiệu"), so it has no `## Chưa làm` list; verdict `Not yet (chưa lãi)` printed by `plan_compile` | #144 |
| 7.6 | `uvx --from founder-vn founder-vn plan --check; echo $?` | after 21:13 | no file trace (check mode writes nothing) | none reported | |
| 8 | confirm `founder/business-plan.md` and `plan --check` exit 0 | repeated by this lane after the run | | `founder-vn 0.3.0`; `business-plan.md khớp với các file hiện có`; `exit=0`; `business-plan.md` kept its 21:13:43 time | |
| 9 | deliberate major mismatch on a Wave B skill: `sed -i '' 's/version: "0.3.0"/version: "1.0.0"/' .kiro/skills/founder-launch/SKILL.md`; `kiro-cli chat --no-interactive --trust-workspace --trust-all-tools --model claude-opus-5.5 "founder-launch"` in the walkthrough folder; the reverse `sed` to restore | 2026-11-27 13:36 (not in the 2026-11-26 session: the operator skipped it then) | 8 min to the restored `SKILL.md` (13:44:38) | the skill stopped at Protocol step 1 once its tools could run (quoted below). A first attempt with `--trust-tools=fs_read,@founder-vn/server_info` had every approval-needing tool denied, `server_info` included: Kiro CLI 2.37.1 `--trust-tools` does not take the `@server/tool` form (a Kiro CLI limit, not a founder-vn skill or tool; no issue). The stop message came in English | #148 |

Elapsed from the install to the final plan: 14:42 to 21:13, 6 h 31 min of wall-clock time. The three long gaps (steps 7.2 and 7.4 and the extra row) make 3 h 57 min of it and have no recorded cause. Design §7 budgets about four hours per pilot participant, two meetings included.

Deviations from the script of `docs/hosts/kiro.md`: the golden idea instead of a new case; the panel ran twice after a pitch change; the CFO inputs are the session's assumptions at the Owner's request, not the Owner's figures; `offer.md` and `brand.md` were added at the Owner's request; step 9 did not run in that session and ran on 2026-11-27 in nested non-interactive sessions started by this lane (row 9), not by the operator at the keyboard.

## Review-checklist walk on the walkthrough outputs

Run by this lane on 2026-11-26 over the walkthrough's `founder/` folder (outside git; nothing from it is committed) with a scratch runner under `.harness/` that applies the checks of `tests/test_wave_a_checklist.py` and the six check functions of `tests/test_wave_b_checklist.py` to that folder. Only file names and the kind of failure are recorded.

| Check (`docs/review-checklist.md`) | Result |
| --- | --- |
| No `$` next to a digit | none in any `.md` |
| No English leaks (the stoplist of `tests/test_wave_a_checklist.py`, lines without a link) | no hit in any `.md`, `offer.md` and `brand.md` included |
| Disclaimer "không phải tư vấn" | present in `cfo.md`, `pricing.md`, `summary.md`, `business-plan.md` and in the four Wave B files |
| Panel caveat "mô phỏng, cận trên, không phải khách hàng thật" | present in `panel/results.md`, `consumer.md`, `pricing.md`, `summary.md`, `business-plan.md`, `marketing.md`, `launch.md` |
| Wave A and Wave B files present | all twelve Wave A artefacts and `permits.md`, `ops.md`, `marketing.md`, `launch.md` |
| Legal claims carry a Công báo link and a date | fails on `cfo.md`, `pricing.md` and `summary.md`: their tax figures carry no Công báo link (#142) |
| Every Công báo link in `permits.md` carries a verification date | fails on the "ngành có điều kiện" line (#142) |
| The plan lists exactly the two after-pilot lines | does not apply: `offer.md` and `brand.md` exist, so the plan has no `## Chưa làm` (#144) |
| Model recorded | `board/board.json` and both `results.json`: `gemini-3.5-flash-lite` with a `prompt_hash`; n = 20, the same seed in both runs, different prompt hashes |
| Installed skills | the ten installed `SKILL.md` files are byte-identical to `skills/*/SKILL.md` at `ca6bc9f`; `10   version: "0.3.0"` |

## Major-mismatch check (criterion 4)

Run on 2026-11-27 by this lane from the walkthrough folder `~/Documents/Research/founder-walkthrough-118` (outside git), after the operator answered the review question of `reviews/issue-118/spec.md` (SPEC-1) by choosing to run the check rather than defer it. The operator had skipped it in the 2026-11-26 session ("bỏ qua"). Host: Kiro CLI 2.37.1, the same binary as the walkthrough, started by the lane as a nested non-interactive session with `--model claude-opus-5.5` (the walkthrough's model; only the name is recorded). Package: `founder-vn` 0.3.0 from PyPI through the installed `.kiro/settings/mcp.json`. Times are local (UTC+7), from `date -u` lines the lane wrote to `.harness/criterion4-times.txt` (git-ignored) and from file modification times.

| Step | Command or measurement | Result |
| --- | --- | --- |
| Before (13:35) | `shasum -a 256` on the installed `.kiro/skills/founder-launch/SKILL.md` and the repository's `skills/founder-launch/SKILL.md`; `cp -a founder/` to a sibling folder outside git as a backup; `stat` of every file under `founder/` to a list | both files `e8908d4ec871…`; `founder/` holds 86 files (modes `-rw-r--r--`, folders `drwxr-xr-x`); the skill file still carries its install time 14:42:20 of 2026-11-26 |
| Set `1.0.0` (13:36:10) | `sed -i '' 's/version: "0.3.0"/version: "1.0.0"/' .kiro/skills/founder-launch/SKILL.md` | `grep -h -E '^ +version:' .kiro/skills/*/SKILL.md \| sort \| uniq -c` gives `9 version: "0.3.0"` and `1 version: "1.0.0"` |
| Run 1 (13:36:28 to 13:40:48) | `kiro-cli chat --no-interactive --trust-workspace --trust-tools=fs_read,@founder-vn/server_info --model claude-opus-5.5 "founder-launch"` | not an observation of the version check: Kiro CLI denied every tool that needs approval, `@founder-vn/server_info`, `founder-vn --version` and `web_fetch` included ("tool permission approval is not supported in non-interactive mode"), because `--trust-tools` does not take the `@server/tool` form in 2.37.1. The session still stopped at step 1, in Vietnamese, inferring the mismatch from the files it could read ("Em dừng ở bước 1 của `founder-launch`, bước kiểm tra phiên bản. … Không kiểm tra được phiên bản."), and wrote nothing |
| Run 2 (13:42:22 to 13:43:29) | `chmod -R a-w founder` and `chmod a-w` on the edited skill file first, the lane's own lock against a write (`--trust-all-tools` trusts `fs_write` too); then `kiro-cli chat --no-interactive --trust-workspace --trust-all-tools --model claude-opus-5.5 "founder-launch"` | the session read the skill, called `@founder-vn/server_info`, ran `command -v founder-vn; founder-vn --version` (no `founder-vn` on PATH: the package runs through `uvx`), and stopped at step 1; the stop message is quoted below; exit 0 |
| Restore (13:44:38) | `chmod -R u+w founder`; `chmod u+w` and `sed -i '' 's/version: "1.0.0"/version: "0.3.0"/'` on the skill file | sha256 `e8908d4ec871…` again, equal to `skills/founder-launch/SKILL.md` at `ca6bc9f`; `10 version: "0.3.0"`; mode `-rw-r--r--` |
| Case folder after | `diff -rq founder/ <backup>`; `stat` of the 86 files against the list taken before; modes | identical content, identical modification times, modes as before; the backup was then deleted. Kiro CLI had created an empty `.kiro/agents/` in the folder on launch; removed |

Run 2, the stop message as the nested Kiro CLI session wrote it (its whole response; the `[tool]` lines of the transcript are left out):

> I stopped at the skill's first step, the version check. The skill's rules say to stop when the major versions differ, and here they do:
>
> - The founder-launch skill is version 1.0.0.
> - The founder-vn MCP server reports `founder-vn 0.3.0`.
> - There's no `founder-vn` command on your system to check instead (`command not found`).
>
> To continue, either upgrade the founder-vn package the MCP server runs to a 1.x release, or install the founder-launch skill version made for 0.x. The skill comes from github.com/Jakeschincariol/founder-skill (commit fd9385b). This project has no README with the install command.
>
> Two things will affect the next run:
>
> - `founder/launch.md` already exists, written Nov 26 at 13:13. The skill will first show the Owner what's in it and ask what to change.
> - Every file in `founder/` is read-only (`-r--r--r--`), `launch.md` included. The skill can't save a new version until you make it writable again.
>
> I haven't changed any files. Tell me when the versions match and I'll run founder-launch again.

What this shows: with the installed package at 0.3.0 and the skill at 1.0.0, Protocol step 1 of `founder-launch` read the version through `server_info`, saw the major mismatch and stopped before Step 0 without writing a file (design Q45). Friction: the message is in English where the #19 stop on 0.2.0 was in Vietnamese; filed as #148. In the message, "Nov 26 at 13:13" is the UTC form of `launch.md`'s 20:13 local time, and the read-only files were the lane's lock, not the skill's doing.

Text identity, as before: the shared `## Protocol` block (from its heading to the next `## ` heading) has the same sha256 (prefix `9b27c1dd8629`) in all ten `skills/*/SKILL.md` and in `skills/founder-board/SKILL.md` at `v0.2.0`, the block whose stop the #19 walkthrough observed on 0.2.0.

## Issues filed (criterion 6)

- #142 (`founder-permits`, `founder-cfo`, `founder-plan`, `founder-vn install`): a clean install has no `permits/sources.md`, so no legal figure can be sourced. Blocking for verified legal figures; filed, not fixed, by the operator's decision of 2026-11-26 (close #118 with the README naming the defect).
- #143 (`panel init`, `panel run`; MCP `panel_init`, `panel_run`): a new panel keeps the previous panel's answers. Reproduction in the issue: after a second `panel init` with another pitch and seed, `founder-vn panel check` lists only the buyers that never answered.
- #144 (`founder-plan`, `plan_compile`): the plan's "Chưa làm" lines tell the Owner to run `founder-offer` and `founder-brand`, which 0.3.0 does not ship.
- #148 (the shared `## Protocol` block of the ten skills, observed on `founder-launch`): the Protocol step 1 stop on a major mismatch came in English in the criterion-4 run of 2026-11-27; the #19 stop on 0.2.0 came in Vietnamese. The block fixes the condition and the addressee, not the language.

All four carry `needs-triage` and a list of options for the operator to choose from.

## Lát

| Test | Assertion line while red | Green rerun |
| --- | --- | --- |
| `test_readme_truth_table_is_honest_about_release_status_and_hosts` and `test_readme_names_purpose_audience_hosts_and_both_install_routes` (Install: 0.3.0 is the current PyPI release, `v0.3.0` tagged 2026-11-26; 0.2.0 was the first; both routes "released, 0.3.0 on PyPI"; no "pending the `v0…` tag"; still no "verified on 0.3.0"; Vietnamese "Bản hiện hành trên PyPI là 0.3.0", `v0.3.0`, 26/11/2026, no "đang chờ tag") | `AssertionError: released, 0.3.0 on PyPI` and `assert '0.3.0 (Wave B, ten skills) is the current PyPI release' in '# founder-vn…'` (2 failed, 10 passed) | `uv run pytest tests/test_front_door.py -q`: 12 passed (commit `eb4e2ed`) |
| `test_kiro_page_has_the_clean_install_walkthrough_for_19` (the page says `` `v0.3.0` (published 2026-11-26) is the current release ``, links `../evidence/issue-118-wave-b-walkthrough.md`, has no `issue-#118` and no "pending" in its walkthrough section, and names 2026-11-26, #118 and #142) | ``AssertionError: assert '`v0.3.0` (published 2026-11-26) is the current release' in '# Kiro: registering the founder-vn MCP server…'`` (1 failed, 11 deselected) | `uv run pytest tests/test_hosts.py -q`: 12 passed (commit `5fa7c1f`) |
| `test_readme_truth_table_is_honest_about_release_status_and_hosts` (Kiro CLI row "full pipeline incl. Wave B verified on 0.3.0 (walkthrough 2026-11-26, #118)" with #142 and the 0.2.0 history; the `founder-permits` row names #142; no "has not run yet" and no "pending walkthrough"; the host index Kiro row "verified end to end on 0.3.0 incl. Wave B (walkthrough 2026-11-26, #118" with #142 and #19, and the index links this record; Vietnamese "đã xác nhận trên 0.3.0 (walkthrough 26/11/2026, #118)" and #142 twice) | `AssertionError: assert ('has not run yet' not in '# founder-v…')`, on "0.3.0 has not run yet (#118)" (1 failed, 11 passed) | `uv run pytest tests/test_front_door.py tests/test_hosts.py -q`: 24 passed (commit `eb8585d`). On the way to green, the new assertion `"pending" not in hosts_index` was narrowed to `"pending walkthrough"`, because the Gemini row of the index says "pending confirmation" by design |
| `test_issue_118_evidence_records_the_kiro_cli_run` (replaces `test_issue_118_template_has_unticked_boxes_and_claims_no_run`: the `issue-#118` template is gone; this file has the seven criteria with 1, 2, 3, 5 and 6 ticked and criterion 4 open as "skipped by the operator"; at least 15 numbered record rows; the PyPI version command, `founder-vn 0.3.0`, `founder/business-plan.md`, `plan --check`, both model names, #142, #143, #144, `## Giới hạn`; no template wording, no secret) | `AssertionError: the template is replaced` / `assert not True` (1 failed, 11 deselected) | `uv run pytest tests/test_hosts.py -q`: 12 passed (commit `2d5a447`) |

## Cổng ba đoạn

Run at the last code commit `2d5a447` (the record slice); the commit after it touches only this evidence file. Counts read from `.harness/gate-*.log`. The first `unit` run was red, 1 failed and 463 passed: `tests/test_package.py::test_package_has_single_source_version` read `'0.2.0' == '0.3.0'` because the local `.venv` still carried the installed metadata of 0.2.0. `uv sync --frozen --reinstall-package founder-vn` refreshed it (`- founder-vn==0.2.0`, `+ founder-vn==0.3.0`), the same refresh #117 recorded, and `unit` was rerun alone.

```
bash scripts/harness/gate-segment.sh static   # All checks passed!; 304 files already formatted; skill-lint: 10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.0)
bash scripts/harness/gate-segment.sh unit     # 464 passed in 22.08s
bash scripts/harness/gate-segment.sh build    # Successfully built dist/founder_vn-0.3.0.tar.gz and dist/founder_vn-0.3.0-py3-none-any.whl
bash scripts/harness/gate-segment.sh verify
gate-segment verify: latest line per segment (.harness/gate-segments.txt)
  static 0 2d5a447dcd417e842b318cd3b4513f040e828dc4 2026-11-27T04:40:49Z
  unit 0 2d5a447dcd417e842b318cd3b4513f040e828dc4 2026-11-27T04:42:06Z
  build 0 2d5a447dcd417e842b318cd3b4513f040e828dc4 2026-11-27T04:42:14Z
gate-segment verify: GREEN on 2d5a447dcd417e842b318cd3b4513f040e828dc4
```

## Giới hạn

- Times are reconstructed from file modification times, not measured with a stopwatch. Steps 1, 4, 6.6 and 7.6 leave no file and have no time. The operator, asked about friction the files would not show, answered "ok": three gaps of 1 h 50 min, 1 h 8 min and 59 min have no recorded cause.
- The idea file was the golden `idea.md`, so the ticket's "or a pilot participant's case" was not exercised. The survey, the two panels (20 personas each, the same seed), the CFO inputs and every report were produced in the session. The CFO inputs are the session's assumptions at the Owner's request, not the Owner's figures, so the verdict `Not yet (chưa lãi)` says nothing about the golden case or any real shop.
- Criterion 4 was observed in a nested, non-interactive Kiro CLI session that this lane started from the walkthrough folder with `--trust-all-tools` and `--model claude-opus-5.5`, on 2026-11-27, not in the operator's interactive session of 2026-11-26 and not with the operator at the keyboard. The lane read the transcript Kiro CLI printed, not the model's reasoning. The write lock on `founder/` during run 2 was the lane's, so the record cannot say whether the session would have written anything had the files been writable; it said it had not, and the folder was unchanged. Run 1 is not a version-check observation: its tools were denied.
- After the restore, `founder-launch` was not run again (`docs/hosts/kiro.md` step 9 says "confirm the skill runs again"): a full run would rewrite `founder/launch.md` and the record's times. The restore is shown byte-identical to the file that ran in step 7.4 instead.
- #142 is blocking for verified legal figures on a clean install. By the operator's decision it is filed, not fixed, and the README names it next to the "verified" claim; the tax figures in the walkthrough's `cfo.md`, `pricing.md` and `summary.md` are unverified.
- The walkthrough's plan holds two sections, "Đề xuất giá trị" and "Thương hiệu", from files that no founder-vn 0.3.0 skill writes, made at the Owner's request (#144). The Wave B check of the two after-pilot lines could not apply.
- One host. Claude Code, Codex, Gemini / Antigravity CLI, Grok Build and KiroCrew stay "not yet verified".
- The Kiro CLI session's model is recorded as the operator named it (`claude-opus-5.5`); the criterion-4 sessions used the same name through `--model`. This lane read no host configuration and did not observe the walkthrough session: what the skills did on 2026-11-26 is read from the files the session wrote and from what those files say about themselves.
- The walkthrough folder stays outside git. This record quotes no case content beyond what the golden example already publishes: no competitor names, no prices, no persona text, no Owner inputs.
- The tag push and the approval of `Publish to PyPI` were run by this lane with the operator's `gh` account, each on the operator's instruction in the session. No test reaches PyPI or GitHub Actions. The two dry-run folders were inside the repository's git-ignored `.harness/`, not outside every git tree; the installer writes relative to the current folder, so the repository's own `.kiro/` was not touched.
- The README slices: `HARNESS_SINGLE_OWNER_FILES=README.md` was exported in this Kiro CLI session, so `.kiro/hooks/guard.sh` let the lane edit `README.md`. #5 and #19 had to apply a hand patch instead.

## Giải quyết review nội bộ

No self-review was run (lane rule: review is two independent turns after the pull request opens).
