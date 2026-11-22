Commit mã đã chấm: 52bb5ea825e3

# Review trục Spec, issue #3, vòng 1

**Phán quyết**: PASS. Không có finding chặn.

Phạm vi: `git diff --stat main...HEAD` (14 file, 529 dòng thêm) và 5 commit từ `main..HEAD`. Đã đọc từng file trong diff và đối chiếu với `docs/founder-vn-design.md` §4 và §5. Chạy `uv run pytest tests/test_front_door.py -q`: 11 passed. Các test này nằm trong `tests/`, nên cổng `unit` (pytest) chạy chúng.

## Đối chiếu từng criterion

| Criterion | Bằng chứng | Kết quả |
|---|---|---|
| README tiếng Anh + mục tiếng Việt: mục đích, đối tượng, host, hai đường cài, ghi công (tác giả, nguồn, commit), bảng trạng thái giữ chỗ | `README.md`: các mục "Who it is for", "Supported hosts", "Install" (bảng 3 route, ghi rõ chưa phát hành), "Status" (hàng placeholder), "Credit" (Jake Schincariol, URL, commit `fd9385b0...`), "Tiếng Việt". Test `test_readme_*` | Đạt |
| LICENSE MIT, giữ thông báo MIT của upstream | `LICENSE`: thông báo founder-vn, rồi nguyên văn MIT của Jake Schincariol. Test `test_license_is_mit_and_keeps_the_upstream_notice` | Đạt |
| CONTRIBUTING: quy tắc cứng + định nghĩa "xong" của skill | `CONTRIBUTING.md` mục "The hard rule" và "Definition of done for a skill" (golden-case, tests, checklist). Khớp §5 của thiết kế | Đạt |
| Mẫu issue "Law changed" với 4 trường | `.github/ISSUE_TEMPLATE/law-changed.yml`: what_changed, source_link, effective_date, affected_skill, cả bốn `required`. Test kiểm id của trường | Đạt |
| Quy ước skill: frontmatter, ngôn ngữ | `docs/skill-conventions.md`: bảng trường (`name`, `description` có cụm kích hoạt tiếng Việt, `license`, `metadata.version` = phiên bản package, `metadata.author/source/commit`), ví dụ, mục "Language" (hướng dẫn tiếng Anh, đầu ra cho Owner tiếng Việt, "anh/chị", không `$`) | Đạt |
| Khối protocol dùng chung | `docs/skill-conventions.md` mục "Shared protocol": đủ 5 quy tắc (kiểm version bằng `server_info` hoặc `founder-vn --version`, dừng khi lệch major; ưu tiên MCP, rồi CLI, rồi dừng và in hướng dẫn cài; không tự tính số; không trả lời thay người mua; không viết verdict). Test `test_shared_protocol_block_carries_the_five_rules`. `src/founder_vn/cli.py` có `--version`, nên lệnh trong khối là thật | Đạt |
| Checklist rà soát | `docs/review-checklist.md`: 5 mục (không `$`, không lọt tiếng Anh, mọi khẳng định có link, có miễn trừ, có cảnh báo panel). Khớp §5 của thiết kế. Test `test_review_checklist_has_the_five_items` | Đạt |
| Chỉ mục host + một trang stub mỗi host | `docs/hosts/README.md` liệt kê 6 host; có `claude.md`, `codex.md`, `gemini.md`, `grok.md`, `kirocrew.md`, và `kiro.md` đã có sẵn trên `main`. Test `test_hosts_index_links_one_existing_page_per_host` kiểm link trỏ tới file có thật | Đạt |

Ràng buộc đã kiểm: không có `$` trong README và `docs/hosts/`; các trang host chỉ nêu tên biến `FOUNDER_LLM_*`, không có giá trị; không có tên người hay địa điểm thật; README và CONTRIBUTING tiếng Anh với một mục tiếng Việt, đúng bảng ngôn ngữ ở §4. Ticket không có artefact Owner-facing nào (không `examples/`, không báo cáo), nên không có mục nào để chấm về VND hay cảnh báo panel ngoài checklist và README tiếng Việt, và README tiếng Việt có câu miễn trừ.

## Quan sát không chặn (không gắn mã)

- `CONTRIBUTING.md` mục "Definition of done" đặt thêm hai chi tiết thiết kế không có trong §5: golden file nằm dưới `tests/golden/` hoặc `examples/`, và evidence phải ghi tên model và prompt hash. Ticket chỉ yêu cầu "golden-case run, tests, review checklist". Hai chi tiết này nên được operator xác nhận khi ticket skill đầu tiên dùng đến; chúng không làm hỏng criterion nào.
- `docs/evidence/issue-3-front-door.md` nêu giới hạn đúng thực tế: `skill_lint` chạy trên 0 skill nên ví dụ frontmatter và khối protocol chưa qua linter.

## Chưa xác minh

- Mẫu issue chưa được GitHub render; test chỉ kiểm id trường dạng văn bản.
- Kết quả CI của `Gate` ở commit này trong tin nhắn mở đầu ghi `Gate: in_progress`, chưa có kết luận cuối. Tôi chỉ chạy lại `tests/test_front_door.py` ở máy cục bộ, không chạy ba đoạn của cổng.
- Chất lượng câu chữ tiếng Việt chỉ được đọc bằng mắt; không có test nào chấm nó.

<promise>PASS</promise>
