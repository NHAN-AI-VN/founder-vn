"""The one function behind `founder-vn version` and the MCP tool `server_info`."""

from founder_vn import __version__


def version_text() -> str:
    """Return the version line both transports print, without a trailing newline."""
    return f"founder-vn {__version__}"
