#!/usr/bin/env python3
"""Unified DAOS command-line front door."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from daos_core import audit_memory_surfaces, build_orientation_bundle, run_reset_recovery_test, validate_pack_dir, write_reset_handoff


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

    orient = subparsers.add_parser(
        "orient",
        help="build a read-only assistant orientation bundle",
        description="Build a deterministic DAOS orientation bundle for an assistant. No files are modified and no LLM is called.",
    )
    orient.add_argument("pack_dir", help="Path to a DAOS pack directory to orient from")
    orient.add_argument("--task", default=None, help="Current task to include in the orientation bundle")

    reset_test = subparsers.add_parser(
        "reset-test",
        help="run deterministic reset recovery checks",
        description="Check whether a DAOS pack can support fresh-session reset recovery. No files are modified and no LLM is called.",
    )
    reset_test.add_argument("pack_dir", help="Path to a DAOS pack directory to test")

    handoff = subparsers.add_parser(
        "handoff",
        help="overwrite the reset handoff artifact",
        description="Write the current exact reset handoff into a DAOS pack. This overwrites wiki/cache/reset-handoff.md.",
    )
    handoff.add_argument("pack_dir", help="Path to a DAOS pack directory to update")
    handoff.add_argument("--lane", required=True, help="Current lane for the handoff")
    handoff.add_argument("--status", required=True, help="Current status for the handoff")
    handoff.add_argument("--why", required=True, help="Why this handoff exists")
    handoff.add_argument("--next", required=True, help="Exact next move after reset or idle")
    handoff.add_argument("--verify", required=True, help="First verification to run before continuing")

    memory_audit = subparsers.add_parser(
        "memory-audit",
        help="audit DAOS memory surfaces",
        description="Read-only audit of DAOS active and durable memory surfaces. No files are modified.",
    )
    memory_audit.add_argument("pack_dir", help="Path to a DAOS pack directory to audit")

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


def run_orient(pack_dir_arg: str, task: str | None) -> int:
    exit_code, stdout, stderr = build_orientation_bundle(pack_dir_arg, task=task)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_reset_test(pack_dir_arg: str) -> int:
    exit_code, stdout, stderr = run_reset_recovery_test(pack_dir_arg)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_handoff(args: argparse.Namespace) -> int:
    exit_code, stdout, stderr = write_reset_handoff(
        args.pack_dir,
        lane=args.lane,
        status=args.status,
        why=args.why,
        next_move=args.next,
        verify=args.verify,
    )
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_memory_audit(pack_dir_arg: str) -> int:
    exit_code, stdout, stderr = audit_memory_surfaces(pack_dir_arg)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "check":
        return run_check(args.pack_dir)
    if args.command == "orient":
        return run_orient(args.pack_dir, args.task)
    if args.command == "reset-test":
        return run_reset_test(args.pack_dir)
    if args.command == "handoff":
        return run_handoff(args)
    if args.command == "memory-audit":
        return run_memory_audit(args.pack_dir)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
