#!/usr/bin/env python3
"""skill-lint: the machine half of the review checklist for the distributed skills.

Checks every ``skills/*/SKILL.md`` (the founder-vn skills, not the dev skills under
``.agents/skills``) and every ``examples/**/*.md``:

* frontmatter present (``---`` on the first line, closed by ``---``);
* ``name`` equals the folder name;
* ``description`` holds at least one word with a Vietnamese diacritic (the trigger phrases
  the Facilitator types, docs/founder-vn-design.md §4);
* ``license`` present;
* ``metadata.version`` present and, when ``pyproject.toml`` exists, equal to ``[project].version``
  (skills and package move in lockstep, design §2 / Q45);
* no ``$`` next to a digit, in SKILL.md prose (fenced code is skipped: a shell ``$1`` is not a
  price) and anywhere in ``examples/**/*.md`` (the Owner-facing artifacts, design §3).

Standard library only, Python >= 3.11 (``tomllib``). Exit 0 when every check holds, 1 otherwise;
every finding names the file and the line. With no skill folder the run reports ``0 skill
checked`` and still exits 0, so the gate holds on a repository that has not grown skills yet.

    python3 scripts/skill_lint.py [--root DIR]

One rule per ``rule_*`` function, one line each, so scripts/harness/witness.sh can mutate a rule
and require its fixture case to go red.
"""

from __future__ import annotations

import argparse
import re
import sys
import tomllib
from pathlib import Path

VIETNAMESE = re.compile(
    "[ăâđêôơưĂÂĐÊÔƠƯàáảãạằắẳẵặầấẩẫậèéẻẽẹềếểễệìíỉĩịòóỏõọồốổỗộờớởỡợùúủũụừứửữựỳýỷỹỵ"
    "ÀÁẢÃẠẰẮẲẴẶẦẤẨẪẬÈÉẺẼẸỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌỒỐỔỖỘỜỚỞỠỢÙÚỦŨỤỪỨỬỮỰỲÝỶỸỴ]"
)
DOLLAR = re.compile(r"\$\s?\d|\d\s?\$")
FENCE = re.compile(r"^\s*(```|~~~)")


# ---- rules: one line each -------------------------------------------------------------------
def rule_name_matches(fm: dict, folder: str) -> bool:
    return fm.get("name") == folder


def rule_has_vietnamese(text: str | None) -> bool:
    return VIETNAMESE.search(text or "") is not None


def rule_has_license(fm: dict) -> bool:
    return bool(fm.get("license"))


def rule_has_version(fm: dict) -> bool:
    return bool(fm.get("metadata", {}).get("version"))


def rule_version_matches(skill: str | None, project: str | None) -> bool:
    return project is None or skill == project


def rule_no_dollar(line: str) -> bool:
    return DOLLAR.search(line) is None


# ---- frontmatter ----------------------------------------------------------------------------
def parse_frontmatter(lines: list[str]) -> tuple[dict | None, int]:
    """Return (mapping, line number of the closing ---) or (None, 0) when there is none.

    A small YAML subset: ``key: value`` at the top level, one nested block (``metadata:``) with
    two-space indented ``key: value`` lines, and folded/literal scalars (``>``/``|``) for
    ``description``. Quotes around scalars are stripped. Enough for the SKILL.md frontmatter the
    Agent Skills standard uses; anything else is a finding, not a crash.
    """
    if not lines or lines[0].strip() != "---":
        return None, 0
    fm: dict = {}
    current_block: dict | None = None
    folded_key: str | None = None
    folded_parent: dict | None = None
    for i, raw in enumerate(lines[1:], start=2):
        if raw.strip() == "---":
            return fm, i
        if folded_key is not None and (raw.startswith("  ") or raw.strip() == ""):
            target = folded_parent if folded_parent is not None else fm
            target[folded_key] = (target[folded_key] + " " + raw.strip()).strip()
            continue
        folded_key = None
        folded_parent = None
        if raw.startswith("  ") and current_block is not None:
            key, _, value = raw.strip().partition(":")
            current_block[key.strip()] = _scalar(value)
            if value.strip() in (">", "|", ">-", "|-"):
                current_block[key.strip()] = ""
                folded_key, folded_parent = key.strip(), current_block
            continue
        current_block = None
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        key = key.strip()
        if value.strip() == "":
            fm[key] = {}
            current_block = fm[key]
        elif value.strip() in (">", "|", ">-", "|-"):
            fm[key] = ""
            folded_key = key
        else:
            fm[key] = _scalar(value)
    return None, 0


