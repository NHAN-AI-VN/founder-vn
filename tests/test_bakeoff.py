"""Tests of the model bake-off script `scripts/bakeoff.py` against the fake provider."""

import importlib.util
import json
import re
import shutil
from pathlib import Path
from types import ModuleType

import pytest
from conftest import FakeProvider

from founder_vn import panel

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


def _setenv(monkeypatch: pytest.MonkeyPatch, provider: FakeProvider) -> None:
    monkeypatch.setenv("FOUNDER_LLM_BASE_URL", provider.base_url)
    monkeypatch.setenv("FOUNDER_LLM_API_KEY", "khoa-gia")
    monkeypatch.setenv("FOUNDER_LLM_MODEL", "mo-hinh-gia")


def _buyer(body: dict) -> str:
    match = re.search(r'"id": "(P\d+)"', body["messages"][0]["content"])
    assert match
    return match.group(1)


def _answer(pid: str, buys: bool, model: str) -> str:
    return json.dumps(
        {
            "id": pid,
            "buys": buys,
            "reason_code": "need" if buys else "price",
            "reason": f"{model} nói {pid} {'mua' if buys else 'không mua'}.",
            "would_change_my_mind": "" if buys else "Giảm còn 30.000 đ thì mua.",
            "purchases_first_month": 4 if buys else 0,
            "price_too_cheap": 15000,
            "price_cheap": 25000,
            "price_expensive": 40000,
            "price_too_expensive": 60000,
        },
        ensure_ascii=False,
    )


IDS = ["P001", "P002", "P003", "P004", "P005"]


