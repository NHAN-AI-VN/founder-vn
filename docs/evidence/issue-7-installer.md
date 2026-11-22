# Evidence: issue #7 installer (`founder-vn install --host`) and host pages

## Seam

Derived from the acceptance criteria (the ticket has no `## Seam` section); every line is inferred.

- `founder_vn.install` (module, `run(project, host, print_only, skills_dir)`): plans and performs the copy of packaged skills into the host's project-level skills folder and renders the host's MCP registration snippet. It takes an injectable source directory, so tests use a synthetic skills fixture (the product `skills/` folder does not exist yet). Criteria 1 and 2.
- `founder-vn install --host <kiro|claude|codex|grok|kirocrew> [--print-only]` (CLI command): the public entry a Facilitator types. Exit code, stdout and written files are asserted through the golden runner. Criteria 1, 2 and 4.
- `docs/hosts/*.md` (pages): the Gemini page and the filled stubs are checked by `tests/test_hosts.py`. Criteria 3 and 5.
- Not a seam: an MCP tool. See "Parity decision" below.

## Parity decision

`install` has no MCP tool. `docs/agents/standards.md` requires parity for a computation reached through both transports. Installing writes outside `founder/` into the host's own skill folder, and it runs before the MCP server is registered, so the server cannot be the way to install it. The design (§5) names `founder-vn install` only as a CLI command. The installer therefore stays CLI-only on purpose.

## Lát

(filled per slice)

## Cổng ba đoạn

(filled after the gate)

## Giới hạn

(filled at the end)
