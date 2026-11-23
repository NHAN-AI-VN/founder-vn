"""CLI `founder-vn`: wraps the same functions as the MCP server."""

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from founder_vn import cfo, files, info, install, panel, plan, pricing


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
    panel_parser = sub.add_parser(
        "panel", help="buyer panel: init, run, status, check, save, tally"
    )
    panel_sub = panel_parser.add_subparsers(dest="panel_command", required=True)
    init_parser = panel_sub.add_parser("init", help="deal persona cards from customer.json")
    init_parser.add_argument("--customer", default="customer.json", help="under founder/")
    init_parser.add_argument("--pitch", default="pitch.md", help="under founder/")
    init_parser.add_argument("--n", type=int, default=panel.DEFAULT_N, help="number of buyers")
    init_parser.add_argument("--seed", type=int, help="same seed, same cards")
    panel_sub.add_parser("check", help="list buyers whose answer is missing or broken")
    save_parser = panel_sub.add_parser("save", help="file a buyer's printed reply (stdin)")
    save_parser.add_argument("id", help="buyer id, e.g. P003")
    panel_sub.add_parser("tally", help="count the answers into results.md and results.json")
    panel_sub.add_parser("run", help="ask each buyer through the configured model; prints a job id")
    status_parser = panel_sub.add_parser("status", help="progress of a `panel run` job")
    status_parser.add_argument("job_id", help="job id printed by `panel run`")
    work_parser = panel_sub.add_parser("work", help=argparse.SUPPRESS)
    work_parser.add_argument("job_id")
    plan_parser = sub.add_parser(
        "plan", help="compile business-plan.md from what exists under founder/"
    )
    plan_parser.add_argument(
        "--check", action="store_true", help="write nothing; exit 1 if business-plan.md is stale"
    )
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
    if args.command == "panel":
        try:
            if args.panel_command == "init":
                sys.stdout.write(
                    panel.init(Path.cwd(), args.customer, args.pitch, args.n, args.seed)
                )
            elif args.panel_command == "check":
                text, code = panel.check(Path.cwd())
                sys.stdout.write(text)
                return code
            elif args.panel_command == "run":
                sys.stdout.write(panel.run(Path.cwd(), detached=True))
            elif args.panel_command == "status":
                sys.stdout.write(panel.job_status(Path.cwd(), args.job_id))
            elif args.panel_command == "work":
                panel.work(Path.cwd(), args.job_id)
            elif args.panel_command == "tally":
                sys.stdout.write(panel.run_tally(Path.cwd()))
            else:
                sys.stdout.write(panel.save(Path.cwd(), args.id, sys.stdin.read()))
        except (panel.PanelError, files.PathRefused) as e:
            print(f"lỗi: {e}", file=sys.stderr)
            return 2
        return 0
    if args.command == "plan":
        try:
            text, code = plan.run(Path.cwd(), args.check)
            sys.stdout.write(text)
            return code
        except (cfo.NumbersError, panel.PanelError, files.PathRefused) as e:
            print(f"lỗi: {e}", file=sys.stderr)
            return 2
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


if __name__ == "__main__":
    run()
