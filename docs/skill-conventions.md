# Skill conventions

Every skill lives in `skills/<name>/SKILL.md`. `scripts/skill_lint.py` checks the machine-checkable
parts; `docs/review-checklist.md` holds the rest.

## Frontmatter

| Field | Rule |
|---|---|
| `name` | Equals the folder name; English, lowercase, hyphens (design §4). |
| `description` | English sentence plus Vietnamese trigger phrases the Facilitator types, with diacritics. |
| `license` | `MIT`. |
| `metadata.version` | Equals the package version in `src/founder_vn/__init__.py`; skills and package move together. |
| `metadata.author` | The upstream author of the skill this one adapts (Jake Schincariol), or the founder-vn author for a new skill. |
| `metadata.source` | The upstream URL, `https://github.com/Jakeschincariol/founder-skill`. |
| `metadata.commit` | The upstream commit the adaptation is based on (full hash, see README Credit). |

Example:

```yaml
---
name: example-skill
description: >-
  One English sentence on what the skill does. Dùng khi anh/chị nói "phân tích ý tưởng",
  "kiểm tra giá bán", "lập kế hoạch kinh doanh".
license: MIT
metadata:
  version: "0.1.0"
  author: Jake Schincariol
  source: https://github.com/Jakeschincariol/founder-skill
  commit: fd9385b0cfe1b96bebce3898fbd506d73eff5a9d
---
```

## Language

- Instructions inside `SKILL.md` are English.
- Everything the Owner reads (reports, questions, the simulated-buyer brief) is Vietnamese and
  addresses the Owner as "anh/chị".
- File names, JSON keys and skill names are English (design §4).
- No `$` anywhere in Owner-facing text: amounts are VND in Vietnamese format (`35.000 đ`).

## Shared protocol

Every skill includes the block below, copied exactly, as its first section after the title.
`tests/test_front_door.py` asserts that this block carries all five rules.

````markdown
## Protocol

1. Check the version: call the MCP tool `server_info`, or run `founder-vn --version` in the shell.
   Compare its major version with `metadata.version` of this skill. On a major mismatch, stop and
   tell the Facilitator to update the package or the skill.
2. Prefer MCP tools. If the MCP server is not available, run the `founder-vn` CLI through the
   shell. If neither is available, stop and print the install instructions from the README.
3. Never compute a number yourself. Every figure comes from a `founder-vn` tool or command.
4. Never answer for a buyer. Simulated buyers answer only through the panel tools.
5. Never write the verdict. The verdict comes from the tool output and is shown as given.
````
