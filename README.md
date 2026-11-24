# founder-vn

Founder skills for Vietnam: a set of agent skills plus one Python package (CLI `founder-vn` and MCP
server `founder-vn-mcp`) that help a **Facilitator** work through a business idea with an **Owner**
(a small-business owner or founder in Vietnam). The skills ask the questions and write the
Vietnamese report; the package does every calculation, so no number comes from a model.

Owner-facing output is Vietnamese and addresses the Owner as "anh/chị". Instructions inside the
skills are English.

## Who it is for

- **Facilitators** (advisors, trainers, incubator staff) who run a session with an Owner on a
  coding-agent host and need a repeatable, sourced result.
- **Owners** read the output; they do not install anything.

## Supported hosts

Kiro CLI, Claude Code, Codex, Gemini / Antigravity CLI (needs confirmation at install), Grok Build,
KiroCrew (added through its dashboard; it does not read a workspace `mcp.json`). One page per host
is in [docs/hosts/](docs/hosts/README.md).

## Install

Version 0.2.0 is the first PyPI release (0.1.0 was never published). It is pending the `v0.2.0`
tag: until the tag is pushed and `release.yml` publishes through trusted publishing, the PyPI
package and the `founder-vn install` command below are **not yet released**; only the development
route works today.

| Route | Command | State |
|---|---|---|
| Development (skills only) | `npx skills add NHAN-AI-VN/founder-vn` | works from the repository |
| Facilitator | `founder-vn install --host kiro\|claude\|codex\|grok\|kirocrew` | not yet released, pending the `v0.2.0` tag |
| MCP server | `uvx --from founder-vn founder-vn-mcp` | not yet released, pending the `v0.2.0` tag |

## Model

The buyer panel (`founder-vn panel run`, MCP `panel_run`) asks one OpenAI-compatible model,
configured in the host's environment by `FOUNDER_LLM_BASE_URL`, `FOUNDER_LLM_API_KEY` and
`FOUNDER_LLM_MODEL`; there is no default provider, and the values never go into a config file or
this repository. Suggested `FOUNDER_LLM_MODEL`: **`gemini-3.5-flash-lite`**, the reference model
chosen by the bake-off in [docs/bakeoff/README.md](docs/bakeoff/README.md) (what was tried, what was
chosen, why). Panel results are comparable across hosts and across Owners only when every run uses
this model; `founder/panel/results.json` records the model that answered. Per-host setup:
[docs/hosts/](docs/hosts/README.md).

## Status

| Skill | Ticket | Status | Golden artefact |
|---|---|---|---|
| `founder-board` | #14 | shipped (Wave A) | [`board.md`](examples/barbershop/founder/board.md) |
| `founder-competitors` | #13 | shipped (Wave A) | [`competitors.md`](examples/barbershop/founder/competitors.md) |
| `founder-consumer` | #16 | shipped (Wave A) | [`consumer.md`](examples/barbershop/founder/consumer.md) |
| `founder-pricing` | #17 | shipped (Wave A) | [`pricing.md`](examples/barbershop/founder/pricing.md) |
| `founder-cfo` | #12 | shipped (Wave A) | [`cfo.md`](examples/barbershop/founder/cfo.md) |
| `founder-plan` | #18 | shipped (Wave A): writes `summary.md`, compiles `business-plan.md` | [`business-plan.md`](examples/barbershop/founder/business-plan.md) |
| `founder-permits` | | not started (Wave B) | |
| `founder-ops` | | not started (Wave B) | |
| `founder-marketing` | | not started (Wave B) | |
| `founder-launch` | | not started (Wave B) | |

Golden artefacts are under `examples/barbershop/founder/`.

