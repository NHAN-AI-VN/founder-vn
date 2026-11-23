"""MCP stdio server `founder-vn-mcp`: wraps the same functions as the CLI."""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from founder_vn import __version__, cfo, info, panel, pricing

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
    n: int = 100,
    seed: int | None = None,
) -> str:
    """Deal persona cards (same text as `founder-vn panel init`).

    `customer` and `pitch` are read under founder/; the cards are written to founder/panel/.
    The same `seed` gives the same cards.
    """
    return panel.init(Path.cwd(), customer, pitch, n, seed)


@mcp.tool()
def panel_tally() -> str:
    """Count the buyers' answers into results.md and results.json (same text as `founder-vn panel tally`)."""
    return panel.run_tally(Path.cwd())


def main() -> None:
    """Entry point of `founder-vn-mcp`: serve over stdio."""
    mcp.run("stdio")


if __name__ == "__main__":
    main()
