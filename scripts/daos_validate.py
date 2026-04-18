#!/usr/bin/env python3
"""Validate whether a DAOS pack is minimally filled enough to operate."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


REQUIRED_FILES = ("assistant-charter.md", "operating-profile.md")
REQUIRED_LABELS = {
    "assistant-charter.md": (
        "- Primary outcome:",
        "- Primary failure mode:",
        "- Default uncertainty behavior:",
        "- Low-stakes reversible actions that can proceed:",
        "- Actions that always require approval:",
        "- Desired feel in daily use:",
    ),
    "operating-profile.md": (
        "- Primary outcome:",
        "- Primary failure mode:",
        "- Uncertainty behavior:",
        "- Safety / approval boundary:",
        "- Master list source:",
        "- Memory front door:",
        "- Durable memory home:",
        "- Ask-vs-act rule:",
        "- Escalation / approval rule:",
    ),
}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check whether a DAOS pack is minimally filled enough to operate."
    )
    parser.add_argument("pack_dir", help="Path to a DAOS pack directory to validate")
    return parser.parse_args(argv)


def read_text(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def has_filled_label(lines: list[str], label: str) -> bool:
    for line in lines:
        if line.startswith(label):
            return bool(line[len(label) :].strip())
    return False


def validate_pack(pack_dir: str | Path) -> list[str]:
    root = Path(pack_dir).expanduser().resolve()
    issues: list[str] = []

    if not root.exists():
        return [f"Pack directory does not exist: {root}"]
    if not root.is_dir():
        return [f"Pack path is not a directory: {root}"]

    file_contents: dict[str, list[str]] = {}
    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file():
            issues.append(f"Missing required file: {name}")
            continue
        file_contents[name] = read_text(path)

    for filename, labels in REQUIRED_LABELS.items():
        lines = file_contents.get(filename)
        if lines is None:
            continue
        for label in labels:
            if not has_filled_label(lines, label):
                issues.append(f"{filename} has an empty required field: {label}")

    operating_lines = file_contents.get("operating-profile.md")
    if operating_lines is not None and not any(line.startswith("### Lane: ") and not line.endswith("[name]") for line in operating_lines):
        issues.append("operating-profile.md needs at least one filled lane section")

    return issues


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    issues = validate_pack(args.pack_dir)
    pack_dir = Path(args.pack_dir).expanduser().resolve()

    if issues:
        print(f"DAOS pack validation failed: {pack_dir}", file=sys.stderr)
        for issue in issues:
            print(f"- {issue}", file=sys.stderr)
        return 1

    print(f"DAOS pack validation passed: {pack_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
