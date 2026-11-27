# Evidence: issue #148 the Protocol step-1 stop is Vietnamese, in one fixed shape (Q60)

## Seam

Taken from the `## Seam` section of the ticket and refined here (the refinements are marked).

- The shared `## Protocol` block: `docs/skill-conventions.md` is the canonical text, the ten `skills/*/SKILL.md` are its copies. `tests/test_front_door.py` pins the step-1 stop template as a sixth needle of the canonical block and the step-2 Vietnamese stop; the per-skill lockstep tests (`test_skill_carries_the_shared_protocol_block_verbatim` in each `tests/test_*_skill.py`) hold the ten copies to the canonical text. Red first on the canonical block. Refinement: the eleven files change in the same slice, because the lockstep tests make a canonical-only change red on ten skills.
- `scripts/skill_lint.py` behind the CI Gate and the `static` segment: the new rule (the `## Protocol` block of every skill carries the template verbatim, with its placeholders). `tests/test_skill_lint.py` carries the rule's own tests: a skill whose block lacks the template is one finding naming the file and the line, the ten skills are 0 findings. Red first with a skill fixture lacking the line. Refinement: the lint is also a harness mechanism (`scripts/harness/witness.sh` runs on CI when the lint changes), so the same slice adds the witness fixture `scripts/harness/fixtures/skill-lint/no-protocol-stop` and a `--witness-red` mutation of the rule; the eight existing fixtures gain the block so they keep failing for their one reason.
- `docs/hosts/kiro.md` step 9 behind `tests/test_hosts.py`: the expected prefix `Dừng ở bước 1 của Protocol`, next to the step-1 condition sentence the test already pins. Red first.
- `docs/founder-vn-design.md` (§4 row, Q60, the heading range), `docs/agents/standards.md` (skills bullet), `AGENTS.md` and `tests/test_install.py` (the `Q1–Q60` range). Refinement: pinned by a new test in `tests/test_front_door.py`, red first, so the design and standards change is a slice like the others.

## Lát

One red-then-green slice per seam, each its own commit; the red run is the targeted file only (`uv run pytest tests/<file>.py -q -k <test>`), the green rerun the whole file.

| Test | Red assertion | Green |
|---|---|---|
| `tests/test_front_door.py::test_shared_protocol_block_quotes_the_vietnamese_stop_template` (commit `77e3085`) | `assert 'Dừng ở bước 1 của Protocol: gói founder-vn <phiên bản gói> …' in '## Protocol\n\n1. Check the version: …'` — the canonical block had no template | `uv run pytest tests/test_front_door.py -q` 13 passed; the ten lockstep tests `test_skill_carries_the_shared_protocol_block_verbatim` 173 passed across the ten `tests/test_*_skill.py` |
| `tests/test_skill_lint.py::test_skill_lint_reports_a_protocol_block_that_lacks_the_vietnamese_stop_template` (commit `0397fb9`) | `assert 0 == 1` — the lint exited 0 with `skill-lint: 1 skill checked, 0 example file(s), 0 finding(s)` on a fixture whose Protocol block lacks the line | `uv run pytest tests/test_skill_lint.py -q` 4 passed (the finding is `skills/demo/SKILL.md:<heading line>: …`, one line; the ten skills 0 findings) |
| `tests/test_hosts.py::test_kiro_step_9_expects_the_vietnamese_stop_and_keeps_the_step_1_condition` (commit `4d84c62`) | `assert 'Dừng ở bước 1 của Protocol' in '. Open `.kiro/skills/founder-board/SKILL.md` and set …'` — step 9 named no prefix | `uv run pytest tests/test_hosts.py -q` 13 passed, the existing pin on the condition sentence included |
| `tests/test_front_door.py::test_design_and_standards_record_q60` (commit `9a27988`) | `assert ('(Q1–Q60)' in '# founder-vn: bản thiết kế …')` — no Q60, no §4 row | `uv run pytest tests/test_front_door.py tests/test_install.py -q` 46 passed |

Deviations: slice 1 changes eleven files in one commit (canonical block and ten skills), because the lockstep tests make a canonical-only change red on the ten skills. Slice 2 also touches the harness witness (`scripts/harness/witness.sh`, `scripts/harness/fixtures/skill-lint/`), see below. `AGENTS.md` and `tests/test_install.py` move the decision range to `Q1–Q60` in slice 4, as #144 did for Q59. `metadata.version` of the ten skills and `src/` are untouched.

