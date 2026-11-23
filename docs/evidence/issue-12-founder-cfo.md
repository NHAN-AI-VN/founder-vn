# Evidence: issue #12 founder-cfo skill and the first sources-ledger entries

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The ticket adds no Python code: `founder_vn.cfo` (T05, issue #6) is unchanged and owned by that ticket. The seams are the shipped files.

- `permits/sources.md` (sources ledger): the first two entries, `tax_rate_on_revenue` for "cắt tóc, làm đầu, gội đầu" and `tax_free_threshold`, each with official link, Công báo number and date, article, verbatim excerpt and verification line (criterion 2, CONTRIBUTING hard rule). Checked by a ledger-shape test.
- `skills/founder-cfo/SKILL.md` (skill file): the instructions the host model follows. Seam because the Owner-terms cost questions, the lookup, the tool call, the plain-Vietnamese flag read-back and the disclaimer live only here (criteria 1, 2, 3). Checked by `scripts/skill_lint.py` and by reading the text in a test.
- `founder-vn cfo --out` (existing CLI command, unchanged): produces `examples/barbershop/founder/cfo.md` from `numbers.json` (criterion 4). The golden files are checked by content tests.
- `docs/founder-vn-design.md` decision log (Q52): the combined-rate model decision the operator made for this ticket.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| sources ledger | `tests/test_sources_ledger.py` (6 tests) | `FileNotFoundError: [Errno 2] No such file or directory: '.../permits/sources.md'`; after the file existed, 2 failed (entry headings split on the overview section, and the verification line absent) before the test filter and the line were fixed | `uv run pytest tests/test_sources_ledger.py -q` (6 passed) |
| founder-cfo skill | `tests/test_cfo_skill.py` (11 tests) | `FileNotFoundError: [Errno 2] No such file or directory: '.../skills/founder-cfo/SKILL.md'`; with the file written, `test_states_the_two_tax_model_limits_and_the_temporary_relief_line` failed at `assert 'có ưu đãi tạm thời, chưa tính' in '---\nname: founder-cfo...'` (capital letter) | `uv run pytest tests/test_cfo_skill.py -q` (11 passed) |
| golden case | `test_golden_numbers_json_holds_the_ledger_values_for_the_sector`, `test_golden_cfo_md_is_the_tool_output_plus_the_limits_section` | `FileNotFoundError: [Errno 2] No such file or directory: '.../examples/barbershop/founder/numbers.json'` and `.../cfo.md` (2 failed, 11 passed) | `uv run pytest tests/test_cfo_skill.py tests/test_golden_case.py -q` (19 passed) |

The golden `cfo.md` was produced by `founder-vn cfo founder/numbers.json --out cfo.md` run in `examples/barbershop/`, then the "Giới hạn của phần thuế" section was appended (the text of SKILL.md Step 6). The test regenerates the tool text with `cfo.run` and requires the file to start with it, so the tool part cannot drift by hand. No code under `src/` changed, so there is no red-green slice for `src/`.

Inputs of `numbers.json` (synthetic, from `idea.md` of the example): per-unit costs are the percentages of `idea.md` applied to the 280.000 đ average ticket (commission 25%, supplies 7%, marketing 4%, payment 1%); monthly fixed costs are the lines of `idea.md` (the Tết bonus as one month of base pay divided by 12); startup items sum to 1.250.000.000 đ; `ramp_per_day` is an assumed ramp (the idea gives no ramp), reaching the planned 40 per day in month 9. Retail sales (about 5% of revenue) and the landlord's house-rent tax are not in the model.

Report numbers, from the generated file: break-even 28 lượt per day, year-1 revenue 2.639.000.000 đ, year-1 tax 184.730.000 đ, year-1 operating profit after tax 23.836.000 đ, cash needed 1.424.635.000 đ; two flags (over the threshold, startup not recovered in year 1).

Design: Q52 is recorded in `docs/founder-vn-design.md` (decision log, heading now Q1–Q52).

## Cổng ba đoạn

Last code commit: `a62d8fb` (golden slice). Each segment ran once at HEAD `1bda173` (the Q52 docs commit); counts read from `.harness/gate-*.log`. This evidence commit touches only `docs/evidence/`.

```
bash scripts/harness/gate-segment.sh static
bash scripts/harness/gate-segment.sh unit
bash scripts/harness/gate-segment.sh build
bash scripts/harness/gate-segment.sh verify
static: ruff check "All checks passed!", ruff format --check "143 files already formatted", skill-lint "2 skills checked, 4 example file(s), 0 finding(s)"
unit:   257 passed
build:  Successfully built dist/founder_vn-0.1.0.tar.gz and dist/founder_vn-0.1.0-py3-none-any.whl
gate-segment verify: GREEN on 1bda1736b371553a6ad24d7ba0e07a4be99fab8b
```

## Giải quyết review nội bộ

Lane không tự chạy `/code-review` (steering lane-implement). Hai lượt review độc lập do harness dispatch sau khi PR mở; kết quả nằm ở `reviews/issue-12/`.

## Giới hạn

- **Skill chưa chạy bằng agent trên Kiro CLI trong sandbox.** Tiêu chí 4 của ticket ("Golden case run on Kiro CLI") chưa đóng: operator chạy `/founder-cfo` trên Kiro CLI tại máy mình trước T18 và ghi kết quả vào file này bằng một commit riêng; ticket giữ `ready-for-agent`. Ở đây `numbers.json` do lane viết từ `idea.md` và `cfo.md` do lệnh `founder-vn cfo --out` sinh, không phải do một phiên agent chạy skill. Review checklist (`docs/review-checklist.md`) mới được kiểm phần máy (`skill_lint`, không có `$`) và phần đọc của lane, chưa có lượt Kiro CLI.
- Các test của skill kiểm văn bản chỉ dẫn, không kiểm hành vi của mô hình.
- Hai mục sổ nguồn được operator kiểm chứng ngày 23/11/2026 trên bản PDF Công báo và chép nguyên văn từ comment của operator trên issue #12; lane không fetch lại nguồn (vbpl.vn trả 403, Công báo cần User-Agent trình duyệt). Lane không kiểm chứng độc lập nội dung pháp lý. Không rà thông tư của Bộ Tài chính. Hai ưu đãi tạm thời (Nghị định 174/2025/NĐ-CP; Nghị quyết 43/2026/QH16 và Nghị định 398/2026/NĐ-CP) chưa kiểm chứng, không đưa vào mô hình.
- **Phần giới hạn thuế trong `cfo.md` do skill nối vào, không do công cụ sinh.** `src/founder_vn/cfo.py` (T05) không có chỗ cho đoạn chữ này và không đổi trong lane, nên dòng "có ưu đãi tạm thời, chưa tính" và hai giới hạn của Q52 (sai lệch tối đa 20 triệu đồng mỗi năm theo hướng an toàn; trên 3 tỷ đồng TNCN tính trên thu nhập với thuế suất 17%) nằm ở phần nối. Chạy lại `founder-vn cfo --out cfo.md` ghi đè file và xóa phần nối; skill Step 6 nối lại. Việc tách tỷ lệ thành hai, cờ máy cho mốc 3 tỷ đồng và đưa phần giới hạn vào báo cáo công cụ là ticket mới sau T11 (Q52).
- Báo cáo của công cụ vẫn có đoạn "Lưu ý" nói thuế suất và ngưỡng "là số anh/chị nhập"; với skill này hai số đến từ sổ nguồn. Không đổi vì `cfo.py` ngoài phạm vi.
- Kế hoạch ở công suất mục tiêu (40 lượt mỗi ngày, khoảng 3,36 tỷ đồng mỗi năm) vượt mốc 3 tỷ đồng; năm 1 của case (2.639.000.000 đ) chưa vượt, nên số thuế năm 1 trong `cfo.md` không chịu giới hạn thứ hai, nhưng các năm sau thì có.
- Dữ liệu tổng hợp: `numbers.json` là ước tính kế hoạch từ `idea.md`, ramp là giả định; không có số liệu thật.
