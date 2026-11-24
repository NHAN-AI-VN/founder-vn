"""Board run: three lens memos (Offers, Product, Systems) asked of the configured model.

One set of functions behind ``founder-vn board run`` and the MCP tool ``board_run``. The skill
writes a standalone brief to ``founder/board/brief.md``; the package asks the model once per lens,
as three independent completions, and files each valid memo as ``<lens>.json`` and ``<lens>.md``.
The job runs on the same runner pattern as ``panel run`` and is polled with the same ``job_status``.
The chair's summary is the host's job, not the package's. State goes through ``founder_vn.files``.
"""

import hashlib
import json
import subprocess
import sys
import threading
import time
import uuid
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

from founder_vn import files, llm, panel

BOARD_DIR = "board"
BRIEF = "brief.md"
ATTEMPTS = panel.ATTEMPTS
MAX_INVALID = panel.MAX_INVALID
BACKOFF = panel.BACKOFF
VOTES = {
    "go": "nên làm",
    "conditional": "làm có điều kiện",
    "no_go": "chưa nên làm",
}
FIELDS = ("score", "vote", "strong", "would_kill", "questions", "conditions")
LIST_FIELDS = (
    ("strong", "Điểm mạnh"),
    ("would_kill", "Điều có thể giết ý tưởng này"),
    ("questions", "Câu hỏi còn mở"),
    ("conditions", "Điều kiện"),
)
RULE = (
    "Quy tắc bắt buộc: chỉ áp dụng khung tư duy đã được xuất bản trong nguồn dưới đây như một công "
    "cụ phân tích; không bao giờ nói thay tác giả, không đóng vai tác giả, không đặt vào miệng tác "
    "giả một câu nào, không trích dẫn như thể tác giả đang nhận xét ý tưởng này."
)
LENSES: dict[str, dict[str, str]] = {
    "offers": {
        "title": "Offers",
        "source": "100M Offers (Alex Hormozi)",
        "framework": (
            "Đề xuất giá trị là sản phẩm. Xét bằng phương trình giá trị: kết quả khách mơ ước và "
            "khả năng tin là đạt được, chia cho thời gian chờ và công sức, rủi ro khách phải gánh. "
            "Hỏi: lời hứa có cụ thể và đo được không; có gói, bảo đảm hay phần thêm nào khiến việc "
            "từ chối là điều dại dột; giá có tương xứng với giá trị chứ không chỉ so với đối thủ; "
            "ai là nhóm khách có nhu cầu rõ và sẵn sàng trả; có cách nào nâng giá trị mà không "
            "giảm giá."
        ),
    },
    "product": {
        "title": "Product",
        "source": "tiểu sử Steve Jobs do Walter Isaacson viết",
        "framework": (
            "Chất lượng và sự tập trung của sản phẩm. Xét theo các bài học Isaacson rút ra từ "
            "tiểu sử: sản phẩm có một trải nghiệm cốt lõi rõ ràng không; có dám nói không với "
            "những thứ làm loãng nó không; chi tiết, kể cả phần khách không nhìn thấy, có được "
            "chăm chút không; toàn bộ trải nghiệm từ lúc khách biết đến tới lúc quay lại có liền "
            "mạch không; sản phẩm có khiến người dùng muốn kể cho người khác không."
        ),
    },
    "systems": {
        "title": "Systems",
        "source": "The E-Myth Revisited (Michael E. Gerber)",
        "framework": (
            "Doanh nghiệp là một hệ thống chứ không phải một công việc. Xét theo ba vai: kỹ "
            "thuật viên, quản lý, nhà doanh nghiệp. Hỏi: nếu chủ vắng mặt một tháng thì tiệm có "
            "chạy không; mỗi việc lặp lại đã có quy trình viết ra để người mới làm đúng chưa; "
            "tiệm có thể nhân bản thành tiệm thứ hai theo cùng cách không; chủ đang làm việc "
            "trong tiệm hay đang xây tiệm; các con số vận hành (công suất, lượt khách, giờ làm) "
            "có người theo dõi không."
        ),
    },
}
TEMPLATE = """Bạn là một thành viên hội đồng cố vấn, đọc bản tóm tắt ý tưởng kinh doanh của một chủ hộ \
kinh doanh nhỏ ở Việt Nam qua một lens duy nhất.
Mã lens: {id}
Lens: {title}
Nguồn của lens: {source}

{rule}

Khung của lens này: {framework}

Chỉ dựa vào bản tóm tắt dưới đây. Không biết gì ngoài nó. Không bịa số liệu, không bịa đối thủ; \
thiếu dữ kiện thì đặt thành câu hỏi. Viết bằng tiếng Việt, xưng hô với chủ là "anh/chị", không dùng \
ký hiệu đô la; tiền viết theo đồng Việt Nam, ví dụ 35.000 đ. Ý kiến của bạn có thể khác các lens \
khác; đừng cố đồng ý cho êm.

Bản tóm tắt:

{brief}

Chỉ trả lời bằng một đối tượng JSON, không viết thêm gì, với các trường:
- "score": số nguyên từ 1 đến 10, điểm của lens này cho ý tưởng
- "vote": một trong "go", "conditional", "no_go"
- "strong": danh sách câu tiếng Việt, những điểm mạnh theo lens này (ít nhất một)
- "would_kill": danh sách câu tiếng Việt, điều có thể giết ý tưởng này (ít nhất một)
- "questions": danh sách câu hỏi còn mở, mỗi câu nên được trả lời bằng một con số hay một việc \
làm cụ thể (có thể để trống)
- "conditions": danh sách điều kiện phải đạt trước khi làm, mỗi điều kiện kiểm tra được (có thể để \
trống)
"""