| Host | State |
|---|---|
| Kiro CLI | full pipeline: pending walkthrough (#19) |
| Claude Code | not yet verified |
| Codex | not yet verified |
| Gemini / Antigravity CLI | not yet verified |
| Grok Build | not yet verified |
| KiroCrew | not yet verified |

## Golden case

`examples/barbershop/` is the project's worked example: one real business idea, a four-chair men's
barbershop in Ho Chi Minh City planned as a household business, anonymised (working name, no personal
names, location at former-district level) and published with the case owner's consent (the case owner
is the project owner; design decision Q51). Every skill is developed and demonstrated on it, and
[`examples/barbershop/founder/idea.md`](examples/barbershop/founder/idea.md) is the idea file every
skill reads first. The Wave A example is complete: `idea.md`, `board.md`, `competitors.md`,
`consumer.md` with `customer.json`, `pitch.md` and the `panel/` results, `pricing.md`, `numbers.json`
with `cfo.md`, `summary.md` and the compiled
[`business-plan.md`](examples/barbershop/founder/business-plan.md) in
[`examples/barbershop/founder/`](examples/barbershop/founder/). The plan file is written by
`founder-vn plan` run from `examples/barbershop/`, never by hand. Pilot participants' folders stay outside version control (design §6).

## Contributing and law updates

See [CONTRIBUTING.md](CONTRIBUTING.md). Every legal claim needs an official link and a verification
date. If a law changed, open a "Law changed" issue.
Skill conventions: [docs/skill-conventions.md](docs/skill-conventions.md). Review checklist:
[docs/review-checklist.md](docs/review-checklist.md).

## Credit

founder-vn adapts [founder-skill](https://github.com/Jakeschincariol/founder-skill) by
Jake Schincariol (MIT). Upstream source: https://github.com/Jakeschincariol/founder-skill, adapted
from commit `fd9385b0cfe1b96bebce3898fbd506d73eff5a9d`. The upstream MIT notice is preserved in
[LICENSE](LICENSE).

## Tiếng Việt

founder-vn là bộ skill cho agent lập trình cùng một package Python (CLI `founder-vn` và MCP server
`founder-vn-mcp`), giúp **người hỗ trợ** (Facilitator) cùng **chủ doanh nghiệp** (Owner) rà soát một
ý tưởng kinh doanh ở Việt Nam. Skill đặt câu hỏi và viết báo cáo tiếng Việt; package tính mọi con
số, nên không có số nào do mô hình tự nghĩ ra.

- **Host hỗ trợ**: Kiro CLI, Claude Code, Codex, Gemini / Antigravity CLI (cần xác nhận khi cài),
  Grok Build, KiroCrew (thêm qua dashboard).
- **Cách cài**: `npx skills add NHAN-AI-VN/founder-vn` (phát triển); `founder-vn install --host ...`
  và `uvx --from founder-vn founder-vn-mcp` (chưa phát hành: 0.2.0 là bản PyPI đầu tiên, 0.1.0 chưa
  bao giờ được phát hành, và 0.2.0 đang chờ tag `v0.2.0`).
- **Trạng thái**: sáu skill đợt A (`founder-board` #14, `founder-competitors` #13, `founder-consumer`
  #16, `founder-pricing` #17, `founder-cfo` #12, `founder-plan` #18) đã có, kèm sản phẩm mẫu trong
  `examples/barbershop/founder/`; bốn skill đợt B (`permits`, `ops`, `marketing`, `launch`)
  chưa bắt đầu. Kiro CLI: chạy trọn quy trình đang chờ walkthrough (#19); mọi host khác chưa xác nhận.
- **Quy tắc cứng**: mọi khẳng định pháp lý cần link chính thức và ngày kiểm tra. Luật đổi thì mở
  issue "Law changed".
- **Mô hình cho panel người mua**: đặt `FOUNDER_LLM_MODEL=gemini-3.5-flash-lite` (mô hình tham
  chiếu chọn qua bake-off, [docs/bakeoff/README.md](docs/bakeoff/README.md)); panel chỉ so sánh
  được giữa các host khi mọi lần chạy dùng đúng mô hình này.
- **Nguồn gốc**: điều chỉnh từ founder-skill của Jake Schincariol (MIT), commit
  `fd9385b0cfe1b96bebce3898fbd506d73eff5a9d`.
- Báo cáo chỉ là bản mô phỏng, không phải tư vấn tài chính, thuế hay pháp lý.
