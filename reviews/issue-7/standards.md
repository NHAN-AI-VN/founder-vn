Commit mã đã chấm: a442adab7b7a

# Standards review, issue #7, vòng 2

Phán quyết: PASS. Không còn finding chặn trên trục Standards.

## Phạm vi đã xét

`git diff --stat main...HEAD` và `git log --oneline main..HEAD` (từ `eee6595` đến `a442ada`). Kể từ vòng 1 (`0ea2211`) nhánh thêm bốn commit: `359ffee` (mã: `src/founder_vn/cli.py`, `tests/test_install_cli.py`), `ddb3ce2` và `a442ada` (chỉ `docs/evidence/issue-7-installer.md`), `94cb0d7` (`reviews/issue-7/ledger.md`).

Chuẩn đã đối chiếu: `AGENTS.md`, `docs/agents/standards.md` (gồm ngoại lệ installer do `68a9c1d`), `docs/agents/evidence-gates.md`, `docs/evidence/issue-7-installer.md`, `reviews/issue-7/ledger.md`, `src/founder_vn/install.py`, `src/founder_vn/cli.py`, `tests/test_install_cli.py`. Diff không chạm `skills/` ngoài `.gitkeep` nên checklist skill không áp dụng; không có `docs/adr/` hay `CONTRIBUTING.md` liên quan.

## Đóng các finding vòng 1

- S1 (ghi ngoài khoá đường dẫn): ngoại lệ đã nằm trong `docs/agents/standards.md`; `install.py` giữ trong phạm vi đó (thư mục từ `SKILL_FOLDERS`, từ chối đích resolve ra ngoài project bằng `InstallRefused` trước khi ghi, không xoá, `--print-only` không ghi).
- S2 (thiếu đỏ rồi xanh): bảng "Red by mutation" trong evidence có 7 đột biến. Đã tự chạy lại hai đột biến rồi hoàn nguyên: đổi "60 seconds" làm `test_codex_snippet_carries_the_timeout_note` và golden codex đỏ; cho CLI trả 0 khi bị từ chối làm `test_cli_refusal_exits_2` đỏ. Cây làm việc sạch sau đó.
- S3 (cờ `--skills-dir`): `359ffee` bỏ cờ khỏi CLI; `grep skills-dir` trong `src/` và `tests/` không còn kết quả. CLI luôn dùng `packaged_skills_dir()`, nên tập file ghi ra đúng như ngoại lệ mô tả. Test CLI chuyển sang patch `install.packaged_skills_dir` qua fixture autouse.

## Hình dạng vòng lặp

(a) `seam:` (`eee6595`) đứng trước mọi `slice(`. (b) Mọi commit chạm `src/` (`bbe41ed`, `1fae020`, `df19a24`, `359ffee`) đều chạm test, và có dòng trong `## Lát` (`359ffee` ở dòng "drop `--skills-dir` (S3)"). (c) Test đi qua `install.run` và CLI, đúng seam đã khai. (d) `## Cổng ba đoạn` ghi `GREEN on 94cb0d7f…`; `94cb0d7` là hậu duệ của commit mã cuối `359ffee` và các commit sau đó (`94cb0d7`, `a442ada`) chỉ chạm evidence/review, nên cổng không stale.

Chạy tại HEAD: `uv run --frozen pytest -q` được 132 passed; `uv run --frozen ruff check .` sạch; `uv run --frozen ruff format --check .` sạch.

## Chưa xác minh

- Run Gate 45103219267 báo `success` nhưng job `Gate` còn `in_progress` trong tin nhắn giao việc; chưa xác nhận kết quả cuối từ CI. Cổng CI chạy lại trọn ở commit cuối.
- `gate-segment.sh verify` không chạy lại được trong sandbox này (thiếu `.harness/gate-segments.txt`); dòng GREEN trong evidence chưa được tái tạo độc lập, chỉ có pytest và ruff chạy lại ở trên.
- Không test nào khẳng định `founder-vn install --skills-dir` bị argparse từ chối; quy tắc "nguồn là gói" chỉ được giữ bằng việc cờ không còn trong mã. Không chặn (chuẩn không đòi test cho một tham số vắng mặt), ghi để lane sau cân nhắc.
- Chưa dựng wheel để xác nhận `founder_vn/skills/.gitkeep`; dựa vào evidence và `test_pyproject_ships_skills_in_the_wheel`.

<promise>PASS</promise>
