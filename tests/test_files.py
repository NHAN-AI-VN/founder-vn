from pathlib import Path

import pytest

from founder_vn import files
from founder_vn.files import PathRefused


def test_write_inside_root_is_accepted(project_root: Path) -> None:
    written = files.write_text(project_root, "report.md", "xin chào")
    assert written == project_root / "founder" / "report.md"
    assert written.read_text(encoding="utf-8") == "xin chào"


def test_write_creates_nested_directories(project_root: Path) -> None:
    files.write_text(project_root, "panel/answers.json", "{}")
    assert (project_root / "founder" / "panel" / "answers.json").is_file()


def test_read_inside_root(project_root: Path) -> None:
    files.write_text(project_root, "a.md", "x")
    assert files.read_text(project_root, "a.md") == "x"


def test_dotdot_is_refused(project_root: Path) -> None:
    with pytest.raises(PathRefused, match=r"\.\."):
        files.write_text(project_root, "../escape.md", "x")
    assert not (project_root / "escape.md").exists()


def test_dotdot_inside_nested_path_is_refused(project_root: Path) -> None:
    with pytest.raises(PathRefused):
        files.write_text(project_root, "a/../b.md", "x")


def test_absolute_path_outside_root_is_refused(project_root: Path, tmp_path_factory) -> None:
    outside = tmp_path_factory.mktemp("outside") / "x.md"
    with pytest.raises(PathRefused, match="absolute"):
        files.write_text(project_root, str(outside), "x")
    assert not outside.exists()


def test_absolute_path_inside_root_is_accepted(project_root: Path) -> None:
    target = project_root / "founder" / "ok.md"
    assert files.write_text(project_root, str(target), "x") == target


def test_symlink_escaping_root_is_refused(project_root: Path, tmp_path_factory) -> None:
    outside = tmp_path_factory.mktemp("outside")
    root = project_root / "founder"
    root.mkdir()
    (root / "link").symlink_to(outside, target_is_directory=True)
    with pytest.raises(PathRefused, match="symlink"):
        files.write_text(project_root, "link/x.md", "x")
    assert not (outside / "x.md").exists()


def test_symlinked_file_escaping_root_is_refused(project_root: Path, tmp_path_factory) -> None:
    outside = tmp_path_factory.mktemp("outside") / "t.md"
    outside.write_text("old", encoding="utf-8")
    root = project_root / "founder"
    root.mkdir()
    (root / "t.md").symlink_to(outside)
    with pytest.raises(PathRefused, match="symlink"):
        files.write_text(project_root, "t.md", "new")
    assert outside.read_text(encoding="utf-8") == "old"


@pytest.mark.parametrize("name", ["x.py", "x.txt", "x", "x.md.exe", "x.MD.sh"])
def test_extension_other_than_md_json_is_refused(project_root: Path, name: str) -> None:
    with pytest.raises(PathRefused, match="extension"):
        files.write_text(project_root, name, "x")


def test_no_delete_function_exists() -> None:
    public = [n for n in dir(files) if not n.startswith("_")]
    forbidden = ("delete", "remove", "unlink", "rmtree", "rmdir")
    assert [n for n in public if any(f in n.lower() for f in forbidden)] == []


def test_files_module_never_calls_a_deleting_api() -> None:
    source = Path(files.__file__).read_text(encoding="utf-8")
    for call in (".unlink(", ".rmdir(", "os.remove", "os.unlink", "rmtree"):
        assert call not in source
