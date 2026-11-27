"""MCP stdio server `founder-vn-mcp`: wraps the same functions as the CLI."""

from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

from founder_vn import __version__, board, cfo, info, panel, plan, pricing

mcp = MCPServer("founder-vn", version=__version__)


@mcp.tool()
def server_info() -> str:
    """Return the founder-vn package version (same text as `founder-vn version`)."""
    return info.version_text()


@mcp.tool()
def cfo_analyse(
    numbers: str,
    price: str | None = None,
    volume: float = 1.0,
    as_json: bool = False,
    out: str | None = None,
) -> str:
    """Unit economics report from numbers.json (same text as `founder-vn cfo`).

    `numbers` is read under founder/; `price` is a what-if price (e.g. "40k"), `volume` a
    multiplier; `as_json` returns JSON; `out` writes the report under founder/ (e.g. "cfo.md").
    """
    return cfo.run(Path.cwd(), numbers, price, volume, as_json, out)


@mcp.tool()
def pricing_psm(source: str, as_json: bool = False, out: str | None = None) -> str:
    """Van Westendorp price sensitivity (same text as `founder-vn pricing`).

    `source` is a JSON file under founder/ with the panel's four price answers and optional
    competitor prices; `as_json` returns JSON; `out` writes the report under founder/
    (e.g. "pricing.md").
    """
    return pricing.run(Path.cwd(), source, as_json, out)


@mcp.tool()
def panel_init(
    customer: str = "customer.json",
    pitch: str = "pitch.md",
    n: int = panel.DEFAULT_N,
    seed: int | None = None,
) -> str:
    """Deal persona cards (same text as `founder-vn panel init`).

    `customer` and `pitch` are read under founder/; the cards are written to founder/panel/.
    The same `seed` gives the same cards.
    """
    try:
        return panel.init(Path.cwd(), customer, pitch, n, seed)
    except panel.PanelError as e:
        raise ToolError(f"lỗi: {e}") from None


@mcp.tool()
def panel_tally() -> str:
    """Count the buyers' answers into results.md and results.json (same text as `founder-vn panel tally`)."""
    return panel.run_tally(Path.cwd())


@mcp.tool()
def panel_run() -> str:
    """Ask each buyer through the configured model (same text as `founder-vn panel run`).

    Returns at once with a `job_id`; answers land in founder/panel/answers/ as they arrive. Poll
    `job_status`. Only buyers without a valid answer are asked, so calling it again resumes.
    """
    return panel.run(Path.cwd(), detached=False)


@mcp.tool()
def board_run() -> str:
    """Ask the three board lenses through the configured model (same text as `founder-vn board run`).

    Reads the standalone brief founder/board/brief.md and returns at once with a `job_id`; the
    memos land in founder/board/ as they arrive. Poll `job_status`. Only lenses without a valid
    memo are asked, so calling it again resumes.
    """
    return board.run(Path.cwd(), detached=False)


@mcp.tool()
def job_status(job_id: str) -> str:
    """Progress of a `panel_run` or `board_run` job (same text as `founder-vn panel status`): counts and last error."""
    return panel.job_status(Path.cwd(), job_id)


@mcp.tool()
def plan_compile(check: bool = False) -> str:
    """Compile founder/business-plan.md (same text as `founder-vn plan`).

    The verdict is computed from the CFO numbers only; the panel is a separate demand-signal
    line. With `check` nothing is written and the text says whether the plan is current.
    """
    return plan.run(Path.cwd(), check)[0]


def main() -> None:
    """Entry point of `founder-vn-mcp`: serve over stdio."""
    mcp.run("stdio")


if __name__ == "__main__":
    main()
