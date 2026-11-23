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
INCOME_STEP = 100_000
DEFAULT_AGE = (25, 45)

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


def deal(customer: dict[str, Any], n: int, seed: int) -> list[dict[str, Any]]:
    """Deal ``n`` persona cards. Same customer, ``n`` and ``seed`` give the same cards."""
    rng = random.Random(seed)
    low_age, high_age = customer.get("age", DEFAULT_AGE)
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


def init(project: Path, customer: str, pitch: str, n: int, seed: int | None) -> str:
    """Deal the cards and write ``panel.json`` and ``personas.json``; return the stdout text."""
    spec = json.loads(files.read_text(project, customer))
    text = files.read_text(project, pitch).strip()
    if seed is None:
        seed = random.SystemRandom().randrange(1, 10**6)
    cards = deal(spec, n, seed)
    files.write_text(
        project, _path("panel.json"), _dump({"n": n, "seed": seed, "customer": spec, "pitch": text})
    )
    files.write_text(project, _path("personas.json"), _dump(cards))
    return f"Đã chia {len(cards)} người mua (seed {seed}) vào founder/{PANEL_DIR}/\n"
