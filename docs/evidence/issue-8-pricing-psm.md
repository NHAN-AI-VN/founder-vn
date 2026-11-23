# Evidence: issue #8 pricing slice, Van Westendorp on VND

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred. The design does not define the input file, so the lane fixes one: a JSON file under `founder/` with `answers` (a list of objects with the keys `too_cheap`, `bargain`, `getting_expensive`, `too_expensive`) and an optional `competitor_prices` list; every price may be a number or Vietnamese text.

- `founder_vn.pricing` (module): the one function behind both transports. Parses prices through `founder_vn.vnd.parse_vn_number`, drops answers that are unparseable or not above zero and counts them, warns below 8 valid answers, computes the Van Westendorp points, renders the Vietnamese report or JSON (criteria 1, 2, 3).
- `founder-vn pricing` (CLI command): one end of the parity pair, with `--json` and `--out`; golden-file tests run through it (criteria 3, 4).
- `pricing_psm` (MCP tool of `founder-vn-mcp`): the other end; the parity test asserts identical stdout and files (criterion 4).
- `founder_vn.files.write_text` (path-locked layer): the only way `pricing.md` is written, so a path escape stays refused (criterion 3).

## Lát

| Slice | Test | Assertion while red | Green rerun |
|---|---|---|---|

## Giới hạn

To be completed.
