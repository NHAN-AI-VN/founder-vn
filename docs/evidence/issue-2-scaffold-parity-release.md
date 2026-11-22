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

Deviations: `mcp` resolves to 2.x (`mcp.server.mcpserver.MCPServer`, `mcp.Client`), so the dependency is `mcp>=2,<3`. `scripts/skill_lint.py` was reformatted with `ruff format` and E501 is ignored so the static gate passes once `pyproject.toml` exists.
