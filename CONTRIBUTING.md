# Contributing to founder-vn

The design is `docs/founder-vn-design.md`; when code and design disagree, the design wins and the
fix lands in the same change. Tickets are the GitHub issues of this repository. Coding standards:
`docs/agents/standards.md`.

## The hard rule

**Every legal claim needs an official link and a verification date.** A tax rate, a threshold, a
licence rule or a deadline appears in a skill, a report or a fixture only with the link to the
official source (a government or regulator page) and the date you checked it. A claim without both
is not merged.

## Reporting a stale law

Open an issue with the **Law changed** template (`.github/ISSUE_TEMPLATE/law-changed.yml`): what
changed, the source link, the effective date and the affected skill.

## Conventions

- Skill frontmatter, language rules and the shared protocol section:
  [docs/skill-conventions.md](docs/skill-conventions.md).
- Host registration pages: [docs/hosts/README.md](docs/hosts/README.md).
- Data in fixtures, examples and logs is synthetic or anonymised. Never write credentials or the
  values of `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` or `FOUNDER_LLM_MODEL`.

## Definition of done for a skill

A skill is done when all of these hold:

1. **Golden-case run**: the skill ran end to end on the sample case, and the output is committed
   as a golden file under `tests/golden/` (or `examples/`) with the model name and prompt hash
   recorded in the evidence file.
2. **Tests**: new behaviour has tests written red first, then green; `uv run pytest` passes and
   `python3 scripts/skill_lint.py` exits 0.
3. **Review checklist**: every item of [docs/review-checklist.md](docs/review-checklist.md) holds,
   and the pull request template section for skills is ticked.

## Pull requests

Fill in `.github/PULL_REQUEST_TEMPLATE.md`. Each change carries evidence in
`docs/evidence/issue-<n>-<slug>.md`. Run the gate before opening the pull request:

```bash
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
```

## Licence

By contributing you agree your work is released under the MIT licence in [LICENSE](LICENSE).
