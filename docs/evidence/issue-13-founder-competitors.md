# Evidence: issue #13 founder-competitors, field-survey form and skill

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code and no CLI or MCP tool: the design (§3) makes the skill a prompt plus a printable form, so the seams are the shipped files.

- `skills/founder-competitors/SKILL.md` (skill file): the instructions the host model follows. Seam because the required-form gate, the supplementary-web rule, the output shape and the thin-data warning live only here (criteria 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `skills/founder-competitors/survey-form.md` (printable form, Vietnamese): the file the skill prints for the Owner. Seam because criterion 1 lists its six fields (criterion 1).
- `founder_vn.install` (existing module, unchanged): the skill must be found and copied with its form. Tested through `install.run` against the real `skills/` folder (criteria 1, 2).

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| form, skill gates, output shape, lint, installer | `tests/test_competitors_skill.py` (8 tests) | `FileNotFoundError: [Errno 2] No such file or directory: '.../skills/founder-competitors/SKILL.md'` (and `survey-form.md`) | `uv run pytest tests/test_competitors_skill.py -q` (8 passed) |
| SPEC-2: survey method, source column, disclaimer by method | `test_skill_copies_the_survey_method_and_sets_the_source_by_method` | `AssertionError: assert 'Cách khảo sát' in '---\nname: founder-competitors...'` | `uv run pytest tests/test_competitors_skill.py -q` (12 passed) |
| SPEC-2: disclaimer varies by method | `test_disclaimer_varies_by_method` | `AssertionError: assert 'varies by method' in '---\nname: founder-competitors...'` | same command |
| SPEC-2: empty review count is not thin data | `test_empty_review_count_is_not_thin_data` | `AssertionError: assert 'An empty review-count cell is not a number' in '---...'` | same command |
| SPEC-2: desk survey says small sample in map and gap | `test_desk_survey_states_small_sample_in_map_and_gap` | `AssertionError: assert 'small sample' in '---...'` | same command |
| SPEC-1: golden `competitors.md` | `test_golden_competitors_follows_the_skill_on_the_desk_survey_form` | `FileNotFoundError: [Errno 2] No such file or directory: '.../examples/barbershop/founder/competitors.md'` | `uv run pytest tests/test_competitors_skill.py -q` (13 passed) |

The first red run was witnessed before the skill files existed; one slice because the form and the skill are one deliverable and the tests read both. The tests check the text of the instructions (the required-form stop, the supplementary and linked rule, the no-invention rule, the table, the thin-data warning), not model behaviour.

## Cổng ba đoạn

Last code commit: `49a103f` (last commit touching `skills/`, `tests/`, `examples/`). Each segment ran once at that HEAD; counts read from `.harness/gate-*.log`. Commits after it (`3c83c5a` ledger, this evidence) touch only `reviews/` and `docs/evidence/`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "136 files already formatted", skill-lint "1 skill checked, 3 example file(s), 0 finding(s)"
unit:   238 passed
build:  Successfully built dist/founder_vn-0.1.0-py3-none-any.whl and dist/founder_vn-0.1.0.tar.gz
gate-segment verify: GREEN on 49a103f2e8b299290c5f50e267e833d79c97ab95
```

## Giới hạn

- **Kiro CLI is not available in the lane sandbox.** The golden case run is the lane agent's own run, following the updated `skills/founder-competitors/SKILL.md` step by step on `examples/barbershop/founder/survey-form.md`. It is not a run by a Kiro CLI session, so it does not prove that another model obeys the skill.
- **The input is a desk survey from public sources (access date 23/11/2026), not a field survey.** `competitors.md` copies that declaration, and its source column says desk survey. All counts of customers at peak hours, menu photos and complaints are blank in the form and stay "chưa có số liệu". The Owner's on-foot survey will replace this form; rerunning the skill on it is a follow-up.
- Criterion 4 review checklist (`.github/PULL_REQUEST_TEMPLATE.md`), checked against `competitors.md`: six sections present; 8 rows (5 to 10); declaration copied verbatim at the top; source column is desk survey with date and link on every row; no "khảo sát thực địa" as source; only numbers from the form; empty cells "chưa có số liệu"; no quote invented ("chưa có trích dẫn"); empty review counts not shown as thin-data warnings; no web search added, stated in section 4; disclaimer present; no `$` next to a digit; addresses at old-district level. Passed.
- Commands run for the example files: `uv run python scripts/skill_lint.py` (0 findings, 3 example files); `uv run pytest -q` (238 passed, includes `test_example_is_anonymised`); link and path validation: every link in `competitors.md` was copied from the form (not fetched again, so liveness is not proven), and the paths it names (`founder/idea.md`, `founder/survey-form.md`) exist in the example folder.
- The tests read instruction text and the example file; they do not test model behaviour.
- The survey form is the lane's design of the six fields in the ticket plus a review-count table; the Owner has not tried it on foot.
- No CLI or MCP tool was added: the design asks for none.
- README skill table was not changed.

## Giải quyết review nội bộ

- Gate red at `d193b6a`: `test_example_is_anonymised` failed on a sub-district urban-area name in the filled form. Fixed at `cada7bc` (addresses stop at old-district level); the Gate was green after.
- Round 2, S1 (stale gate block): gate rerun at the last code commit `49a103f`, block replaced above.
- Round 2, S2 (evidence omitted the example files and had a wrong limit): `## Giới hạn` rewritten, example-file validation recorded, this section filled.
- Round 2, SPEC-1 (no `competitors.md`): written by following the updated skill; test added (`49a103f`).
- Round 2, SPEC-2 (skill hardcoded `khảo sát thực địa`): skill now copies the method declaration, sets source and disclaimer by method, and treats an empty review count as "chưa có số liệu" (`f26e526`, four tests).
- Round 2, SPEC-3 (stale evidence): this file.
- Noted while writing `competitors.md`: form entry 1 says Tony Barber House closes "3 giờ 15 phút" earlier than the idea, but 19:45 against 21:00 is 1 giờ 15 phút. Both figures were kept and flagged to the Owner in section 2; the form was not edited.
