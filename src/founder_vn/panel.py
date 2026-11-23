"""Panel bookkeeping: deal persona cards, check and file buyer answers, tally the result.

One set of functions behind ``founder-vn panel`` and the MCP tools ``panel_init`` and
``panel_tally``. The package never answers for a buyer: every number in the tally is counted from
the answer files the buyers wrote. State lives under ``founder/panel/`` and goes through
``founder_vn.files`` only.
"""

import json
import math
import random
from pathlib import Path
from typing import Any

from founder_vn import files

PANEL_DIR = "panel"
DEFAULT_N = 20
INCOME_STEP = 100_000
REASONS = ("price", "habit", "need", "trust", "quality", "convenience", "timing", "values", "other")
REASON_LABELS = {
    "price": "giá",
    "habit": "thói quen",
    "need": "nhu cầu",
    "trust": "độ tin cậy",
    "quality": "chất lượng",
    "convenience": "tiện lợi",
    "timing": "thời điểm",
    "values": "giá trị cá nhân",
    "other": "lý do khác",
}
THIN_GROUP = 8
# Canonical price answers: the names the buyer brief asks for; the short names pricing reads are
# accepted too and win when both are present.
PRICE_KEYS = {
    "too_cheap": "price_too_cheap",
    "bargain": "price_cheap",
    "getting_expensive": "price_expensive",
    "too_expensive": "price_too_expensive",
}
PRICING_INPUT = "pricing_input.json"
ANSWER_FIELDS = ("id", "buys", "reason_code", "reason")

GIVEN_NAMES = [
    "Minh Anh",
    "Gia Bảo",
    "Thu Hà",
    "Quốc Việt",
    "Ngọc Lan",
    "Hoàng Nam",
    "Thanh Tâm",
    "Đức Anh",
    "Bích Ngọc",
    "Tuấn Kiệt",
    "Phương Thảo",
    "Hải Đăng",
    "Khánh Linh",
    "Anh Tuấn",
    "Mai Chi",
    "Trung Hiếu",
    "Diệu Linh",
    "Bảo Châu",
    "Thành Long",
    "Kim Ngân",
    "Văn Khoa",
    "Hồng Nhung",
    "Đình Phúc",
    "Thuỳ Dương",
    "Công Minh",
    "Yến Nhi",
    "Nhật Huy",
    "Tố Uyên",
    "Quang Vinh",
    "Lan Phương",
    "Duy Khánh",
    "Thảo Vy",
    "Hữu Phước",
    "Cẩm Tú",
    "Gia Hân",
    "Trọng Nghĩa",
    "Mỹ Duyên",
    "Xuân Bách",
    "Hà My",
    "Việt Hoàng",
]


class PanelError(ValueError):
    """The panel input is missing or malformed; the message names the field."""


def _path(*parts: str) -> str:
    return "/".join((PANEL_DIR, *parts))


def _quota(items: list[dict[str, Any]], n: int) -> list[int]:
    """Split ``n`` across ``items`` by their ``share`` exactly (largest remainder)."""
    total = sum(float(it.get("share", 1)) for it in items) or 1.0
    raw = [n * float(it.get("share", 1)) / total for it in items]
    counts = [int(r) for r in raw]
    order = sorted(range(len(items)), key=lambda i: raw[i] - counts[i], reverse=True)
    for i in order[: n - sum(counts)]:
        counts[i] += 1
    return counts


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _pair(value: Any, field: str) -> None:
    ok = isinstance(value, list) and len(value) == 2 and all(_is_number(v) for v in value)
    if not ok:
        raise PanelError(f"'{field}' phải là [thấp, cao], hai số")
    if value[0] > value[1] or value[0] <= 0:
        raise PanelError(f"'{field}' phải lớn hơn 0 và thấp không vượt cao")


def _weighted(items: Any, group: str) -> None:
    if not isinstance(items, list) or not items:
        raise PanelError(f"customer.json thiếu trường '{group}'")
    for i, item in enumerate(items):
        where = f"{group}[{i}]"
        if not isinstance(item, dict) or not str(item.get("name", "")).strip():
            raise PanelError(f"thiếu trường '{where}.name'")
        share = item.get("share")
        if not _is_number(share) or share <= 0:
            raise PanelError(f"'{where}.share' phải là số lớn hơn 0")


