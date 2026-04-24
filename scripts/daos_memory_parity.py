#!/usr/bin/env python3
"""Audit DAOS memory parity beyond file existence."""

from __future__ import annotations

import argparse
from pathlib import Path

from daos_core.parity import audit_memory_parity


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read-only audit of whether a DAOS pack's memory surfaces match DAOS parity rules. No files are modified."
    )
    parser.add_argument("pack_dir", help="Path to a DAOS pack directory to audit")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    root = Path(args.pack_dir).expanduser().resolve()
    result = audit_memory_parity(root)

    print(f"Status: {result.status}")
    print("Findings:")
    if result.findings:
        for finding in result.findings:
            print(f"- {finding.severity}: {finding.message}")
    else:
        print("- no material memory parity issues found")

    print("Repairs made:")
    if result.repairs_made:
        for repair in result.repairs_made:
            print(f"- {repair}")
    else:
        print("- none")

    print("Recommended next move:")
    if result.status == "healthy":
        print("- keep operating; rerun after meaningful memory/doctrine changes")
    elif result.status == "watch":
        print("- inspect warnings and apply the smallest safe correction if the drift is real")
    else:
        print("- repair errors before treating this DAOS pack as parity-aligned")

    return 1 if result.status == "drift" else 0


if __name__ == "__main__":
    raise SystemExit(main())
