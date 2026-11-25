# Evidence: issue #19 Wave A clean-install walkthrough on Kiro CLI

Lane run by the project owner (the ticket is `ready-for-human`; the dispatcher skips it). The operator's allocation comment on #19 (2026-11-25T05:08:45Z) grants `README.md`, lane branch `lane/issue-19`, target `main`. The machine-doable half of T18 was split out to #89 (T18a, PR #90, merged 2026-11-24); this lane records the human half: the walkthrough on a real Kiro CLI, the tag and the PyPI release, the README truth table, the known-issues list.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `uvx --from founder-vn founder-vn install` for the Kiro host, run from PyPI in an empty folder, and `uvx --from founder-vn founder-vn-mcp` answering `initialize` with `serverInfo.version` `0.2.0`: the clean-install route a Facilitator uses (criteria 1 and 2). Witnessed by hand on the operator's machine; no test reaches PyPI.
- Protocol step 1 of the six skills (`server_info` against `metadata.version`) inside a Kiro CLI session: the only place "a deliberate major mismatch stops the skill with the expected message" can be observed (criterion 2). No automated seam (spec #1: skills have no automated seam).
- `README.md` truth table (Install, Status, Host) and `docs/hosts/README.md`: asserted by `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` (criterion 3). The one red-then-green slice of this lane.
- The tracker: known issues of Wave B as GitHub issues (criterion 4), not code.

## Acceptance criteria of #19

- [x] Clean-install walkthrough executed on Kiro CLI and recorded (commands, time taken, friction); blocking defects fixed or filed. Record below; no blocking defect; three frictions filed as #93, #94, #95 and one documentation order fixed in this lane.
- [x] `v0.2.0` tagged and on PyPI; every skill carries `metadata.version` 0.2.0; the version check passes; a deliberate major mismatch stops the skill with the expected message. Release record and step 8 below.
- [x] README status table: Kiro CLI full pipeline verified; other hosts marked not yet verified. `README.md` host table, Vietnamese section and `docs/hosts/README.md`, pinned by `tests/test_front_door.py`.
- [x] Known-issues list for Wave B opened as issues: #93 (`founder-consumer` writes no `consumer.md`), #94 (installer prints `mcp.json`, writes nothing), #95 (`panel tally` `results.md` has no disclaimer line).

## Release record (criterion 2)

Done by the operator on 2026-11-24 after #89 (T18a, PR #90) merged as `212f609`; the lane of #89 bumped `__version__` and the six `metadata.version` to 0.2.0 and `scripts/skill_lint.py` keeps them equal.

| Step | Command or measurement | Result |
| --- | --- | --- |
| Dry run on the local wheel, empty folder | `uv build`; `uvx --no-cache --from ../../dist/founder_vn-0.2.0-py3-none-any.whl founder-vn --version`; `… founder-vn install --host kiro`; MCP `initialize` over stdio | `founder-vn 0.2.0`; six skills copied, `mcp.json` snippet printed with `["--from", "founder-vn", "founder-vn-mcp"]`; `serverInfo {"name": "founder-vn", "version": "0.2.0"}`, protocol `2025-06-18`, stderr empty |
| PyPI name free | `curl -s -o /dev/null -w '%{http_code}' https://pypi.org/pypi/founder-vn/json` | `404` before the release |
| Pending publisher | configured by the operator on pypi.org: project `founder-vn`, owner `NHAN-AI-VN`, repository `founder-vn`, workflow `release.yml`, environment `pypi` (H-6 of `docs/agents/kiro-harness.md`) | done 2026-11-24 |
| GitHub environment `pypi` | `gh api -X PUT repos/NHAN-AI-VN/founder-vn/environments/pypi` with the operator as required reviewer | job `Publish to PyPI` waits for the operator's approval; the publish is the one irreversible step |
| Tag | `git tag -a v0.2.0 212f609 && git push origin v0.2.0` (2026-11-24T08:14Z) | run 45354393229: `Build` success (tag equals `v0.2.0`, `uv build`), `Publish to PyPI` waiting → approved via `pending_deployments` → success |
| On PyPI | `curl -s https://pypi.org/pypi/founder-vn/json` | `version 0.2.0`, files `founder_vn-0.2.0-py3-none-any.whl`, `founder_vn-0.2.0.tar.gz` |
| From PyPI, empty folder | `uvx --no-cache --from founder-vn founder-vn --version`; `uvx --from founder-vn founder-vn install --host kiro`; `uvx --from founder-vn founder-vn-mcp` + `initialize` | `founder-vn 0.2.0`; six skills copied; `serverInfo` version `0.2.0`, stderr empty |
| Installed skills in lockstep | `grep -h 'version:' .kiro/skills/*/SKILL.md \| sort \| uniq -c` in the walkthrough folder | `6   version: "0.2.0"` |

## Record (criterion 1)

Operator: the project owner, acting as Facilitator and as Owner. Host: Kiro CLI 2.37.1 on macOS, in an empty folder outside every git tree; the session's model, named by the operator, `opus 5.5` (only the name is recorded). Package: `founder-vn` 0.2.0 from PyPI. Panel and board model: `gemini-3.5-flash-lite` (recorded by `founder/panel/results.json` and `founder/board/board.json`; n = 20 buyers; the three board lenses). Date: 2026-11-25, times are local (UTC+7). The operator did not keep a stopwatch: `started` and `duration` are read from the modification times of the files each step wrote (`stat -f '%Sm'` in the walkthrough folder), so a step's duration includes the Owner's own thinking and typing between the previous file and its own. Asked afterwards for friction the files would not show (download waits, repeated tool-permission prompts, unclear wording), the operator reported none.

| step | command | started | duration | friction | issue filed |
|---|---|---|---|---|---|
| 1 | `mkdir founder-walkthrough && cd founder-walkthrough` | before 09:22 | no file trace | none | |
| 2 | `uvx --from founder-vn founder-vn install --host kiro` | 09:22 | seconds (all six skills written at 09:22:26) | first `uvx` run downloads the package and 31 dependencies | |
| 3 | create `.kiro/settings/mcp.json` by hand from the printed snippet | 09:40 (file written 09:40:19) | shares the 18 minutes after step 2 with step 4 | the installer prints the snippet and writes nothing; the folder and file are made by hand | #94 |
| 4 | export the three `FOUNDER_LLM_*` names in the shell; `test -n` on each | between 09:22 and 09:50 | no file trace | none; the MCP server inherited the variables and the panel ran | |
| 5 | `kiro-cli chat`; `founder/idea.md` in place (the golden `examples/barbershop/founder/idea.md`, copied on 2026-11-24 12:00) | about 09:50 | | the operator reused the golden idea instead of writing a new case (see limits) | |
| 6.1 | `founder-board` | 09:50 (`board/brief.md` 09:51:47) | 12 min to `board.md` 10:02:04; `board_run` 09:52:57 to 09:53:00 (3 s for three lenses) | version check (Protocol step 1) passed against `server_info` 0.2.0 | |
| 6.2 | `founder-competitors` | 10:02 | 34 min to `competitors.md` 10:35:56, of which the Owner's desk survey of 7 competitors (`phieu-khao-sat-doi-thu.md`, 10:33:47) is most; the skill's own output took about 2 min | the skill produces nothing until a filled form exists (by design); a desk survey leaves distance and peak-hour counts as "chưa có số liệu" | |
| 6.3 | `founder-consumer` | 10:36 | 27 min to `panel/results.md` 11:02:55; `customer.json` 11:02:05, `pitch.md` 11:02:16, `panel_run` n = 20 from 11:02:44 to 11:02:50 (6 s), `panel_tally` 11:02:55 | the Owner's five-point reading exists only in the chat, no `consumer.md`; `panel/results.md` has the caveat but no disclaimer line | #93, #95 |
| 6.4 | `founder-cfo` | 11:03 | 36 min; `numbers.json` 11:38:30, `cfo.md` 11:39:17 (`cfo_analyse` under a minute) | gathering the inputs dominates; the tax lookup in `permits/sources.md` found the sector entry and `cfo.md` carries the Công báo links and dates | |
| 6.5 | `founder-pricing` | 11:39 | 9 min; `pricing_input.json` 11:45:23, `pricing.md` 11:48:24 | run after `founder-cfo` because the skill reads `cfo.md`; `docs/hosts/kiro.md` listed pricing before cfo | fixed here (`43c6553`) |
| 6.6 | `founder-plan` | 11:48 | 5 min; `business-plan.md` 11:50:22, `summary.md` 11:53:03 | none; verdict "Profitable (có lãi)" computed by `plan_compile`, not written by the skill | |
| 7 | `uvx --from founder-vn founder-vn plan --check; echo $?` | 11:53, repeated by this lane at 12:08 | | `business-plan.md khớp với các file hiện có`, `exit=0`; `founder/business-plan.md` exists | |
| 8 | `sed -i '' 's/version: "0.2.0"/version: "1.0.0"/' .kiro/skills/founder-board/SKILL.md`; new `kiro-cli chat`; `founder-board`; restore | 11:53 | 9 min to the restored `SKILL.md` (12:02:17) | the skill stopped at Protocol step 1 (quoted below); after the restore all six skills read `version: "0.2.0"` | |

Step 8, the stop message as the Kiro CLI session wrote it (operator's transcript, truncated by the operator):

> Tôi dừng ở bước 1 của Protocol vì phiên bản bị lệch số major. Tôi chưa làm Bước 0, chưa viết lại brief, chưa gọi board_run và chưa ghi file nào vào founder/ ...

Elapsed from the install to the restored skill file: 09:22 to 12:02, 2 h 40 min, of which the Owner's own work (desk survey about 30 min, CFO inputs about 35 min) is roughly an hour. Design §7 budgets about four hours per pilot participant including two meetings; this run is inside that.

## Review-checklist walk on the walkthrough outputs

Run by this lane on 2026-11-25 in the walkthrough folder (outside git; nothing from it is committed), with `grep` over `founder/*.md`, `founder/board/*.md` and `founder/panel/results.md`:

| Check (`docs/review-checklist.md`) | Result |
| --- | --- |
| No `$` | no `$` in any Owner-facing file |
| Disclaimer "không phải tư vấn tài chính, thuế hay pháp lý" | present in `board.md`, `board/offers.md`, `board/product.md`, `board/systems.md`, `competitors.md`, `cfo.md`, `pricing.md`, `business-plan.md`, `summary.md`; absent in `panel/results.md` (tool output; #95) |
| Panel caveat "mô phỏng, cận trên, không phải khách hàng thật" | present wherever a panel result is shown: `board.md`, `panel/results.md`, `pricing.md`, `business-plan.md`, `summary.md` |
| Legal claims with official link and date | `cfo.md` cites Luật 48/2024/QH15, Luật 109/2025/QH15, Nghị định 253/2026/NĐ-CP and Nghị định 68/2026/NĐ-CP with `congbao.chinhphu.vn` links and Công báo dates |
| Survey method copied verbatim | first line of `competitors.md` is the form's "Cách khảo sát: khảo sát bàn giấy từ nguồn công khai, ngày 25/11/2026 …"; 7 competitors in the table |
| Break-even flag never hidden | `pricing.md` flags 199.000 đ as below the CFO break-even (margin −13 %, 51 lượt/ngày) next to the price |
| Model recorded | `panel/results.json` `model` = `gemini-3.5-flash-lite`, `n` = 20, `prompt_hash` present; `board/board.json` `model` = `gemini-3.5-flash-lite`, `prompt_hash` present |

## Lát

| Test | Assertion line while red | Green rerun |
| --- | --- | --- |
| `test_readme_truth_table_is_honest_about_release_status_and_hosts` (rewritten for the released state: `v0.2.0` with its date, no "pending", Kiro CLI row "full pipeline verified", other hosts "not yet verified", `docs/hosts/README.md` Kiro row "verified end to end", Vietnamese "đã xác nhận") | `AssertionError: assert ('v0.2.0' in '# founder-vn\n\nFounder skills for Vietnam…' and '2026-11-24' in …)` (`tests/test_front_door.py:140`) | `uv run pytest tests/test_front_door.py -q` after the README patch and `docs/hosts/README.md` |
| `test_kiro_page_has_the_clean_install_walkthrough_for_19` (order `board, competitors, consumer, cfo, pricing, plan`) | `AssertionError: founder-pricing reads cfo.md, so founder-cfo runs first` / `assert [1398, 1420, …] == [1398, 1420, …]` with the page stashed to its previous text | `uv run pytest tests/test_hosts.py -q -k clean_install_walkthrough`: 1 passed (commit `43c6553`) |
| `test_issue_19_evidence_records_the_kiro_cli_run` (replaces `test_issue_19_template_has_unticked_boxes_and_claims_no_run`) | `AssertionError: the four #19 criteria are ticked` / `assert (0 >= 4)` | `uv run pytest tests/test_hosts.py -q -k evidence_records` |

## Giới hạn

- Times are reconstructed from file modification times, not measured with a stopwatch; steps 1 and 4 leave no file and have no time; the 18 minutes between the install (09:22) and `mcp.json` (09:40) cover steps 3 and 4 and reading the printed snippet.
- The idea file was the golden `idea.md` (byte-identical to `examples/barbershop/founder/idea.md`), not a new case: the ticket's "new case" was not exercised. The survey (7 competitors), the panel (20 fresh personas and answers), the CFO inputs and every report were produced in the session. The first non-golden case is P01 of T19 (#20).
- One host. Claude Code, Codex, Gemini / Antigravity CLI, Grok Build and KiroCrew stay "not yet verified".
- The Kiro CLI session's model is recorded as the operator named it (`opus 5.5`); the lane did not read the host's configuration. The version check that passed in step 6.1 and the stop in step 8 were performed by that host model following Protocol step 1; the lane quotes the operator's transcript and did not observe the session. No automated seam exists for a skill run (spec #1).
- The walkthrough folder stays outside git. This record quotes no content of the case beyond what the golden example already publishes, no competitor names, no persona text.
- The `README.md` slice: `.kiro/hooks/guard.sh` refused this lane's edit (single-owner rule; the guard reads `HARNESS_SINGLE_OWNER_FILES`, unset in this CLI session, and does not read the allocation comment), the same gap #5 recorded. The operator applied `.harness/readme-issue-19.patch` by hand in their shell and the lane committed it; the allocation comment on #19 grants `README.md`.
- The release steps (tag, approval, publish) were run by the operator with their own credentials from this machine; the lane records them, no test reaches PyPI or GitHub Actions.

## Giải quyết review nội bộ

No self-review was run (lane rule: review is two independent turns after the pull request opens).
