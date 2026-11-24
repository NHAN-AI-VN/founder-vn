"""Model bake-off for the buyer panel (ticket T14, design Q42): the same five personas on each
candidate model, compared on JSON validity, buys, latency and cost per buyer; the Vietnamese voice
and the honesty of the replies are judged by the project owner from ``replies.md``.

    uv run python scripts/bakeoff.py docs/bakeoff [--seed 14] [--pause 4]

Reads ``<dir>/models.json`` (the candidates with their price per 1M tokens, the official price
page and the date the owner verified it), ``<dir>/customer.json`` and ``<dir>/pitch.md`` (the
shapes ``founder-vn panel init`` reads); deals the personas with ``founder_vn.panel.deal``, sends
``founder_vn.panel.brief`` through ``founder_vn.llm`` to each candidate and validates each reply
with ``founder_vn.panel.extract_answer``, so the numbers describe the panel as it really runs.
The endpoint and the key come from ``FOUNDER_LLM_BASE_URL`` and ``FOUNDER_LLM_API_KEY``; the
candidate names come from ``models.json``. Nothing about the configuration but the model names
and the prompt hash is written.

A development tool of the project owner, next to ``skill_lint.py``: not a computation for the
Owner, so it has no CLI/MCP pair.
"""

import argparse
import dataclasses
import json
import re
import statistics
import sys
import time
from collections.abc import Callable
from datetime import date
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from founder_vn import llm, panel  # noqa: E402

PERSONAS = 5
DEFAULT_SEED = 14
ATTEMPTS = 3
BACKOFF = 10.0  # seconds before the second attempt of a failed call; doubles
PAUSE = 4.0  # seconds between two calls: free tiers allow about 15 requests a minute
MODEL_FIELDS = ("name", "input_usd_per_1m", "output_usd_per_1m", "price_source", "price_verified")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


class BakeoffError(ValueError):
    """An input of the bake-off is missing or malformed; the message names the field."""


def _read(directory: Path, name: str) -> str:
    try:
        return (directory / name).read_text(encoding="utf-8")
    except FileNotFoundError:
        raise BakeoffError(f"không thấy {directory / name}") from None


def _read_json(directory: Path, name: str) -> Any:
    try:
        return json.loads(_read(directory, name))
    except json.JSONDecodeError as e:
        raise BakeoffError(f"{name} không phải JSON hợp lệ: {e}") from None


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def load_models(directory: Path) -> dict[str, Any]:
    """The parsed ``models.json``: at least two candidates, each with the five fields."""
    spec = _read_json(directory, "models.json")
    models = spec.get("models") if isinstance(spec, dict) else None
    if not isinstance(models, list) or len(models) < 2:
        raise BakeoffError("models.json cần ít nhất hai mô hình trong 'models' để so sánh")
    for i, model in enumerate(models):
        where = f"models[{i}]"
        if not isinstance(model, dict):
            raise BakeoffError(f"'{where}' phải là một đối tượng JSON")
        for field in MODEL_FIELDS:
            if field not in model:
                raise BakeoffError(f"models.json thiếu trường '{where}.{field}'")
        if not isinstance(model["name"], str) or not model["name"].strip():
            raise BakeoffError(f"'{where}.name' phải là tên mô hình, không rỗng")
        for field in ("input_usd_per_1m", "output_usd_per_1m"):
            if not _is_number(model[field]) or model[field] < 0:
                raise BakeoffError(f"'{where}.{field}' phải là số USD mỗi 1M token, từ 0 trở lên")
        if not isinstance(model["price_source"], str) or not model["price_source"].startswith(
            "http"
        ):
            raise BakeoffError(f"'{where}.price_source' phải là link tới trang giá chính thức")
        if not isinstance(model["price_verified"], str) or not DATE.fullmatch(
            model["price_verified"]
        ):
            raise BakeoffError(
                f"'{where}.price_verified' phải là ngày chủ dự án đã kiểm giá, dạng YYYY-MM-DD"
            )
    return spec


def load_customer(directory: Path) -> dict[str, Any]:
    """``customer.json`` as ``founder-vn panel init`` would accept it."""
    customer = _read_json(directory, "customer.json")
    try:
        panel.validate_customer(customer)
    except panel.PanelError as e:
        raise BakeoffError(str(e)) from None
    return customer


