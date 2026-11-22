"""CLI `founder-vn`: wraps the same functions as the MCP server."""

import argparse
import sys
from collections.abc import Sequence

from founder_vn import info


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="founder-vn")
    parser.add_argument("--version", action="store_true", help="print the version and exit")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("version", help="print the package version")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI; return the process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version or args.command == "version":
        print(info.version_text())
        return 0
    parser.print_help()
    return 2


def run() -> None:
    sys.exit(main())
