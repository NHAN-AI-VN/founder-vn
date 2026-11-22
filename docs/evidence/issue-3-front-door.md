# Evidence: issue #3 repo front door, governance, skill conventions

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- Root documents (`README.md`, `LICENSE`, `CONTRIBUTING.md`): the files a visitor reads first; asserted by content (required sections, strings, links), as `tests/test_hosts.py` asserts `docs/hosts/kiro.md`.
- `.github/ISSUE_TEMPLATE/law-changed.yml`: a GitHub issue form; asserted as parsed YAML-free text with the four required fields.
- `docs/skill-conventions.md`: the frontmatter fields and the shared protocol block every later skill ticket copies; the protocol block is asserted verbatim.
- `docs/review-checklist.md`: the human half of `scripts/skill_lint.py`; asserted by its five required items.
- `docs/hosts/README.md` and one page per host: asserted by index links resolving to existing files.
- All of the above live in `tests/test_front_door.py`.
