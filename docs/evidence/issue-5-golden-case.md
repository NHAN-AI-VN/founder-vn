# Evidence: issue #5 golden case (idea.md for the chosen business)

Lane run by the project owner on Kiro CLI (the ticket is `ready-for-human`; the dispatcher skips it). The operator's allocation comment on #5 (2026-11-23T06:43:15Z) grants `README.md`, lane branch `lane/issue-5`, target `main`.

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `examples/barbershop/founder/idea.md`: the idea file of the golden case, in the upstream shape (`founder-board/SKILL.md` step 0: title plus the five bullets what, who, what at what price, where and how, budget and constraints), Vietnamese, VND. It is the file every skill reads first (spec #1: "one project root per Owner", artifacts keep upstream's names; design §5: `examples/<case-mẫu>/founder/`), so its path and shape are the public boundary; asserted by content in `tests/test_golden_case.py`.
- `examples/barbershop/**/*.md` anonymised: no personal names, no phone numbers or e-mail addresses, no street address, location at former-district level, no `$` next to a digit (`scripts/skill_lint.py` scans `examples/**/*.md`; the test repeats the `$` check and adds the phone, e-mail and street-address shapes).
- `README.md` (single-owner, allocated): names `examples/barbershop/` as the golden case; asserted by `tests/test_golden_case.py`.
- `docs/founder-vn-design.md`: the sector change of the golden case (Q51, amending Q21 and the week-1 row of §7) lands in this change because the design wins over code and the owner changed the design here; not a test seam, reviewed by reading.

No automated seam exists for the skills that will consume the file (spec #1: "Skills have no automated seam"); this ticket proves the file and its pointer, not a skill run.

## Decision recorded in this lane

- The golden case is no longer an F&B business. The project owner chose, in this lane session on 2026-11-23, their own barbershop concept (market study v2 of 2026-11-13, kept outside the repository) as the golden case: design Q51 (`docs/founder-vn-design.md`, amending Q21 and the week-1 row of §7), spec #1 user story 48 and the title and "What to build" of #5 were changed the same day; the three acceptance criteria of #5 are unchanged. Reasons and consequences are in Q51; the one open consequence (the F&B path of `founder-permits`, Q47, is no longer exercised by the golden case) is deferred to Wave B by Q51, not decided here.
- Working name: a descriptive placeholder, "Tiệm cắt tóc nam kiểu barbershop (tên gọi tạm)". The owner first proposed a name built on the study's reference brand (a real barbershop operating in Ho Chi Minh City and Hanoi); the lane did not use it because the example is public and "no real names" covers real brands, and the study itself conditions any use of that brand on a licence. The owner can rename with a one-line change.
- Consent (criterion 2): the case owner is the project owner. Agreement to publish the anonymised artefacts was given on 2026-11-23 in this session by choosing the case, approving the design change and applying the README edit by hand. No third party is involved, so no consent form was signed; `pilot/consent.md` is for pilot participants and allows aggregate publication only, which is why it was not reused.

## Lát

| Test | Assertion line while red | Green rerun |
| --- | --- | --- |
| `test_idea_file_sits_in_the_example_project_root` | `AssertionError: PosixPath('.../examples/barbershop/founder/idea.md')` / `assert False` | `uv run pytest tests/test_golden_case.py -q`: 4 passed (commit `dbfbf1a`) |
| `test_idea_file_has_the_upstream_shape_in_vietnamese` | `FileNotFoundError: [Errno 2] No such file or directory: '.../examples/barbershop/founder/idea.md'` | same run, passed |
| `test_idea_file_prices_are_vnd_in_vietnamese_format` | `FileNotFoundError` (same path) | same run, passed |
| `test_example_is_anonymised` | `AssertionError: PosixPath('.../examples/barbershop')` / `assert []` | same run, passed |
| `test_readme_names_the_example_directory_as_the_golden_case` | `AssertionError: assert 'examples/barbershop/' in '# founder-vn\n\nFounder skills for Vietnam...'` (1 failed, 4 passed) | `uv run pytest tests/test_golden_case.py -q`: 5 passed (commit `811b7bf`) |

The README slice: `.kiro/hooks/guard.sh` refused the lane's edit of `README.md` (single-owner rule; the guard reads `HARNESS_SINGLE_OWNER_FILES`, unset in this CLI session, and does not read the allocation comment). The lane did not work around the guard: it wrote the patch to `.harness/readme-golden-case.patch`, checked it with `git apply --check`, and the operator applied it in their own shell; the lane then ran the test green and committed. `skill_lint.py` at `811b7bf`: `0 skill checked, 1 example file(s), 0 finding(s)`.

## Cổng ba đoạn

```
static 0 811b7bf6fdca439d916094f3d2c6192ab9f2cac0 (ruff check: All checks passed!; ruff format --check: 175 files already formatted; skill-lint: 0 skill checked, 1 example file(s), 0 finding(s))
unit   0 811b7bf6fdca439d916094f3d2c6192ab9f2cac0 (224 passed in 21.53s)
build  0 811b7bf6fdca439d916094f3d2c6192ab9f2cac0 (founder_vn-0.1.0 tar.gz and wheel built)
gate-segment verify: GREEN on 811b7bf6fdca439d916094f3d2c6192ab9f2cac0
```

`check-doc-paths.sh` at the same HEAD: 23 path(s) in 2 file(s) exist. The commit after that HEAD touches only this evidence file.

## Giới hạn

- The tests check the shape and the anonymisation patterns of `idea.md` (five Vietnamese bullets, VND format, no `$`, no phone number, e-mail or street address), not the quality of the Vietnamese nor whether the numbers are right; every figure is the owner's planning estimate from a desk study and is labelled so in the file. Nothing was run with a skill yet (T11–T17 will).
- Anonymisation is partly a judgement: the location is given at former-district level ("khu Phú Mỹ Hưng (Quận 7 cũ)"), competitor and reference brands are described, not named, and no person is named; a reader who knows the owner could still connect the concept to them, which the owner accepts as the case owner.
- The study assumes a company (VAT on list prices, social insurance); `idea.md` frames the first shop as a household business with list prices as what the customer pays, and leaves the revenue-tax rate and threshold to the CFO skill (T11, sourced), so the CFO numbers will not reproduce the study's EBITDA table and are not meant to.
- The off-peak discount window is written as "ngày thường 10:00–16:00" because the study says both "thứ Hai–Thứ Năm" and "nghỉ thứ Hai"; the owner should fix the window when pricing is run.
- Spec #1 and ticket #5 were edited in place by the operator's `gh` account; GitHub keeps the edit history, and Q51 is the durable record.
- The guard's single-owner rule has no channel to the operator's allocation comment on the CLI either (`docs/agents/kiro-harness.md` §8 names the same gap for Kiro Web); this lane bridged it by hand. A `ready-for-human` ticket that needs a single-owner file therefore costs one operator action per file; not fixed here.

## Giải quyết review nội bộ

No self-review was run (lane rule: review is two independent turns after the pull request opens).