def validate_customer(customer: Any) -> None:
    """Raise ``PanelError`` naming the first offending field of ``customer.json``."""
    if not isinstance(customer, dict):
        raise PanelError("customer.json phải là một đối tượng JSON")
    for key in ("business", "target"):
        if not str(customer.get(key, "")).strip():
            raise PanelError(f"customer.json thiếu trường '{key}'")
    _weighted(customer.get("segments"), "segments")
    _weighted(customer.get("behaviours"), "behaviours")
    for i, segment in enumerate(customer["segments"]):
        field = f"segments[{i}].income"
        _pair(segment.get("income"), field)
        low, high = segment["income"]
        if math.floor(high / INCOME_STEP) < math.ceil(low / INCOME_STEP):
            raise PanelError(f"'{field}' không chứa mức nào chia hết cho 100.000 đ")
    _pair(customer.get("age"), "age")
    objections = customer.get("objections")
    if not isinstance(objections, list) or not objections:
        raise PanelError("customer.json thiếu trường 'objections'")
    if not all(isinstance(o, str) and o.strip() for o in objections):
        raise PanelError("'objections' chỉ gồm các câu không rỗng")


def deal(customer: dict[str, Any], n: int, seed: int) -> list[dict[str, Any]]:
    """Deal ``n`` persona cards. Same customer, ``n`` and ``seed`` give the same cards."""
    rng = random.Random(seed)
    low_age, high_age = customer["age"]
    segments: list[dict[str, Any]] = []
    for segment, k in zip(customer["segments"], _quota(customer["segments"], n), strict=True):
        segments += [segment] * k
    behaviours: list[dict[str, Any]] = []
    for behaviour, k in zip(customer["behaviours"], _quota(customer["behaviours"], n), strict=True):
        behaviours += [behaviour] * k
    rng.shuffle(segments)
    rng.shuffle(behaviours)
    names = GIVEN_NAMES[:]
    rng.shuffle(names)
    while len(names) < n:
        names += [f"{x} {len(names) // len(GIVEN_NAMES) + 1}" for x in GIVEN_NAMES]
    objections = customer["objections"]
    habits = customer.get("habits") or []
    cards = []
    for i in range(n):
        segment, behaviour = segments[i], behaviours[i]
        low = math.ceil(segment["income"][0] / INCOME_STEP)
        high = math.floor(segment["income"][1] / INCOME_STEP)
        cards.append(
            {
                "id": f"P{i + 1:03d}",
                "name": names[i],
                "age": rng.randint(int(low_age), int(high_age)),
                "segment": segment["name"],
                "income": rng.randint(low, high) * INCOME_STEP,
                "behaviour": behaviour["name"],
                "behaviour_how": behaviour.get("how", ""),
                "objection": objections[rng.randrange(len(objections))],
                "habit": habits[rng.randrange(len(habits))] if habits else "",
            }
        )
    return cards


def _dump(obj: Any) -> str:
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def _read(project: Path, path: str) -> str:
    try:
        return files.read_text(project, path)
    except FileNotFoundError:
        raise PanelError(f"không thấy founder/{path}") from None


def _read_json(project: Path, path: str) -> Any:
    try:
        return json.loads(_read(project, path))
    except json.JSONDecodeError as e:
        raise PanelError(f"{path} không phải JSON hợp lệ: {e}") from None


def init(project: Path, customer: str, pitch: str, n: int, seed: int | None) -> str:
    """Deal the cards and write ``panel.json`` and ``personas.json``; return the stdout text."""
    if n < 1:
        raise PanelError("'--n' phải từ 1 trở lên")
    spec = _read_json(project, customer)
    validate_customer(spec)
    text = _read(project, pitch).strip()
    if not text:
        raise PanelError(f"{pitch} trống: viết lời chào hàng trước (bán gì, giá bao nhiêu, ở đâu)")
    if seed is None:
        seed = random.SystemRandom().randrange(1, 10**6)
    cards = deal(spec, n, seed)
    files.write_text(
        project, _path("panel.json"), _dump({"n": n, "seed": seed, "customer": spec, "pitch": text})
    )
    files.write_text(project, _path("personas.json"), _dump(cards))
    return f"Đã chia {len(cards)} người mua (seed {seed}) vào founder/{PANEL_DIR}/\n"


def _load_cards(project: Path) -> list[dict[str, Any]]:
    try:
        return json.loads(files.read_text(project, _path("personas.json")))  # type: ignore[no-any-return]
    except FileNotFoundError:
        raise PanelError("chưa có panel: chạy 'founder-vn panel init' trước") from None


