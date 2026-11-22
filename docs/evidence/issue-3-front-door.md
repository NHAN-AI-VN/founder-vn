# Evidence: issue #3 repo front door, governance, skill conventions

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- Root documents (`README.md`, `LICENSE`, `CONTRIBUTING.md`): the files a visitor reads first; asserted by content (required sections, strings, links), as `tests/test_hosts.py` asserts `docs/hosts/kiro.md`.
- `.github/ISSUE_TEMPLATE/law-changed.yml`: a GitHub issue form; asserted as parsed YAML-free text with the four required fields.
- `docs/skill-conventions.md`: the frontmatter fields and the shared protocol block every later skill ticket copies; the protocol block is asserted verbatim.
- `docs/review-checklist.md`: the human half of `scripts/skill_lint.py`; asserted by its five required items.
- `docs/hosts/README.md` and one page per host: asserted by index links resolving to existing files.
- All of the above live in `tests/test_front_door.py`.

## Lát

All slices live in `tests/test_front_door.py`; each test was run red (file missing) before the document was written. Rerun: `uv run pytest tests/test_front_door.py -q` (11 passed).

| Slice | Tests | Assertion while red | 
|---|---|---|
| LICENSE, README | `test_license_is_mit_and_keeps_the_upstream_notice`, `test_readme_*` (3) | `FileNotFoundError: ... LICENSE` / `README.md` |
| CONTRIBUTING, issue form | `test_contributing_states_the_legal_rule_and_the_definition_of_done`, `test_law_changed_issue_template_has_the_four_fields` | `FileNotFoundError: ... CONTRIBUTING.md` / `law-changed.yml` |
| conventions, protocol | `test_conventions_list_every_frontmatter_field`, `test_shared_protocol_block_carries_the_five_rules` | `FileNotFoundError: ... docs/skill-conventions.md` |
| checklist, hosts | `test_review_checklist_has_the_five_items`, `test_hosts_index_links_one_existing_page_per_host`, `test_host_pages_carry_no_secret_values_or_dollar_amounts` | `FileNotFoundError: ... docs/review-checklist.md` / `docs/hosts/README.md` |

Deviation: the conventions slice commit shipped with one test failing (`AssertionError: author`, a field-name precedence bug in the test, which looked for `author` instead of `metadata.author`). The next commit fixed the test; the document was right.

## Upstream

Commit recorded in the README: `fd9385b0cfe1b96bebce3898fbd506d73eff5a9d`, the HEAD of `Jakeschincariol/founder-skill` read through the GitHub API on 2026-11-22. The upstream `LICENSE` (MIT, `Copyright (c) 2026 Jake Schincariol`) was fetched from the same HEAD and is preserved verbatim in `LICENSE`, below the founder-vn notice.

## Cổng ba đoạn

```
static 0 79e0347dff0357f2aaaa164b56acdeec8df9ec58 (ruff check, ruff format --check, skill-lint: 0 skill checked, 0 finding)
unit   0 79e0347dff0357f2aaaa164b56acdeec8df9ec58 (45 passed)
build  0 79e0347dff0357f2aaaa164b56acdeec8df9ec58 (founder_vn-0.1.0 sdist and wheel built)
gate-segment verify: GREEN on 79e0347dff0357f2aaaa164b56acdeec8df9ec58
```

The commit after that HEAD touches only this evidence file.

## Giới hạn

- The tests check content (strings, links, structure), not the quality of the prose or the Vietnamese wording.
- `skill-lint` checked 0 skills: no `skills/` folder exists yet, so the frontmatter example and the protocol block were not run through it.
- The `law-changed.yml` form was not rendered by GitHub; the test checks its field ids only.
- No install route was run: the PyPI release and `founder-vn install` do not exist yet. The README marks them "not yet released". `founder-vn --version` named in the protocol block is from the design; this ticket does not check that the CLI accepts it.
- Host stub pages carry no verified registration steps except Kiro.
- The commit hash is upstream HEAD at fetch time, not a reviewed baseline of what each skill adapts.

## Giải quyết review nội bộ

No self-review was run (lane rule: review is two independent turns after the pull request opens).
