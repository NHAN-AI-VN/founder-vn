# Evidence: issue #143 panel init refuses a re-deal over answers of another deal (Q58)

## Seam

Inferred from the acceptance criteria of the ticket body (the ticket's own Seam section was written by AI at triage; refined here).

- `panel.init` behind `founder-vn panel init` (`tests/test_panel_cli.py`): the refusal (exit 2, stderr text, files byte-identical) and the pass-through of an identical deal.
- MCP `panel_init` (`tests/test_panel_parity.py`): the same text as a tool error; one `panel.init`, so one text.
- `skills/founder-consumer/SKILL.md` Step 3 (`tests/test_consumer_skill.py`): the refusal sentence.
- `docs/founder-vn-design.md`: Q58 and the §2 clause.

## Lát

Red run before the code (`uv run pytest tests/test_panel_cli.py tests/test_panel_parity.py tests/test_consumer_skill.py -q -k "refus or identical or reproduction or empty_answers or step_3"`): 9 failed, 7 passed (the 7 are the pass-through cases). Green after: 63 passed in the three files.

| Test | Red assertion | Green |
|---|---|---|
| `test_init_refuses_a_changed_pitch_over_answers` | exit code 0, not 2 | `uv run pytest tests/test_panel_cli.py -q` |
| `test_init_refuses_other_seed_or_other_n_over_answers` | exit code 0, not 2 | same |
| `test_init_refuses_when_answers_exist_and_the_panel_on_disk_is_unreadable` (4 params) | exit code 0 or crash, not 2 | same |
| `test_issue_143_reproduction_stops_at_the_third_command` | exit code 0, not 2 | same |
| `test_panel_init_refusal_is_the_same_text_through_cli_and_mcp` | `is_error` false | `uv run pytest tests/test_panel_parity.py -q` |
| `test_step_3_tells_the_owner_to_set_an_earlier_panel_aside_when_init_refuses` | sentence absent from SKILL.md | `uv run pytest tests/test_consumer_skill.py -q` |

Pass-through tests (identical deal, no or empty `answers/`) were green before and stay green; they pin the criteria that must not change.

Deviation: the MCP server did not turn `PanelError` into a tool error (the library reported "Error executing tool"), so `panel_init` in `src/founder_vn/server.py` now raises `ToolError("lỗi: <text>")`. The tool error text is the library prefix `Error executing tool panel_init: ` plus the CLI stderr text; the test pins that. The red-then-green slices were committed as one code commit, not one per slice.

`tests/test_install.py` pinned "(Q1–Q57)" in the design header; it now pins Q1–Q58 and still requires Q57. `AGENTS.md` range moved to Q1–Q58.

## Cổng ba đoạn

See the `verify` output of the last HEAD (`.harness/gate-segments.txt`).

## Giới hạn

- The guard compares prompt hashes of the panel on disk and the new deal; it does not inspect answer contents. Any file in `answers/` counts.
- `check`, `tally`, `run` and `_answer_file_problem` are unchanged by design (option 2 not chosen).
- The MCP text is verified with the real stdio server; no real model was run.
