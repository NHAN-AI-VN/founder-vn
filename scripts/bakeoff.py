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

import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from founder_vn import panel  # noqa: E402

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
