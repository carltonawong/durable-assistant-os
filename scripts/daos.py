#!/usr/bin/env python3
"""Unified DAOS command-line front door."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from daos_core import validate_pack_dir


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="DAOS local harness commands. Only shipped commands are listed here."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check = subparsers.add_parser(
        "check",
        help="read-only pack health check",
        description="Run a read-only DAOS pack health check. No files are modified.",
    )
    check.add_argument("pack_dir", help="Path to a DAOS pack directory to check")

    return parser.parse_args(argv)


def run_check(pack_dir_arg: str) -> int:
    pack_dir = Path(pack_dir_arg).expanduser().resolve()
    result = validate_pack_dir(pack_dir)

    if result.errors:
        print(f"DAOS check failed: {pack_dir}", file=sys.stderr)
        print(f"errors: {len(result.errors)}", file=sys.stderr)
        for issue in result.errors:
            print(f"- {issue}", file=sys.stderr)
        print(f"warnings: {len(result.warnings)}", file=sys.stderr)
        for warning in result.warnings:
            print(f"- {warning}", file=sys.stderr)
        print("next: fill required fields or restore missing required files, then run check again", file=sys.stderr)
        return 1

    print(f"DAOS check passed: {pack_dir}")
    print("errors: 0")
    print(f"warnings: {len(result.warnings)}")
    for warning in result.warnings:
        print(f"- {warning}")
    if result.warnings:
        print("next: review warnings before relying on this pack operationally")
    else:
        print("next: use this pack with the DAOS read order and live-reality checks")
    return 0


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "check":
        return run_check(args.pack_dir)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
