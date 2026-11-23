"""CLI `founder-vn`: wraps the same functions as the MCP server."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from founder_vn import cfo, files, info, install, pricing


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="founder-vn")
    parser.add_argument("--version", action="store_true", help="print the version and exit")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("version", help="print the package version")
    cfo_parser = sub.add_parser("cfo", help="unit economics report from numbers.json")
    cfo_parser.add_argument("numbers", help="numbers.json under founder/")
    cfo_parser.add_argument("--price", help="what-if price, e.g. 40.000 or 40k")
    cfo_parser.add_argument("--volume", type=float, default=1.0, help="what-if volume multiplier")
    cfo_parser.add_argument("--json", action="store_true", help="print the numbers as JSON")
    cfo_parser.add_argument("--out", help="write the report under founder/ (e.g. cfo.md)")
    pricing_parser = sub.add_parser(
        "pricing", help="Van Westendorp price sensitivity from the panel's price answers"
    )
    pricing_parser.add_argument("source", help="JSON file under founder/ with answers and prices")
    pricing_parser.add_argument("--json", action="store_true", help="print the numbers as JSON")
    pricing_parser.add_argument("--out", help="write the report under founder/ (e.g. pricing.md)")
    install_parser = sub.add_parser(
        "install", help="copy skills into a host and print its MCP setup"
    )
    install_parser.add_argument("--host", required=True, choices=install.HOSTS)
    install_parser.add_argument(
        "--print-only", action="store_true", help="show the plan and snippet without writing"
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the CLI; return the process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version or args.command == "version":
        print(info.version_text())
        return 0
    if args.command == "cfo":
        try:
            sys.stdout.write(
                cfo.run(Path.cwd(), args.numbers, args.price, args.volume, args.json, args.out)
            )
        except (cfo.NumbersError, files.PathRefused, ValueError) as e:
            print(f"lỗi: {e}", file=sys.stderr)
            return 2
        return 0
    if args.command == "pricing":
        try:
            sys.stdout.write(pricing.run(Path.cwd(), args.source, args.json, args.out))
        except (pricing.PricingInputError, files.PathRefused) as e:
            print(f"lỗi: {e}", file=sys.stderr)
            return 2
        return 0
    if args.command == "install":
        try:
            text = install.run(Path.cwd(), args.host, args.print_only)
        except install.InstallRefused as e:
            print(f"lỗi: {e}", file=sys.stderr)
            return 2
        sys.stdout.write(text)
        return 0
    parser.print_help()
    return 2


def run() -> None:
    sys.exit(main())
