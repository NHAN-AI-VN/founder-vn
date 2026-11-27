Commit mã đã chấm: 4d3663c8f2f6

# Review trục Spec, #163, vòng 1

Phán quyết: PASS. Không có finding chặn.

## Đối chiếu từng criterion

1. Lockstep 0.3.1: đáp ứng. `src/founder_vn/__init__.py` có `__version__ = "0.3.1"`. Mười `skills/*/SKILL.md` đều có `version: "0.3.1"` (đếm bằng grep). `python3 scripts/skill_lint.py` chạy lại ở HEAD cho `10 skills checked, 19 example file(s), 0 finding(s) (package version 0.3.1)`. Golden `tests/golden/version.json` đổi `0.3.0` thành `0.3.1`, commit `0cc3ff0` nói rõ lý do. Parity CLI/MCP chạy trong `pytest` của cổng unit: `uv run pytest tests -q` cho 502 passed ở HEAD. `uv.lock` và `pyproject.toml` không đổi. Witness lockstep được trích trong bằng chứng (một skill lùi về 0.3.0, đúng một finding, đã khôi phục). Tôi không chạy lại phần scratch edit.
2. README và `docs/hosts/README.md`: đáp ứng. Câu tiếng Anh nằm ở mục Install, câu tiếng Việt khớp. Các câu 0.3.0 hiện hành, `released, 0.3.0 on PyPI` và câu #142 giữ nguyên chữ. Không câu nào gọi 0.3.1 là "released" hay "verified". `tests/test_front_door.py` thu hẹp hai khẳng định phủ định về tag 0.3.0 và thêm khẳng định dương cho ba câu pending (EN, VI, hosts index). Test này nằm trong cổng unit và xanh.
3. `docs/hosts/kiro.md`: đáp ứng. Lệnh dry-run dùng wheel `0.3.1`. Câu "`v0.3.0` (published 2026-11-26) is the current release" và các câu #118/#142 không bị chạm. `tests/test_hosts.py` đổi cùng lát. Ngoài lệnh ticket nêu, ví dụ `args` ở bước 3 cũng đổi sang wheel 0.3.1. Đó là cùng một wheel, cùng một lệnh dry-run, và đã được ghi trong bằng chứng, nên không vượt phạm vi.
4. Cổng và bằng chứng: đáp ứng. Commit `1cf20b8` (seam) đứng trước mọi lát. `docs/evidence/issue-163-release-0-3-1-prep.md` có `## Seam`, `## Lát` (bốn hàng, mỗi hàng có khẳng định đỏ), `## Giới hạn` (không tag, không publish PyPI, không cài sạch, không chạy skill, không host nào được xác minh trên 0.3.1). CI `Gate` success. Phần `verify` trong bằng chứng ghi GREEN ở `fab92e0`, và commit sau đó chỉ thêm file bằng chứng.

## Phạm vi và giới hạn

Diff chỉ gồm 18 file đúng với seam. Không có thay đổi ở `release.yml`, `permits/sources.md`, hành vi skill hay `uv.lock`. Các câu #142/#118 không bị viết lại.

## Chưa xác minh

- Lần chạy scratch edit của witness lockstep và các lần đỏ của từng lát chỉ được đọc từ file bằng chứng. Tôi không dựng lại chúng.
- Tôi không chạy lại `gate-segment.sh build` và `verify`. Tôi dựa vào bằng chứng và CI.

<promise>PASS</promise>
