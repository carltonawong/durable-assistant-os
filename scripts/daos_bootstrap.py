#!/usr/bin/env python3
"""Bootstrap a DAOS starter workspace by writing a schema-backed pack into a target directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

from daos_core import blank_starter_pack, filled_example_pack, write_pack_core_files


REPO_ROOT = Path(__file__).resolve().parents[1]
BLANK_SOURCE = REPO_ROOT / "starter-pack"
FILLED_SOURCE = REPO_ROOT / "examples" / "starter-pack-example"
DAOS_MARKER_FILES = ("assistant-charter.md", "operating-profile.md")
CORE_GENERATED_FILES = {"assistant-charter.md", "operating-profile.md", "daos-pack.json"}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a DAOS starter workspace by generating either the blank starter-pack "
            "or the filled starter-pack example into a target directory."
        )
    )
    parser.add_argument("output_dir", help="Destination directory to create or replace")
    parser.add_argument(
        "--filled-example",
        action="store_true",
        help="Generate the filled starter-pack example instead of the blank starter-pack scaffold",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing non-empty destination directory if it already looks like a DAOS pack",
    )
    return parser.parse_args(argv)


def source_dir(use_filled_example: bool) -> Path:
    source = FILLED_SOURCE if use_filled_example else BLANK_SOURCE
    if not source.is_dir():
        raise FileNotFoundError(f"Source scaffold does not exist: {source}")
    return source


def is_daos_directory(path: Path) -> bool:
    return path.is_dir() and all((path / marker).exists() for marker in DAOS_MARKER_FILES)


def validate_destination(destination: Path, force: bool) -> None:
    if destination.exists() and destination.is_file():
        raise ValueError(f"Destination exists as a file, not a directory: {destination}")

    if destination.is_dir() and any(destination.iterdir()):
        if not force:
            raise ValueError(
                f"Destination already exists and is not empty: {destination}. "
                "Use --force to replace it."
            )
        if not is_daos_directory(destination):
            raise ValueError(
                f"Destination already exists and is not empty: {destination}; "
                "refusing to delete a non-DAOS directory with --force."
            )


def clear_destination(destination: Path, force: bool) -> None:
    validate_destination(destination, force)
    if destination.is_dir() and force:
        shutil.rmtree(destination)


def copy_support_files(source: Path, destination: Path) -> None:
    for item in source.iterdir():
        if item.name in CORE_GENERATED_FILES:
            continue
        target = destination / item.name
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        if item.is_dir():
            shutil.copytree(item, target)
        else:
            shutil.copy2(item, target)


def bootstrap(output_dir: str | Path, *, use_filled_example: bool = False, force: bool = False) -> Path:
    destination = Path(output_dir).expanduser().resolve()
    source = source_dir(use_filled_example)
    clear_destination(destination, force)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir(parents=True, exist_ok=True)

    pack = (
        filled_example_pack(generator="scripts/daos_bootstrap.py")
        if use_filled_example
        else blank_starter_pack(generator="scripts/daos_bootstrap.py")
    )
    write_pack_core_files(destination, pack)
    copy_support_files(BLANK_SOURCE, destination)
    if use_filled_example:
        copy_support_files(source, destination)
    return destination


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    try:
        destination = bootstrap(
            args.output_dir,
            use_filled_example=args.filled_example,
            force=args.force,
        )
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    source_label = "filled starter-pack example" if args.filled_example else "blank starter-pack"
    print(f"Created DAOS workspace from {source_label}: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
