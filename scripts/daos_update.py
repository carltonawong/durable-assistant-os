#!/usr/bin/env python3
"""Inspect a DAOS pack and report or apply a safe update posture."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from daos_core import validate_pack_dir


REPO_ROOT = Path(__file__).resolve().parents[1]
STARTER_PACK_DIR = REPO_ROOT / "starter-pack"
USER_OWNED_FILES = (
    "assistant-charter.md",
    "operating-profile.md",
)
FRAMEWORK_OWNED_FILES = (
    "README.md",
    "lane-snapshot.md",
    "cadence-review.md",
)
MANAGED_METADATA_FILE = "daos-pack.json"
OPTIONAL_METADATA_FIELDS = (
    "framework_version",
    "pack_id",
)
DEFAULT_SCHEMA_VERSION = "1"
DEFAULT_FRAMEWORK_VERSION = "0.1.0-alpha3"
DEFAULT_DURABLE_CAPTURE_RULE = (
    "if a second review shows something should not live mainly in hot cache or chat, "
    "create/update a durable note in the same pass"
)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Inspect a DAOS pack and show or apply a safe update posture without rewriting user-owned files."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("check", "plan", "apply"):
        subparser = subparsers.add_parser(command)
        subparser.add_argument("pack_dir", help="Path to a DAOS pack directory")

    return parser.parse_args(argv)


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def ensure_managed_dirs(pack_dir: Path) -> tuple[Path, Path, Path, Path]:
    root = pack_dir / ".daos"
    backups = root / "backups"
    migrations = root / "migrations"
    review_notes = root / "review-notes"
    root.mkdir(exist_ok=True)
    backups.mkdir(exist_ok=True)
    migrations.mkdir(exist_ok=True)
    review_notes.mkdir(exist_ok=True)
    return root, backups, migrations, review_notes


def build_managed_manifest(pack_dir: Path, manifest: dict[str, object]) -> dict[str, object]:
    return {
        "last_checked_at": iso_now(),
        "managed_metadata_file": MANAGED_METADATA_FILE,
        "schema_version": str(manifest.get("schema_version", DEFAULT_SCHEMA_VERSION)),
        "framework_version": str(manifest.get("framework_version", DEFAULT_FRAMEWORK_VERSION)),
        "pack_id": str(manifest.get("pack_id", "")),
        "protected_files": list(USER_OWNED_FILES),
        "framework_owned_files": list(FRAMEWORK_OWNED_FILES),
        "pack_path": str(pack_dir),
    }


def build_updated_manifest(existing_manifest: dict[str, object] | None) -> tuple[dict[str, object], list[str]]:
    actions: list[str] = []
    manifest = dict(existing_manifest or {})

    if not existing_manifest:
        actions.append("created daos-pack.json")
    if not str(manifest.get("schema_version", "")).strip():
        manifest["schema_version"] = DEFAULT_SCHEMA_VERSION
        actions.append("set schema_version")
    if not str(manifest.get("framework_version", "")).strip():
        manifest["framework_version"] = DEFAULT_FRAMEWORK_VERSION
        actions.append("set framework_version")
    if not str(manifest.get("pack_id", "")).strip():
        manifest["pack_id"] = str(uuid4())
        actions.append("set pack_id")
    if not str(manifest.get("pack_kind", "")).strip():
        manifest["pack_kind"] = "starter-pack"
        actions.append("set pack_kind")
    if not str(manifest.get("generator", "")).strip():
        manifest["generator"] = "scripts/daos_update.py"
        actions.append("set generator")
    return manifest, actions


def backup_file_if_present(path: Path, backups_dir: Path, stamp: str) -> list[str]:
    if not path.exists():
        return []
    target_dir = backups_dir / stamp
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, target_dir / path.name)
    return [f"backed up {path.name} to {target_dir}"]


def restore_framework_owned_files(pack_dir: Path) -> list[str]:
    actions: list[str] = []
    for filename in FRAMEWORK_OWNED_FILES:
        target = pack_dir / filename
        if target.exists():
            continue
        source = STARTER_PACK_DIR / filename
        if not source.is_file():
            continue
        shutil.copy2(source, target)
        actions.append(f"restored {filename}")
    return actions


def backup_user_owned_file(path: Path, backups_dir: Path, stamp: str) -> list[str]:
    return backup_file_if_present(path, backups_dir, stamp)


def add_durable_capture_rule_if_safe(pack_dir: Path, backups_dir: Path, stamp: str) -> tuple[list[str], list[str]]:
    profile_path = pack_dir / "operating-profile.md"
    if not profile_path.is_file():
        return [], []
    content = profile_path.read_text(encoding="utf-8")
    if "- Durable capture rule:" in content:
        return [], []
    section_header = "## 5. Memory / trust defaults\n\n"
    if section_header not in content:
        return [], [
            "could not safely add durable capture rule to operating-profile.md because the memory/trust section header was missing"
        ]
    insertion_anchor = "- Escalation / approval rule:"
    anchor_index = content.find(insertion_anchor)
    if anchor_index == -1:
        return [], [
            "could not safely add durable capture rule to operating-profile.md because the escalation/approval line was missing"
        ]
    line_end = content.find("\n", anchor_index)
    if line_end == -1:
        return [], [
            "could not safely add durable capture rule to operating-profile.md because the escalation/approval line was malformed"
        ]
    insertion = f"- Durable capture rule: {DEFAULT_DURABLE_CAPTURE_RULE}\n"
    updated = content[: line_end + 1] + insertion + content[line_end + 1 :]
    actions = backup_user_owned_file(profile_path, backups_dir, stamp)
    profile_path.write_text(updated, encoding="utf-8")
    actions.append("added missing durable capture rule to operating-profile.md")
    return actions, []


def write_review_note(review_notes_dir: Path, review_items: list[str], stamp: str) -> Path | None:
    if not review_items:
        return None
    path = review_notes_dir / f"{stamp}-warning-review.md"
    content = [
        "# DAOS Update Review Note",
        "",
        f"Generated: {iso_now()}",
        "",
        "## Why this exists",
        "",
        "The updater found warning-level or review-required items that were not rewritten automatically.",
        "",
        "## Review items",
        "",
    ]
    content.extend(f"- {item}" for item in review_items)
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def apply_updates(pack_dir: Path) -> str:
    validation = validate_pack_dir(pack_dir)
    if validation.errors:
        raise ValueError("pack has blocking validation errors; refuse apply until the pack is minimally operable")

    existing_manifest, _ = load_manifest(pack_dir)
    updated_manifest, actions = build_updated_manifest(existing_manifest)

    root, backups_dir, migrations_dir, review_notes_dir = ensure_managed_dirs(pack_dir)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    action_log: list[str] = []
    action_log.extend(backup_file_if_present(pack_dir / MANAGED_METADATA_FILE, backups_dir, stamp))

    manifest_path = pack_dir / MANAGED_METADATA_FILE
    manifest_path.write_text(json.dumps(updated_manifest, indent=2) + "\n", encoding="utf-8")
    managed_manifest = build_managed_manifest(pack_dir, updated_manifest)
    (root / "manifest.json").write_text(json.dumps(managed_manifest, indent=2) + "\n", encoding="utf-8")
    actions.append("wrote .daos/manifest.json")

    restore_actions = restore_framework_owned_files(pack_dir)
    actions.extend(restore_actions)

    mixed_actions, review_items = add_durable_capture_rule_if_safe(pack_dir, backups_dir, stamp)
    action_log.extend(item for item in mixed_actions if item.startswith("backed up "))
    actions.extend(item for item in mixed_actions if not item.startswith("backed up "))

    review_items.extend(validation.warnings)
    review_note_path = write_review_note(review_notes_dir, review_items, stamp)
    if review_note_path is not None:
        actions.append(f"wrote review note: {review_note_path.name}")

    mode = "metadata-plus-additive-safe-migrations" if restore_actions or mixed_actions or review_note_path else "metadata-only"
    migration_record = {
        "applied_at": iso_now(),
        "mode": mode,
        "protected_files": list(USER_OWNED_FILES),
        "framework_owned_files": list(FRAMEWORK_OWNED_FILES),
        "actions": actions,
        "backups": action_log,
        "warnings_seen": validation.warnings,
        "review_items": review_items,
    }
    migration_path = migrations_dir / f"{stamp}-apply.json"
    migration_path.write_text(json.dumps(migration_record, indent=2) + "\n", encoding="utf-8")

    lines = [f"DAOS pack update apply: {pack_dir}", f"applied posture: {mode}"]
    if action_log:
        lines.append("backups:")
        lines.extend(f"- {item}" for item in action_log)
    else:
        lines.append("backups:")
        lines.append("- no existing managed metadata file needed backup")
    lines.append("actions:")
    lines.extend(f"- {item}" for item in actions)
    lines.append(f"migration_record: {migration_path}")
    if review_note_path is not None:
        lines.append(f"review note: {review_note_path}")
    lines.append("protected files:")
    lines.extend(f"- left untouched: {name}" for name in USER_OWNED_FILES)
    return "\n".join(lines)


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
    lines.append("planned posture: managed metadata only unless a clearly framework-owned additive migration is safe")
    lines.append("protected files:")
    lines.extend(f"- do not overwrite {name}" for name in USER_OWNED_FILES)
    if manifest_gaps:
        lines.append("safe next actions:")
        for gap in manifest_gaps:
            if gap == "missing managed metadata anchor":
                lines.append("- add managed metadata anchor via apply")
            else:
                lines.append(f"- add {gap.split(': ', 1)[1]} to managed metadata")
    else:
        lines.append("safe next actions:")
        lines.append("- no immediate managed metadata patch is required")
    for filename in FRAMEWORK_OWNED_FILES:
        if not (pack_dir / filename).exists():
            lines.append(f"- restore missing framework-owned support file: {filename}")
    profile_path = pack_dir / "operating-profile.md"
    if profile_path.is_file():
        profile_text = profile_path.read_text(encoding="utf-8")
        if "- Durable capture rule:" not in profile_text:
            if "## 5. Memory / trust defaults\n\n" in profile_text and "- Escalation / approval rule:" in profile_text:
                lines.append("- add missing durable capture rule to operating-profile.md")
            else:
                lines.append("- write review note for missing durable capture rule because the operating-profile shape is not safely patchable")
    if validation.errors:
        lines.append("apply blockers:")
        lines.extend(f"- {error}" for error in validation.errors)
    else:
        lines.append("apply blockers:")
        lines.append("- none from minimal validation")
    if validation.warnings:
        lines.append("review items:")
        lines.extend(f"- {warning}" for warning in validation.warnings)
        lines.append("- write review note instead of rewriting warning-level user context")
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

    try:
        if args.command == "check":
            print(render_check(pack_dir))
            return 0
        if args.command == "plan":
            print(render_plan(pack_dir))
            return 0
        if args.command == "apply":
            print(apply_updates(pack_dir))
            return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"ERROR: Unsupported command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
