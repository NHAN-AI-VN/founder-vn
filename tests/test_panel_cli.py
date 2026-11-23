"""Tests of `founder-vn panel` through the CLI."""

import io
import json
import shutil
from collections.abc import Callable
from pathlib import Path

import pytest
from conftest import CliRun

FIXTURES = Path(__file__).parent / "fixtures"
RunCli = Callable[..., CliRun]


@pytest.fixture
def founder(project_root: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """founder/ with the synthetic customer.json and pitch.md; the cwd is the project root."""
    monkeypatch.chdir(project_root)
    root = project_root / "founder"
    root.mkdir()
    shutil.copy(FIXTURES / "panel_customer.json", root / "customer.json")
    shutil.copy(FIXTURES / "panel_pitch.md", root / "pitch.md")
    return root


def _cards(run: CliRun) -> list[dict[str, object]]:
    return json.loads(run.files["panel/personas.json"])


def test_init_deals_vietnamese_cards_by_quota_seed_7(founder: Path, run_cli: RunCli) -> None:
    """Seed 7, n=7. Quotas by largest remainder, worked by hand: segments 0.5/0.3/0.2 give raw
    3.5/2.1/1.4, floors 3/2/1, the one spare seat goes to the largest remainder (0.5): 4/2/1;
    behaviours 0.5/0.3/0.2 give the same 4/2/1."""
    run = run_cli("panel", "init", "--n", "7", "--seed", "7")
    assert run.exit_code == 0
    cards = _cards(run)
    assert [c["id"] for c in cards] == [f"P00{i}" for i in range(1, 8)]
    by_segment = [c["segment"] for c in cards]
    assert by_segment.count("Nhân viên mới đi làm") == 4
    assert by_segment.count("Nhân viên lâu năm") == 2
    assert by_segment.count("Thu nhập cao") == 1
    by_behaviour = [c["behaviour"] for c in cards]
    assert by_behaviour.count("Quen quán") == 4
    assert by_behaviour.count("Mua theo hội nhóm") == 2
    assert by_behaviour.count("Săn voucher app") == 1
    ranges = {
        "Nhân viên mới đi làm": (8_000_000, 15_000_000),
        "Nhân viên lâu năm": (15_000_000, 30_000_000),
        "Thu nhập cao": (30_000_000, 60_000_000),
    }
    for c in cards:
        low, high = ranges[str(c["segment"])]
        assert isinstance(c["income"], int)
        assert c["income"] % 100_000 == 0
        assert low <= c["income"] <= high
        assert isinstance(c["age"], int) and 24 <= c["age"] <= 38
        assert c["objection"] in json.loads(run.files["customer.json"])["objections"]
    assert len({c["name"] for c in cards}) == 7


def test_same_seed_same_cards_other_seed_other_cards(
    founder: Path, run_cli: RunCli, project_root: Path
) -> None:
    first = _cards(run_cli("panel", "init", "--n", "20", "--seed", "7"))
    again = _cards(run_cli("panel", "init", "--n", "20", "--seed", "7"))
    other = _cards(run_cli("panel", "init", "--n", "20", "--seed", "8"))
    assert first == again
    assert first != other


def _fail(founder: Path, capsys: pytest.CaptureFixture[str], change: Callable[[dict], None]) -> str:
    """Apply ``change`` to customer.json, run `panel init`, expect exit 2; return stderr."""
    from founder_vn.cli import main

    customer = json.loads((founder / "customer.json").read_text(encoding="utf-8"))
    change(customer)
    (founder / "customer.json").write_text(json.dumps(customer), encoding="utf-8")
    capsys.readouterr()
    assert main(["panel", "init", "--n", "7", "--seed", "7"]) == 2
    return capsys.readouterr().err


@pytest.mark.parametrize(
    ("change", "field"),
    [
        pytest.param(lambda c: c.pop("business"), "business", id="business"),
        pytest.param(lambda c: c.update(objections=[]), "objections", id="objections"),
        pytest.param(lambda c: c["segments"][1].pop("name"), "segments[1].name", id="seg-name"),
        pytest.param(
            lambda c: c["segments"][1].update(income=[30000000]), "segments[1].income", id="income"
        ),
        pytest.param(
            lambda c: c["segments"][0].update(income=["a", "b"]),
            "segments[0].income",
            id="income-nan",
        ),
        pytest.param(
            lambda c: c["segments"][2].update(income=[60000000, 30000000]),
            "segments[2].income",
            id="income-order",
        ),
        pytest.param(lambda c: c["segments"][2].pop("share"), "segments[2].share", id="seg-share"),
        pytest.param(lambda c: c["behaviours"][0].pop("name"), "behaviours[0].name", id="beh-name"),
        pytest.param(
            lambda c: c["behaviours"][1].update(share=-1), "behaviours[1].share", id="beh-share"
        ),
        pytest.param(lambda c: c.pop("age"), "age", id="age"),
    ],
)
def test_customer_error_names_the_field(
    founder: Path,
    capsys: pytest.CaptureFixture[str],
    change: Callable[[dict], None],
    field: str,
) -> None:
    err = _fail(founder, capsys, change)
    assert err.startswith("lỗi: ")
    assert f"'{field}'" in err


def test_empty_or_missing_pitch_and_bad_n_are_errors(
    founder: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from founder_vn.cli import main

    (founder / "pitch.md").write_text("  \n", encoding="utf-8")
    assert main(["panel", "init", "--seed", "7"]) == 2
    assert "pitch.md" in capsys.readouterr().err
    (founder / "pitch.md").unlink()
    assert main(["panel", "init", "--seed", "7"]) == 2
    assert "pitch.md" in capsys.readouterr().err
    assert main(["panel", "init", "--n", "0", "--seed", "7"]) == 2
    assert "'--n'" in capsys.readouterr().err


def test_init_writes_only_panel_json_and_personas_under_founder_panel(
    founder: Path, run_cli: RunCli
) -> None:
    run = run_cli("panel", "init", "--n", "7", "--seed", "7")
    assert sorted(run.files) == [
        "customer.json",
        "panel/panel.json",
        "panel/personas.json",
        "pitch.md",
    ]
    panel = json.loads(run.files["panel/panel.json"])
    assert (panel["n"], panel["seed"]) == (7, 7)
    assert panel["pitch"] == (FIXTURES / "panel_pitch.md").read_text(encoding="utf-8").strip()
    assert panel["customer"] == json.loads(run.files["customer.json"])
    assert run.stdout == "Đã chia 7 người mua (seed 7) vào founder/panel/\n"


def test_customer_outside_founder_is_refused(
    founder: Path, project_root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    from founder_vn.cli import main

    shutil.copy(FIXTURES / "panel_customer.json", project_root / "customer.json")
    assert main(["panel", "init", "--customer", "../customer.json", "--seed", "7"]) == 2
    assert "path refused" in capsys.readouterr().err
    assert not (founder / "panel").exists()


GOOD = {"id": "P001", "buys": True, "reason_code": "habit", "reason": "Quen quán gần nhà."}


def _answer(founder: Path, pid: str, body: str) -> None:
    target = founder / "panel" / "answers" / f"{pid}.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(body, encoding="utf-8")


def test_check_lists_missing_and_broken_answers_exit_1_seed_7(
    founder: Path, run_cli: RunCli
) -> None:
    run_cli("panel", "init", "--n", "5", "--seed", "7")
    _answer(founder, "P001", json.dumps(GOOD))
    _answer(founder, "P002", "{not json")
    _answer(founder, "P003", json.dumps({**GOOD, "id": "P003", "buys": "yes"}))
    _answer(founder, "P004", json.dumps({"id": "P004", "buys": False}))
    run = run_cli("panel", "check")
    assert run.exit_code == 1
    assert run.stdout.splitlines() == [
        "P002: không phải JSON hợp lệ",
        "P003: 'buys' phải là true hoặc false",
        "P004: thiếu reason, reason_code",
        "P005: chưa có câu trả lời",
    ]


def test_check_all_good_exit_0(founder: Path, run_cli: RunCli) -> None:
    run_cli("panel", "init", "--n", "1", "--seed", "7")
    _answer(founder, "P001", json.dumps(GOOD))
    run = run_cli("panel", "check")
    assert (run.exit_code, run.stdout) == (0, "Mọi câu trả lời đều có và hợp lệ\n")


def test_save_extracts_first_json_object_and_files_it(
    founder: Path, run_cli: RunCli, monkeypatch: pytest.MonkeyPatch
) -> None:
    run_cli("panel", "init", "--n", "2", "--seed", "7")
    reply = "Tôi trả lời thế này:\n" + json.dumps(GOOD) + '\nvà {"id": "khác"}'
    monkeypatch.setattr("sys.stdin", io.StringIO(reply))
    run = run_cli("panel", "save", "P001")
    assert (run.exit_code, run.stdout) == (0, "Đã lưu founder/panel/answers/P001.json\n")
    assert json.loads(run.files["panel/answers/P001.json"]) == GOOD


@pytest.mark.parametrize(
    ("pid", "reply", "message"),
    [
        pytest.param("P001", "không có gì", "không có đối tượng JSON", id="no-json"),
        pytest.param("P001", '{"id": "P001", "buys": tru', "không đọc được", id="broken-json"),
        pytest.param("P001", '{"id": "P002", "buys": true}', "không hợp lệ", id="wrong-id"),
        pytest.param("P009", json.dumps(GOOD), "P009", id="unknown-buyer"),
    ],
)
def test_save_refuses_invalid_answers_and_leaves_no_file(
    pid: str,
    reply: str,
    message: str,
    founder: Path,
    run_cli: RunCli,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    run_cli("panel", "init", "--n", "2", "--seed", "7")
    monkeypatch.setattr("sys.stdin", io.StringIO(reply))
    from founder_vn.cli import main

    assert main(["panel", "save", pid]) == 2
    assert message in capsys.readouterr().err
    assert not (founder / "panel" / "answers").exists()


def _write_answers(founder: Path) -> None:
    answers = json.loads((FIXTURES / "panel_answers.json").read_text(encoding="utf-8"))
    for pid, answer in answers.items():
        _answer(founder, pid, json.dumps(answer, ensure_ascii=False))


@pytest.fixture
def tallied(founder: Path, run_cli: RunCli) -> CliRun:
    """Seed 7, n=7: P001-P005 answered validly, P006 broken, P007 missing."""
    run_cli("panel", "init", "--n", "7", "--seed", "7")
    _write_answers(founder)
    return run_cli("panel", "tally")


def test_tally_counts_and_results_json_keys_seed_7(tallied: CliRun) -> None:
    assert tallied.exit_code == 0
    assert tallied.stdout == (
        "3 mua, 2 không mua (60%). Đã ghi founder/panel/results.md và founder/panel/results.json\n"
    )
    result = json.loads(tallied.files["panel/results.json"])
    assert {
        k: result[k] for k in ("mode", "model", "prompt_hash", "n", "answered", "excluded")
    } == {
        "mode": "manual",
        "model": None,
        "prompt_hash": None,
        "n": 7,
        "answered": 5,
        "excluded": 2,
    }
    assert result["buys"] == 3
    assert result["passes"] == 2
    assert result["buy_rate"] == 0.6
    assert result["excluded_buyers"] == [
        {"id": "P006", "problem": "'buys' phải là true hoặc false"},
        {"id": "P007", "problem": "chưa có câu trả lời"},
    ]
    assert result["flip"] == [
        "Có thẻ tích điểm hoặc giảm giá ly đầu.",
        "Quán mới ngon hơn rõ rệt.",
    ]
    assert sum(r["n"] for r in result["by_segment"]) == 5
    assert sum(r["n"] for r in result["by_behaviour"]) == 5
    assert sum(r["buys"] for r in result["by_behaviour"]) == 3
    assert result["price_answers"] == 3


def test_tally_reads_mode_model_prompt_hash_from_panel_json(founder: Path, run_cli: RunCli) -> None:
    run_cli("panel", "init", "--n", "7", "--seed", "7")
    panel_json = founder / "panel" / "panel.json"
    meta = json.loads(panel_json.read_text(encoding="utf-8"))
    meta |= {"mode": "model", "model": "mô-hình-thử", "prompt_hash": "ab12"}
    panel_json.write_text(json.dumps(meta), encoding="utf-8")
    _write_answers(founder)
    result = json.loads(run_cli("panel", "tally").files["panel/results.json"])
    assert (result["mode"], result["model"], result["prompt_hash"]) == (
        "model",
        "mô-hình-thử",
        "ab12",
    )


def test_tally_without_valid_answers_is_an_error(
    founder: Path, run_cli: RunCli, capsys: pytest.CaptureFixture[str]
) -> None:
    from founder_vn.cli import main

    run_cli("panel", "init", "--n", "3", "--seed", "7")
    assert main(["panel", "tally"]) == 2
    assert "chưa có câu trả lời hợp lệ" in capsys.readouterr().err


def test_tally_golden_seed_7(tallied: CliRun, assert_golden: Callable[[str, CliRun], None]) -> None:
    assert_golden("panel_tally", tallied)


def test_results_md_is_vietnamese_with_caveat_and_no_dollar(tallied: CliRun) -> None:
    md = tallied.files["panel/results.md"]
    assert "Panel là mô phỏng, không phải khách hàng thật" in md
    assert "Tín hiệu cầu (mô phỏng, cận trên)" in md
    assert "anh/chị" in md
    assert "$" not in md
    assert "Giá cao hơn quán quen / mười nghìn." in md


def test_price_answers_are_consumable_by_pricing(tallied: CliRun, run_cli: RunCli) -> None:
    """P001 and P003 use the long names, P002 the short names; P004, P005 gave none."""
    shape = json.loads(tallied.files["panel/pricing_input.json"])
    assert shape["answers"] == [
        {"too_cheap": "15k", "bargain": "25k", "getting_expensive": "40k", "too_expensive": "55k"},
        {"too_cheap": 12000, "bargain": 22000, "getting_expensive": 35000, "too_expensive": 48000},
        {
            "too_cheap": "20.000",
            "bargain": "30.000",
            "getting_expensive": "45.000",
            "too_expensive": "60.000",
        },
    ]
    run = run_cli("pricing", "panel/pricing_input.json", "--json")
    assert run.exit_code == 0
    assert json.loads(run.stdout)["answers"] == {"valid": 3, "dropped": 0}
