# Evidence: issue #7 installer (`founder-vn install --host`) and host pages

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.install` (module, `run(project, host, print_only, skills_dir)`): plans and performs the copy of packaged skills into the host's project-level skills folder and renders the host's MCP registration snippet. It takes an injectable source directory, so tests use a synthetic skills fixture (the product `skills/` folder does not exist yet). Criteria 1 and 2.
- `founder-vn install --host <kiro|claude|codex|grok|kirocrew> [--print-only]` (CLI command): the public entry a Facilitator types. Exit code, stdout and written files are asserted through the golden runner. Criteria 1, 2 and 4.
- `docs/hosts/*.md` (pages): the Gemini page and the filled stubs are checked by `tests/test_hosts.py`. Criteria 3 and 5.
- Writes: the installer writes into the host's skills folder (`.kiro/skills/`, `.grok/skills/`, `.claude/skills/`, `.agents/skills/`), not under `founder/`, so `founder_vn.files` does not apply. It follows the same rules by its own check: a target that resolves outside the project (`..`, symlink escape) is refused with `InstallRefused` (exit 2), and it never deletes; unrelated files in the folder are left alone.
- Not a seam: an MCP tool. See "Parity decision" below.

## Parity decision

`install` has no MCP tool. `docs/agents/standards.md` requires parity for a computation reached through both transports. Installing writes outside `founder/` into the host's own skill folder, and it runs before the MCP server is registered, so the server cannot be the way to install it. The design (§5) names `founder-vn install` only as a CLI command. The installer therefore stays CLI-only on purpose.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| copy | `tests/test_install.py::test_install_copies_skills_into_the_host_folder` (5 hosts), `test_install_with_no_skills_says_so_and_does_not_crash` | `ImportError: cannot import name 'install' from 'founder_vn'` | `uv run pytest tests/test_install.py -q` |
| idempotent, print-only, escape | `test_install_is_idempotent_and_reports_unchanged`, `test_install_updates_a_changed_file_and_keeps_unrelated_files`, `test_print_only_plans_without_writing`, `test_install_refuses_a_symlink_that_escapes_the_project` | `AssertionError: assert 'unchanged  .kiro/skills/founder-demo/SKILL.md' in ...` and `AttributeError: module 'founder_vn.install' has no attribute 'InstallRefused'` | `uv run pytest tests/test_install.py -q` |
| CLI, snippets, goldens | `tests/test_install_cli.py` (5 golden tests `install_<host>.json`, timeout note, KiroCrew dashboard and trust note, env names without values, no `gemini` value, refusal exit 2) | `FileNotFoundError: ... tests/golden/install_kiro.json` (5 goldens red); the other CLI tests were written together with the code and have no witnessed red | `uv run pytest tests/test_install_cli.py -q` |
| wheel | `tests/test_install.py::test_pyproject_ships_skills_in_the_wheel` | `KeyError: 'force-include'` | `uv run pytest tests/test_install.py -q` |
| host pages | `tests/test_hosts.py` (5 new tests) | `AssertionError: assert 'pending confirmation' in '# Gemini / Antigravity CLI ... Status: stub ...'` and 3 more reds | `uv run pytest tests/test_hosts.py -q` |

New golden files `tests/golden/install_{kiro,claude,codex,grok,kirocrew}.json` are the first output of the new command (generated from the code, then read through once; no absolute path, no timestamp, source skills come from the synthetic `tests/fixtures/skills_src`).

## Cổng ba đoạn

Run on HEAD `c124219` (later commits touch evidence only).

```
static 0 c1242198b6cd1a675b114e0af4833b2a0a631ae2
unit 0 c1242198b6cd1a675b114e0af4833b2a0a631ae2
build 0 c1242198b6cd1a675b114e0af4833b2a0a631ae2
gate-segment verify: GREEN on c1242198b6cd1a675b114e0af4833b2a0a631ae2
```

Logs: `All checks passed!`, `132 passed`, `Successfully built dist/founder_vn-0.1.0-py3-none-any.whl`. The built wheel lists `founder_vn/skills/.gitkeep`, so `skills/` is packaged via hatch `force-include`.

## Giới hạn

- `skills/` holds only `.gitkeep`: no real skill was copied; copy behaviour is proven on a synthetic fixture. The wheel packaging is proven for the folder, not for real skill content.
- The MCP snippets for Claude Code, Codex, Grok Build and KiroCrew come from the ticket and design; none was run on its host. Grok's `config.toml` table name and the Gemini `$NAME` expansion in `env` are unconfirmed. The Codex `tool_timeout_sec = 300` value is an example, not a measured need.
- The golden outputs are English text for the Facilitator (design §4: docs in English); nothing Owner-facing is produced.
- `install` is not an MCP tool (reasoning above); no parity test exists for it.
- Some CLI tests (timeout note, trust note, env names, `gemini` refused, exit 2) had no witnessed red.
- Existing files are overwritten when their content differs (`update`); local edits to an installed skill are lost on re-run. Nothing is deleted.
