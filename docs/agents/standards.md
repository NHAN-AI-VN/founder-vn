# Coding standards

What the Standards review axis checks against. The design (`docs/founder-vn-design.md`) decides *what* is built; this file records *how* code in this repository is written, and points at the design section each rule rests on instead of restating it. A rule here changes by pull request; a review turn cites the rule, never a preference.

## Toolchain (design §2, §5)

- Python ≥ 3.11. One package, `founder_vn`, under `src/founder_vn/`; `pyproject.toml` is the only manifest, `uv.lock` the only lockfile, both committed. `uv sync --frozen` is how an environment is made; a change to dependencies regenerates `uv.lock` in the same commit.
- Runtime dependencies stay at the minimum the design names (`mcp`, `httpx`); a new one needs a purpose tied to a ticket and lands in its own commit with the lock.
- Lint and format are ruff, configured in `pyproject.toml`; `uv run ruff check .` and `uv run ruff format --check .` are gates (CI and the `static` segment).
- Tests are pytest under `tests/`; `uv run pytest -q` is a gate. The wheel builds with `uv build`.
- The gate commands are the same on CI (`.github/workflows/gate.yml`) and in the sandbox (`scripts/harness/gate-segment.sh static|unit|build`), in the same order.

## Shape of the code (design §2)

- Every computation lives in the package once and is reached two ways, the CLI `founder-vn` and the MCP server `founder-vn-mcp`, which wrap the same function; a feature that exists on one transport and not the other is incomplete. A **parity test** asserts byte-identical output through both.
- Every file the package writes goes through the path-locked layer: root `founder/` inside the project, `..` refused, absolute paths outside the root refused, symlinks resolving outside refused, only `.md` and `.json` written, nothing deleted. No other code path opens a file for writing, with the one exception below.
- The installer (`founder_vn.install`, `founder-vn install --host`, design §5) is the only code path that writes outside `founder/`, and its targets are fixed by the package, not chosen at run time: it writes `<project>/<host skills folder>/<skill>/…` for the folders listed in `install.SKILL_FOLDERS`, and the files it writes are exactly the files shipped under the package's `skills/<name>/` (every file of a folder that holds a `SKILL.md`, whatever its extension; the set is fixed by the package and reviewed in this repository, so the `.md`/`.json` limit of the layer, which guards against paths chosen at run time, does not apply). It keeps the layer's refusals: a target whose resolved path leaves the resolved project (`..`, a symlink escape) is refused with `InstallRefused` and exit code 2 before anything is written; nothing is deleted; `--print-only` writes nothing. Besides the skill files, it writes one fixed set of MCP registration files, `install.REGISTRATION_FILES`: `.kiro/settings/mcp.json`, `.mcp.json`, `.codex/config.toml` and `.grok/config.toml`. Their content is fixed by the package; each is written only when absent (an existing file, even a dangling symlink, is left untouched and the snippet is printed instead), never merged and never deleted; each target is checked to resolve inside the project, with `InstallRefused` and exit code 2 before anything is written, and the `.md`/`.json` limit does not apply to the `.toml` ones for the same reason (the set is fixed by the package, not chosen at run time). KiroCrew has no registration file and stays print-only. (Q54, #94.) It also writes one more fixed target for every host of `install.SKILL_FOLDERS`, KiroCrew included: `<project>/permits/sources.md`, the source ledger shipped in the wheel as `founder_vn/permits/sources.md` (else the repository's `permits/`). It follows the rule of the skill files, not of the registration files: `create` when absent, `update` when the project file differs from the packaged ledger (the packaged content wins and the plan says so), `unchanged` when identical; never deleted, no other file under `permits/` touched; `--print-only` writes nothing; a target resolving outside the project is refused with `InstallRefused` and exit code 2 before anything is written. (Q57, #142.) The installer is CLI-only: it runs before any MCP server is registered, so the parity rule above does not apply to it. (Decided by the operator on lane #7, finding S1 in `reviews/issue-7/standards.md`.)
- A missing numeric input is an error that names the field, never a default. Tax rates and thresholds are inputs with a source link, never constants.
- Public functions carry type hints; a module's public surface is what its tests import.
- The LLM client is one OpenAI-compatible client configured by `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL`; unconfigured is a clear error with setup instructions. No reliance on `response_format`, `seed` or `temperature`; JSON is extracted leniently and validated. Model name and prompt hash are recorded in the artifacts they produced.

## Tests (design §5)

- No network in tests: the fake OpenAI-compatible provider fixture answers every model call. A test that would reach a real endpoint is a defect.
- Golden files for every report the CLI prints (Vietnamese text, VND formatting); a change in output is a change in a golden file, reviewed as such.
- Determinism by seed where the design says so (persona cards); the test states the seed.
- A new gate (lint rule, check script, hook) is commissioned red-then-green: `docs/agents/evidence-gates.md`.

## Owner-facing output (design §3, §4)

- Reports, `examples/`, the simulated-buyer brief and every `.md` the package writes for the Owner are Vietnamese, address the Owner as "anh/chị", and format money as VND (`35.000 đ`); a `$` next to a digit is a finding (`scripts/skill_lint.py` catches it in `skills/` and `examples/`).
- Identifiers stay English: skill names `founder-*`, commands, file names under `founder/`, JSON keys.
- Every legal or numeric claim in a skill or example carries an official link and a verification date; the disclaimer and the simulated-panel caveat of the upstream skills are kept.
- The verdict `Profitable / Not yet / Incomplete` is computed from CFO numbers only; no code path lets the panel gate it.

## Skills (design §2, §5)

- `skills/<name>/SKILL.md` frontmatter: `name` equals the folder, `description` carries Vietnamese trigger phrases, `license`, `metadata.version` equals the package version, upstream `author`/`source`/`commit`. `scripts/skill_lint.py` checks the machine-checkable half.
- Instructions in English; the shared protocol section (version check, MCP first then CLI, never compute, never answer for a buyer, never write the verdict) is copied from the convention ticket T02 defines. What the skill says to the Facilitator when the protocol stops it (a major mismatch, neither MCP nor CLI) is Vietnamese; the step-1 stop has the shape the block quotes, `Dừng ở bước 1 của Protocol: …`, and `scripts/skill_lint.py` requires that line in every skill's block (Q60, #148).

## Git

- Branch `lane/issue-<n>` per ticket; `main` is never pushed to directly; history is never rewritten on a shared branch.
- Unattended lanes make the loop visible in git: one commit `seam: #<n> <slug>` carrying the evidence file's `## Seam`, then one commit `slice(<seam>): <behaviour>` per red-green slice carrying the test and the code (`.kiro/steering/lane-implement.md`). A commit that touches `src/` without touching a test is a Standards finding unless it is documentation, configuration or a generated file.
- Commit messages name the ticket (`#<n>`) and, for an address turn, the finding they close.
