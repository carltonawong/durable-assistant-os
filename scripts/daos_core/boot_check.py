from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .validate import validate_pack_dir


@dataclass
class BootCheckResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    sections: dict[str, list[str]] = field(default_factory=dict)


def _read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("runtime config must be a JSON object")
    return data


def _as_path(value: object) -> Path | None:
    if not isinstance(value, str) or not value.strip():
        return None
    return Path(value).expanduser().resolve()


def _is_relative_to(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def _lower_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip().lower() for item in value if str(item).strip()]


def _bool_from(mapping: dict[str, Any], key: str) -> bool | None:
    value = mapping.get(key)
    return value if isinstance(value, bool) else None


def _hot_cache_updated_line(root: Path) -> str:
    hot_cache = root / "wiki" / "cache" / "hot-cache.md"
    if not hot_cache.is_file():
        return "missing"
    for line in hot_cache.read_text(encoding="utf-8").splitlines():
        if line.startswith("**Updated:**"):
            value = line.split(":**", 1)[-1].strip() if ":**" in line else line.replace("**Updated:**", "").strip()
            return value or "blank"
    return "missing Updated field"


def run_boot_check(pack_dir: str | Path, runtime_config: str | Path | None = None) -> tuple[int, str, str]:
    """Read-only DAOS boot-order/runtime hierarchy check.

    The check is generic first: it verifies installed DAOS structure, then consumes
    an optional synthetic/runtime-exported JSON fixture for adapter-specific boot
    facts. It does not modify files or call external services.
    """
    root = Path(pack_dir).expanduser().resolve()
    result = BootCheckResult()

    validation = validate_pack_dir(root)
    structure_lines: list[str] = []
    if validation.errors:
        result.errors.extend(validation.errors)
        structure_lines.append(f"pack validation errors: {len(validation.errors)}")
    else:
        structure_lines.append("DAOS pack structure validates")
    if validation.warnings:
        result.warnings.extend(validation.warnings)
        structure_lines.append(f"pack validation warnings: {len(validation.warnings)}")
    else:
        structure_lines.append("pack validation warnings: 0")
    result.sections["Installed Structure"] = structure_lines

    runtime: dict[str, Any] = {}
    if runtime_config:
        config_path = Path(runtime_config).expanduser().resolve()
        try:
            runtime = _read_json(config_path)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            result.errors.append(f"runtime config could not be read: {exc}")
        else:
            result.sections.setdefault("Installed Structure", []).append(f"runtime config: {config_path}")
    else:
        result.warnings.append("runtime boot order is unverified; pass --runtime-config for adapter-specific checks")
        result.sections.setdefault("Installed Structure", []).append("runtime config: not provided")

    startup_lines: list[str] = []
    startup_root = _as_path(runtime.get("startup_root")) if runtime else None
    declared_home = _as_path(runtime.get("daos_home")) if runtime else None
    if runtime:
        if startup_root is None:
            result.warnings.append("runtime config has no startup_root")
            startup_lines.append("startup_root: missing")
        elif _is_relative_to(startup_root, root) or startup_root == root:
            startup_lines.append(f"startup_root: inside DAOS pack/home ({startup_root})")
        else:
            result.errors.append("startup root is outside the DAOS pack/home")
            startup_lines.append(f"startup_root: outside DAOS pack/home ({startup_root})")
        if declared_home is None:
            result.warnings.append("runtime config has no daos_home")
            startup_lines.append("daos_home: missing")
        elif declared_home != root:
            result.warnings.append("runtime daos_home does not match the checked pack")
            startup_lines.append(f"daos_home: {declared_home} (checked pack: {root})")
        else:
            startup_lines.append(f"daos_home: matches checked pack ({root})")
    else:
        startup_lines.append("not checked without runtime config")
    result.sections["Startup Root"] = startup_lines

    precedence_lines: list[str] = []
    precedence = _lower_list(runtime.get("prompt_precedence")) if runtime else []
    if precedence:
        precedence_lines.append("order: " + " -> ".join(precedence))
        private_positions = [i for i, name in enumerate(precedence) if "private" in name or name in {"memory", "user_profile", "runtime_memory"}]
        daos_positions = [i for i, name in enumerate(precedence) if "daos" in name or "hot_cache" in name or "project" in name]
        if private_positions and daos_positions and min(private_positions) < min(daos_positions):
            result.errors.append("private runtime memory appears before DAOS/project context")
        if not daos_positions:
            result.errors.append("prompt precedence does not include DAOS/project/hot-cache context")
    elif runtime:
        result.warnings.append("runtime config has no prompt_precedence list")
        precedence_lines.append("order: missing")
    else:
        precedence_lines.append("not checked without runtime config")
    result.sections["Prompt/Context Precedence"] = precedence_lines

    topology_lines: list[str] = []
    topology = runtime.get("session_topology") if runtime else None
    if isinstance(topology, dict):
        shared_expected = _bool_from(topology, "shared_collaboration_lanes")
        split_per_user = _bool_from(topology, "group_sessions_per_user")
        topology_lines.append(f"shared_collaboration_lanes: {shared_expected}")
        topology_lines.append(f"group_sessions_per_user: {split_per_user}")
        if shared_expected is True and split_per_user is True:
            result.errors.append("group sessions are split per user while shared DAOS lanes are expected")
    elif runtime:
        result.warnings.append("runtime config has no session_topology object")
        topology_lines.append("session_topology: missing")
    else:
        topology_lines.append("not checked without runtime config")
    result.sections["Session Topology"] = topology_lines

    handoff_lines: list[str] = []
    handoff = runtime.get("reset_handoff") if runtime else None
    if isinstance(handoff, dict):
        enabled = _bool_from(handoff, "enabled")
        reads_reset = _bool_from(handoff, "reads_reset_handoff")
        reads_hot = _bool_from(handoff, "reads_hot_cache")
        handoff_lines.append(f"enabled: {enabled}")
        handoff_lines.append(f"reads_reset_handoff: {reads_reset}")
        handoff_lines.append(f"reads_hot_cache: {reads_hot}")
        if enabled is not True:
            result.errors.append("reset/handoff hook is not enabled")
        if reads_reset is not True:
            result.errors.append("reset/handoff hook does not read reset-handoff.md")
        if reads_hot is not True:
            result.warnings.append("reset/handoff hook does not read hot-cache.md")
    elif runtime:
        result.warnings.append("runtime config has no reset_handoff object")
        handoff_lines.append("reset_handoff: missing")
    else:
        handoff_lines.append("not checked without runtime config")
    result.sections["Reset/Handoff Wiring"] = handoff_lines

    cache_lines = [f"hot-cache Updated: {_hot_cache_updated_line(root)}"]
    hot_cache = root / "wiki" / "cache" / "hot-cache.md"
    if hot_cache.is_file():
        age_hours = (datetime.now(timezone.utc).timestamp() - hot_cache.stat().st_mtime) / 3600
        cache_lines.append(f"hot-cache file age hours: {age_hours:.1f}")
        if age_hours > 72:
            result.warnings.append("hot-cache.md file timestamp is older than 72 hours")
    else:
        result.errors.append("wiki/cache/hot-cache.md is missing")
    result.sections["Cache Freshness"] = cache_lines

    failed = bool(result.errors)
    lines = [f"DAOS boot check {'failed' if failed else 'passed'}: {root}", f"errors: {len(result.errors)}", f"warnings: {len(result.warnings)}"]
    for heading, items in result.sections.items():
        lines.extend(["", heading])
        lines.extend(f"- {item}" for item in items)
    if result.errors:
        lines.extend(["", "errors"])
        lines.extend(f"- {error}" for error in result.errors)
    if result.warnings:
        lines.extend(["", "warnings"])
        lines.extend(f"- {warning}" for warning in result.warnings)
    lines.extend(["", "next moves:"])
    if failed:
        lines.append("- fix startup root, context precedence, session topology, or reset wiring before trusting this runtime as DAOS-first")
    elif runtime:
        lines.append("- runtime fixture is DAOS-first enough for this read-only gate; still verify live behavior after adapter changes")
    else:
        lines.append("- export or write a runtime config fixture to verify boot order beyond installed structure")
    return (1 if failed else 0), "\n".join(lines) + "\n", ""
