"""Wave B example completeness: permits, ops, marketing, launch and the plan's after-pilot lines (issue #117).

Each check is a function over a directory, so a test can run it on a mutated copy under tmp_path
and watch it go red; the committed example is never mutated.
"""

import re
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
FOUNDER = ROOT / "examples" / "barbershop" / "founder"
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
DATE = re.compile(r"\d{2}/\d{2}/\d{4}")
LINK = "https://congbao.chinhphu.vn/"
WAVE_B_FILES = ("permits.md", "ops.md", "marketing.md", "launch.md")
PANEL_FILES = ("marketing.md", "launch.md")
CAVEAT_PARTS = ("mô phỏng", "cận trên", "không phải khách hàng thật")
AFTER_PILOT = (
    "- Đề xuất giá trị: chạy skill `founder-offer` (tạo founder/offer.md).",
    "- Thương hiệu: chạy skill `founder-brand` (tạo founder/brand.md).",
)


def check_files_present(folder: Path) -> None:
    for name in WAVE_B_FILES:
        assert (folder / name).is_file(), name


def check_no_dollar(folder: Path) -> None:
    for name in WAVE_B_FILES:
        assert not DOLLAR.search((folder / name).read_text(encoding="utf-8")), name


def check_disclaimer(folder: Path) -> None:
    for name in WAVE_B_FILES:
        assert "không phải tư vấn" in (folder / name).read_text(encoding="utf-8"), name


def check_panel_caveat(folder: Path) -> None:
    for name in PANEL_FILES:
        text = (folder / name).read_text(encoding="utf-8")
        for part in CAVEAT_PARTS:
            assert part in text, (name, part)


def check_permits_links_dated(folder: Path) -> None:
    lines = [
        line
        for line in (folder / "permits.md").read_text(encoding="utf-8").splitlines()
        if LINK in line
    ]
    assert lines, "permits.md carries no congbao.chinhphu.vn link"
    for line in lines:
        assert DATE.search(line), line[:100]


def check_plan_after_pilot(folder: Path) -> None:
    text = (folder / "business-plan.md").read_text(encoding="utf-8")
    section = text.split("\n## Chưa làm\n", 1)[1].split("\n## ", 1)[0]
    bullets = [line for line in section.splitlines() if line.startswith("- ")]
    assert tuple(bullets) == AFTER_PILOT, bullets


CHECKS = {
    "present": check_files_present,
    "dollar": check_no_dollar,
    "disclaimer": check_disclaimer,
    "caveat": check_panel_caveat,
    "dated_links": check_permits_links_dated,
    "after_pilot": check_plan_after_pilot,
}


def test_example_holds_every_wave_b_artifact() -> None:
    check_files_present(FOUNDER)


def test_no_dollar_in_wave_b_files() -> None:
    check_no_dollar(FOUNDER)


def test_every_wave_b_file_carries_the_disclaimer() -> None:
    check_disclaimer(FOUNDER)


def test_files_quoting_a_panel_number_carry_the_caveat() -> None:
    check_panel_caveat(FOUNDER)


def test_every_congbao_link_in_permits_carries_a_verification_date() -> None:
    check_permits_links_dated(FOUNDER)


def test_business_plan_lists_exactly_the_two_after_pilot_lines() -> None:
    check_plan_after_pilot(FOUNDER)


def _copy(tmp_path: Path) -> Path:
    folder = tmp_path / "founder"
    shutil.copytree(FOUNDER, folder)
    return folder


def _edit(folder: Path, name: str, old: str, new: str, count: int = -1) -> None:
    path = folder / name
    text = path.read_text(encoding="utf-8")
    assert old in text, (name, old)
    path.write_text(text.replace(old, new, count), encoding="utf-8")


def _drop_file(folder: Path) -> None:
    (folder / "ops.md").unlink()


def _add_dollar(folder: Path) -> None:
    _edit(folder, "launch.md", "199.000 đ", "$199", 1)


def _drop_disclaimer(folder: Path) -> None:
    _edit(folder, "ops.md", "không phải tư vấn", "chỉ là tham khảo")


def _drop_caveat(folder: Path) -> None:
    _edit(folder, "marketing.md", "cận trên", "gần đúng")


def _undate_link(folder: Path) -> None:
    text = (folder / "permits.md").read_text(encoding="utf-8").splitlines(keepends=True)
    index = next(i for i, line in enumerate(text) if LINK in line)
    text[index] = DATE.sub("(chưa ghi ngày)", text[index])
    (folder / "permits.md").write_text("".join(text), encoding="utf-8")


def _extra_after_pilot(folder: Path) -> None:
    _edit(
        folder,
        "business-plan.md",
        "## Chưa làm\n\n",
        "## Chưa làm\n\n- Giấy phép: chạy skill `founder-permits` (tạo founder/permits.md).\n",
    )


MUTATIONS = {
    "present": _drop_file,
    "dollar": _add_dollar,
    "disclaimer": _drop_disclaimer,
    "caveat": _drop_caveat,
    "dated_links": _undate_link,
    "after_pilot": _extra_after_pilot,
}


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_each_check_goes_red_on_its_mutation(name: str, tmp_path: Path) -> None:
    folder = _copy(tmp_path)
    CHECKS[name](folder)
    MUTATIONS[name](folder)
    with pytest.raises(AssertionError):
        CHECKS[name](folder)
