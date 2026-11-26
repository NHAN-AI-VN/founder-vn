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
| sources ledger verified (`slice(sources ledger)` after `4b5e670`) | `tests/test_sources_ledger.py` (4 new tests: four permits entries with one status line dated 26/11/2026, every entry has a verification line and none says `chưa kiểm chứng`, `conditional_sectors` pointer without a fee, 168/2025 excerpts; count pinned at ten documents) | 5 failed: `AssertionError: 143/2025/QH15` and the count/entry tests, against the drafts | `uv run pytest tests/test_sources_ledger.py -q` (10 passed) |
| founder-permits skill, verified figures (`7cadb42`) | `tests/test_permits_skill.py` (3 new tests: fee wording, conditional-sector pointer, search endpoint) | 3 failed: the fee wording, the `luat-so-143-2025-qh15-468703.htm` link and `POST https://api-searchcongbao.chinhphu.vn/search/all` were absent | `uv run pytest tests/test_permits_skill.py -q` (12 passed) |
| golden `permits.md` (`8f4c0dc`) | `tests/test_permits_example.py` (5 tests) | 5 failed with `FileNotFoundError: .../examples/barbershop/founder/permits.md`; after the file existed, the fee-wording assertion failed on a capital "Mức" and was fixed in the file | `uv run pytest tests/test_permits_example.py -q` (5 passed) |
| README row and front door (`8f4c0dc`) | `tests/test_front_door.py` (row `founder-permits` moves to the shipped set with `#112` and `permits.md`) | with the README row restored to the old text: `assert ('#112' in '| `founder-permits` | | not started (Wave B) | |')` | `uv run pytest tests/test_front_door.py -q` (12 passed) |

`business-plan.md` was regenerated with `founder-vn plan` in `examples/barbershop` in the same commit as `permits.md`: a `permits.md` at the example path adds the section "Giấy phép và thuế" (+58 lines, -1 line: the "chưa có" pointer is replaced). `tests/test_plan_example.py` (compiler output equals the file, `plan --check` exit 0) passes on it.

## Pausa BLOCKED và câu trả lời của operator

- Paused at `4b5e670` with the three drafted entries marked `chưa kiểm chứng bởi operator`; the BLOCKED comment asked for one confirmation per figure or document (registration authority and online filing, Nghị định 168/2025 articles, tax registration and declaration, e-invoice, the two old entries, conditional sectors, the date, scope).
- Answer (operator, 26/11/2026, on the issue): all nine boxes ticked, verified against the digitally signed Công báo PDFs with `pdftotext -layout`. It added verbatim excerpts from Nghị định 168/2025 (Điều 85, 88, 91, 94, 95, 97, 99, 116; Công báo 885+886 and 887+888, 15/07/2025) and Nghị định 296/2026 (Điều 17 khoản 4, Điều 18 khoản 3), a new document row for Luật Đầu tư 143/2025/QH15 (Điều 7, Phụ lục IV; Công báo 42, 22/01/2026), the Công báo search endpoint for the run-time re-check, and the rule that the fee amount is not in any decree. Verification date for the new and drafted entries: 26/11/2026. The two old entries stay at 23/11/2026 and byte-identical.
- Applied: four `chưa kiểm chứng` lines replaced by `kiểm chứng ngày 26/11/2026 bởi operator trên bản PDF Công báo` (three drafted entries and `conditional_sectors`); one sentence of the preamble that said `chưa kiểm chứng` about two temporary incentives was reworded to `chưa có bản kiểm chứng` so the file has no `chưa kiểm chứng` at all (it is outside every entry).

## Tra lại nguồn khi viết golden (26/11/2026)

Through the endpoint above with a browser-like `User-Agent`: search by số ký hiệu returned the expected `id_van_ban` for Nghị định 168/2025, 68/2026, 141/2026, Luật 48/2024, 109/2025, 143/2025, 149/2025 and 09/2026. For Nghị định 296/2026 and 253/2026 the search did not list them (50 results asked), but their `/van-ban/<slug>-<id>.htm` pages answer HTTP 200. PDF text was not compared again, so the golden writes "kiểm chứng ngày X, chưa xác nhận lại hôm nay" beside every figure.

## Cổng ba đoạn

```
bash scripts/harness/gate-segment.sh static    # exit 0 (ruff check, ruff format --check, skill-lint: 7 skills, 16 example files, 0 findings)
bash scripts/harness/gate-segment.sh unit      # exit 0 (389 passed)
bash scripts/harness/gate-segment.sh build     # exit 0 (Successfully built dist/founder_vn-0.2.0-py3-none-any.whl)
bash scripts/harness/gate-segment.sh verify    # gate-segment verify: GREEN on 8f4c0dca63a7e78b154365e2e8601ab9e7b77b27
```

`8f4c0dc` is the last code commit; only this evidence file follows it.

## Giới hạn

- No Kiro CLI run: the golden `permits.md` was written by the lane following `skills/founder-permits/SKILL.md` in the sandbox, as #13 did. No model call, no panel.
- No F&B path (Q56): `chứng nhận an toàn thực phẩm` and F&B tax rates are not in this checklist.
- Unsourced on purpose: the registration fee amount (no decree states it); the golden says so and tells the Owner to ask the commune registration office. No figure or condition for conditional sectors beyond the pointer.
- The golden's run-time re-check did not compare PDF text; every figure carries "chưa xác nhận lại hôm nay". Nghị định 253/2026 and 296/2026 did not come back from the search endpoint.
- Tests read text and structure; they do not prove the legal content, which rests on the operator's 26/11/2026 verification of the ledger.
- `uv run pytest tests -q` also passed (389) at `8f4c0dc`.
