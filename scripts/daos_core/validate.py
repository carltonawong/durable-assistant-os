from __future__ import annotations

import json
from dataclasses import dataclass, field
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
LANE_REQUIRED_LABELS = (
    "- Status:",
    "- Foreground:",
    "- Pressure:",
    "- Short note:",
)
EXPECTED_SCHEMA_VERSION = "1"


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


def read_text(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def has_filled_label(lines: list[str], label: str) -> bool:
    for line in lines:
        if line.startswith(label):
            return bool(line[len(label) :].strip())
    return False


def get_label_value(lines: list[str], label: str) -> str:
    for line in lines:
        if line.startswith(label):
            return line[len(label) :].strip()
    return ""


def collect_lane_sections(lines: list[str]) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_name: str | None = None
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("### Lane: "):
            if current_name is not None:
                sections.append((current_name, current_lines))
            current_name = line[len("### Lane: ") :].strip()
            current_lines = []
            continue

        if current_name is not None:
            if line.startswith("## "):
                sections.append((current_name, current_lines))
                current_name = None
                current_lines = []
            else:
                current_lines.append(line)

    if current_name is not None:
        sections.append((current_name, current_lines))

    return sections


def collect_top_level_lanes(lines: list[str]) -> list[str]:
    lanes: list[str] = []
    in_section = False
    for line in lines:
        if line.startswith("## 2. Top-level lane map"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            lanes.append(line[2:].strip())
    return [lane for lane in lanes if lane]


def validate_manifest(path: Path, result: ValidationResult) -> None:
    if not path.is_file():
        result.warnings.append("daos-pack.json is missing; older packs are still accepted, but generated packs should include it")
        return

    try:
        manifest = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.errors.append(f"daos-pack.json is not valid JSON: {exc}")
        return

    schema_version = str(manifest.get("schema_version", "")).strip()
    if schema_version != EXPECTED_SCHEMA_VERSION:
        result.errors.append(
            f"daos-pack.json has unsupported schema_version: {schema_version or '[missing]'}"
        )


def validate_cadence_review(path: Path, result: ValidationResult) -> None:
    if not path.is_file():
        return

    lines = read_text(path)
    prompts = (
        "- Keep:",
        "- Add:",
        "- Remove:",
    )
    if all(not has_filled_label(lines, prompt) for prompt in prompts):
        result.warnings.append("cadence-review.md looks blank; keep it for later or fill it after real use")


def validate_operating_profile_lints(lines: list[str], lane_sections: list[tuple[str, list[str]]], result: ValidationResult) -> None:
    top_level_lanes = collect_top_level_lanes(lines)
    lane_names = [name for name, _ in lane_sections if name and name != "[name]"]
    unique_lane_names = set(lane_names)

    duplicates = sorted({name for name in lane_names if lane_names.count(name) > 1})
    if duplicates:
        result.warnings.append(
            "operating-profile.md has duplicate lane names: " + ", ".join(duplicates)
        )

    missing_from_map = sorted(unique_lane_names.difference(top_level_lanes))
    if missing_from_map:
        result.warnings.append(
            "operating-profile.md has lane snapshots missing from the top-level lane map: "
            + ", ".join(missing_from_map)
        )

    foreground_yes = 0
    for _, lane_lines in lane_sections:
        if get_label_value(lane_lines, "- Foreground:").lower() == "yes":
            foreground_yes += 1
    if foreground_yes > 3:
        result.warnings.append(
            f"operating-profile.md has more than 3 foreground lanes ({foreground_yes}); the focus set may be overloaded"
        )

    memory_front_door = get_label_value(lines, "- Memory front door:").lower()
    if memory_front_door and all(token not in memory_front_door for token in ("thread", "cache", "continuity", "local")):
        result.warnings.append(
            "operating-profile.md memory front door may be too thin; consider a local thread/cache/continuity front door"
        )


def validate_pack_dir(pack_dir: str | Path) -> ValidationResult:
    root = Path(pack_dir).expanduser().resolve()
    result = ValidationResult()

    if not root.exists():
        result.errors.append(f"Pack directory does not exist: {root}")
        return result
    if not root.is_dir():
        result.errors.append(f"Pack path is not a directory: {root}")
        return result

    validate_manifest(root / "daos-pack.json", result)

    file_contents: dict[str, list[str]] = {}
    for name in REQUIRED_FILES:
        path = root / name
        if not path.is_file():
            result.errors.append(f"Missing required file: {name}")
            continue
        file_contents[name] = read_text(path)

    for filename, labels in REQUIRED_LABELS.items():
        lines = file_contents.get(filename)
        if lines is None:
            continue
        for label in labels:
            if not has_filled_label(lines, label):
                result.errors.append(f"{filename} has an empty required field: {label}")

    operating_lines = file_contents.get("operating-profile.md")
    if operating_lines is not None:
        lane_sections = collect_lane_sections(operating_lines)
        filled_lanes = [
            (name, lines)
            for name, lines in lane_sections
            if name and name != "[name]"
        ]
        if not filled_lanes:
            result.errors.append("operating-profile.md needs at least one filled lane section")
        for lane_name, lane_lines in filled_lanes:
            for label in LANE_REQUIRED_LABELS:
                if not has_filled_label(lane_lines, label):
                    result.errors.append(
                        f"operating-profile.md lane '{lane_name}' has an empty required field: {label}"
                    )
        validate_operating_profile_lints(operating_lines, filled_lanes, result)

    validate_cadence_review(root / "cadence-review.md", result)
    return result
