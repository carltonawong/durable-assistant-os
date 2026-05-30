#!/usr/bin/env python3
"""Export and inspect DAOS portability bundles."""

# DAOS baseline note: current public framework baseline is v0.2.7; this module remains part of the current release surface.

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path


BUNDLE_VERSION = "1"
PACK_MANIFEST = "daos-pack.json"
MANAGED_MANIFEST = ".daos/manifest.json"
MIGRATIONS_DIR = ".daos/migrations"


def iso_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Export and inspect DAOS portability bundles"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    export = subparsers.add_parser("export", help="Create a portability bundle")
    export.add_argument("--pack-dir", required=True)
    export.add_argument("--wiki-root", required=True)
    export.add_argument("--out", required=True)
    export.add_argument("--include-active-memory", action="store_true")
    export.add_argument("--hot-cache")
    export.add_argument("--agent-continuity")

    inspect = subparsers.add_parser("inspect", help="Inspect a portability bundle")
    inspect.add_argument("bundle_dir")

    plan = subparsers.add_parser("plan", help="Plan a portability import")
    plan.add_argument("bundle_dir")
    plan.add_argument("--target-wiki-root", required=True)
    plan.add_argument("--target-pack-dir")
    plan.add_argument("--review-output")

    apply_cmd = subparsers.add_parser("apply", help="Apply a safe portability import")
    apply_cmd.add_argument("bundle_dir")
    apply_cmd.add_argument("--target-wiki-root", required=True)
    apply_cmd.add_argument("--target-pack-dir", required=True)
    apply_cmd.add_argument("--review-input")
    apply_cmd.add_argument(
        "--durable-conflicts",
        choices=("keep", "stage", "overwrite"),
        default="keep",
        help="How to handle conflicting durable wiki files (default: keep)",
    )
    apply_cmd.add_argument(
        "--active-memory",
        choices=("stage", "skip"),
        default="stage",
        help="How to handle bundled active-memory sidecars (default: stage)",
    )

    return parser.parse_args(argv)


def require_dir(path: Path, label: str) -> None:
    if not path.exists():
        raise ValueError(f"{label} does not exist: {path}")
    if not path.is_dir():
        raise ValueError(f"{label} is not a directory: {path}")


def require_file(path: Path, label: str) -> None:
    if not path.exists():
        raise ValueError(f"{label} does not exist: {path}")
    if not path.is_file():
        raise ValueError(f"{label} is not a file: {path}")


def durable_rel_key(rel: Path) -> str:
    return rel.as_posix()


def normalize_review_rel(value: str) -> str:
    return value.strip().replace("\\", "/")


def copy_tree_contents(source: Path, destination: Path) -> int:
    count = 0
    destination.mkdir(parents=True, exist_ok=True)
    for item in source.rglob("*"):
        rel = item.relative_to(source)
        target = destination / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        count += 1
    return count


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def bundle_manifest(pack_dir: Path, wiki_root: Path, include_active_memory: bool, hot_cache: Path | None, agent_continuity: Path | None, durable_count: int, migration_count: int) -> dict[str, object]:
    pack_manifest = read_json(pack_dir / PACK_MANIFEST)
    return {
        "bundle_version": BUNDLE_VERSION,
        "exported_at": iso_now(),
        "pack_id": str(pack_manifest.get("pack_id", "")),
        "schema_version": str(pack_manifest.get("schema_version", "")),
        "framework_version": str(pack_manifest.get("framework_version", "")),
        "payload": {
            "durable_wiki": {
                "included": True,
                "root_name": wiki_root.name,
                "file_count": durable_count,
            },
            "pack_metadata": {
                "included": True,
                "migrations_included": migration_count > 0,
                "migration_file_count": migration_count,
            },
            "active_memory": {
                "included": include_active_memory,
                "hot_cache": hot_cache.name if hot_cache else None,
                "agent_continuity": agent_continuity.name if agent_continuity else None,
            },
        },
    }


