# Running parallel lanes

Read this before dispatching more than one lane at a time. The dispatcher enforces the work-in-progress limit; this document is where that limit and the single-owner list live, and both change only by measurement.

## Work-in-progress limit

`HARNESS_WIP` in `.github/workflows/frontier-dispatch.yml`, `gate.yml` and `after-gate.yml` is `1`: one lane in flight at a time. Raise it only after the collision measurement below exists for at least five merged lanes.

## One owner per merge

A file on this list may be edited by one lane per merge. The dispatcher grants it through `singleOwnerFiles` in the allocation comment (`all` while `HARNESS_WIP` is 1), and `.kiro/hooks/guard.sh` refuses a write to an entry the lane was not granted. Every bullet in this section that opens with a backticked path is read as an entry, up to the next `## ` heading, so an explanatory bullet must open with prose.

- `pyproject.toml` — one manifest: dependencies, version, ruff and pytest configuration.
- `uv.lock` — regenerated from the manifest; two lanes regenerating it collide.
- `README.md` — hand prose; a semantic merge.
- `src/founder_vn/__init__.py` — the package's public surface and version string.

These four are the starting list, chosen because the tickets T01–T09 each touch at least one of them; none is yet backed by a measured collision. An entry leaves the list when five merged lanes show no pair changing it; an entry enters when a measured collision puts it here.

## Free-parallel

Files under `src/founder_vn/<module>.py` and `tests/<module>/` are free-parallel only when the two lanes are in different modules. `skills/<name>/SKILL.md` is free-parallel across skills. Two lanes inside the same module or skill must be serialized.

## Measuring collisions

After five merged lanes, run `git diff --name-only <merge>^1 <merge>` for each merge, form all unordered pairs, and count per file in how many pairs both sides changed it. A file changed in at least one pair in five gets a line in this document: one-owner when the conflict is semantic, free-parallel with a named gate when it is mechanical and a gate already reddens the wrong resolution. A pattern on the one-owner list serializes by the pattern string, not by file, so re-check two hypothetical lanes' file sets against the list before declaring that no bottleneck remains.
