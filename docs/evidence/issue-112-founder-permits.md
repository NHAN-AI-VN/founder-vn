# Evidence: issue #112 founder-permits skill, common path

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-permits/SKILL.md`: the instructions the host model follows. Checked by `scripts/skill_lint.py` and by reading the text in `tests/test_permits_skill.py` (structure, the never-guess rule, the fallback wording, the disclaimer).
- `permits/sources.md`: the only place a legal figure may come from. Checked by `tests/test_sources_ledger.py`.
- `examples/barbershop/founder/permits.md`: the file the Owner reads. Checked for section presence, links with dates, no `$`.
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.

## Lát

Every test runs with no network and no model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| founder-permits skill (`6c806e7`) | `tests/test_permits_skill.py` (9 tests) | all 9 failed with `FileNotFoundError: .../skills/founder-permits/SKILL.md`; after the file existed, `test_frontmatter_matches_the_lint_and_the_package_version` failed with `KeyError: 'version'` (version is dynamic in `pyproject.toml`; the test now reads `founder_vn.__version__`) | `uv run pytest tests/test_permits_skill.py -q` (9 passed) |
| sources ledger drafts (`ecad525`) | `tests/test_sources_ledger.py::test_ledger_lists_the_eight_documents_with_official_links`, `test_ledger_has_the_three_permits_entries_with_link_issue_article_excerpt_and_one_status` | after the ledger gained document 8 the pinned count failed with `assert 8 == 7`; the new-entries test needs the three entries and passes only with them | `uv run pytest tests/test_sources_ledger.py -q` (7 passed) |

## Pausa BLOCKED

The three new ledger entries are drafts: each ends with `- Xác nhận: chưa kiểm chứng bởi operator`. The skill names the ledger keys and quotes no figure. Not done yet, on purpose: the README row and `tests/test_front_door.py` move (the golden `permits.md` does not exist, so the row cannot link it), the golden `permits.md`, the regenerated `business-plan.md` (a `permits.md` at the example path changes the compiler output, and a golden with unverified figures must not be committed), and the test that no entry says `chưa kiểm chứng` at HEAD.

## Giới hạn

- No Kiro CLI run is possible in the lane sandbox; the golden will be written by the lane following the skill, as #13 did.
- No F&B path (Q56).
- Not yet sourced: the documents, time and fee of household-business registration (Nghị định 168/2025/NĐ-CP, original not located on Công báo from the sandbox) and the authority that lists conditional sectors.
