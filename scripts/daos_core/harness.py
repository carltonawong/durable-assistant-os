from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .validate import validate_pack_dir


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _label_value(text: str, label: str) -> str:
    for line in text.splitlines():
        if line.startswith(label):
            return line[len(label) :].strip()
    return ""


def _presence_line(root: Path, relative_path: str) -> str:
    path = root / relative_path
    status = "present" if path.is_file() else "missing"
    return f"- `{relative_path}`: {status}"


def _surface_status(root: Path, relative_path: str, *, directory: bool = False) -> str:
    path = root / relative_path
    if directory:
        status = "present" if path.is_dir() else "missing"
    else:
        status = "present" if path.is_file() else "missing"
    return f"{relative_path}: {status}"


def build_orientation_bundle(pack_dir: str | Path, task: str | None = None) -> tuple[int, str, str]:
    """Build a deterministic DAOS orientation bundle.

    Returns (exit_code, stdout, stderr). This command is read-only and does not call an LLM.
    """
    root = Path(pack_dir).expanduser().resolve()
    validation = validate_pack_dir(root)
    if validation.errors:
        lines = [f"DAOS orient failed: {root}", f"errors: {len(validation.errors)}"]
        lines.extend(f"- {error}" for error in validation.errors)
        return 1, "", "\n".join(lines) + "\n"

    task_line = task.strip() if task and task.strip() else "[not provided]"
    lines = [
        "# DAOS Orientation Bundle",
        "",
        f"Pack: {root}",
        f"Current task: {task_line}",
        "",
        "## Read order",
        "1. Local thread / current user request",
        "2. `wiki/cache/hot-cache.md`",
        "3. `wiki/cache/reset-handoff.md` when resuming after reset, idle, or handoff",
        "4. `wiki/cache/agent-continuity.md` only if still unresolved",
        "5. Durable wiki pages / source notes relevant to the task",
        "6. Verified live reality: repo files, config, runtime state, external systems",
        "",
        "## Core operating files",
        _presence_line(root, "assistant-charter.md"),
        _presence_line(root, "operating-profile.md"),
        _presence_line(root, "wiki/WIKI.md"),
        _presence_line(root, "wiki/index.md"),
        "",
        "## Active memory surfaces",
        _presence_line(root, "wiki/cache/hot-cache.md"),
        _presence_line(root, "wiki/cache/reset-handoff.md"),
        _presence_line(root, "wiki/cache/agent-continuity.md"),
        "",
        "## Required stance",
        "- Verify live reality before acting on stale memory.",
        "- Treat memory as orientation, not proof of current truth.",
        "- Ask only when ambiguity changes the action or approval boundary.",
    ]

    if validation.warnings:
        lines.extend(["", "## Validation notes", f"validation warnings: {len(validation.warnings)}"])
        lines.extend(f"- {warning}" for warning in validation.warnings)

    return 0, "\n".join(lines) + "\n", ""


def run_reset_recovery_test(pack_dir: str | Path) -> tuple[int, str, str]:
    """Run a deterministic reset-recovery proof check.

    Returns (exit_code, stdout, stderr). This is read-only and does not call an LLM.
    """
    root = Path(pack_dir).expanduser().resolve()
    validation = validate_pack_dir(root)
    failures: list[str] = []

    if validation.errors:
        failures.extend(validation.errors)

    hot_cache = root / "wiki" / "cache" / "hot-cache.md"
    reset_handoff = root / "wiki" / "cache" / "reset-handoff.md"
    wiki = root / "wiki" / "WIKI.md"
    agents = root / "AGENTS.md"

    hot_cache_text = ""
    if not hot_cache.is_file():
        failures.append("wiki/cache/hot-cache.md is missing")
    else:
        hot_cache_text = _read_text(hot_cache)
        if "**Updated:**" not in hot_cache_text:
            failures.append("hot-cache.md has no Updated field")
        if "## Current Focus" not in hot_cache_text:
            failures.append("hot-cache.md has no Current Focus section")

    reset_text = ""
    exact_next_move = ""
    first_verification = ""
    if not reset_handoff.is_file():
        failures.append("wiki/cache/reset-handoff.md is missing")
    else:
        reset_text = _read_text(reset_handoff)
        exact_next_move = _label_value(reset_text, "- Exact next move:")
        first_verification = _label_value(reset_text, "- First verification:")
        if not exact_next_move:
            failures.append("reset-handoff.md has no filled Exact next move")
        if not first_verification:
            failures.append("reset-handoff.md has no filled First verification")

    doctrine_text = ""
    for path in (agents, wiki):
        if path.is_file():
            doctrine_text += "\n" + _read_text(path)
    doctrine_lower = doctrine_text.lower()
    if "local thread" not in doctrine_lower or "hot-cache.md" not in doctrine_lower:
        failures.append("baseline doctrine does not state the reset read order")
    if "verified" not in doctrine_lower or "reality" not in doctrine_lower or "memory" not in doctrine_lower:
        failures.append("baseline doctrine does not state live reality over memory")

    if failures:
        lines = [f"DAOS reset test failed: {root}", f"failed checks: {len(failures)}"]
        lines.extend(f"- {failure}" for failure in failures)
        return 1, "", "\n".join(lines) + "\n"

    output = [
        f"DAOS reset test passed: {root}",
        "checks: passed",
        "fresh-session resume summary:",
        "- orientation source: wiki/cache/hot-cache.md",
        "- reset source: wiki/cache/reset-handoff.md",
        f"- exact next move: {exact_next_move}",
        f"- first verification: {first_verification}",
        "- rule: Verify live reality before acting on stale memory.",
    ]
    if validation.warnings:
        output.extend([f"validation warnings: {len(validation.warnings)}"])
        output.extend(f"- {warning}" for warning in validation.warnings)
    return 0, "\n".join(output) + "\n", ""


