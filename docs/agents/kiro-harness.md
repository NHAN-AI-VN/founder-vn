# Harness Kiro: lane không người trông trên Kiro Web và GitHub Actions

**Phiên bản** 0.4 · **Ngày** 2026-11-23 · **Trạng thái** loop đang chạy: bốn lane (#2 T01, #3 T02, #4 T03, #6 T05) merge bằng máy trong ngày 2026-11-22 (FV-M-7); lane #7 (T10) qua điểm dừng BLOCKED đầu tiên (operator trả lời S1 bằng commit trên nhánh lane, FV-D16 ghi hai sửa nhỏ từ đó); `main` được GitHub bảo vệ (yêu cầu PR, 0 approval, không force-push/xoá, H-8); `HARNESS_DISPATCH=on`. Đây là tài liệu quy tắc của harness; luật về chuẩn mã, bằng chứng, lane song song và tracker thuộc `docs/agents/standards.md`, `evidence-gates.md`, `parallel-lanes.md`, `delivery-workflow.md`, `issue-tracker.md`. Bản thiết kế sản phẩm là `docs/founder-vn-design.md`.

**Nguồn**: port từ harness của `NHAN-AI-VN/nhan` tại commit `8adef66b105d92215a70281ae10fa0f9648faaf1` (2026-09-13), đã qua khoảng 50 lane thật ở đó. Mỗi khẳng định về hành vi của Kiro mang một trong ba nhãn: **[đã đo]** chạy thật trên repo này, **[tiền nhiệm]** đo ở `nhan` (Kiro Web, 2026-09) và chưa đo lại ở đây, **[tài liệu]** đọc từ kiro.dev và chưa đo. Bảng ở mục 6 là nơi nhãn đổi. Những gì `nhan` có mà repo này bỏ, và vì sao, ở mục 9.

## 1. Năm thành phần

Phần quyết định là máy, phần suy nghĩ là agent. Không thành phần agent nào giữ credential ghi tới tracker hay quyền merge.

| # | Thành phần | Chạy ở | Kích hoạt | Việc |
|---|---|---|---|---|
| C1 | Dispatcher | `.github/workflows/frontier-dispatch.yml` chạy `scripts/harness/dispatch.sh`; cùng quyết định chạy inline ở cuối mỗi run `Gate` của PR, sau mỗi merge máy, và trong mỗi lượt quét của `after-gate.yml` | `issues` closed/unlabeled do operator làm tay; `workflow_dispatch`; cron quý giờ của `after-gate.yml` (`7,22,37,52`, đồng hồ duy nhất của harness, FV-D5/FV-D16) | Chạy witness; đối chiếu lane đang chạy; tính frontier từ cạnh `blocked_by` native (ticket `ready-for-agent`, không `ready-for-human`, không sub-issue, không blocker mở, không assignee); giữ `HARNESS_WIP`; ghi comment cấp phát `/kiro` bằng token operator; gắn nhãn `kiro` bằng `GITHUB_TOKEN`; gọi lại lane im lặng; nhận nuôi nhánh đã xong (mở PR); park lane BLOCKED/stalled. Khi operator gỡ `harness:blocked` khỏi ticket có PR lane đang mở, nó gọi bộ điều phối review (C4) cho nhánh ấy |
| C2 | Lane implement | Kiro Web autonomous task | comment `/kiro` của dispatcher trên issue; nhãn `kiro` chỉ là dấu lane đang chạy | Đọc `AGENTS.md`, `.kiro/steering/lane-implement.md`, skill `implement` → `tdd`; cài uv, `uv sync --frozen`, `install-hooks.sh`; commit `seam:` rồi từng `slice(`; hook post-commit push từng commit; cổng ba đoạn + `verify`; bằng chứng `docs/evidence/`; mở PR qua `open-lane-pr.sh` |
| C3 | Gate | `.github/workflows/gate.yml`, một job | `pull_request`, `push` lên `main`, `workflow_dispatch` | `uv sync --frozen`, `ruff check`, `ruff format --check`, `pytest`, `uv build` (khi `pyproject.toml` có ở HEAD; chưa có thì skip có log), `skill_lint.py`, `check-doc-paths.sh`, hai chế độ witness khi PR chạm harness, bước `Heavy gates passed`; rồi bước đuôi C4 → C5 → C1 trên PR với script lấy từ `origin/main`. Harness nhận diện Gate bằng **file** `gate.yml` (REST `actions/runs?head_sha=` lọc theo `path`), không bằng tên hiển thị |
| C4 | Reviewer và address | Bước đuôi của job `Gate` và job của `after-gate.yml`, chạy `scripts/harness/review-web.sh` (quyết định thuần ở `review-web.jq`, tin nhắn ở `review-web-turn.sh`). **Không lượt model nào chạy trên runner**: mỗi lượt là một session Kiro Web mở bằng comment `/kiro` do harness đăng với token operator trên issue review của lane (`Review #<n> — Standards`, `— Spec`, `— Address`, nhãn `harness:turn`, mỗi issue một session có ký ức); tin nhắn tự chứa: giá trị của lane, kết quả `Gate` ở HEAD, thân ticket, rồi nguyên văn `.kiro/prompts/<trục>.md` trên `main` | Cùng tập trigger với C5 | Tính **commit mã** (`lane-code.sh`: commit cuối ở HEAD chạm gì ngoài hai báo cáo và ledger), coi một báo cáo là hiện hành khi ghi sau commit mã; thiếu báo cáo hiện hành thì ra lệnh trục ấy (hai trục song song); PASS/PASS thì ghi nhận và để merger; `CHANGES_REQUESTED` hay Gate đỏ thì ra lệnh lượt sửa, tối đa hai vòng; PR xung đột với `main` thì ra lệnh lượt đồng bộ; `BLOCKED`, hết vòng, hay lượt không push gì sau hai lần ra lệnh (mỗi lần chờ 120 phút) thì gắn `harness:blocked`, gỡ `kiro`, comment lên PR. Mỗi lệnh mang dấu `<!-- harness:turn axis= code= head= round= at= -->`; trần 14 lượt một lane; biến repo `HARNESS_WEB_REVIEW=off` tạm dừng |
| C5 | Merger | Bước đuôi của job `Gate` và job của `after-gate.yml`, chạy `scripts/harness/merge-check.sh`, quyết định ở `merge.jq` | Như C4 | Merge khi bốn điều kiện ở `docs/agents/delivery-workflow.md` "Who merges" cùng đúng ở HEAD: run `Gate` mới nhất ở đúng HEAD đã hoàn thành và success (không có run là chưa xanh); hai báo cáo PASS và **hiện hành**; ledger đóng mọi mã finding của mọi vòng; `Closes #<n>` đúng ticket được cấp, nhánh `lane/issue-<n>`, ticket mở, không blocker mở, không từ khoá đóng issue lạ ở bất kỳ vị trí nào trong thân PR hay commit message. PR harness: tác giả là operator và có nhãn `harness:auto-merge`, không check đỏ hay đang chạy. Một merge mỗi lần chạy; kiểm `state == MERGED` trước khi đóng ticket; đóng ticket (`completed`), gỡ `kiro`, đóng issue review không kèm comment; chạy lại dispatcher inline |

## 2. Vòng đời một lane

```
ready-for-agent, không sub-issue, blocker đóng hết, chưa ai nhận
  → C1 ghi comment cấp phát `/kiro`, gắn `kiro`                     (in flight)
  → Kiro Web task: nhánh lane/issue-<n>, seam, slices (push từng commit), cổng ba đoạn,
      bằng chứng, PR "Closes #<n>" qua open-lane-pr.sh
      hoặc comment kết thúc bằng <promise>BLOCKED</promise>        → C1 đổi `kiro` thành `harness:blocked`
      hoặc im lặng: đã nhận, không PR và nhánh không push sau cửa sổ (60 phút; 45 phút khi
        nhánh đã có file bằng chứng) → C1 gọi lại (cùng session) tối đa 4 lần khi mỗi lần gọi
        có tiến triển, một lần khi không; im nữa → `harness:stalled`
      hoặc nhánh đã có bằng chứng ghi `verify` GREEN, im 10 phút, chưa PR → C1 mở PR (adopt)
  → C3 Gate ở đúng HEAD của PR
  → C4 ra lệnh; session Kiro Web review standards + spec trên nhánh lane → PASS/PASS,
      hoặc session sửa (≤ 2 vòng) push rồi C4 ra lệnh review lại,
      hoặc PR xung đột với main: session đồng bộ merge main vào lane rồi push
  → C5 merge, đóng ticket và issue review → C5 gọi C1 → frontier tiến
```

Merge bằng `GITHUB_TOKEN` không đóng ticket `Closes #n` và không phát sự kiện `issues.closed` cho workflow khác [tiền nhiệm], nên C5 tự đóng ticket rồi chạy C1 inline; cron quý giờ (`7,22,37,52`, FV-D16) của `after-gate.yml` là lưới an toàn cho lane im lặng (không phát sự kiện nào). GitHub chạy cron thưa hơn ghi nhiều: `nhan` đo 2–4,6 giờ một lần trên tổ chức gói Free [tiền nhiệm], ở đây đo 4–5 giờ một lần với `*/15` (FV-M-8); FV-D5 chấp nhận độ trễ ấy.

Frontier xếp ticket đã có nhánh `lane/issue-<n>` lên trước (lane được gọi lại giữ chỗ), rồi nhãn `priority`, rồi số nhỏ nhất. Một lane "in flight" khi issue mở còn nhãn `kiro` và Kiro đã trả lời hoặc chưa quá cửa sổ chờ, hoặc một PR mở có `Closes #<n>` trỏ tới ticket mở. `HARNESS_WIP` = 1.

Ticket mang `harness:blocked` là điểm dừng cho người: C4 không ra lệnh lượt nào cho tới khi operator commit lên nhánh lane và gỡ nhãn; C5 vẫn đọc phán quyết ở HEAD như thường, nên PR đã PASS/PASS vẫn merge. Operator không comment lên issue còn nhãn `kiro` và không comment lên issue review: Kiro Web phản ứng với hoạt động của người trên các issue ấy [tiền nhiệm].

Tín hiệu và nơi đặt chúng: lane kết bằng `<promise>COMPLETE</promise>` ở mục *Outcome* của PR, hoặc `<promise>BLOCKED</promise>` ở dòng cuối comment trên issue kèm câu hỏi `- [ ]`. Lượt review và sửa đặt tín hiệu ở dòng cuối file báo cáo trên nhánh lane; C4 và merger đọc file ở HEAD, không đọc câu trả lời, fail-closed: thiếu tín hiệu hay tín hiệu khác PASS là chưa xong.

## 3. Cấp phát

Dispatcher ghi đúng một comment mở đầu bằng `/kiro`, chứa dòng `<!-- harness:allocation -->` và bảng khoá giá trị; comment ấy là lệnh mở session và được ghi bằng `HARNESS_DISPATCH_TOKEN`, token fine-grained của tài khoản operator với quyền Issues read/write, Pull requests read/write (mở PR cho lane đã xong) và Contents read (GitHub từ chối tạo PR từ nhánh mà token không đọc được, "not all refs are readable" [tiền nhiệm]). Thiếu token thì `--apply` từ chối dispatch thay vì gắn một nhãn không ai nhận. Nhãn `kiro` gắn ngay sau đó bằng `GITHUB_TOKEN`: Kiro bỏ qua nhãn do bot gắn, còn nhãn do người gắn mở hai session [tiền nhiệm], nên nhãn chỉ là dấu lane in flight.

| Khoá | Ý nghĩa |
|---|---|
| `singleOwnerFiles` | `all`, `none`, hoặc danh sách glob cách nhau bằng dấu phẩy; tập con của "One owner per merge" trong `docs/agents/parallel-lanes.md`. Với `HARNESS_WIP` bằng 1 dispatcher cấp `all` |
| `laneBranch` | `lane/issue-<n>` |
| `targetBranch` | `main` |
| `dispatchedAt` | RFC 3339 UTC |

Không có `migrationTimestamp`: dự án này không có migration (khác `nhan`).

## 4. Guards

Một script, `.kiro/hooks/guard.sh`, nối vào hai chỗ: `.kiro/hooks/guard.json` (hook v1) và trường `hooks.preToolUse` của `.kiro/agents/founder-guarded.json`. **Nó chạy trên Kiro CLI [đã đo, FV-M-1] và không chạy trong sandbox Kiro Web [đã đo, FV-M-6]**: ở đó đọc `.env` và `git push origin HEAD:main --dry-run` đều đi qua. Vì vậy trên Kiro Web các luật của guard là luật lane tự giữ (comment cấp phát và tin nhắn lượt review nói rõ), lượt review Standards coi vi phạm là finding chặn, và nhánh `main` được GitHub bảo vệ (H-8) để không push thẳng được. Hợp đồng hook: exit 0 cho phép, exit 2 chặn và trả stderr cho model; mọi mã khác chỉ cảnh báo rồi **cho phép**, nên mọi đường từ chối của script đều kết bằng exit 2, kể cả lỗi nội bộ và trường hợp không tìm thấy script.

| Luật | Áp lên | Từ chối |
|---|---|---|
| Đường dẫn và tên bí mật | Giá trị các khoá `path`, `file_path`, `filePath`, `paths`, `directory`, `cwd`, `command`, `cmd`, `script`; hoặc toàn bộ input khi không trích được khoá nào | `.env*` (trừ `.env.example`), `.pypirc`, `.aws/credentials`, `.ssh/id_*`; lệnh shell nêu `FOUNDER_LLM_API_KEY`, `PYPI_TOKEN`, `PYPI_API_TOKEN`, `UV_PUBLISH_TOKEN`, `TWINE_PASSWORD`, `KIRO_API_KEY`, `GITHUB_TOKEN`, `GH_TOKEN`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `NPM_TOKEN`, hoặc `printenv`/`env` trần |
| Git được bảo vệ | Lệnh shell trích được; hoặc toàn bộ input khi tên tool chứa `bash`/`shell` | push tới `main`/`master` kể cả dạng refspec, `--force`, `--delete`, `--mirror`, refspec rỗng nguồn, `git branch -D main`, `gh pr merge`, `pulls/<n>/merge` |
| File một-chủ | Giá trị các khoá đường dẫn | Ghi vào file khớp một mục của "One owner per merge" mà `HARNESS_SINGLE_OWNER_FILES` không cấp (`all`, `none`, hoặc danh sách glob; không đặt là `none`) |

Điểm mù khai sẵn: guard lọc chuỗi trong input của tool, không phải ranh giới chứa; `cat .en*` hay một script đọc file không bị chặn. Luật git chỉ chạm lệnh shell, nên một tài liệu nhắc tới `gh pr merge` vẫn ghi được. Luật file một-chủ chưa có kênh cấp phát tới sandbox Kiro Web (mục 8), nên ở đó nó chỉ có hiệu lực khi danh sách rỗng hoặc lane không chạm file trong danh sách; với `WIP=1` dispatcher cấp `all`.

Witness: `bash scripts/harness/witness.sh` chạy guard với các input mẫu và đòi đúng mã thoát cho từng luật, rồi ở chế độ `--witness-red` đột biến từng cơ chế và đòi phép kiểm đỏ. Trên CI: chế độ thường ở mỗi run của C1 và quét của `after-gate.yml`; cả hai chế độ trong job `Gate` khi PR chạm `scripts/harness/**`, `scripts/skill_lint.py`, `.kiro/**`, `.githooks/**` hay một workflow. Hôm 2026-11-22: 222 ca, 108 đột biến, đủ bị bắt.

## 5. Cấu hình sống ở đâu

| Đường dẫn | Bề mặt đọc | Ghi chú |
|---|---|---|
| `AGENTS.md` | Kiro Web, CLI, IDE, luôn nạp | Luật đè mặc định vendor; tín hiệu |
| `.kiro/steering/lane-implement.md` | Kiro Web, IDE (`inclusion: always`); CLI qua agent nạp file | Quy trình lane cho Python/uv |
| `.kiro/prompts/*.md` | Nguyên văn trong comment `/kiro` của C4 (`review-web-turn.sh` đọc từ `main`) | Hướng dẫn của reviewer, address, sync; không phải steering để Kiro Web không nạp vào task implement |
| `.kiro/agents/founder-guarded.json` | CLI làm agent chính | `kiro-cli agent validate --path` chấp nhận [đã đo] |
| `.kiro/hooks/guard.json` và `guard.sh` | Kiro Web, IDE, CLI | Mục 4 |
| `.kiro/skills/*` | Symlink tới `.agents/skills/*` (27 skill mattpocock, MIT, commit) | `check-skill-links.sh` kiểm; `founder-*` upstream và ID8Labs bị ignore theo tên |
| `.githooks/post-commit`, `pre-commit` | Checkout của lane sau `install-hooks.sh` | Push từng commit trên `lane/issue-*`; `ruff format --check` file staged |
| `scripts/harness/` | GitHub Actions và máy local | bash và jq. `dispatch.sh` + `frontier.jq` + `adopt.jq` + `verify-pick.jq` là C1; `review-web.sh` + `review-web.jq` + `review-web-turn.sh` + `ci-jobs.jq` là C4; `merge-check.sh` + `merge.jq` là C5; `gate-segment.sh` + `run-logged.sh` là cổng sandbox; `open-lane-pr.sh`, `lane-pr-body.sh`, `lane-code.sh`, `check-skill-links.sh`, `check-doc-paths.sh`, `install-hooks.sh`; `witness.sh` chứng kiến tất cả; `setup-wizard.sh` cho mục 7 |
| `scripts/skill_lint.py` | Gate, cổng `static`, witness | Nửa máy của checklist rà soát skill (FV-D2) |
| `.github/workflows/gate.yml`, `frontier-dispatch.yml`, `after-gate.yml` | GitHub Actions | C3 (+ đuôi C4/C5/C1), C1, C4+C5+C1 |
| `reviews/issue-<n>/`, `docs/evidence/` | Hiện vật của lane | Commit trên nhánh lane |
| Secret `HARNESS_DISPATCH_TOKEN`, variable `HARNESS_WEB_REVIEW`, variable `HARNESS_DISPATCH` | Actions | Mục 7; `HARNESS_DISPATCH` là công tắc lane mới (FV-D13) |

## 6. Phép đo

| Mã | Câu hỏi | Cách đo | Kết quả |
|---|---|---|---|
| FV-M-1 | Guard có chạy trên Kiro CLI qua `.kiro/hooks/guard.json` không | Phiên dựng harness này, 2026-11-22, trên Kiro CLI | **[đã đo] Có.** Hai lệnh shell của chính phiên này bị chặn exit 2 (một nêu đường dẫn `.pypirc` trong commit message, một nêu tên biến `PYPI_TOKEN`); commit message phải đi qua file |
| FV-M-2 | Gate trên cây chưa có package | Run 44992554432 trên PR #21 | **[đã đo]** success; `no pyproject.toml at HEAD: Python gates skipped`; skill-lint `0 skill checked`; witness xanh hai chế độ (lúc đó 67 ca, 29 đột biến). Run đầu 44992423679 đỏ ở `Set up job`: `astral-sh/setup-uv` không có tag trôi `v10`, ghim commit `1db35dd8` (v10.4.0) |
| FV-M-3 | Frontier trên tracker thật | `dispatch.sh` khô, 2026-11-22 | **[đã đo]** Lần đầu chọn **#1** (spec, 19 sub-issue, mang `ready-for-agent`, không blocker); sau FV-D10 (bỏ issue có sub-issue) frontier `[2,3,4]`, pick #2. 17 issue mang `ready-for-agent` (gồm #1), 3 `ready-for-human` |
| FV-M-4 | Token OAuth của `gh` đẩy được workflow không | Push commit chứa `gate.yml`, 2026-11-22 | **[đã đo]** Bị từ chối tới khi `gh auth refresh -s workflow`; SSH không có key trên máy operator |
| FV-M-5 | Một `/kiro` của tài khoản operator mở đúng một session; ack sau bao lâu; commit đứng tên ai; session có trả lời trên issue không | Issue probe #22, comment `/kiro` lúc 07:58:49Z 2026-11-22 (đăng qua `gh` của operator, cùng tài khoản với `HARNESS_DISPATCH_TOKEN`); bằng chứng `docs/evidence/probe-m1-sandbox.md` | **[đã đo]** Đúng **một** session (`09b62147…`), ack "Taking a look…" sau **12 giây**; hai commit trên `probe/m1` lúc 07:59:41Z và 07:59:48Z (52 và 59 giây sau lệnh), tác giả `Kiro Agent <244629292+kiro-agent@users.noreply.github.com>`, không phải operator; **không có comment trả lời** trên issue sau 16 phút (harness đọc git, không đọc câu trả lời: đúng thiết kế, nhưng tín hiệu BLOCKED của lane phụ thuộc vào comment, xem mục 8) |
| FV-M-6 | Sandbox: toolchain, internet, biến `FOUNDER_LLM_*`, steering và skill nạp, guard, `/tmp`, push | Cùng probe #22 | **[đã đo]** Python 3.11.15, **`uv` 0.13.5 có sẵn**, git 2.50, jq 1.8, gh 2.95, Linux x86_64, 8 CPU, 31 GB RAM; internet mở (pypi.org 200; **vbpl.vn 403**: không phải việc của harness, nhưng skill permits sẽ gặp); ba biến `FOUNDER_LLM_*` **present** (H-2 xong); **sub-agent không thấy steering, `AGENTS.md` hay skill nào** ("danh mục skill ghi None"; file có trên đĩa, đọc bằng đường dẫn được); **guard không chạy**: đọc `.env` trả ENOENT (tool đã chạy), `git push origin HEAD:main --dry-run` chạy ("Everything up-to-date"); `/tmp` không sống qua lần gọi tool (file ghi ở bước 1 mất ở bước 8); `install-hooks.sh` đặt được `core.hooksPath`; push nhánh bằng git thành công. Hệ quả: FV-D13, FV-D14, H-8, sửa comment cấp phát và tin nhắn lượt review |
| FV-M-7 | Lane đầu (#2 T01) từ `/kiro` tới merge: thời gian, số vòng sửa, số session, chỗ nào cần người | PR #24, issue review #25–#27, 2026-11-22 | **[đã đo] 34 phút từ `/kiro` tới merge, không ai chạm mã.** `/kiro` 08:28:10Z → ack 08:28:23Z (13 s, **một** session) → `seam:` 08:30:44Z → 7 lát `slice(` 08:31–08:34Z (push từng commit) → bằng chứng → PR #24 08:35:33Z do session mở qua `open-lane-pr.sh` (tác giả `app/kiro-agent`, không phải operator) → Gate xanh → hai lượt review 08:36:27Z (mỗi trục một session) → Spec PASS 08:37:50Z, Standards `CHANGES_REQUESTED` 08:39:02Z với S1 (cổng mới không có đỏ-rồi-xanh), **S2 (lane đổi `[project].version` sang `dynamic` khiến luật phiên bản của `skill_lint.py` thành no-op: review bắt đúng một hồi quy của harness)**, S3 (tên test lệch mã) → lượt sửa 08:39:51Z, 5 commit 08:46–08:47Z (3 sửa, ledger, cổng chạy lại) → Gate xanh 08:48Z, bộ điều phối: "settling" → **cron `*/15` không nổ lần nào từ 08:25Z tới 09:03Z**, operator kích `after-gate.yml` tay 08:59:30Z → review vòng 2 PASS/PASS 09:00:52Z và 09:01:23Z → merger merge 09:02:36Z, đóng #2 và #25–#27, cấp #3 lúc 09:02:54Z (ack 09:03:02Z). Lượt sửa dùng 1/2 vòng. Lane tuân hình dạng vòng lặp dù sub-agent không nạp steering (planner chép theo lệnh cấp phát). Hệ quả: FV-D15; `ruff format` của lane định dạng lại `skill_lint.py` làm năm đột biến witness chỉ còn bắt lỗi cú pháp, nhắm lại vào thân hàm |
| FV-M-8 | Cron `*/15` của `after-gate.yml` nổ bao nhiêu lần một ngày; tin nhắn lượt review nói gì về Gate khi C4 chạy ở đuôi chính run Gate | `gh run list --workflow after-gate.yml --event schedule`, từ khi bật (2026-11-22 06:58Z) tới 02:30Z 2026-11-23; báo cáo review của lane #7 (`reviews/issue-7/standards.md`, hai vòng) | **[đã đo] 3 lần nổ trên 78 khe (3,8 %)**: 16:29:49Z, 21:56:12Z, 02:04:34Z, tức trễ 14, 11 và 4 phút so với khe `:15`/`:45`/`:00` gần nhất; khoảng cách 5,4 giờ và 4,1 giờ. Tệ hơn phép đo của `nhan` (2–4,6 giờ). Trong lúc đó loop vẫn tiến bằng sự kiện: bốn lane merge trong ngày không chờ cron lần nào (FV-D15 đóng chỗ chờ phổ biến). **Gate trong tin nhắn**: khi C4 chạy ở bước đuôi của chính run Gate (D31), API còn báo job `Gate` `in_progress` dưới dòng run `success`; reviewer của lane #7 ghi "chưa xác nhận được kết quả cuối từ CI" ở cả hai vòng. Hệ quả: FV-D16 |

Kế thừa từ `nhan` và phải đo lại trước khi tin (tất cả [tiền nhiệm], 2026-09): nhãn do bot gắn không mở session, nhãn do người gắn mở hai session (ở đây chỉ dùng `/kiro`, đã đo một session); `/kiro` thứ hai trên cùng issue nối tiếp session cũ; session chết quanh phút 60 thường ngay sau commit bằng chứng; comment của người trên issue còn nhãn `kiro` đánh thức session; merge bằng `GITHUB_TOKEN` không đóng ticket và không phát sự kiện; từ khoá `Closes #n` được GitHub đọc ở mọi vị trí trong commit message và thân PR; cron GitHub 2–4,6 giờ một lần. Khẳng định của `nhan` M-5 ("steering và AGENTS.md nạp trên Kiro Web") **không tái lập** ở đây cho sub-agent (FV-M-6); có thể planner của session vẫn nạp, chưa đo riêng.

## 7. Tiền đề do người làm và điểm dừng theo thiết kế

`bash scripts/harness/setup-wizard.sh` dẫn từng bước (`--list` để xem trước). Trước lane đầu tiên:

- **H-1** GitHub App Kiro Agent thấy repo `founder-vn` trong tổ chức `NHAN-AI-VN` (hôm 2026-11-22: `kiro-agent` đã cài cho mọi repo của tổ chức [đã đo]).
- **H-2** Project kết nối trên app.kiro.dev; biến sandbox `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL` (FV-D3); internet mở; "Create pull requests as your GitHub user" bật.
- **H-3** Token fine-grained của operator (resource owner `NHAN-AI-VN`, repo `founder-vn`, Issues RW, Pull requests RW, Contents R) làm secret `HARNESS_DISPATCH_TOKEN`. Dispatcher tiền kiểm token ở mọi lần chạy và in tài khoản nó đại diện.
- **H-4** Variable `HARNESS_WEB_REVIEW=on`.
- **H-5** Quyền Actions: ba workflow khai `permissions` tường minh nên mặc định `read` của repo không cản; PR mở bằng token operator nên không cần "Allow GitHub Actions to create and approve pull requests". Wizard chỉ báo trạng thái.
- **H-6** (cho T01) Pending publisher trên PyPI cho `founder-vn`; thiếu thì lane T01 BLOCKED đúng thiết kế ở tiêu chí phát hành.
- **H-7** Ticket #5 T04 (`ready-for-human`, `idea.md` case mẫu) chặn T11–T17: loop đứng sau khoảng chín ticket nếu chưa có.
- **H-8** Bảo vệ nhánh `main` trên GitHub (yêu cầu pull request, 0 approval, không force-push, không xoá): guard không chạy trong sandbox Kiro Web (FV-M-6), nên đây là thứ duy nhất chặn một lane push thẳng lên `main`. Merger máy merge qua PR nên không bị cản. **Đã đặt 2026-11-22 08:27Z** (wizard stage 9 đặt bằng REST sau khi operator xác nhận).
- **H-9** Bật loop: `gh variable set HARNESS_DISPATCH --body on` (FV-D13); `after-gate.yml` và `frontier-dispatch.yml` phải ở trạng thái enabled (`gh workflow enable`). **Bật 2026-11-22 08:27:46Z**; lane #2 cấp 08:28:10Z.

Vòng lặp dừng, đúng thiết kế, ở: ticket `ready-for-human` (#5, #15, #20), tín hiệu BLOCKED, quá hai vòng sửa, lane im hai lần, task Needs attention, frontier rỗng, `HARNESS_DISPATCH=off`. Mỗi chỗ dừng để lại dấu vết máy đọc được: nhãn `harness:blocked`/`harness:stalled` và câu hỏi `- [ ]` trên issue.

Ngân sách session (H-6 của `nhan`, [tiền nhiệm]): một session Kiro Web dừng không báo sau khoảng 60 phút làm việc. Ticket T05, T08, T11 lớn hơn các ticket của `nhan`; nếu hai lane đầu chết nhiều lần ở phút 60 thì cắt ticket thành sub-issue có mục `## Seam` (ngoài phạm vi harness).

## 8. Việc còn mở

- **Cron GitHub không nổ** (FV-M-7, FV-M-8): `*/15` nổ 3 lần trong 19,5 giờ đầu (3,8 % số khe). FV-D15 đóng trường hợp phổ biến nhất (vòng review sau lượt sửa) ngay trong run Gate, và bốn lane đầu merge không chờ cron. Còn lại phụ thuộc cron: lane im lặng cần gọi lại, lượt review/sửa chết cần đánh dấu stalled (120 phút), nhánh đã xong cần nhận nuôi, PR xung đột cần lượt đồng bộ: với cron 4–5 giờ một lần, mỗi chỗ ấy chờ thêm chừng ấy. FV-D16 đổi phút cron (`7,22,37,52`) từ 2026-11-23; **đo lại sau một ngày** bằng `gh run list --workflow after-gate.yml --event schedule`. Nếu vẫn dưới một lần một giờ: hai đường tiếp theo là heartbeat ngoài GitHub (đổi FV-D5; nhan D33/D44 đã có thiết kế) hay chuỗi run tự gọi nhau trong Actions khi còn lượt đang chờ (có trần, tự tắt khi không còn việc); chưa chọn.
- **Tín hiệu BLOCKED của lane đi qua comment trên issue**, mà session probe không trả lời trên issue (FV-M-5) và lane #2 cũng không (chỉ một ack). Nếu lane BLOCKED cũng im lặng như vậy, dispatcher chỉ thấy "im lặng" và gọi lại thay vì park. Chưa gặp; nếu gặp thì cho lane ghi câu hỏi `- [ ]` vào `docs/evidence/issue-<n>-*.md` với dòng cuối `<promise>BLOCKED</promise>` và cho dispatcher đọc file ấy trên nhánh như đọc bằng chứng.
- **Sub-agent không thấy steering** (FV-M-6): lane #2 vẫn giữ đúng hình dạng vòng lặp khi comment cấp phát bảo planner chép hai file vào tin nhắn giao việc (FV-M-7). Theo dõi thêm ở T02–T05; nếu một lane lệch thì nhúng nguyên văn `lane-implement.md` vào comment cấp phát.
- **Guard không chạy trên Kiro Web** (FV-M-6): bù bằng H-8 (đã đặt), luật trong tin nhắn, và lượt review. `gh` trong sandbox có token (push được) nên `gh pr merge` từ lane là khả thi về kỹ thuật; chỉ luật cấm. Nếu một lane merge PR của mình, thêm required status check `Gate` và review bắt buộc vào bảo vệ nhánh.
- **PR của lane đứng tên `app/kiro-agent`**, không phải operator (FV-M-7), dù H-2 bảo bật "Create pull requests as your GitHub user"; không ảnh hưởng merger (chỉ PR harness kiểm tác giả). Ghi để đối chiếu với `nhan` M-7.
- **Lane có thể sửa harness** (FV-M-7, S2): lane #2 sửa `scripts/skill_lint.py` để luật phiên bản đọc được `[tool.hatch.version].path`, đúng việc, và `ruff format` của nó định dạng lại file làm đột biến witness mất ý nghĩa (chỉ còn bắt lỗi cú pháp). Đột biến đã nhắm lại vào thân hàm; luật chung: đột biến nhắm vào dòng thân, không vào dòng `def`.
- Kênh cấp phát file một-chủ tới sandbox Kiro Web: hook không chạy và sandbox không có biến môi trường theo task. Tới khi có, `HARNESS_WIP` = 1 và dispatcher cấp `all`.
- `vbpl.vn` trả 403 cho sandbox (FV-M-6): skill `founder-permits` (đợt B) cần biết; `permits/sources.md` bản lưu là đường dự phòng đã có trong thiết kế §3.
- `check-doc-paths.sh` chỉ kiểm đường dẫn có thư mục; tên file trần (`pyproject.toml`, `GLOSSARY.md`) không kiểm vì được nêu trước khi tồn tại theo thiết kế.
- Chuyển `scripts/harness/` sang Python dưới gate (bash/jq vì repo chưa có ngôn ngữ lúc dựng; T01 đã land).
- Tên workflow release của T01 là `release.yml`, khớp gợi ý của wizard cho pending publisher trên PyPI.
- Phép đo của `nhan` về phút Actions không áp dụng: repo public, run miễn phí; nếu repo thành private thì xem lại D16–D20, D31, D43–D46, D49 của `nhan`.

## 9. Quyết định đã chốt

| Mã | Quyết định | Ngày |
|---|---|---|
| FV-D1 | Port đủ C1–C5, guard, witness từ `nhan` `8adef66b`; chép bash/jq nguyên bản rồi tham số hoá (`main`, không migration, `uv run` thay `npm run`); bỏ mọi quyết định chỉ để tiết kiệm phút Actions (repo public) và mọi thứ Docker/PostgreSQL. Merger là workflow máy, không bao giờ là agent (D1 của `nhan`) | 2026-11-22 |
| FV-D2 | Gate = `uv sync --frozen`, `ruff check`, `ruff format --check`, `pytest`, `uv build`, cộng `scripts/skill_lint.py` (nửa máy của checklist rà soát skill: frontmatter, `name` = thư mục, cụm kích hoạt tiếng Việt, `license`, `metadata.version` = phiên bản package, không `$` cạnh chữ số trong SKILL.md và `examples/`). Cổng sandbox ba đoạn `static | unit | build` + `verify` | 2026-11-22 |
| FV-D3 | Key `FOUNDER_LLM_BASE_URL/API_KEY/MODEL` đặt trong env sandbox Kiro Web; lane tự chạy golden case; không bao giờ in giá trị env vào bằng chứng, log, fixture; guard chặn lệnh nêu tên key; test dùng fake provider | 2026-11-22 |
| FV-D4 | Harness lên repo bằng nhánh `harness/bootstrap` + PR #21, operator merge tay lần đầu (merger không tự merge được chính nó); PR harness sau đi qua nhãn `harness:auto-merge` (D9 của `nhan`) | 2026-11-22 |
| FV-D5 | Hẹn giờ: chỉ cron GitHub `*/15` trong `after-gate.yml`; không heartbeat launchd, không cron ngoài. Chấp nhận lane chết chờ 15 phút–4 giờ | 2026-11-22 |
| FV-D6 | Commit 27 skill mattpocock (MIT, `skills-lock.json`) ở `.agents/skills/` + symlink `.kiro/skills/`, vì sandbox Kiro Web là checkout của repo; `.gitignore` loại đích danh `founder-*` upstream và 12 thư mục ID8Labs (không license). `check-skill-links.sh` kiểm | 2026-11-22 |
| FV-D7 | Nguồn port là clone local `~/nhannguyen/ws/nhan` tại `8adef66b` | 2026-11-22 |
| FV-D8 | Tiền đề Kiro Web chưa có → wizard cho bước người làm; agent dựng dừng sau PR; probe và lane đầu chỉ khi operator ra lệnh | 2026-11-22 |
| FV-D9 | Tin phép đo của `nhan`, gắn [tiền nhiệm]; đo lại bằng issue probe trước lane đầu | 2026-11-22 |
| FV-D10 | Issue có sub-issue là spec/map, không phải lane: `frontier.jq` đọc `sub_issues_summary.total` và bỏ qua. Lý do: FV-M-3, lần chạy khô đầu chọn #1. Sửa ở cơ chế thay vì đổi nhãn tracker, vì cấu trúc tracker nói đúng nó là gì mà không cần giữ một nhãn đồng bộ | 2026-11-22 |
| FV-D11 | Tài liệu luật phải trỏ file có thật: `check-doc-paths.sh` kiểm mọi đường dẫn backtick có thư mục trong `AGENTS.md` và steering; chạy trong Gate; witness kiểm cơ chế trên fixture. Lý do: `nhan` từng có bốn agent trỏ prompt sai đường | 2026-11-22 |
| FV-D12 | Dev skill và product skill tách bạch: `.agents/skills/` (công cụ phát triển, không phân phối) và `skills/` (sản phẩm founder-vn); `skill_lint.py` chỉ kiểm `skills/` | 2026-11-22 |
| FV-D13 | Công tắc tạm dừng lane mới: variable repo `HARNESS_DISPATCH` (`on`/`off`). Khi `off`, `dispatch.sh --apply` quyết định khô và không cấp phát, không gọi lại, không nhận nuôi; `gate.yml` và `after-gate.yml` đặt `HARNESS_DISPATCH_INLINE=0` và bỏ lượt dispatcher cuối run; review và merge của lane đang chạy vẫn tiếp tục (`HARNESS_WEB_REVIEW` là công tắc riêng của review). Lý do: sau khi PR #21 merge và wizard đặt token, cron `*/15` của `after-gate.yml` sẽ tự cấp #2 trước khi operator ra lệnh; hai workflow bị tắt tay lúc 07:53Z để chặn, công tắc thay cho việc tắt workflow. Đặt `off` lúc 08:15Z | 2026-11-22 |
| FV-D14 | Luật của guard trên Kiro Web đi bằng tin nhắn và bảo vệ nhánh, không bằng hook: FV-M-6 đo guard không chạy trong sandbox. Comment cấp phát và tin nhắn lượt review nêu rõ bốn luật (không push `main`, không force-push, không merge, không in giá trị `FOUNDER_LLM_*`) và bảo planner chép `AGENTS.md`, steering và cấp phát vào mọi tin nhắn giao việc cho sub-agent (sub-agent không thấy chúng, FV-M-6). H-8 bảo vệ nhánh `main` trên GitHub (đặt 08:27Z: yêu cầu PR, 0 approval, không force-push, không xoá, không áp cho admin) | 2026-11-22 |
| FV-D15 | Đuôi Gate chờ nhánh yên rồi đăng vòng review ngay trong run (nhan D41, bị D49 bỏ để tiết kiệm phút): khi bộ điều phối trả `wait: settling` sau lượt sửa, bước đuôi `gate.yml` ngủ 60 giây và quyết định lại, tối đa 12 lần, thay vì để cron đăng. Lý do FV-M-7: cron `*/15` không nổ 38 phút, lane #2 đứng 11 phút chờ vòng 2 tới khi operator kích tay. Phí: tối đa 12 phút runner cho lần push cuối của mỗi lượt sửa, miễn phí trên repo public; push mới hơn huỷ run đang chờ (concurrency) và Gate của nó tiếp tục | 2026-11-22 |
| FV-D16 | Hai sửa nhỏ từ FV-M-8. (a) Cron của `after-gate.yml` đổi từ `*/15` sang `7,22,37,52 * * * *`: GitHub bỏ hay trễ sự kiện schedule khi tải cao, nặng nhất ở đầu giờ và các mốc quý giờ; vẫn là FV-D5 (chỉ cron GitHub), chỉ đổi phút; đo lại tỷ lệ nổ sau một ngày rồi mới quyết tiếp (giữ nguyên, hay heartbeat ngoài GitHub, tức đổi FV-D5). (b) Tin nhắn lượt review nói đúng kết quả Gate khi C4 chạy ở đuôi chính run Gate: `ci-jobs.jq` đọc job của run tự thân (`HARNESS_GATE_SELF_RUN`) bằng `HARNESS_GATE_SELF_CONCLUSION` thay cho `in_progress` của API, kèm một dòng giải thích; khi run ấy đỏ, `gh` không đọc được log của run còn chạy, nên tin nhắn chỉ nêu bước đỏ và bảo session chạy lại ba đoạn `gate-segment.sh` thay cho trích log. Witness: 4 ca, 2 đột biến | 2026-11-23 |

Cơ chế kế thừa nguyên bản từ `nhan`, với mã quyết định bên đó để tra: D11 seam-trước-lát; D13 dispatch bằng `/kiro` + nhãn bot; D15/D33/D39/D54 gọi lại lane im lặng (cửa sổ 60/45 phút, tối đa 4 lần khi có tiến triển); D18 merger kiểm lại blocker và từ khoá đóng; D22 ledger chấp nhận bullet; D23 hook post-commit; D24/D24b adopt nhánh đã xong và lý do lỗi API; D25 lượt đồng bộ; D26 `open-lane-pr.sh`; D27 `run-logged.sh`; D28 cổng theo đoạn; D30 park là điểm dừng thật; D32 nhãn `priority`; D35 lane có nhánh giữ chỗ; D38 câu trả lời lỗi của Kiro; D40 ledger không phải mã; D41/D49 chờ nhánh yên sau lượt sửa; D42 trần 14 lượt và `extra_round`; D47/D51 kiểm pick bằng GET riêng; D53 tín hiệu BLOCKED đọc từ comment cuối không phải của Kiro; D55 kiểm merge thật trước khi đóng ticket.

Bỏ, không port: D12/D14/D29/D45/D52 (Docker, PostgreSQL, Gate treo), D16/D17/D19/D20/D31/D43/D44/D46 (phút Actions), D48 (vitest shuffle), spec lane, heartbeat launchd, `migrationTimestamp`.
