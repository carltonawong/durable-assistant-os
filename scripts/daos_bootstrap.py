#!/usr/bin/env python3
"""Bootstrap a DAOS starter workspace by copying a scaffold into a target directory."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BLANK_SOURCE = REPO_ROOT / "starter-pack"
FILLED_SOURCE = REPO_ROOT / "examples" / "starter-pack-example"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a DAOS starter workspace by copying either the blank starter-pack "
            "or the filled starter-pack example into a target directory."
        )
    )
    parser.add_argument("output_dir", help="Destination directory to create or replace")
    parser.add_argument(
        "--filled-example",
        action="store_true",
        help="Copy examples/starter-pack-example instead of the blank starter-pack scaffold",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing non-empty destination directory",
    )
    return parser.parse_args(argv)


def source_dir(use_filled_example: bool) -> Path:
    source = FILLED_SOURCE if use_filled_example else BLANK_SOURCE
    if not source.is_dir():
        raise FileNotFoundError(f"Source scaffold does not exist: {source}")
    return source


def validate_destination(destination: Path, force: bool) -> None:
    if destination.exists() and destination.is_file():
        raise ValueError(f"Destination exists as a file, not a directory: {destination}")

    if destination.is_dir() and any(destination.iterdir()) and not force:
        raise ValueError(
            f"Destination already exists and is not empty: {destination}. "
            "Use --force to replace it."
        )


def copy_tree(source: Path, destination: Path, force: bool) -> None:
    validate_destination(destination, force)

    if destination.is_dir() and force:
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)


def bootstrap(output_dir: str | Path, *, use_filled_example: bool = False, force: bool = False) -> Path:
    destination = Path(output_dir).expanduser().resolve()
    source = source_dir(use_filled_example)
    copy_tree(source, destination, force)
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