def load_pitch(directory: Path) -> str:
    """``pitch.md`` stripped; empty is an error."""
    text = _read(directory, "pitch.md").strip()
    if not text:
        raise BakeoffError(
            "pitch.md trống: viết lời chào hàng trước (bán gì, giá bao nhiêu, ở đâu)"
        )
    return text


def _cost(candidate: dict[str, Any], reply: llm.Reply) -> float | None:
    if reply.prompt_tokens is None or reply.completion_tokens is None:
        return None
    return (
        reply.prompt_tokens * candidate["input_usd_per_1m"]
        + reply.completion_tokens * candidate["output_usd_per_1m"]
    ) / 1_000_000


def ask(
    config: llm.Config,
    candidate: dict[str, Any],
    card: dict[str, Any],
    pitch: str,
    *,
    timeout: float = llm.TIMEOUT,
    backoff: float = BACKOFF,
    sleep: Callable[[float], Any] = time.sleep,
) -> dict[str, Any]:
    """Ask one candidate for one persona's answer, exactly as the panel asks; return the row.

    A call that fails (429, 5xx, timeout, connection) is retried ``ATTEMPTS`` times with doubling
    backoff; still failing, the row is ``failed``. A reply that is not a valid answer is kept with
    its problem; the script never re-asks to make a model look better.
    """
    prompt = panel.brief(card, pitch)
    row: dict[str, Any] = {
        "model": candidate["name"],
        "id": card["id"],
        "name": card["name"],
        "segment": card["segment"],
    }
    reply: llm.Reply | None = None
    for attempt in range(ATTEMPTS):
        try:
            reply = llm.complete_with_usage(
                dataclasses.replace(config, model=candidate["name"]), prompt, timeout
            )
            break
        except llm.CallFailed as e:
            if attempt == ATTEMPTS - 1:
                return {**row, "state": "failed", "error": str(e)}
            sleep(backoff * 2**attempt)
    assert reply is not None
    answer, problem = panel.extract_answer(reply.content, card["id"])
    prices = (
        {short: answer.get(long) for short, long in panel.PRICE_KEYS.items()} if answer else None
    )
    return {
        **row,
        "state": "answered",
        "raw": reply.content,
        "json_valid": answer is not None,
        "problem": problem,
        "buys": answer["buys"] if answer else None,
        "reason_code": answer["reason_code"] if answer else None,
        "reason": answer["reason"] if answer else None,
        "would_change_my_mind": answer.get("would_change_my_mind") if answer else None,
        "purchases_first_month": answer.get("purchases_first_month") if answer else None,
        "prices": prices,
        "seconds": reply.seconds,
        "prompt_tokens": reply.prompt_tokens,
        "completion_tokens": reply.completion_tokens,
        "cost_usd": _cost(candidate, reply),
    }


def _mean(values: list[Any]) -> float | None:
    numbers = [v for v in values if isinstance(v, (int, float)) and not isinstance(v, bool)]
    return statistics.fmean(numbers) if numbers else None


def summarise(candidate: dict[str, Any], rows: list[dict[str, Any]]) -> dict[str, Any]:
    """The machine-measured side of one candidate, counted from its rows."""
    answered = [r for r in rows if r["state"] == "answered"]
    valid = [r for r in answered if r["json_valid"]]
    return {
        "name": candidate["name"],
        "calls": len(rows),
        "answered": len(answered),
        "failed": len(rows) - len(answered),
        "json_valid": len(valid),
        "json_valid_rate": len(valid) / len(answered) if answered else None,
        "buys": sum(1 for r in valid if r["buys"] is True),
        "mean_seconds": _mean([r["seconds"] for r in answered]),
        "mean_prompt_tokens": _mean([r["prompt_tokens"] for r in answered]),
        "mean_completion_tokens": _mean([r["completion_tokens"] for r in answered]),
        "mean_cost_usd_per_buyer": _mean([r["cost_usd"] for r in answered]),
        "input_usd_per_1m": candidate["input_usd_per_1m"],
        "output_usd_per_1m": candidate["output_usd_per_1m"],
        "price_source": candidate["price_source"],
        "price_verified": candidate["price_verified"],
    }


def _dump(obj: Any) -> str:
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


def _vnd(value: Any) -> str:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return "—"
    return f"{int(round(value)):,}".replace(",", ".") + " đ"


