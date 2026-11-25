# Evidence: issue #94 the installer writes the MCP registration file

## Seam

Written by the operator in the ticket body (Q54, 2026-11-25); not inferred.

- `founder-vn install --host <host>` and its `--print-only` mode (CLI only, Q34; no MCP counterpart, so no parity slice): the files the Facilitator ends up with and the plan it prints. Module seam: `install.run` in `src/founder_vn/install.py`.
- `tests/test_install.py`, `tests/test_install_cli.py`, `tests/golden/install_*.json`: red first for the written registration file, the present-file case and the print-only case.
- `docs/hosts/*.md`: the host pages name the registration file (`tests/test_hosts.py`).

Out of scope: merging into an existing registration file; KiroCrew (stays print-only); the walkthrough record (#19).

## Lát

No model and no network. Red and green run with `uv run pytest tests/test_install.py -q`.

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| kiro absent | `test_kiro_writes_the_registration_file_when_absent` | `FileNotFoundError` on `.kiro/settings/mcp.json` (4 failed, 13 passed with the three below) | 17 passed |
| kiro present | `test_kiro_leaves_an_existing_registration_file_byte_unchanged` | `exists     .kiro/settings/mcp.json (not modified)` not in output | 17 passed |
| print-only | `test_print_only_writes_no_registration_file` | `create     .kiro/settings/mcp.json` not in output | 17 passed |
| symlink escape | `test_registration_file_through_an_escaping_symlink_is_refused` | `Failed: DID NOT RAISE InstallRefused` | 17 passed |
| kirocrew | `test_kirocrew_has_no_registration_file` | Passed on first run (characterisation of the print-only rule) | 17 passed |
| claude, codex, grok | `test_project_file_hosts_write_when_absent_and_print_when_present` (3 params) | `create     .mcp.json` / `.codex/config.toml` / `.grok/config.toml` not in output (3 failed, 17 passed) | 20 passed |
| CLI goldens | `test_print_only_golden[kiro,claude,codex,grok]` | 4 failed on the new plan line and project paths | 10 passed; goldens regenerated, explained in the commit message |
| host pages | `test_host_pages_name_the_project_registration_file_the_installer_writes` | Passed on first run (docs commit follows the code commit) | `tests/test_hosts.py` 11 passed |

## Quyết định của lane

- Codex and Grok project paths were checked against the official docs on 2026-11-25: Codex reads project `.codex/config.toml` for a trusted project ([config basics](https://learn.chatgpt.com/docs/config-file/config-basic)); Grok Build reads `[mcp_servers]` from the project `.grok/config.toml` ([settings](https://docs.x.ai/build/settings.md), [settings reference](https://docs.x.ai/build/settings/reference.md)). Both are written when absent; the host pages previously said `~/` and now say the project file.
- Output: a `create`/`exists ... (not modified)` line follows the skill lines; the snippet is still printed in every case. The path check runs before any skill is copied, so a refused registration path writes nothing.
- `README.md` names no snippet behaviour, so it is unchanged. `AGENTS.md` heading text Q1–Q53 became Q1–Q54 with the log.

## Cổng ba đoạn

Last code commit: `b2c5f1a`. Each segment ran once at that HEAD; this evidence commit is the only commit after it.

```
static: ruff check and format clean, skill-lint 0 findings
unit:   364 passed
build:  Successfully built dist/founder_vn-0.2.0-py3-none-any.whl
```

## Giới hạn

- Not witnessed: a real Codex or Grok Build session loading the written project file; Codex only loads it for a trusted project.
- An existing but different registration file is never merged or compared; the Facilitator edits it by hand (out of scope by the ticket).
- Written file contents are checked by parsing JSON and TOML, not by running a host.