def answer_problem(answer: Any, pid: str) -> str | None:
    """None when ``answer`` is a valid answer of buyer ``pid``, else a short problem."""
    if not isinstance(answer, dict):
        return "không phải một đối tượng JSON"
    missing = sorted(set(ANSWER_FIELDS) - set(answer))
    if missing:
        return "thiếu " + ", ".join(missing)
    if answer["id"] != pid:
        return f"id là {answer['id']!r}, cần {pid}"
    if not isinstance(answer["buys"], bool):
        return "'buys' phải là true hoặc false"
    if answer["reason_code"] not in REASONS:
        return f"reason_code {answer['reason_code']!r} không thuộc: {', '.join(REASONS)}"
    return None


def _answer_file_problem(project: Path, pid: str) -> str | None:
    try:
        text = files.read_text(project, _path("answers", f"{pid}.json"))
    except FileNotFoundError:
        return "chưa có câu trả lời"
    try:
        return answer_problem(json.loads(text), pid)
    except json.JSONDecodeError:
        return "không phải JSON hợp lệ"


def check(project: Path) -> tuple[str, int]:
    """List buyers whose answer is missing or broken; return the text and the exit code."""
    lines = []
    for card in _load_cards(project):
        problem = _answer_file_problem(project, card["id"])
        if problem:
            lines.append(f"{card['id']}: {problem}")
    if not lines:
        return "Mọi câu trả lời đều có và hợp lệ\n", 0
    return "\n".join(lines) + "\n", 1


def save(project: Path, pid: str, reply: str) -> str:
    """File a buyer's own printed reply: its first JSON object, written only when valid."""
    if pid not in {c["id"] for c in _load_cards(project)}:
        raise PanelError(f"panel này không có người mua {pid}")
    start = reply.find("{")
    if start < 0:
        raise PanelError("không có đối tượng JSON trong câu trả lời")
    try:
        answer, _ = json.JSONDecoder().raw_decode(reply[start:])
    except json.JSONDecodeError as e:
        raise PanelError(f"JSON trong câu trả lời không đọc được: {e}") from None
    problem = answer_problem(answer, pid)
    if problem:
        raise PanelError(
            f"câu trả lời của {pid} không hợp lệ ({problem}); chạy lại brief của người mua đó"
        )
    target = _path("answers", f"{pid}.json")
    files.write_text(project, target, _dump(answer))
    return f"Đã lưu founder/{target}\n"