def _num(value: float | None, digits: int) -> str:
    return "—" if value is None else f"{value:.{digits}f}".replace(".", ",")


def _cell(value: Any) -> str:
    return "—" if value in (None, "") else str(value).replace("|", "/").replace("\n", " ")


def replies_md(results: dict[str, Any]) -> str:
    """The Vietnamese side-by-side document the owner reads to judge voice and honesty."""
    models = results["models"]
    lines = [
        "# Bake-off mô hình cho panel người mua",
        "",
        f"Chạy ngày {results['ran_at']}: {len(results['personas'])} người mua mô phỏng, mỗi "
        f"người hỏi {len(models)} mô hình bằng đúng brief của `founder-vn panel run`. Seed "
        f"{results['seed']}, hash prompt `{results['prompt_hash']}`. Panel là mô phỏng, không "
        "phải khách hàng thật; tài liệu này chỉ để chọn mô hình tham chiếu.",
        "",
        "## Số đo máy",
        "",
        "| mô hình | JSON hợp lệ | nói mua | lỗi gọi | độ trễ TB (giây) | token vào/ra TB | "
        "chi phí TB mỗi người mua (USD) | giá vào/ra (USD mỗi 1M token, ngày kiểm) |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for m in models:
        lines.append(
            f"| {m['name']} | {m['json_valid']}/{m['answered']} | {m['buys']}/{m['json_valid']} | "
            f"{m['failed']} | {_num(m['mean_seconds'], 1)} | "
            f"{_num(m['mean_prompt_tokens'], 0)}/{_num(m['mean_completion_tokens'], 0)} | "
            f"{_num(m['mean_cost_usd_per_buyer'], 6)} | "
            f"{_num(m['input_usd_per_1m'], 2)}/{_num(m['output_usd_per_1m'], 2)} "
            f"({m['price_verified']}) |"
        )
    lines += [
        "",
        '"Nói mua" là số người mua mô phỏng trả lời `buys: true`; một mô hình nói mua gần hết '
        "là một mô hình đang chiều người bán.",
        "",
        "## Phiếu chấm của chủ dự án",
        "",
        'Đọc mục "Từng người mua" rồi chấm 1–5 (5 là tốt nhất). Mô hình được chọn ghi vào '
        "trường `reference` của `models.json`.",
        "",
        "| mô hình | giọng Việt tự nhiên (1–5) | thẳng thắn, không chiều người bán (1–5) | ghi chú |",
        "| --- | ---: | ---: | --- |",
    ]
    lines += [f"| {m['name']} |  |  |  |" for m in models]
    lines += ["", "## Từng người mua"]
    for card in results["personas"]:
        lines += [
            "",
            f"### {card['id']} · {card['name']}, {card['age']} tuổi, {card['segment']}, "
            f"thu nhập {_vnd(card['income'])}/tháng",
            "",
            f"Cách mua: {card['behaviour']}. {card['behaviour_how']} Điều e ngại: "
            f"{card['objection'].rstrip('.')}. Thói quen: {card['habit'] or '—'}",
            "",
            "| mô hình | mua? | lý do (nguyên văn) | điều gì đổi ý | lần/tháng | "
            "rẻ nghi ngờ / đáng mua / bắt đầu đắt / quá đắt | JSON |",
            "| --- | --- | --- | --- | ---: | --- | --- |",
        ]
        for row in results["replies"]:
            if row["id"] != card["id"]:
                continue
            if row["state"] == "failed":
                lines.append(
                    f"| {row['model']} | — | lỗi gọi: {_cell(row['error'])} | — | — | — | — |"
                )
                continue
            if not row["json_valid"]:
                lines.append(
                    f"| {row['model']} | — | {_cell(row['raw'])} | — | — | — | "
                    f"hỏng: {_cell(row['problem'])} |"
                )
                continue
            prices = row["prices"] or {}
            lines.append(
                f"| {row['model']} | {'mua' if row['buys'] else 'không'} | {_cell(row['reason'])} | "
                f"{_cell(row['would_change_my_mind'])} | {_cell(row['purchases_first_month'])} | "
                f"{_vnd(prices.get('too_cheap'))} / {_vnd(prices.get('bargain'))} / "
                f"{_vnd(prices.get('getting_expensive'))} / {_vnd(prices.get('too_expensive'))} | "
                "hợp lệ |"
            )
    return "\n".join(lines) + "\n"


def run(
    directory: Path,
    *,
    seed: int = DEFAULT_SEED,
    pause: float = PAUSE,
    backoff: float = BACKOFF,
    timeout: float = llm.TIMEOUT,
    sleep: Callable[[float], Any] = time.sleep,
    env: dict[str, str] | None = None,
    only: set[str] | None = None,
) -> dict[str, Any]:
    """Deal the personas, ask every candidate, write ``results.json`` and ``replies.md``.

    With ``only``, just the named candidates are asked again and the other candidates' rows are
    kept from the existing ``results.json`` of the same seed and prompt hash.
    """
    spec = load_models(directory)
    customer = load_customer(directory)
    pitch = load_pitch(directory)
    try:
        config = llm.load_config(env)
    except llm.NotConfigured as e:
        raise BakeoffError(str(e)) from None
    cards = panel.deal(customer, PERSONAS, seed)
    prompt_hash = panel.prompt_hash(cards, pitch)
    names = [c["name"] for c in spec["models"]]
    kept: list[dict[str, Any]] = []
    if only is not None:
        unknown = sorted(only - set(names))
        if unknown:
            raise BakeoffError(
                f"--only nêu mô hình không có trong models.json: {', '.join(unknown)}"
            )
        previous = _read_json(directory, "results.json")
        if previous.get("seed") != seed or previous.get("prompt_hash") != prompt_hash:
            raise BakeoffError(
                "results.json hiện có chạy với seed hoặc prompt khác; bỏ --only để chạy lại cả ba"
            )
        kept = [r for r in previous["replies"] if r["model"] not in only]
    rows: list[dict[str, Any]] = []
    for candidate in spec["models"]:
        if only is not None and candidate["name"] not in only:
            continue
        for card in cards:
            if rows:
                sleep(pause)
            rows.append(
                ask(config, candidate, card, pitch, timeout=timeout, backoff=backoff, sleep=sleep)
            )
    rows = sorted(kept + rows, key=lambda r: (names.index(r["model"]), r["id"]))
    results = {
        "ran_at": date.today().isoformat(),
        "seed": seed,
        "prompt_hash": prompt_hash,
        "business": customer["business"],
        "personas": cards,
        "models": [
            summarise(c, [r for r in rows if r["model"] == c["name"]]) for c in spec["models"]
        ],
        "replies": rows,
    }
    (directory / "results.json").write_text(_dump(results), encoding="utf-8")
    (directory / "replies.md").write_text(replies_md(results), encoding="utf-8")
    return results


def main(argv: list[str] | None = None) -> int:
    """Run the bake-off from the command line; return the exit code (2 on a bad input)."""
    parser = argparse.ArgumentParser(
        prog="bakeoff.py",
        description="Ask the same five simulated buyers of every candidate model; write "
        "results.json and replies.md into the directory.",
    )
    parser.add_argument("directory", type=Path, help="holds models.json, customer.json, pitch.md")
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="same seed, same personas")
    parser.add_argument(
        "--pause", type=float, default=PAUSE, help="seconds between two calls (free-tier pacing)"
    )
    parser.add_argument(
        "--backoff", type=float, default=BACKOFF, help="seconds before retrying a failed call"
    )
    parser.add_argument(
        "--timeout", type=float, default=llm.TIMEOUT, help="seconds to wait for one reply"
    )
    parser.add_argument(
        "--only",
        action="append",
        default=None,
        metavar="MODEL",
        help="ask only this candidate again (repeatable); other rows kept from results.json",
    )
    args = parser.parse_args(argv)
    try:
        results = run(
            args.directory,
            seed=args.seed,
            pause=args.pause,
            backoff=args.backoff,
            timeout=args.timeout,
            only=set(args.only) if args.only else None,
        )
    except BakeoffError as e:
        print(f"lỗi: {e}", file=sys.stderr)
        return 2
    for m in results["models"]:
        print(
            f"{m['name']}: JSON hợp lệ {m['json_valid']}/{m['answered']}, nói mua {m['buys']}, "
            f"lỗi gọi {m['failed']}, độ trễ TB {_num(m['mean_seconds'], 1)} giây, chi phí TB "
            f"{_num(m['mean_cost_usd_per_buyer'], 6)} USD mỗi người mua"
        )
    print(f"Đã ghi {args.directory / 'results.json'} và {args.directory / 'replies.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
