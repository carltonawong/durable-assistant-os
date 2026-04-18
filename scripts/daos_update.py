#!/usr/bin/env python3
"""Inspect a DAOS pack and report a safe update posture."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from daos_core import validate_pack_dir


USER_OWNED_FILES = (
    "assistant-charter.md",
    "operating-profile.md",
)
MANAGED_METADATA_FILE = "daos-pack.json"
OPTIONAL_METADATA_FIELDS = (
    "framework_version",
    "pack_id",
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a DAOS pack and show a safe update posture without rewriting user-owned files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("check", "plan"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("pack_dir", help="Path to a DAOS pack directory")

    return parser.parse_args(argv)


def load_manifest(pack_dir: Path) -> tuple[dict[str, object] | None, list[str]]:
    manifest_path = pack_dir / MANAGED_METADATA_FILE
    if not manifest_path.is_file():
        return None, ["missing managed metadata anchor"]

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, [f"invalid managed metadata anchor: {exc}"]

    gaps: list[str] = []
    for field in OPTIONAL_METADATA_FIELDS:
        value = str(manifest.get(field, "")).strip()
        if not value:
            gaps.append(f"missing metadata field: {field}")
    return manifest, gaps


def update_ready(manifest_gaps: list[str], validation_errors: list[str]) -> str:
    if validation_errors:
        return "needs-review"
    if manifest_gaps:
        return "yes"
    return "stable"


def render_check(pack_dir: Path) -> str:
    validation = validate_pack_dir(pack_dir)
    manifest, manifest_gaps = load_manifest(pack_dir)
    lines = [f"DAOS pack update check: {pack_dir}"]
    lines.append(f"manifest: {'present' if manifest is not None else 'missing'}")
    lines.append(f"schema_version: {str((manifest or {}).get('schema_version', '[missing]'))}")
    lines.append(f"framework_version: {str((manifest or {}).get('framework_version', '[missing]'))}")
    lines.append(f"pack_id: {str((manifest or {}).get('pack_id', '[missing]'))}")
    lines.append(f"validation_errors: {len(validation.errors)}")
    lines.append(f"validation_warnings: {len(validation.warnings)}")
    lines.append(f"upgrade_ready: {update_ready(manifest_gaps, validation.errors)}")
    if manifest_gaps:
        lines.append("metadata_gaps:")
        lines.extend(f"- {gap}" for gap in manifest_gaps)
    if validation.errors:
        lines.append("blocking_errors:")
        lines.extend(f"- {error}" for error in validation.errors)
    if validation.warnings:
        lines.append("lint_warnings:")
        lines.extend(f"- {warning}" for warning in validation.warnings)
    return "\n".join(lines)


def render_plan(pack_dir: Path) -> str:
    validation = validate_pack_dir(pack_dir)
    _, manifest_gaps = load_manifest(pack_dir)
    lines = [f"DAOS pack update plan: {pack_dir}"]
    lines.append("planned posture: managed metadata only unless a future additive migration is explicitly safe")
    lines.append("protected files:")
    lines.extend(f"- do not overwrite {name}" for name in USER_OWNED_FILES)
    if manifest_gaps:
        lines.append("safe next actions:")
        for gap in manifest_gaps:
            if gap == "missing managed metadata anchor":
                lines.append("- add managed metadata anchor when an explicit updater write path is implemented")
            else:
                lines.append(f"- add {gap.split(': ', 1)[1]} to managed metadata")
    else:
        lines.append("safe next actions:")
        lines.append("- no immediate managed metadata patch is required")
    if validation.errors:
        lines.append("apply blockers:")
        lines.extend(f"- {error}" for error in validation.errors)
    else:
        lines.append("apply blockers:")
        lines.append("- none from minimal validation")
    if validation.warnings:
        lines.append("review items:")
        lines.extend(f"- {warning}" for warning in validation.warnings)
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    pack_dir = Path(args.pack_dir).expanduser().resolve()

    if not pack_dir.exists():
        print(f"ERROR: Pack directory does not exist: {pack_dir}", file=sys.stderr)
        return 1
    if not pack_dir.is_dir():
        print(f"ERROR: Pack path is not a directory: {pack_dir}", file=sys.stderr)
        return 1

    if args.command == "check":
        print(render_check(pack_dir))
        return 0
    if args.command == "plan":
        print(render_plan(pack_dir))
        return 0

    print(f"ERROR: Unsupported command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
