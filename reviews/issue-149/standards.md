Commit mã đã chấm: 42bb26bdd28b

# Review trục Standards, #149, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Phạm vi đã xét

`git log --oneline main..HEAD`: `105b81f` seam, `67218ff` slice(front-door), `42bb26b` docs (evidence). `git diff --stat main...HEAD`: `README.md`, `docs/hosts/README.md`, `docs/hosts/kiro.md`, `tests/test_front_door.py`, `tests/test_hosts.py`, `docs/evidence/issue-149-release-0-3-1.md`. Không có thay đổi ở `src/`, `skills/`, `examples/`.

Chuẩn đối chiếu: `docs/agents/standards.md`, `docs/agents/evidence-gates.md` (mục hình dạng bằng chứng và vòng lặp seam/slice/cổng), `AGENTS.md`. CI `Gate` ở `42bb26bdd28b`: success.

## Kết quả theo chuẩn

- Hình dạng vòng lặp (a): `105b81f` (`seam:`, chỉ chạm file bằng chứng, 16 dòng gồm `## Seam`, ghi là suy ra từ tiêu chí) đứng trước commit `slice(` duy nhất `67218ff`.
- (b): `67218ff` không chạm `src/` (chỉ tài liệu và hai file test); dòng tương ứng có trong `## Lát`.
- (c): test nằm ở seam đã khai (mục 4 của `## Seam`: `tests/test_front_door.py::test_readme_truth_table_is_honest_about_release_status_and_hosts` và `tests/test_hosts.py::test_kiro_page_has_the_clean_install_walkthrough_for_19`), đều là test trên văn bản front door, không chạm internals.
- (d): khối `## Cổng ba đoạn` ghi `verify` GREEN ở `67218ff8bd2b`, là commit mã cuối; commit sau (`42bb26b`) chỉ chạm file bằng chứng nên cổng không stale.
- Bằng chứng đỏ rồi xanh: bảng `## Lát` ghi dòng assertion lúc đỏ và lần chạy xanh.
- Checklist skill: diff không chạm `skills/` hay `examples/`, mục này không áp dụng. Diff không có `$` cạnh chữ số.
- Không số mặc định thay lỗi, không tỷ lệ thuế hay ngưỡng hardcode, không biến `FOUNDER_LLM_*` trong diff, không test gọi mạng thật (các test chỉ đọc file văn bản).
- Khẳng định "verified": README giữ "verified on 0.3.0" và có assertion `"verified on 0.3.1" not in kiro_row`, khớp lựa chọn của bản thiết kế §5 mà bằng chứng viện dẫn.
- File một-chủ: bằng chứng ghi `README.md` được cấp phát trong comment phân lane của operator; ghi rõ ngoại lệ guard ở mục `## Giới hạn`.

## Chưa xác minh

- Các sự kiện phát hành (tag `v0.3.1`, Build, phê duyệt, sha256 trên PyPI, cài sạch, chạy lại `founder-permits` và `founder-cfo`) do operator chứng kiến bằng tay; reviewer không có quyền kiểm lại PyPI hay Actions của lượt chạy đó và không kiểm lại. Đây thuộc trục Spec.
- Không chạy lại bộ test cục bộ; dựa vào CI `Gate` success ở commit này và khối cổng trong bằng chứng.
- Không đối chiếu từng dòng `docs/founder-vn-design.md` §2–§5 ngoài khẳng định "verified" ở trên.

<promise>PASS</promise>
