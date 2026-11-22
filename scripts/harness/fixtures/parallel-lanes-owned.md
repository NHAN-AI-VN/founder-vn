# Fixture: a parallel-lanes document with a populated one-owner list

Used only by scripts/harness/witness.sh through HARNESS_OWNED_PATHS_FILE. The real list lives in
docs/agents/parallel-lanes.md.

## One owner per merge

- `README.md` — hand prose; a semantic merge.
- `pyproject.toml` — one manifest, one owner per merge.
- `tests/golden/*.txt` — a pattern entry, matched by glob.
- This bullet opens with prose and must not be read as an entry.

## Free-parallel

- `src/founder_vn/*.py` is not on the list above and stays free-parallel.