### Commissioning the lint rule (red before trust)

The gate under test is `scripts/skill_lint.py`, run as the Gate and the `static` segment run it. The violation is a copy of the ten skills under `.harness/lint-red/` with the template line removed from `founder-launch/SKILL.md` (`grep -v "Dừng ở bước 1 của Protocol"`).

```
$ python3 scripts/skill_lint.py --root .harness/lint-red        # before the rule, at 77e3085
skill-lint: 10 skills checked, 0 example file(s), 0 finding(s) (package version 0.3.0)
exit 0
$ python3 scripts/skill_lint.py --root .harness/lint-red        # with the rule, at 0397fb9
.harness/lint-red/skills/founder-launch/SKILL.md:19: `## Protocol` block lacks the Vietnamese step-1 stop template `Dừng ở bước 1 của Protocol:…` (docs/skill-conventions.md, Shared protocol)
skill-lint: 10 skills checked, 0 example file(s), 1 finding(s) (package version 0.3.0)
exit 1
$ python3 scripts/skill_lint.py                                 # the ten skills
skill-lint: 10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.0)
exit 0
```

Harness witness (CI runs it in both modes when a pull request touches `scripts/skill_lint.py`): with the rule in place and the fixtures unchanged, `bash scripts/harness/witness.sh` went red on `FAIL skill-lint: ok (want exit 0, got 1: …SKILL.md:12: `## Protocol` block lacks the Vietnamese step-1…)`, which is the rule catching a fixture that had no block. The eight fixtures gained the block at their end (their one violation keeps its line number: `dollar` still reports `SKILL.md:21:`), the new fixture `no-protocol-stop` expects the finding at `SKILL.md:15`, and a `--witness-red` mutation replaces the rule's body with `return True`. After: `bash scripts/harness/witness.sh` → `234 passed, 0 failed`; `bash scripts/harness/witness.sh --witness-red` → `every mutation was caught (117, 14 at a time)`, with `RED mutation "lint: accept a Protocol block without the Vietnamese stop template" turned 1 case(s) red`.

Blind spots of the rule: it checks that the template is present verbatim somewhere in the `## Protocol` section; it does not check the sentence around it ("The stop message is in Vietnamese…"), the block's position in the file, or step 2's Vietnamese stop. The lockstep tests cover those for the ten skills by comparing each block to the canonical text.

## Cổng ba đoạn

Last code commit: `9a27988` (slice 4); `ca20a0c` after it changes only `docs/skill-conventions.md` prose (the pointer sentence above the block). Run at `ca20a0c`, each segment once; numbers read from `.harness/gate-*.log`:

```
$ bash scripts/harness/gate-segment.sh static
320 files already formatted
All checks passed!
skill-lint: 10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.0)
$ bash scripts/harness/gate-segment.sh unit
502 passed in 23.09s
$ bash scripts/harness/gate-segment.sh build
Successfully built dist/founder_vn-0.3.0.tar.gz
Successfully built dist/founder_vn-0.3.0-py3-none-any.whl
$ bash scripts/harness/gate-segment.sh verify
gate-segment verify: GREEN on ca20a0c75f12236c8cc711f57bed7ab4cb9e93c0
```

The wheel built by the `build` segment lists ten `founder_vn/skills/founder-*/SKILL.md` and its `founder-launch/SKILL.md` carries the template line (`unzip -l`, `unzip -p … | grep -c`, both read by hand after the segment).

## Giải quyết review nội bộ

No internal review turn in this lane (`/code-review` is replaced by the harness review turns). Two points the lane settled itself: the template sits on one line in the block, in Q60 and in the §4 row, so a verbatim lookup (tests and lint) finds it without whitespace folding; a skill with no `## Protocol` heading at all is also a finding of the new rule, reported at the first body line, since its block is empty.

## Giới hạn

- No host model was run: the new stop was not observed in a session. The next clean-install walkthrough (#149 or the next milestone) does that, as the ticket's out-of-scope says. What this lane proves is the text: the eleven blocks are byte-identical and carry the template, the lint refuses a block without it, and step 9 of the host page says what to expect.
- The lint rule is a substring check of the template inside the `## Protocol` section (blind spots above).
- No network, no `FOUNDER_LLM_*` value read or written; the sandbox variables were not needed by any step.