def write_reset_handoff(
    pack_dir: str | Path,
    *,
    lane: str,
    status: str,
    why: str,
    next_move: str,
    verify: str,
) -> tuple[int, str, str]:
    root = Path(pack_dir).expanduser().resolve()
    required_values = {
        "--lane": lane,
        "--status": status,
        "--why": why,
        "--next": next_move,
        "--verify": verify,
    }
    blank = [name for name, value in required_values.items() if not value.strip()]
    if blank:
        return 1, "", f"DAOS handoff failed: {blank[0]} must not be blank\n"

    if not root.is_dir():
        return 1, "", f"DAOS handoff failed: pack directory does not exist: {root}\n"
    if not (root / "assistant-charter.md").is_file() or not (root / "operating-profile.md").is_file():
        return 1, "", f"DAOS handoff failed: {root} does not look like a DAOS pack\n"

    cache_dir = root / "wiki" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    handoff_path = cache_dir / "reset-handoff.md"
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    content = f"""# Reset Handoff

Use this as the named DAOS reset/wake-up continuity artifact.

Read it when the current thread is not enough after reset or long idle.

If anything here conflicts with verified files, runtime state, or durable wiki pages, verify first and prefer reality.

## Current Handoff
**Last updated:** {timestamp}  
**Updated by:** DAOS CLI  
**Lane:** {lane.strip()}  
**Status:** {status.strip()}

- Why this handoff exists: {why.strip()}
- Exact next move: {next_move.strip()}
- First verification: {verify.strip()}
- If stale or contradicted: Re-read the current thread, hot cache, and verified files before continuing.

## Editing rules
- overwrite instead of append
- keep one resumable handoff, not a diary
- point to durable notes instead of duplicating them
- clear or rewrite when the exact handoff changes
"""
    handoff_path.write_text(content, encoding="utf-8")
    return 0, f"DAOS handoff written: {handoff_path}\n", ""


def audit_memory_surfaces(pack_dir: str | Path) -> tuple[int, str, str]:
    root = Path(pack_dir).expanduser().resolve()
    validation = validate_pack_dir(root)
    if any(error.startswith("Pack directory does not exist") or error.startswith("Pack path is not a directory") for error in validation.errors):
        lines = [f"DAOS memory audit failed: {root}"]
        lines.extend(f"- {error}" for error in validation.errors)
        return 1, "", "\n".join(lines) + "\n"

    file_surfaces = [
        "wiki/cache/hot-cache.md",
        "wiki/cache/hot-cache-log.md",
        "wiki/cache/reset-handoff.md",
        "wiki/cache/agent-continuity.md",
        "wiki/index.md",
        "wiki/log.md",
        "wiki/WIKI.md",
    ]
    directory_surfaces = ["wiki/raw", "wiki/sources"]
    warnings: list[str] = []
    lines = [f"DAOS memory audit: {root}", "", "surfaces:"]

    for surface in file_surfaces:
        status = _surface_status(root, surface)
        lines.append(f"- {status}")
        if status.endswith("missing"):
            warnings.append(f"{surface} is missing")

    for surface in directory_surfaces:
        display = surface + "/"
        status = _surface_status(root, surface, directory=True)
        lines.append(f"- {display}: {status.rsplit(': ', 1)[1]}")
        if status.endswith("missing"):
            warnings.append(f"{display} is missing")

    hot_cache = root / "wiki" / "cache" / "hot-cache.md"
    if hot_cache.is_file():
        text = _read_text(hot_cache)
        if "**Updated:**" not in text:
            warnings.append("hot-cache.md has no Updated field")
        if "## Current Focus" not in text:
            warnings.append("hot-cache.md has no Current Focus section")

    reset_handoff = root / "wiki" / "cache" / "reset-handoff.md"
    if reset_handoff.is_file():
        text = _read_text(reset_handoff)
        if not _label_value(text, "- Exact next move:"):
            warnings.append("reset-handoff.md has no filled Exact next move")
        if not _label_value(text, "- First verification:"):
            warnings.append("reset-handoff.md has no filled First verification")

    raw_dir = root / "wiki" / "raw"
    source_dir = root / "wiki" / "sources"
    if raw_dir.is_dir():
        raw_notes = [path for path in raw_dir.rglob("*") if path.is_file() and path.name != "README.md"]
        lines.append(f"raw notes beyond README: {len(raw_notes)}")
    if source_dir.is_dir():
        source_notes = [path for path in source_dir.rglob("*") if path.is_file() and path.name != "README.md"]
        lines.append(f"source notes beyond README: {len(source_notes)}")

    lines.extend(["", f"warnings: {len(warnings)}"])
    lines.extend(f"- {warning}" for warning in warnings)
    return 0, "\n".join(lines) + "\n", ""