def export_bundle(args: argparse.Namespace) -> str:
    pack_dir = Path(args.pack_dir).expanduser().resolve()
    wiki_root = Path(args.wiki_root).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve()
    require_dir(pack_dir, "pack_dir")
    require_dir(wiki_root, "wiki_root")
    if not (pack_dir / PACK_MANIFEST).is_file():
        raise ValueError(f"pack_dir is missing {PACK_MANIFEST}: {pack_dir}")

    if out_dir.exists():
        raise ValueError(f"output directory already exists: {out_dir}")

    hot_cache = Path(args.hot_cache).expanduser().resolve() if args.hot_cache else None
    agent_continuity = Path(args.agent_continuity).expanduser().resolve() if args.agent_continuity else None
    if args.include_active_memory and (hot_cache is None or agent_continuity is None):
        raise ValueError("--include-active-memory requires both --hot-cache and --agent-continuity")
    if args.include_active_memory:
        require_file(hot_cache, "hot_cache")
        require_file(agent_continuity, "agent_continuity")

    out_dir.mkdir(parents=True)
    (out_dir / "pack").mkdir()
    shutil.copy2(pack_dir / PACK_MANIFEST, out_dir / "pack" / PACK_MANIFEST)

    migration_count = 0
    managed_manifest = pack_dir / MANAGED_MANIFEST
    if managed_manifest.is_file():
        managed_target = out_dir / "pack" / ".daos"
        managed_target.mkdir(parents=True, exist_ok=True)
        shutil.copy2(managed_manifest, managed_target / "manifest.json")
        migrations_dir = pack_dir / MIGRATIONS_DIR
        if migrations_dir.is_dir():
            migration_count = copy_tree_contents(migrations_dir, managed_target / "migrations")

    durable_target = out_dir / "durable" / "wiki"
    durable_count = copy_tree_contents(wiki_root, durable_target)

    if args.include_active_memory:
        active_dir = out_dir / "active"
        active_dir.mkdir()
        shutil.copy2(hot_cache, active_dir / "hot-cache.md")
        shutil.copy2(agent_continuity, active_dir / "agent-continuity.md")

    manifest = bundle_manifest(pack_dir, wiki_root, args.include_active_memory, hot_cache, agent_continuity, durable_count, migration_count)
    (out_dir / "portability-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    return f"DAOS portability export: {out_dir}\nbundle_version: 1\ndurable_wiki_files: {durable_count}\nactive_memory_included: {'yes' if args.include_active_memory else 'no'}"


def load_bundle_manifest(bundle_dir: Path) -> dict[str, object]:
    require_dir(bundle_dir, "bundle_dir")
    manifest_path = bundle_dir / "portability-manifest.json"
    if not manifest_path.is_file():
        raise ValueError(f"bundle is missing portability-manifest.json: {bundle_dir}")
    return read_json(manifest_path)


def inspect_bundle(bundle_dir: Path) -> str:
    manifest = load_bundle_manifest(bundle_dir)
    payload = manifest["payload"]
    lines = [f"DAOS portability bundle: {bundle_dir}"]
    lines.append(f"bundle_version: {manifest['bundle_version']}")
    lines.append(f"pack_id: {manifest['pack_id']}")
    lines.append(f"schema_version: {manifest['schema_version']}")
    lines.append(f"framework_version: {manifest['framework_version']}")
    lines.append(f"durable_wiki_files: {payload['durable_wiki']['file_count']}")
    lines.append(f"active_memory_included: {'yes' if payload['active_memory']['included'] else 'no'}")
    return "\n".join(lines)


def summarize_durable_import(durable_root: Path, target_wiki_root: Path) -> tuple[int, int, int]:
    new_files = 0
    unchanged_files = 0
    conflicts = 0
    for item in durable_root.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(durable_root)
        target = target_wiki_root / rel
        if not target.exists():
            new_files += 1
            continue
        if target.read_text(encoding="utf-8") == item.read_text(encoding="utf-8"):
            unchanged_files += 1
            continue
        conflicts += 1
    return new_files, unchanged_files, conflicts


def collect_new_durable_files(durable_root: Path, target_wiki_root: Path) -> list[str]:
    new_files: list[str] = []
    for item in durable_root.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(durable_root)
        target = target_wiki_root / rel
        if not target.exists():
            new_files.append(durable_rel_key(rel))
    return new_files


def collect_durable_conflicts(durable_root: Path, target_wiki_root: Path) -> list[str]:
    conflicts: list[str] = []
    for item in durable_root.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(durable_root)
        target = target_wiki_root / rel
        if target.exists() and target.read_text(encoding="utf-8") != item.read_text(encoding="utf-8"):
            conflicts.append(durable_rel_key(rel))
    return conflicts


def write_plan_review(
    output_path: Path,
    *,
    bundle_dir: Path,
    target_wiki_root: Path,
    target_pack_dir: Path | None,
    new_files: int,
    unchanged_files: int,
    conflicts: list[str],
    new_file_items: list[str],
    active_memory_stage: Path | None,
) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# DAOS Portability Plan Review",
        "",
        f"- Bundle: `{bundle_dir}`",
        f"- Target wiki root: `{target_wiki_root}`",
        f"- Target pack dir: `{target_pack_dir}`" if target_pack_dir else "- Target pack dir: not provided",
        "- Default durable-conflict policy: `keep`",
        "",
        "## Summary",
        "",
        f"- durable_new_files: {new_files}",
        f"- durable_unchanged_files: {unchanged_files}",
        f"- durable_conflicts: {len(conflicts)}",
    ]
    if active_memory_stage is not None:
        lines.extend(["", "## Active Memory", "", f"- Stage path: `{active_memory_stage}`"])
    if conflicts:
        lines.extend(["", "## Durable Conflicts", ""])
        lines.extend(f"- {item}" for item in conflicts)
    else:
        lines.extend(["", "## Durable Conflicts", "", "- None"])
    lines.extend(["", "## Proposed Decisions", ""])
    for item in conflicts:
        lines.append(f"- durable-conflict:{item} = keep")
    for item in new_file_items:
        lines.append(f"- new-file:{item} = import")
    if active_memory_stage is not None:
        lines.append("- active-memory = stage")
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def parse_review_input(review_input: Path) -> dict[str, object]:
    if not review_input.is_file():
        raise ValueError(f"review input does not exist: {review_input}")
    decisions: dict[str, object] = {"durable_conflicts": {}, "new_files": {}, "active_memory": None}
    for raw_line in review_input.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line.startswith("- ") or " = " not in line:
            continue
        left, right = line[2:].split(" = ", 1)
        if left.startswith("durable-conflict:"):
            rel = normalize_review_rel(left.split(":", 1)[1])
            action = right.strip()
            if action not in {"keep", "stage", "overwrite"}:
                raise ValueError(f"unsupported durable conflict action in review input: {action}")
            decisions["durable_conflicts"][rel] = action
        elif left.startswith("new-file:"):
            rel = normalize_review_rel(left.split(":", 1)[1])
            action = right.strip()
            if action not in {"import", "skip"}:
                raise ValueError(f"unsupported new-file action in review input: {action}")
            decisions["new_files"][rel] = action
        elif left == "active-memory":
            action = right.strip()
            if action not in {"stage", "skip"}:
                raise ValueError(f"unsupported active-memory action in review input: {action}")
            decisions["active_memory"] = action
    return decisions


