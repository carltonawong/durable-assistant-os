from __future__ import annotations

from pathlib import Path

from .validate import validate_pack_dir


def _presence_line(root: Path, relative_path: str) -> str:
    path = root / relative_path
    status = "present" if path.is_file() else "missing"
    return f"- `{relative_path}`: {status}"


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