def test_run_asks_each_candidate_the_same_five_personas_and_writes_results_and_replies(
    bakeoff_dir: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def script(body: dict, n: int) -> tuple[int, str, float]:
        model, pid = body["model"], _buyer(body)
        if model == "mo-hinh-b" and pid == "P003":
            return 200, "Dạ em không biết trả lời bằng JSON.", 0.0
        return 200, _answer(pid, buys=model != "mo-hinh-c", model=model), 0.0

    fake_provider.script = script
    fake_provider.usage = lambda body, n: (600, 150) if body["model"] == "mo-hinh-a" else (600, 300)
    slept: list[float] = []
    results = bakeoff.run(bakeoff_dir, seed=7, pause=4.0, backoff=10.0, sleep=slept.append)

    assert len(fake_provider.requests) == 15
    for name in ("mo-hinh-a", "mo-hinh-b", "mo-hinh-c"):
        assert [_buyer(r) for r in fake_provider.requests if r["model"] == name] == IDS
    assert slept == [4.0] * 14
    customer = json.loads((bakeoff_dir / "customer.json").read_text(encoding="utf-8"))
    pitch = (bakeoff_dir / "pitch.md").read_text(encoding="utf-8").strip()
    cards = panel.deal(customer, 5, 7)
    assert fake_provider.requests[0]["messages"][0]["content"] == panel.brief(cards[0], pitch)
    assert results["prompt_hash"] == panel.prompt_hash(cards, pitch)
    assert results["seed"] == 7 and [p["id"] for p in results["personas"]] == IDS

    a, b, c = results["models"]
    assert (a["name"], a["calls"], a["answered"], a["failed"]) == ("mo-hinh-a", 5, 5, 0)
    assert (a["json_valid"], a["json_valid_rate"], a["buys"]) == (5, 1.0, 5)
    assert (b["json_valid"], b["json_valid_rate"], b["buys"]) == (4, 0.8, 4)
    assert (c["json_valid"], c["buys"]) == (5, 0)
    assert a["mean_cost_usd_per_buyer"] == pytest.approx(600 * 0.25 / 1e6 + 150 * 1.5 / 1e6)
    assert b["mean_cost_usd_per_buyer"] == pytest.approx(600 * 0.3 / 1e6 + 300 * 2.5 / 1e6)
    assert a["mean_seconds"] > 0 and a["mean_prompt_tokens"] == 600
    assert (a["price_source"], a["price_verified"]) == (MODELS[0]["price_source"], "2026-11-23")
    broken = [r for r in results["replies"] if r["model"] == "mo-hinh-b" and r["id"] == "P003"]
    assert broken[0]["json_valid"] is False and broken[0]["problem"] == "không có đối tượng JSON"
    assert broken[0]["raw"] == "Dạ em không biết trả lời bằng JSON."

    written = json.loads((bakeoff_dir / "results.json").read_text(encoding="utf-8"))
    assert written == results
    text = (bakeoff_dir / "replies.md").read_text(encoding="utf-8")
    assert text.startswith("# Bake-off mô hình cho panel người mua")
    assert "## Phiếu chấm" in text and "giọng Việt" in text
    for name in ("mo-hinh-a", "mo-hinh-b", "mo-hinh-c"):
        assert name in text
    for card in cards:
        assert card["name"] in text
    assert "mo-hinh-c nói P001 không mua." in text
    assert "Giảm còn 30.000 đ thì mua." in text and "60.000 đ" in text
    assert "Dạ em không biết trả lời bằng JSON." in text
    assert "mô phỏng" in text
    for secret in (fake_provider.base_url, "khoa-gia", "$"):
        assert secret not in text and secret not in json.dumps(written, ensure_ascii=False)


def test_a_candidate_that_keeps_failing_is_recorded_failed_after_retries_with_backoff(
    bakeoff_dir: Path, monkeypatch: pytest.MonkeyPatch, fake_provider: FakeProvider
) -> None:
    _setenv(monkeypatch, fake_provider)

    def script(body: dict, n: int) -> tuple[int, str, float]:
        if body["model"] == "mo-hinh-b":
            return 429, "", 0.0
        return 200, _answer(_buyer(body), buys=True, model=body["model"]), 0.0

    fake_provider.script = script
    slept: list[float] = []
    results = bakeoff.run(bakeoff_dir, seed=7, pause=4.0, backoff=10.0, sleep=slept.append)
    a, b, c = results["models"]
    assert (b["calls"], b["answered"], b["failed"]) == (5, 0, 5)
    assert (b["json_valid_rate"], b["mean_cost_usd_per_buyer"], b["mean_seconds"]) == (
        None,
        None,
        None,
    )
    assert (a["failed"], c["failed"]) == (0, 0)
    assert [r["model"] for r in fake_provider.requests].count("mo-hinh-b") == 15
    assert (slept.count(10.0), slept.count(20.0), slept.count(4.0)) == (5, 5, 14)
    row = next(r for r in results["replies"] if r["model"] == "mo-hinh-b")
    assert (row["state"], row["error"]) == ("failed", "máy chủ mô hình trả mã 429")
    text = (bakeoff_dir / "replies.md").read_text(encoding="utf-8")
    assert "lỗi gọi: máy chủ mô hình trả mã 429" in text


def test_main_exit_codes_and_messages(
    bakeoff_dir: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    fake_provider: FakeProvider,
) -> None:
    for name in ("FOUNDER_LLM_BASE_URL", "FOUNDER_LLM_API_KEY", "FOUNDER_LLM_MODEL"):
        monkeypatch.delenv(name, raising=False)
    assert bakeoff.main([str(bakeoff_dir)]) == 2
    assert "FOUNDER_LLM_BASE_URL" in capsys.readouterr().err
    _setenv(monkeypatch, fake_provider)
    fake_provider.script = lambda body, n: (200, _answer(_buyer(body), True, body["model"]), 0.0)
    assert bakeoff.main([str(bakeoff_dir), "--seed", "7", "--pause", "0"]) == 0
    out = capsys.readouterr().out
    assert "replies.md" in out and "mo-hinh-a" in out and "5/5" in out
    (bakeoff_dir / "models.json").unlink()
    assert bakeoff.main([str(bakeoff_dir)]) == 2
    assert "models.json" in capsys.readouterr().err