class BoardError(panel.PanelError):
    """The board input is missing or malformed; the message names the file or field."""


def _dump(obj: Any) -> str:
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def _path(*parts: str) -> str:
    return "/".join((BOARD_DIR, *parts))


def prompt(lens: str, brief: str) -> str:
    """The Vietnamese prompt of one lens: its framework, the never-speak-as-the-author rule and
    the standalone brief. A lens sees nothing but this text."""
    spec = LENSES[lens]
    text = TEMPLATE
    fields = {"id": lens, **spec, "rule": RULE, "brief": brief}
    for key, value in fields.items():
        text = text.replace("{" + key + "}", value)
    return text


def prompt_hash(brief: str) -> str:
    """SHA-256 of the prompt template, the lens texts and the brief."""
    payload = "\n".join([TEMPLATE, RULE, _dump(LENSES), brief])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _text_list(value: Any) -> bool:
    return isinstance(value, list) and all(isinstance(v, str) and v.strip() for v in value)


def memo_problem(memo: Any) -> str | None:
    """None when ``memo`` has the fixed shape, else a short problem naming the field."""
    if not isinstance(memo, dict):
        return "không phải một đối tượng JSON"
    score = memo.get("score")
    if isinstance(score, bool) or not isinstance(score, int) or not 1 <= score <= 10:
        return "'score' phải là số nguyên từ 1 đến 10"
    if memo.get("vote") not in VOTES:
        return f"'vote' phải là một trong {', '.join(VOTES)}"
    for field in ("strong", "would_kill"):
        if not _text_list(memo.get(field)) or not memo[field]:
            return f"'{field}' phải là danh sách câu, ít nhất một"
    for field in ("questions", "conditions"):
        if not _text_list(memo.get(field)):
            return f"'{field}' phải là danh sách câu (có thể trống)"
    return None


def extract_memo(reply: str) -> tuple[dict[str, Any] | None, str | None]:
    """The first JSON object in ``reply`` and ``None``, or ``None`` and what is wrong with it."""
    start = reply.find("{")
    if start < 0:
        return None, "không có đối tượng JSON"
    try:
        memo, _ = json.JSONDecoder().raw_decode(reply[start:])
    except json.JSONDecodeError as e:
        return None, f"JSON không đọc được: {e}"
    problem = memo_problem(memo)
    return (None, problem) if problem else ({k: memo[k] for k in FIELDS}, None)


def memo_md(lens: str, memo: dict[str, Any]) -> str:
    """The Vietnamese memo of one lens in its fixed shape."""
    spec = LENSES[lens]
    lines = [
        f"# Lens {spec['title']}: {spec['source']}",
        "",
        f"**Điểm: {memo['score']}/10** · **Phiếu: {VOTES[memo['vote']]}**",
    ]
    for key, title in LIST_FIELDS:
        lines += ["", f"## {title}", ""]
        items = memo[key]
        lines += [f"- {item}" for item in items] if items else ["- chưa có"]
    lines += [
        "",
        "Đây là ý kiến mô phỏng theo một khung đã xuất bản, không nói thay tác giả và không phải "
        "tư vấn tài chính, thuế hay pháp lý.",
    ]
    return "\n".join(lines) + "\n"


def _memo_problem_on_disk(project: Path, lens: str) -> str | None:
    try:
        text = files.read_text(project, _path(f"{lens}.json"))
    except FileNotFoundError:
        return "chưa có memo"
    try:
        return memo_problem(json.loads(text))
    except json.JSONDecodeError:
        return "không phải JSON hợp lệ"


