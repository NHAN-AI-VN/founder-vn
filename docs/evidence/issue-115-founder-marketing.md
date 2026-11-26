# Evidence: issue #115 founder-marketing skill

## Seam

Taken from the ticket's `## Seam` section (written by the operator); nothing here is inferred.

- `skills/founder-marketing/SKILL.md`: structure, the channel list, the objection-traceability rule, the no-invented-quote rule. Checked by `scripts/skill_lint.py` and `tests/test_marketing_skill.py`.
- `examples/barbershop/founder/marketing.md`: sections in order, 30 campaign rows, every hook with an objection source, panel caveat once, disclaimers, no `$`. Checked in `tests/test_marketing_skill.py`.
- `examples/barbershop/founder/business-plan.md`: compiler output with the `Tiếp thị` section (`tests/test_plan_example.py`).
- `README.md` status row (single-owner file, allocated `all` under WIP 1), with `tests/test_front_door.py`.

## Lát

Every test runs with no network and no model.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| founder-marketing skill | `tests/test_marketing_skill.py` (11 skill tests) | all 11 failed with `FileNotFoundError: .../skills/founder-marketing/SKILL.md`; after the file existed, 4 failed (`assert 'làm sao để có khách' in ...` because a line wrap split the trigger phrase; `one statement`, `compute nothing new`, `no article or figure` missing), fixed in the skill | `uv run pytest tests/test_marketing_skill.py -q` (11 passed); `uv run python scripts/skill_lint.py` 0 findings |
| golden `marketing.md` | `tests/test_marketing_skill.py` (8 golden tests: seven sections in order, 30 relative-day rows each with a source, every quote verbatim from `panel/results.md`, every hook tied to an objection, ShopeeFood/GrabFood "Không áp dụng", budget quotes the percentage with no amount, panel caveat once, generic advertising disclaimer, no `$`) | with `marketing.md` moved away: `8 failed, 11 passed` (`FileNotFoundError: .../examples/barbershop/founder/marketing.md`; the business-plan test failed on `assert '## Tiếp thị' in ...`) | `uv run pytest tests/test_marketing_skill.py -q` (18 passed, 1 failed: the business-plan test, red until the next slice) |
| `business-plan.md` regenerated | `tests/test_marketing_skill.py::test_business_plan_carries_the_marketing_section`; `tests/test_plan_example.py::test_business_plan_is_the_compiler_output_and_check_passes` | `assert '## Tiếp thị' in '# Kế hoạch kinh doanh: ...'` on the old plan | `founder-vn plan` in `examples/barbershop` (+121 lines, -1: the "Tiếp thị" pointer becomes the section), then `uv run pytest tests/test_plan_example.py tests/test_marketing_skill.py -q` (26 passed) |
| README row and front door | `tests/test_front_door.py` (`founder-marketing` moves to the shipped set with `#115` and `marketing.md`; `founder-launch` stays "not started") | `assert ('#115' in '| `founder-marketing` | | not started (Wave B) | |')` | `uv run pytest tests/test_front_door.py -q` (12 passed) |
| review vòng 1 (S1, SPEC-1, SPEC-2, SPEC-3) | `tests/test_marketing_skill.py` (câu cảnh báo có "cận trên"; `## Protocol` một lần) | S1/SPEC-1: test khoá câu cũ, đỏ nếu chỉ đổi golden; SPEC-2: `assert 2 == 1` với dòng thừa; SPEC-3: không có test riêng, rà văn bản golden | `uv run pytest tests/test_marketing_skill.py tests/test_plan_example.py -q` (26 passed); ledger ở `reviews/issue-115/ledger.md` |

| review vòng 2 (câu hỏi operator, trả lời (b)) | `tests/test_marketing_skill.py::test_a_channel_with_no_source_in_the_owners_files_is_not_applicable`, `::test_golden_local_creators_not_applicable_without_a_source_and_unused_downstream`, `::test_golden_budget_shares_sum_to_ten_and_not_applicable_channels_get_zero`; `tests/test_plan_example.py::test_business_plan_is_the_compiler_output_and_check_passes` | `assert 'no file of the Owner' in …` (skill lacked the rule); `assert 'Không áp dụng' in '| Người sáng tạo địa phương | Dùng ở mức nhỏ …'` (golden funded an unsourced channel); plan `--check` exit 1 after the golden changed | `uv run pytest tests/test_marketing_skill.py -q` (22 passed, commit `b93a806`); `uv run pytest tests/test_plan_example.py tests/test_marketing_skill.py -q` (29 passed, commit `f6c0f9e`) |

The golden slice commit carried the still-red business-plan test (the plan is regenerated in the next commit); no commit after that is red. `numbers.json`, `cfo.md`, `pricing.md`, `summary.md` and `panel/` are unchanged.

## Giới hạn

- No Kiro CLI run: the golden `marketing.md` was written by the lane following `skills/founder-marketing/SKILL.md` in the sandbox, as #13, #112 and #114 did. No model call, no panel run.
- The campaign is relative to opening day ("Ngày 1"); `idea.md` says the opening is not decided, so there is no calendar date.
- No spend figure beyond the Owner's percentage: the budget quotes "marketing 4%" and divides it into shares of 10; no revenue or đồng amount (that is `founder-cfo`'s).
- Local creators: no Owner file shows these customers follow them, so after the operator's answer (b) to review round 2 (`reviews/issue-115/operator-answer.md`) the golden marks the channel "Không áp dụng (chưa có nguồn)", gives it no campaign row, share or metric, and names what would reopen it (a real customer naming it). The skill now states this rule for any listed channel without a source.
- Tests check structure, verbatim quotes and forbidden content; they do not show the campaign would bring customers. The panel is a simulation and the golden promises no reach or conversion.
- The two panel flips not decided in `idea.md` (drop the deposit, a trial ticket of about 120.000 đ) are not used as messages.

## Cổng ba đoạn

Chạy lại từng đoạn ở code commit `f6c0f9e` (các commit sau chỉ chạm `reviews/issue-115/` và file bằng chứng này). Lần trước: `39bdfe1` (vòng 1).

```
bash scripts/harness/gate-segment.sh static    # exit 0 (ruff check, ruff format --check, skill-lint: 9 skills, 18 example files, 0 findings)
bash scripts/harness/gate-segment.sh unit      # exit 0 (429 passed)
bash scripts/harness/gate-segment.sh build     # exit 0 (Successfully built dist/founder_vn-0.2.0-py3-none-any.whl)
bash scripts/harness/gate-segment.sh verify    # gate-segment verify: GREEN on f6c0f9ee16db2c2aa1e37fe58c9259f0ffd221f3
```
