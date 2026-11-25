Commit mã đã chấm: 284a8efcdced

# Review trục Standards, issue #19, vòng 1

Phán quyết: CHANGES_REQUESTED (một finding chặn, lane sửa được).

## Phạm vi đã xét

`git diff --stat main...HEAD`: `README.md`, `docs/evidence/issue-19-wave-a-walkthrough.md`, `docs/hosts/README.md`, `docs/hosts/kiro.md`, `tests/test_front_door.py`, `tests/test_hosts.py`. Không có file nào dưới `src/`, `skills/`, `examples/`, nên các mục khoá đường dẫn, parity CLI/MCP, fake provider, số mặc định, thuế hardcode và checklist skill không bị diff chạm tới.

Chuẩn đã đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (Git, Tests, Owner-facing output), `docs/agents/evidence-gates.md` (Documentation, Where evidence lives), `docs/agents/parallel-lanes.md` (README.md là file một-chủ).

Đã chạy lại: `uv run pytest tests/test_front_door.py tests/test_hosts.py -q` cho 22 passed. CI `Gate` ở `284a8efcdced`: success.

## Hình dạng vòng lặp (`git log --stat main..HEAD`)

- (a) `20788c7 seam:` mang `## Seam` và đứng trước mọi commit `slice(`. Đạt.
- (b) Không commit nào chạm `src/`. Mỗi commit `slice(` chạm test (`43c6553`, `e625d2b`, `c8cfaf8`) và có dòng trong `## Lát` (ba dòng, mỗi dòng có câu assertion đỏ và lần chạy xanh). Đạt.
- (c) Test nằm ở seam đã khai (bảng truth table README, trang host, file bằng chứng). Đạt.
- (d) `## Cổng ba đoạn` ghi `verify: GREEN on c8cfaf82…`; `c8cfaf8` là commit mã cuối (`284a8ef` chỉ sửa file bằng chứng). Cổng không stale. Đạt.
- `README.md` là file một-chủ; bằng chứng ghi comment cấp phát của operator trên #19 và việc operator tự áp patch. Không phải finding.

## Finding chặn

### S1: `docs/hosts/kiro.md` còn nói bản phát hành "chưa có" ngay trong bước lane vừa viết lại

- Chỗ: `docs/hosts/kiro.md`, đoạn "`uvx --from founder-vn founder-vn-mcp` resolves the package from PyPI, so it works once the `v0.2.0` release ... is published" (dưới khối `mcp.json`, dòng 29-30), và bước 2 (dòng 54, "Before the `v0.2.0` tag (wheel built with `uv build` ...") và bước 3 (dòng 67-68) của "Clean-install walkthrough": "Before the tag, put the wheel path in `args` in place of the package name ...".
- Sai gì: diff này đổi `README.md`, `docs/hosts/README.md` và chính bước 3 (thêm câu về #94) để nói `v0.2.0` đã lên PyPI ngày 2026-11-24, nhưng các câu trên vẫn nói tag chưa tồn tại. Một người đọc trang Kiro nhận hai trạng thái khác nhau cho cùng một bản phát hành. Không test nào ghim hai câu này, nên `tests/test_hosts.py` vẫn xanh.
- Chuẩn: `docs/agents/evidence-gates.md`, "Select validation" (với tài liệu, kiểm tra các tham chiếu và trạng thái, "raw-text check does not prove..."), và ý "một nguồn, con trỏ ở nơi khác" của luật 2 cùng file: một trạng thái phát hành không được sống ở hai chỗ nói ngược nhau. Cũng là loại "tên/khẳng định nói một điều mà thực tế khác" trong hướng dẫn review.
- Vì sao chặn: lane này tuyên bố "bảng sự thật của README đúng" và là lane ghi nhận bản phát hành; trang host chính của host đã xác nhận không được tự mâu thuẫn với bảng đó.
- Cách sửa (commit bổ sung, không viết lại lịch sử): sửa ba câu về thì đã phát hành (bỏ "Before the tag" hoặc đổi thành đường dẫn wheel cục bộ chỉ dành cho phát triển trước khi có bản trên PyPI), thêm một assertion vào `test_kiro_page_has_the_clean_install_walkthrough_for_19` (đỏ trước, xanh sau) cấm `Before the` + `tag` và `once the` trên trang, rồi chạy lại ba đoạn cổng và cập nhật SHA trong `## Cổng ba đoạn`. File thuộc cấp phát của lane, không cần file một-chủ, nên không phải BLOCKED.

## Chưa xác minh

- Các số liệu trong bảng bằng chứng (giờ từ mtime, phiên bản `kiro-cli 2.37.1`, run 45354393229, các issue #93 #94 #95 đã mở) đến từ lời khai của operator; không có credential tới GitHub API ở đây nên không đối chiếu được. Không gắn mã.
- Nội dung phiên Kiro CLI (bước 8) là bản chép của operator; không có automated seam cho skill (spec #1).

<promise>CHANGES_REQUESTED</promise>
