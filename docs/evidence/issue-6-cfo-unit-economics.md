# Evidence: issue #6 CFO unit economics, revenue tax, VND and number utilities

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.vnd` (module): `format_vnd` and `parse_vn_number`, the shared locale utilities. Pure functions with table-driven golden tests (criterion 3).
- `founder_vn.cfo` (module): the one function behind both transports, covering analyse, report and render. It takes `numbers.json`, applies revenue tax, exposes the three verdict inputs in JSON and renders the Vietnamese report (criteria 1, 2, 4, 5).
- `founder-vn cfo` (CLI command): one end of the parity pair, with `--price`, `--volume` and JSON mode; golden-file tests run through it (criteria 4, 5, 6).
- `cfo_analyse` (MCP tool of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files (criterion 6).
- `founder_vn.files.write_text` (path-locked layer): the only way `cfo.md` is written, so a path escape stays refused (criterion 5).

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|

## Cổng ba đoạn

## Giải quyết review nội bộ

## Giới hạn
