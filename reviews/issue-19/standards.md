Commit mã đã chấm: a65a6fd96e9e

# Review trục Standards, issue #19, vòng 2

Phán quyết: PASS (không còn finding chặn).

## Phạm vi đã xét

`git diff --stat main...HEAD`: `README.md`, `docs/evidence/issue-19-wave-a-walkthrough.md`, `docs/hosts/README.md`, `docs/hosts/kiro.md`, `tests/test_front_door.py`, `tests/test_hosts.py`, cùng các file `reviews/issue-19/`. Không có file nào dưới `src/`, `skills/`, `examples/`, nên các mục khoá đường dẫn, parity CLI/MCP, fake provider, số mặc định, thuế hardcode và checklist skill không bị diff chạm tới.

Chuẩn đã đối chiếu: `AGENTS.md`, `docs/agents/standards.md`, `docs/agents/evidence-gates.md`, `docs/agents/parallel-lanes.md`.

Đã chạy lại ở `a65a6fd`: `uv run pytest tests/test_hosts.py tests/test_front_door.py -q` cho 22 passed; `ruff check` sạch; `ruff format --check` sạch (204 file). CI `Gate` ở `a65a6fd96e9e`: success.

## S1 của vòng 1: đã sửa

- `docs/hosts/kiro.md` (commit `0f422f3`): ba chỗ cũ ("works once the `v0.2.0` release ... is published", "Before the `v0.2.0` tag", "After the tag", "Before the tag, put the wheel path") đã đổi sang trạng thái đã phát hành (PyPI, 2026-11-24); đường dẫn wheel chỉ còn là biến thể cục bộ cho phát triển. `grep` không còn cụm "tag", "pending", "to come", "will be", "not yet" nào trên trang.
- Có test ghim: `tests/test_hosts.py:106-109`, assertion mới trong `test_kiro_page_has_the_clean_install_walkthrough_for_19`, cấm `Before the ... tag`, `once the \`v0.2.0\``, `after the tag`. Dòng đỏ có trong `## Lát` của file bằng chứng (hàng thứ tư), kèm lần chạy xanh ở `0f422f3`.

## Hình dạng vòng lặp (`git log --stat main..HEAD`)

- (a) `20788c7 seam:` mang `## Seam`, đứng trước mọi commit `slice(`. Đạt.
- (b) Không commit nào chạm `src/`. Các commit `slice(` (`43c6553`, `e625d2b`, `c8cfaf8`) chạm test và có dòng `## Lát`; commit sửa `0f422f3` chạm `tests/test_hosts.py` và có dòng `## Lát`. Đạt.
- (c) Test nằm ở seam đã khai (bảng README, trang host, file bằng chứng). Đạt.
- (d) `## Cổng ba đoạn` ghi `gate-segment verify: GREEN on 0f422f3f80d6b5fa76cec559419be4877b22c667`. `0f422f3` là commit mã cuối: `git diff --stat 0f422f3 HEAD` chỉ chạm `docs/evidence/issue-19-wave-a-walkthrough.md` và `reviews/issue-19/ledger.md`, không có `src/` hay test. Cổng không stale. Đạt.

## Chưa xác minh

- Số liệu trong file bằng chứng (giờ từ mtime, `kiro-cli 2.37.1`, run 45354393229, issue #93 #94 #95) là lời khai của operator; không có credential tới GitHub API nên không đối chiếu được.
- Nội dung phiên Kiro CLI (bước 8) là bản chép của operator; không có automated seam cho skill.
- Các dòng log cổng (`.harness/gate-*.log`) không nằm trong git, nên chỉ đọc được qua khối trích trong file bằng chứng.

<promise>PASS</promise>
