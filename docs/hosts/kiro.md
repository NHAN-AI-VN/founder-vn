# Kiro: registering the founder-vn MCP server

`founder-vn install --host kiro` writes this to the workspace `.kiro/settings/mcp.json` when that file does not exist. When it exists, the installer prints the snippet and leaves the file as it is (never merged); add the entry by hand there, or at user level (`~/.kiro/settings/mcp.json`):

```json
{
  "mcpServers": {
    "founder-vn": {
      "command": "uvx",
      "args": ["--from", "founder-vn", "founder-vn-mcp"]
    }
  }
}
```

`founder-vn-mcp` is the console script of the `founder-vn` package (`pyproject.toml`,
`[project.scripts]`). The server answers the `server_info` tool with the package version, the same
text as `founder-vn version`.

Model calls read `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and `FOUNDER_LLM_MODEL` from the
environment of the host. Set them in the host's own environment; do not write their values into
`mcp.json` or into this repository.

Reference model for the buyer panel: set `FOUNDER_LLM_MODEL` to `gemini-3.5-flash-lite` (the model
chosen by the bake-off, [docs/bakeoff/README.md](../bakeoff/README.md)). Panel results are
comparable across hosts and across Owners only when every run uses this model; `results.json`
records the model that answered.

`uvx --from founder-vn founder-vn-mcp` resolves the package from PyPI, and `v0.2.0` (the first release on PyPI, published 2026-11-24) is available there (see `.github/workflows/release.yml`).

## Installing the skills

```bash
founder-vn install --host kiro
```

Copies the skills into `.kiro/skills/` of the current project (idempotent; `--print-only` shows the plan and the snippet without writing) and writes the `mcp.json` registration above when `.kiro/settings/mcp.json` is absent (otherwise it prints the snippet and leaves the file).

## Clean-install walkthrough

For ticket #19. The operator ran this on a real Kiro CLI on 2026-11-25 against PyPI release 0.2.0
and recorded it in [docs/evidence/issue-19-wave-a-walkthrough.md](../evidence/issue-19-wave-a-walkthrough.md)
(commands, times, friction, the issues filed). The steps below are the script to repeat it.

1. Start from an empty folder and open a shell in it:

   ```bash
   mkdir founder-walkthrough && cd founder-walkthrough
   ```

2. Install the package and the skills. Pick one variant.

   From a local wheel (development only: built with `uv build` in the repository, copied to `./dist/`):

   ```bash
   uvx --from ./dist/founder_vn-0.2.0-py3-none-any.whl founder-vn install --host kiro
   ```

   From PyPI (the released package):

   ```bash
   uvx --from founder-vn founder-vn install --host kiro
   ```

3. Check the MCP registration: on a clean project the installer of step 2 has already written
   `.kiro/settings/mcp.json` with the snippet above (Q54, #94); if the file existed, it was left unchanged and the
   snippet was printed, so add the entry by hand. For a local wheel, edit `args` and put the wheel path in `args` in place of the package name: `["--from", "./dist/founder_vn-0.2.0-py3-none-any.whl", "founder-vn-mcp"]`.
4. Set the three model variables in the shell that starts Kiro CLI: `FOUNDER_LLM_BASE_URL`,
   `FOUNDER_LLM_API_KEY`, `FOUNDER_LLM_MODEL`. Check each is present with `test -n "$NAME"`; never
   print or write the values.
5. Start Kiro CLI in the folder and write the idea into `founder/idea.md` (the Owner's words).
6. Run the six Wave A skills in this order, one per step, and wait for each to finish:
   1. `founder-board`
   2. `founder-competitors` (with no filled survey form in `founder/`, the skill prints the form and stops; fill it, then run again)
   3. `founder-consumer`
   4. `founder-cfo`
   5. `founder-pricing` (reads `cfo.md` and `numbers.json` for the break-even check, so it runs after `founder-cfo`)
   6. `founder-plan`
7. Confirm `founder/business-plan.md` exists and `founder-vn plan --check` exits 0.
8. Deliberate major-mismatch check. Open `.kiro/skills/founder-board/SKILL.md` and set
   `metadata.version` to `1.0.0` (`version: "1.0.0"`). Run `founder-board` again. Expect the stop message of Protocol step 1: "On a major mismatch, stop and tell the Facilitator to update the package or the skill". Then restore the file (set the version back to `0.2.0`, or run the install command of step 2 again) and confirm the skill runs again.

Record each step in this table (copy it into the evidence file):

| step | command | started | duration | friction | issue filed |
|---|---|---|---|---|---|
|  |  |  |  |  |  |
