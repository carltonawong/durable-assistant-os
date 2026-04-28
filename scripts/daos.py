#!/usr/bin/env python3
"""Unified DAOS command-line front door."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from daos_bootstrap import bootstrap
from daos_core import audit_memory_surfaces, build_state_report, build_orientation_bundle, find_instruction_carriers, prepend_daos_coexistence_rule, run_reset_recovery_test, validate_pack_dir, write_instruction_scan_report, write_reset_handoff


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        return argparse.Namespace(command="status", pack_dir=None)

    parser = argparse.ArgumentParser(
        prog="daos",
        description="DAOS local harness commands. Only shipped commands are listed here."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser(
        "status",
        help="show compact DAOS setup and continuity status",
        description="Show the current DAOS setup and continuity status. No files are modified.",
    )
    status.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")

    on = subparsers.add_parser(
        "on",
        help="show what DAOS is currently on",
        description="Alias for status: show the current DAOS setup and DAOS On continuity surface. No files are modified.",
    )
    on.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")


    init = subparsers.add_parser(
        "init",
        help="install the DAOS baseline",
        description="Install the mandatory DAOS baseline and optionally scan existing instruction carriers for coexistence review.",
    )
    init.add_argument("pack_dir", nargs="?", help="Destination DAOS home. Defaults to DAOS_HOME or ~/.daos.")
    init.add_argument("--blank", action="store_true", help="Install baseline without scanning existing instruction carriers")
    init.add_argument("--scan", action="append", default=[], help="Working directory to scan for existing agent instruction files")
    init.add_argument("--force", action="store_true", help="Replace an existing non-empty DAOS destination")

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


def resolve_default_pack_dir(pack_dir_arg: str | None) -> Path:
    if pack_dir_arg:
        return Path(pack_dir_arg).expanduser().resolve()
    configured = os.environ.get("DAOS_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".daos").resolve()


def run_status(pack_dir_arg: str | None) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = build_state_report(pack_dir)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def _resolve_init_scan_paths(args: argparse.Namespace) -> list[Path]:
    if args.blank:
        return []
    if args.scan:
        return [Path(path).expanduser().resolve() for path in args.scan]
    if sys.stdin.isatty():
        default = Path.cwd()
        response = input(f"Working directory to scan for agent instructions [{default}]: ").strip()
        return [Path(response).expanduser().resolve() if response else default.resolve()]
    return [Path.cwd().resolve()]


def _approve_instruction_edits(carriers: list[Path], backup_root: Path) -> dict[Path, Path]:
    if not carriers or not sys.stdin.isatty():
        return {}
    pending = []
    for carrier in carriers:
        try:
            text = carrier.read_text(encoding="utf-8")
        except OSError:
            continue
        if "DAOS coexistence rule" not in text:
            pending.append(carrier)
    if not pending:
        return {}

    print("DAOS found existing agent instruction files.")
    for carrier in pending:
        print(f"DAOS wants approval to prepend the coexistence rule to: {carrier}")
    response = input("Apply these approved instruction edits now? [y/N]: ").strip().lower()
    if response not in {"y", "yes"}:
        return {}

    applied: dict[Path, Path] = {}
    for carrier in pending:
        backup_path = prepend_daos_coexistence_rule(carrier, backup_root=backup_root)
        if backup_path:
            applied[carrier] = backup_path
    return applied


def run_init(args: argparse.Namespace) -> int:
    pack_dir = resolve_default_pack_dir(args.pack_dir)
    try:
        scan_paths = _resolve_init_scan_paths(args)
        destination = bootstrap(pack_dir, force=args.force)
        report_path = None
        applied_backups: dict[Path, Path] = {}
        carriers = find_instruction_carriers(scan_paths) if scan_paths else []
        if carriers:
            timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
            backup_root = destination / ".daos" / "backups" / "instructions" / timestamp
            applied_backups = _approve_instruction_edits(carriers, backup_root)
        if scan_paths:
            report_path = write_instruction_scan_report(
                destination,
                scan_paths,
                applied_paths=list(applied_backups.keys()),
                backup_paths=applied_backups,
            )
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"DAOS init failed: {exc}", file=sys.stderr)
        return 1

    print(f"DAOS initialized: {destination}")
    print("purpose: shared continuity baseline for agents; existing instruction files are edited only with approval")
    print("baseline: installed mandatory wiki/cache framework")
    if args.blank:
        print("instruction scan: skipped (--blank)")
    elif report_path:
        display_report_path = report_path
        try:
            display_report_path = report_path.relative_to(destination)
        except ValueError:
            pass
        print(f"instruction scan: wrote review report inside DAOS home: {display_report_path}")
        if applied_backups:
            print(f"instruction edits: applied with approval ({len(applied_backups)})")
            print("instruction backups: .daos/backups/instructions/")
        else:
            print("instruction edits: none applied; review report lists any proposed edits")
    print("next: run `daos` or `daos status` to view setup and continuity status")
    return 0


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
    if args.command in {"status", "on"}:
        return run_status(args.pack_dir)
    if args.command == "init":
        return run_init(args)
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