def plan_import(
    bundle_dir: Path,
    target_wiki_root: Path,
    target_pack_dir: Path | None = None,
    review_output: Path | None = None,
) -> str:
    manifest = load_bundle_manifest(bundle_dir)
    payload = manifest["payload"]
    durable_root = bundle_dir / "durable" / "wiki"
    require_dir(durable_root, "bundle durable wiki")
    new_files, unchanged_files, conflicts = summarize_durable_import(durable_root, target_wiki_root)
    new_file_items = collect_new_durable_files(durable_root, target_wiki_root)
    conflict_items = collect_durable_conflicts(durable_root, target_wiki_root)
    active_memory_stage = target_pack_dir / ".daos" / "portability-stage" / "active-memory" if (payload['active_memory']['included'] and target_pack_dir is not None) else None
    lines = [f"DAOS portability plan: {bundle_dir}"]
    lines.append("would restore pack metadata anchors")
    lines.append(f"would copy durable wiki files to {target_wiki_root}")
    lines.append(f"durable_new_files: {new_files}")
    lines.append(f"durable_unchanged_files: {unchanged_files}")
    lines.append(f"durable_conflicts: {conflicts}")
    lines.append("default durable-conflict policy: keep")
    if payload['active_memory']['included']:
        if active_memory_stage is not None:
            lines.append(f"active-memory stage: {active_memory_stage}")
        else:
            lines.append("would stage active-memory files for review, not live activation")
    if review_output is not None:
        review_path = write_plan_review(
            review_output,
            bundle_dir=bundle_dir,
            target_wiki_root=target_wiki_root,
            target_pack_dir=target_pack_dir,
            new_files=new_files,
            unchanged_files=unchanged_files,
            conflicts=conflict_items,
            new_file_items=new_file_items,
            active_memory_stage=active_memory_stage,
        )
        lines.append(f"review artifact: {review_path}")
    return "\n".join(lines)