def _group(rows: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(row[key], []).append(row)
    out = [
        {
            "name": name,
            "n": len(members),
            "buys": sum(1 for m in members if m["buys"]),
            "buy_rate": sum(1 for m in members if m["buys"]) / len(members),
        }
        for name, members in groups.items()
    ]
    return sorted(out, key=lambda g: (-g["buy_rate"], g["name"]))


def _reasons(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        groups.setdefault(row["reason_code"], []).append(row)
    out = [
        {
            "reason_code": code,
            "n": len(members),
            "quotes": [{"id": m["id"], "text": m["reason"]} for m in members[:2]],
        }
        for code, members in groups.items()
    ]
    return sorted(out, key=lambda r: (-r["n"], r["reason_code"]))


def _price_row(row: dict[str, Any]) -> dict[str, Any] | None:
    picked = {q: row.get(q, row.get(long)) for q, long in PRICE_KEYS.items()}
    return picked if all(v is not None for v in picked.values()) else None


def _number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


def tally(project: Path) -> dict[str, Any]:
    """Count the valid answers; ``excluded`` buyers have a missing or broken answer."""
    meta = _read_json(project, _path("panel.json"))
    rows: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []
    for card in _load_cards(project):
        problem = _answer_file_problem(project, card["id"])
        if problem:
            excluded.append({"id": card["id"], "problem": problem})
            continue
        answer = _read_json(project, _path("answers", f"{card['id']}.json"))
        rows.append({**card, **answer})
    if not rows:
        raise PanelError("chưa có câu trả lời hợp lệ nào: cho từng người mua trả lời trước")
    buyers = [r for r in rows if r["buys"]]
    passers = [r for r in rows if not r["buys"]]
    monthly = [v for r in buyers if (v := _number(r.get("purchases_first_month"))) is not None]
    prices = [p for r in rows if (p := _price_row(r)) is not None]
    return {
        "mode": meta.get("mode", "manual"),
        "model": meta.get("model"),
        "prompt_hash": meta.get("prompt_hash"),
        "business": meta["customer"]["business"],
        "seed": meta["seed"],
        "n": len(rows) + len(excluded),
        "answered": len(rows),
        "excluded": len(excluded),
        "excluded_buyers": excluded,
        "buys": len(buyers),
        "passes": len(passers),
        "buy_rate": len(buyers) / len(rows),
        "by_segment": _group(rows, "segment"),
        "by_behaviour": _group(rows, "behaviour"),
        "why_not": _reasons(passers),
        "why_yes": _reasons(buyers),
        "flip": [
            r["would_change_my_mind"].strip()
            for r in passers
            if isinstance(r.get("would_change_my_mind"), str) and r["would_change_my_mind"].strip()
        ],
        "purchases_first_month_per_buyer": sum(monthly) / len(monthly) if monthly else None,
        "price_answers": len(prices),
        "price_rows": prices,
    }


def _pct(value: float) -> str:
    return f"{value * 100:.0f}%"


def _quotes(reasons: list[dict[str, Any]]) -> list[str]:
    return [
        f"| {REASON_LABELS[r['reason_code']]} | {r['n']} | "
        + " · ".join(f'"{q["text"].replace("|", "/")}" ({q["id"]})' for q in r["quotes"])
        + " |"
        for r in reasons
    ]


def results_md(res: dict[str, Any]) -> str:
    """The Vietnamese results report, counted from the answers only."""
    lines = [
        f"# Panel người mua: {res['business']}",
        "",
        f"**{res['buys']} mua, {res['passes']} không mua** ({_pct(res['buy_rate'])} mua) trên "
        f"{res['answered']} người mua mô phỏng. Seed {res['seed']}, chia lại sẽ ra đúng các thẻ này.",
        "",
        f"Tín hiệu cầu (mô phỏng, cận trên): {_pct(res['buy_rate'])} người mua mô phỏng nói sẽ mua.",
        "",
        f"Chế độ chạy: {res['mode']}; mô hình: {res['model'] or 'không có'}.",
    ]
    if res["excluded"]:
        left = ", ".join(f"{e['id']} ({e['problem']})" for e in res["excluded_buyers"][:10])
        lines += [
            "",
            f"{res['excluded']} trên {res['n']} người mua không có câu trả lời hợp lệ nên bị loại: "
            f"{left}.",
        ]
    lines += [
        "",
        "Panel là mô phỏng, không phải khách hàng thật. Dùng nó để tìm ra các phản đối và điểm "
        "yếu, rồi xác nhận điều quan trọng với khách thật (bán trước, danh sách chờ, trang giới "
        "thiệu có ghi giá) trước khi anh/chị chi tiền. Kết quả này không quyết định việc lãi hay lỗ.",
    ]
    for title, key in (("Theo nhóm khách", "by_segment"), ("Theo cách mua", "by_behaviour")):
        lines += ["", f"## {title}", "", "| nhóm | số người | tỷ lệ mua |", "| --- | ---: | ---: |"]
        for g in res[key]:
            thin = " (mỏng)" if g["n"] < THIN_GROUP else ""
            lines.append(f"| {g['name']} | {g['n']} | {_pct(g['buy_rate'])}{thin} |")
    header = ["", "| lý do | số người | nguyên văn |", "| --- | ---: | --- |"]
    lines += ["", "## Vì sao không mua", *header, *_quotes(res["why_not"])]
    lines += ["", "## Vì sao mua", *header, *_quotes(res["why_yes"])]
    if res["flip"]:
        lines += ["", "## Điều gì có thể đổi một lời từ chối", ""]
        lines += [f"- {text}" for text in res["flip"][:12]]
    per_buyer = res["purchases_first_month_per_buyer"]
    if per_buyer is not None:
        times = f"{per_buyer:.1f}".replace(".", ",")
        lines += ["", f"Người mua nói sẽ mua trung bình **{times} lần** trong tháng đầu."]
    if res["price_answers"]:
        lines += [
            "",
            f"{res['price_answers']} người trả lời đủ bốn câu hỏi về giá, đã gom vào "
            f"founder/{_path(PRICING_INPUT)}. Chạy `founder-vn pricing {_path(PRICING_INPUT)}`.",
        ]
    return "\n".join(lines) + "\n"


def run_tally(project: Path) -> str:
    """Write ``results.md``, ``results.json`` and ``pricing_input.json``; return the stdout text."""
    res = tally(project)
    files.write_text(project, _path("results.md"), results_md(res))
    price_rows = res.pop("price_rows")
    files.write_text(project, _path("results.json"), _dump(res))
    files.write_text(
        project, _path(PRICING_INPUT), _dump({"business": res["business"], "answers": price_rows})
    )
    return (
        f"{res['buys']} mua, {res['passes']} không mua ({_pct(res['buy_rate'])}). "
        f"Đã ghi founder/{_path('results.md')} và founder/{_path('results.json')}\n"
    )
