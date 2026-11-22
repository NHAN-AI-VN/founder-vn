# Evidence: issue #2 scaffold, CLI/MCP parity, release path

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.files` (module): the path-locked layer under `<project>/founder/`. It is the one place the package writes, so refusals are tested here (criterion 2).
- `founder-vn version` (CLI command): one end of the parity pair (criterion 1).
- `server_info` (MCP tool of `founder-vn-mcp`): the other end; the parity test compares both texts byte for byte (criterion 1).
- Fake OpenAI-compatible provider (test fixture, 127.0.0.1 `/v1/chat/completions`): the no-network seam every later model call goes through (criterion 3).
- Temporary project root, CLI golden runner and in-process MCP client (test fixtures): the remaining criterion 3 seams.

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|
| scaffold | `tests/test_package.py::test_package_has_single_source_version` | No witnessed red: manifest slice, the test only proves the environment runs | `uv run pytest tests/test_package.py -q` |
| files | `tests/test_files.py` (16 tests, one per refusal) | `ImportError: cannot import name 'files' from 'founder_vn'` | `uv run pytest tests/test_files.py -q` |
| parity | `tests/test_parity.py::test_cli_version_equals_mcp_server_info` | `ImportError: cannot import name 'info' from 'founder_vn'` | `uv run pytest tests/test_parity.py -q` |
| fixtures | `tests/test_fixtures.py` (7 tests) | No separate red: fixtures and their tests are one test-only commit; `test_cli_golden_runner_detects_a_changed_output` and `test_network_guard_refuses_a_non_loopback_connection` assert the failure paths | `uv run pytest tests/test_fixtures.py -q` |
| release | `tests/test_release.py` (3 tests: tag trigger, OIDC without token, tag equals version check) | `FileNotFoundError: [Errno 2] No such file or directory: '.github/workflows/release.yml'` | `uv run pytest tests/test_release.py -q` |
| hosts | `tests/test_hosts.py` (2 tests: snippet is JSON naming the console script, no secret values) | `FileNotFoundError: [Errno 2] No such file or directory: 'docs/hosts/kiro.md'` | `uv run pytest tests/test_hosts.py -q` |

Deviations: `mcp` resolves to 2.x (`mcp.server.mcpserver.MCPServer`, `mcp.Client`), so the dependency is `mcp>=2,<3`. `scripts/skill_lint.py` was reformatted with `ruff format` and E501 is ignored so the static gate passes once `pyproject.toml` exists.

## Smoke check from the built wheel

Command: `uv build`, then the wheel `dist/founder_vn-0.1.0-py3-none-any.whl` installed into a clean venv (`uv venv`, `uv pip install`), then an in-process `mcp.Client` over stdio started `founder-vn-mcp` and called `server_info`.
Result: `founder-vn 0.1.0`; `founder-vn version` from the same venv prints `founder-vn 0.1.0`.

## Kiro registration

`docs/hosts/kiro.md` holds the `mcp.json` entry (`command` `uvx`, `args` `["founder-vn-mcp"]`), checked by `tests/test_hosts.py` against `[project.scripts]`. The pull request body repeats it.

## Cổng ba đoạn

Run on the last code commit (`1bca122`); the commits after it change only this file.

```
gate-segment verify: latest line per segment (.harness/gate-segments.txt)
  static 0 1bca1223cebd05cffd68bcfbdd91b381873b7527 2026-11-22T08:34:35Z
  unit 0 1bca1223cebd05cffd68bcfbdd91b381873b7527 2026-11-22T08:34:37Z
  build 0 1bca1223cebd05cffd68bcfbdd91b381873b7527 2026-11-22T08:34:38Z
gate-segment verify: GREEN on 1bca1223cebd05cffd68bcfbdd91b381873b7527
```

Logs: `All checks passed!`, `32 passed in 1.31s`, `Successfully built dist/founder_vn-0.1.0-py3-none-any.whl`.

## Giới hạn

This lane does not prove:

- PyPI publication. `release.yml` was not run: the lane cannot push tags or reach PyPI. Only its text is tested (`tests/test_release.py`).
- `uvx founder-vn-mcp` resolving from PyPI. The smoke check used the local wheel.
- That the Kiro host loads the `mcp.json` entry; only the JSON and the script name are checked.

Owner actions after merge, in order: configure the PyPI trusted publisher for repository `NHAN-AI-VN/founder-vn`, workflow `release.yml`, environment `pypi`; create the GitHub environment `pypi`; push tag `v0.1.0`. Acceptance criteria 4 and 5 are complete only after these.

## Giải quyết review nội bộ

No self-review turn was run (lane rule: review is two independent turns dispatched after the pull request opens). `reviews/issue-2/` is the harness's.
