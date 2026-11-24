"""Tests of the model bake-off script `scripts/bakeoff.py` against the fake provider."""

import importlib.util
import json
import shutil
from pathlib import Path
from types import ModuleType

import pytest

SCRIPT = Path(__file__).parent.parent / "scripts" / "bakeoff.py"
FIXTURES = Path(__file__).parent / "fixtures"


def _load() -> ModuleType:
    spec = importlib.util.spec_from_file_location("bakeoff", SCRIPT)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


bakeoff = _load()

MODELS = [
    {
        "name": "mo-hinh-a",
        "input_usd_per_1m": 0.25,
        "output_usd_per_1m": 1.5,
        "price_source": "https://example.invalid/pricing",
        "price_verified": "2026-11-23",
    },
    {
        "name": "mo-hinh-b",
        "input_usd_per_1m": 0.3,
        "output_usd_per_1m": 2.5,
        "price_source": "https://example.invalid/pricing",
        "price_verified": "2026-11-23",
    },
    {
        "name": "mo-hinh-c",
        "input_usd_per_1m": 0.75,
        "output_usd_per_1m": 3.75,
        "price_source": "https://example.invalid/pricing",
        "price_verified": "2026-11-23",
    },
]


@pytest.fixture
def bakeoff_dir(tmp_path: Path) -> Path:
    """A bake-off directory with the synthetic customer and pitch and three priced candidates."""
    shutil.copy(FIXTURES / "panel_customer.json", tmp_path / "customer.json")
    shutil.copy(FIXTURES / "panel_pitch.md", tmp_path / "pitch.md")
    (tmp_path / "models.json").write_text(
        json.dumps({"models": MODELS, "reference": None}, ensure_ascii=False), encoding="utf-8"
    )
    return tmp_path


def _write_models(directory: Path, models: list[dict]) -> None:
    (directory / "models.json").write_text(json.dumps({"models": models}), encoding="utf-8")


def test_models_file_problems_are_errors_naming_the_field(bakeoff_dir: Path) -> None:
    assert [m["name"] for m in bakeoff.load_models(bakeoff_dir)["models"]] == [
        "mo-hinh-a",
        "mo-hinh-b",
        "mo-hinh-c",
    ]
    broken = [dict(MODELS[0]), {k: v for k, v in MODELS[1].items() if k != "price_verified"}]
    _write_models(bakeoff_dir, broken)
    with pytest.raises(bakeoff.BakeoffError, match=r"models\[1\]\.price_verified"):
        bakeoff.load_models(bakeoff_dir)
    _write_models(bakeoff_dir, [dict(MODELS[0]), {**MODELS[1], "input_usd_per_1m": "0,30"}])
    with pytest.raises(bakeoff.BakeoffError, match=r"models\[1\]\.input_usd_per_1m"):
        bakeoff.load_models(bakeoff_dir)
    _write_models(bakeoff_dir, [dict(MODELS[0]), {**MODELS[1], "price_verified": "hôm qua"}])
    with pytest.raises(bakeoff.BakeoffError, match=r"models\[1\]\.price_verified.*YYYY-MM-DD"):
        bakeoff.load_models(bakeoff_dir)
    _write_models(bakeoff_dir, [dict(MODELS[0])])
    with pytest.raises(bakeoff.BakeoffError, match="hai"):
        bakeoff.load_models(bakeoff_dir)
    (bakeoff_dir / "models.json").unlink()
    with pytest.raises(bakeoff.BakeoffError, match="models.json"):
        bakeoff.load_models(bakeoff_dir)


def test_customer_and_pitch_are_checked_like_the_panel_does(bakeoff_dir: Path) -> None:
    assert bakeoff.load_pitch(bakeoff_dir).startswith(
        (bakeoff_dir / "pitch.md").read_text(encoding="utf-8").strip()[:20]
    )
    customer = bakeoff.load_customer(bakeoff_dir)
    assert len(customer["segments"]) == 3
    (bakeoff_dir / "pitch.md").write_text("\n", encoding="utf-8")
    with pytest.raises(bakeoff.BakeoffError, match="pitch.md"):
        bakeoff.load_pitch(bakeoff_dir)
    broken = {**customer, "segments": []}
    (bakeoff_dir / "customer.json").write_text(json.dumps(broken), encoding="utf-8")
    with pytest.raises(bakeoff.BakeoffError, match="segments"):
        bakeoff.load_customer(bakeoff_dir)
