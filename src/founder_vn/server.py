"""MCP stdio server `founder-vn-mcp`: wraps the same functions as the CLI."""

from mcp.server.mcpserver import MCPServer

from founder_vn import __version__, info

mcp = MCPServer("founder-vn", version=__version__)


@mcp.tool()
def server_info() -> str:
    """Return the founder-vn package version (same text as `founder-vn version`)."""
    return info.version_text()


def main() -> None:
    """Entry point of `founder-vn-mcp`: serve over stdio."""
    mcp.run("stdio")


if __name__ == "__main__":
    main()