def write_collision_review(target_pack_dir: Path, collisions: list[str]) -> Path:
    review_dir = target_pack_dir / ".daos" / "portability-review"
    review_dir.mkdir(parents=True, exist_ok=True)
    path = review_dir / f"{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-collision.md"
    content = ["# DAOS Portability Collision Review", "", "The import found durable wiki collisions and left them untouched.", "", "## Collisions", ""]
    content.extend(f"- {item}" for item in collisions)
    path.write_text("\n".join(content) + "\n", encoding="utf-8")
    return path


def stage_copy(source: Path, destination_root: Path, rel: Path) -> None:
    destination = destination_root / rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def backup_existing(source: Path, destination_root: Path, rel: Path) -> None:
    destination = destination_root / rel
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def apply_import(
    bundle_dir: Path,
    target_wiki_root: Path,
    target_pack_dir: Path,
    *,
    durable_conflicts: str = "keep",
    active_memory: str = "stage",
    review_input: Path | None = None,
) -> str:
    manifest = load_bundle_manifest(bundle_dir)
    durable_root = bundle_dir / "durable" / "wiki"
    pack_root = bundle_dir / "pack"
    require_dir(durable_root, "bundle durable wiki")
    require_dir(pack_root, "bundle pack")

    review_decisions = parse_review_input(review_input) if review_input is not None else {"durable_conflicts": {}, "new_files": {}, "active_memory": None}
    if review_decisions["active_memory"] is not None:
        active_memory = str(review_decisions["active_memory"])

    target_pack_dir.mkdir(parents=True, exist_ok=True)
    target_wiki_root.mkdir(parents=True, exist_ok=True)

    copied = 0
    overwritten = 0
    collisions: list[str] = []
    staged_conflicts = 0
    active_memory_staged = 0
    stage_root = target_pack_dir / ".daos" / "portability-stage"
    backup_root = target_pack_dir / ".daos" / "portability-backups" / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    for item in durable_root.rglob("*"):
        if item.is_dir():
            continue
        rel = item.relative_to(durable_root)
        rel_str = durable_rel_key(rel)
        target = target_wiki_root / rel
        if not target.exists():
            if review_decisions["new_files"].get(rel_str, "import") == "skip":
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)
            copied += 1
            continue
        if target.read_text(encoding="utf-8") != item.read_text(encoding="utf-8"):
            collisions.append(rel_str)
            action = review_decisions["durable_conflicts"].get(rel_str, durable_conflicts)
            if action == "stage":
                stage_copy(item, stage_root / "durable-conflicts", rel)
                staged_conflicts += 1
                continue
            if action == "overwrite":
                backup_existing(target, backup_root / "durable-wiki", rel)
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
                overwritten += 1
                continue
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item, target)
        copied += 1

    shutil.copy2(pack_root / PACK_MANIFEST, target_pack_dir / PACK_MANIFEST)
    managed_manifest = pack_root / ".daos" / "manifest.json"
    managed_target = target_pack_dir / ".daos"
    managed_target.mkdir(parents=True, exist_ok=True)
    if managed_manifest.is_file():
        shutil.copy2(managed_manifest, managed_target / "manifest.json")
    else:
        generated_manifest = {
            "imported_at": iso_now(),
            "bundle_version": manifest["bundle_version"],
            "pack_id": manifest["pack_id"],
            "schema_version": manifest["schema_version"],
            "framework_version": manifest["framework_version"],
        }
        (managed_target / "manifest.json").write_text(json.dumps(generated_manifest, indent=2) + "\n", encoding="utf-8")

    active_root = bundle_dir / "active"
    if manifest["payload"]["active_memory"]["included"] and active_memory == "stage":
        if active_root.is_dir():
            active_memory_staged = copy_tree_contents(active_root, stage_root / "active-memory")
        else:
            raise ValueError(f"bundle manifest says active memory is included but active payload is missing: {active_root}")

    lines = [f"DAOS portability apply: {bundle_dir}", f"copied durable wiki files: {copied}", "restored pack metadata anchors"]
    if review_input is not None:
        lines.append(f"review-driven apply: {review_input}")
        conflict_actions = set(review_decisions["durable_conflicts"].values())
        if len(conflict_actions) == 1:
            lines.append(f"durable-conflicts: {next(iter(conflict_actions))}")
        elif conflict_actions:
            lines.append("durable-conflicts: mixed")
        else:
            lines.append(f"durable-conflicts: {durable_conflicts}")
        new_file_actions = set(review_decisions["new_files"].values())
        if new_file_actions == {"skip"}:
            lines.append("new-files: skip")
        elif "skip" in new_file_actions:
            lines.append("new-files: selective")
        elif new_file_actions == {"import"}:
            lines.append("new-files: import")
        lines.append(f"active-memory: {active_memory}")
    if collisions and all(review_decisions["durable_conflicts"].get(item, durable_conflicts) == "keep" for item in collisions):
        review = write_collision_review(target_pack_dir, collisions)
        lines.append(f"collision review: {review}")
    elif collisions and any(review_decisions["durable_conflicts"].get(item, durable_conflicts) == "keep" for item in collisions):
        keep_collisions = [item for item in collisions if review_decisions["durable_conflicts"].get(item, durable_conflicts) == "keep"]
        review = write_collision_review(target_pack_dir, keep_collisions)
        lines.append(f"collision review: {review}")
    if staged_conflicts:
        lines.append(f"staged incoming durable conflicts: {staged_conflicts}")
    if overwritten:
        lines.append(f"overwrote durable wiki conflicts: {overwritten}")
        lines.append(f"conflict backups: {backup_root}")
    if manifest["payload"]["active_memory"]["included"]:
        if active_memory == "stage":
            lines.append(f"active-memory stage: {stage_root / 'active-memory'} ({active_memory_staged} files)")
        else:
            lines.append("active-memory payload skipped")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.command == "export":
            print(export_bundle(args))
            return 0
        if args.command == "inspect":
            print(inspect_bundle(Path(args.bundle_dir).expanduser().resolve()))
            return 0
        if args.command == "plan":
            target_pack_dir = Path(args.target_pack_dir).expanduser().resolve() if args.target_pack_dir else None
            review_output = Path(args.review_output).expanduser().resolve() if args.review_output else None
            print(plan_import(
                Path(args.bundle_dir).expanduser().resolve(),
                Path(args.target_wiki_root).expanduser().resolve(),
                target_pack_dir,
                review_output,
            ))
            return 0
        if args.command == "apply":
            review_input = Path(args.review_input).expanduser().resolve() if args.review_input else None
            print(apply_import(
                Path(args.bundle_dir).expanduser().resolve(),
                Path(args.target_wiki_root).expanduser().resolve(),
                Path(args.target_pack_dir).expanduser().resolve(),
                durable_conflicts=args.durable_conflicts,
                active_memory=args.active_memory,
                review_input=review_input,
            ))
            return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"ERROR: Unsupported command: {args.command}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