def _read_brief(project: Path) -> str:
    try:
        text = files.read_text(project, _path(BRIEF)).strip()
    except FileNotFoundError:
        raise BoardError(
            f"không thấy founder/{_path(BRIEF)}: viết bản tóm tắt tự đứng một mình trước"
        ) from None
    if not text:
        raise BoardError(f"founder/{_path(BRIEF)} trống: viết bản tóm tắt tự đứng một mình trước")
    return text


def _job_path(job_id: str) -> str:
    return panel._job_path(job_id, BOARD_DIR)


def start_job(project: Path, launch: Callable[[Path, str], None]) -> str:
    """Record the model and prompt hash, create a job for the lenses without a valid memo and
    hand it to ``launch``; return at once with the job as JSON."""
    brief = _read_brief(project)
    try:
        config = llm.load_config()
    except llm.NotConfigured as e:
        raise BoardError(str(e)) from None
    targets = [lens for lens in LENSES if _memo_problem_on_disk(project, lens)]
    meta = {
        "mode": "model",
        "model": config.model,
        "prompt_hash": prompt_hash(brief),
        "lenses": list(LENSES),
    }
    files.write_text(project, _path("board.json"), _dump(meta))
    job_id = f"J-{uuid.uuid4().hex[:8]}"
    state = "running" if targets else "done"
    job = {
        "job_id": job_id,
        "state": state,
        "targets": targets,
        "done": [],
        "failed": [],
        "excluded": [],
        "last_error": None,
    }
    files.write_text(project, _job_path(job_id), _dump(job))
    if targets:
        launch(project, job_id)
    return _dump({"job_id": job_id, "state": state, "lenses": len(targets)})


def _ask(
    project: Path, config: llm.Config, lens: str, brief: str, timeout: float, backoff: float
) -> tuple[str, str | None]:
    """Ask one lens; return ``done``, ``failed`` or ``excluded`` and the last error.

    The retry rules are the panel's: a failing call is retried with doubling backoff up to
    ``ATTEMPTS`` times (``failed``); a reply that is not a valid memo is asked once more, and
    invalid twice the lens is ``excluded``. Only a valid memo is written.
    """
    text = prompt(lens, brief)
    problem = None
    for _ in range(MAX_INVALID):
        reply = ""
        for attempt in range(ATTEMPTS):
            try:
                reply = llm.complete(config, text, timeout)
                break
            except llm.CallFailed as e:
                if attempt == ATTEMPTS - 1:
                    return "failed", f"{lens}: {e}"
                time.sleep(backoff * 2**attempt)
        memo, problem = extract_memo(reply)
        if memo is not None:
            files.write_text(project, _path(f"{lens}.json"), _dump(memo))
            files.write_text(project, _path(f"{lens}.md"), memo_md(lens, memo))
            return "done", None
    return "excluded", f"{lens}: {problem}"


def execute(
    project: Path, job_id: str, *, timeout: float = llm.TIMEOUT, backoff: float = BACKOFF
) -> None:
    """Ask each lens of the job, one independent completion each, and file the memos."""
    job = panel._read_job(project, job_id, BOARD_DIR)
    config = llm.load_config()
    brief = _read_brief(project)
    with ThreadPoolExecutor(max_workers=len(LENSES)) as pool:
        futures = {
            pool.submit(_ask, project, config, lens, brief, timeout, backoff): lens
            for lens in job["targets"]
        }
        for future in as_completed(futures):
            outcome, error = future.result()
            job[outcome].append(futures[future])
            if error:
                job["last_error"] = error
            files.write_text(project, _job_path(job_id), _dump(job))
    job["state"] = "done"
    files.write_text(project, _job_path(job_id), _dump(job))


def work(project: Path, job_id: str) -> None:
    """Run a job to the end; whatever goes wrong is written into the job, not lost."""
    try:
        execute(project, job_id)
    except Exception as e:  # the worker has no caller to tell: the job file is the report
        job = panel._read_job(project, job_id, BOARD_DIR)
        job |= {"state": "error", "last_error": f"{type(e).__name__}: {e}"}
        files.write_text(project, _job_path(job_id), _dump(job))


def _in_thread(project: Path, job_id: str) -> None:
    threading.Thread(target=work, args=(project, job_id), daemon=True).start()


def _in_process(project: Path, job_id: str) -> None:
    """A detached ``founder-vn board work``: it outlives the short-lived CLI call."""
    subprocess.Popen(
        [sys.executable, "-m", "founder_vn.cli", "board", "work", job_id],
        cwd=project,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )


def run(project: Path, detached: bool) -> str:
    """Start the job for the lenses without a valid memo and return its id at once.

    ``detached`` hands the work to a separate process (the CLI); otherwise a thread of the
    long-lived MCP server does it.
    """
    return start_job(project, _in_process if detached else _in_thread)
