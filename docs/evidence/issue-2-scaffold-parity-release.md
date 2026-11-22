# Evidence: issue #2 scaffold, CLI/MCP parity, release path

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.files` (module): the path-locked layer under `<project>/founder/`. It is the one place the package writes, so refusals are tested here (criterion 2).
- `founder-vn version` (CLI command): one end of the parity pair (criterion 1).
- `server_info` (MCP tool of `founder-vn-mcp`): the other end; the parity test compares both texts byte for byte (criterion 1).
- Fake OpenAI-compatible provider (test fixture, 127.0.0.1 `/v1/chat/completions`): the no-network seam every later model call goes through (criterion 3).
- Temporary project root, CLI golden runner and in-process MCP client (test fixtures): the remaining criterion 3 seams.

## Lát

(filled per slice)