def _scalar(value: str) -> str:
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        v = v[1:-1]
    return v


# ---- checks ---------------------------------------------------------------------------------
def project_version(root: Path) -> str | None:
    pyproject = root / "pyproject.toml"
    if not pyproject.is_file():
        return None
    with pyproject.open("rb") as fh:
        data = tomllib.load(fh)
    project = data.get("project", {})
    if "version" in project:
        return str(project["version"])
    path = data.get("tool", {}).get("hatch", {}).get("version", {}).get("path")
    if "version" in project.get("dynamic", []) and path:
        match = re.search(
            r"""^__version__\s*=\s*['"]([^'"]+)['"]""",
            (root / path).read_text(encoding="utf-8"),
            re.MULTILINE,
        )
        if match:
            return match.group(1)
    return None


def check_skill(path: Path, folder: str, version: str | None, findings: list[str]) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    fm, end = parse_frontmatter(lines)
    rel = path.as_posix()
    if fm is None:
        findings.append(f"{rel}:1: no frontmatter (--- ... ---)")
        body_start = 0
    else:
        body_start = end
        if not rule_name_matches(fm, folder):
            findings.append(
                f"{rel}:1: name is {fm.get('name')!r}, expected {folder!r} (the folder name)"
            )
        if not rule_has_vietnamese(
            fm.get("description") if isinstance(fm.get("description"), str) else None
        ):
            findings.append(
                f"{rel}:1: description has no Vietnamese trigger phrase (no diacritic found)"
            )
        if not rule_has_license(fm):
            findings.append(f"{rel}:1: license missing")
        if not rule_has_version(fm):
            findings.append(f"{rel}:1: metadata.version missing")
        elif not rule_version_matches(str(fm["metadata"]["version"]), version):
            findings.append(
                f"{rel}:1: metadata.version {fm['metadata']['version']!r} differs from pyproject [project].version {version!r}"
            )
    in_fence = False
    for n, line in enumerate(lines[body_start:], start=body_start + 1):
        if FENCE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not rule_no_dollar(line):
            findings.append(
                f"{rel}:{n}: `$` next to a digit; Owner-facing money is VND (`35.000 đ`)"
            )


def check_example(path: Path, findings: list[str]) -> None:
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not rule_no_dollar(line):
            findings.append(
                f"{path.as_posix()}:{n}: `$` next to a digit; examples are Owner-facing and use VND"
            )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="repository root (default: current directory)")
    args = ap.parse_args(argv)
    root = Path(args.root)
    version = project_version(root)
    findings: list[str] = []
    skills = (
        sorted(p for p in (root / "skills").glob("*/SKILL.md"))
        if (root / "skills").is_dir()
        else []
    )
    for skill in skills:
        check_skill(skill, skill.parent.name, version, findings)
    examples = sorted((root / "examples").rglob("*.md")) if (root / "examples").is_dir() else []
    for example in examples:
        check_example(example, findings)
    for f in findings:
        print(f, file=sys.stderr)
    noun = "skill" if len(skills) == 1 else "skills"
    if len(skills) == 0:
        noun = "skill"
    print(
        f"skill-lint: {len(skills)} {noun} checked, {len(examples)} example file(s), {len(findings)} finding(s)"
        + (f" (package version {version})" if version else "")
    )
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
