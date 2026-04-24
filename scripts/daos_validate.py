#!/usr/bin/env python3
"""Validate whether a DAOS pack is minimally filled enough to operate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from daos_core import validate_pack_dir


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only check of whether a DAOS pack is minimally filled enough to operate. No files are modified."
    )
    parser.add_argument("pack_dir", help="Path to a DAOS pack directory to validate")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    result = validate_pack_dir(args.pack_dir)
    pack_dir = Path(args.pack_dir).expanduser().resolve()

    if result.errors:
        print(f"DAOS pack validation failed: {pack_dir}", file=sys.stderr)
        for issue in result.errors:
            print(f"- {issue}", file=sys.stderr)
        if result.warnings:
            print(f"warnings: {len(result.warnings)}", file=sys.stderr)
            for warning in result.warnings:
                print(f"- {warning}", file=sys.stderr)
        return 1

    print(f"DAOS pack validation passed: {pack_dir}")
    print("errors: 0")
    print(f"warnings: {len(result.warnings)}")
    for warning in result.warnings:
        print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
