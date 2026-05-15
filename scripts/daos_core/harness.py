from __future__ import annotations

from datetime import datetime
import hashlib
import json
import os
from pathlib import Path

from .validate import validate_pack_dir

INSTRUCTION_CARRIER_PATTERNS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "HERMES.md",
    "OPENCLAW.md",
    "QUINN.md",
    ".cursorrules",
    ".github/copilot-instructions.md",
    ".hermes/AGENTS.md",
    ".hermes/instructions.md",
    ".openclaw/AGENTS.md",
    ".openclaw/instructions.md",
)

DAOS_COEXISTENCE_BLOCK = """## DAOS coexistence rule

This agent may keep using private/local/session memory for local recall and agent-specific behavior.

For cross-agent or cross-tool continuity, use the DAOS wiki/cache system as the shared continuity layer.

Private memory can orient this agent, but DAOS is the shared continuity layer for the ecosystem.

Current verified reality outranks all memory.
"""

PLACEHOLDER_MARKERS = (
    "Fill with the current shared foreground lane.",
    "Fill with compact Current Focus entries only.",
    "Format: `[Name] -",
    "Prune stale entries after durable state exists",
    "Keep this as the front door only.",
    "If it feels incongruent, check `hot-cache-log.md`.",
    "Record only important current corrections.",
    "Remove stale corrections when superseded.",
    "Do not turn this into a change diary.",
    "Newest meaningful entries stay at the top.",
    "Use this for fallback reconstruction",
    "Recurring hygiene should prune obvious log bloat.",
    "YYYY-MM-DD",
    "[lane]",
    "empty | fresh | stale | blocked",
    "uncertain | resumable | blocked",
    "Last meaningful lane:",
    "Last meaningful focus item:",
    "Current verified takeaway:",
    "Next resumable move and what to verify first:",
)


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



def _section_bullets(text: str, heading: str) -> list[str]:
    bullets: list[str] = []
    in_section = False
    for line in text.splitlines():
        if line.strip() == heading:
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if in_section and line.startswith("- "):
            bullets.append(line)
    return bullets


def _recent_log_entries(text: str, limit: int = 3) -> list[str]:
    entries: list[str] = []
    current_header = ""
    for line in text.splitlines():
        if line.startswith("## "):
            current_header = line[3:].strip()
            continue
        if current_header and line.startswith("- "):
            entry = f"[{current_header}] {line[2:].strip()}"
            if _looks_placeholder_text(entry):
                continue
            entries.append(entry)
            if len(entries) >= limit:
                break
    return entries


def _count_report_section_items(scan_report: Path, heading: str) -> int:
    if not scan_report.is_file():
        return 0
    items = _section_bullets(_read_text(scan_report), heading)
    return len([line for line in items if line != "- none"])


def _count_instruction_carriers(scan_report: Path) -> int:
    return _count_report_section_items(scan_report, "## Instruction carriers found")


def _find_instruction_carriers(scan_root: Path) -> list[Path]:
    found: list[Path] = []
    if not scan_root.exists():
        return found
    if scan_root.is_file():
        return [scan_root] if scan_root.name in {Path(pattern).name for pattern in INSTRUCTION_CARRIER_PATTERNS} else []
    for pattern in INSTRUCTION_CARRIER_PATTERNS:
        candidate = scan_root / pattern
        if candidate.is_file():
            found.append(candidate)
    cursor_rules = scan_root / ".cursor" / "rules"
    if cursor_rules.is_dir():
        found.extend(sorted(path for path in cursor_rules.rglob("*") if path.is_file()))
    return sorted(set(found))


def find_instruction_carriers(scan_paths: list[Path]) -> list[Path]:
    carriers: list[Path] = []
    for scan_path in scan_paths:
        carriers.extend(_find_instruction_carriers(scan_path))
    return sorted(set(carriers))


def instruction_carrier_needs_daos_rule(path: Path) -> bool:
    if not path.is_file():
        return False
    return "DAOS coexistence rule" not in _read_text(path)


def _backup_instruction_carrier(path: Path, backup_root: Path) -> Path:
    backup_root.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha1(str(path).encode("utf-8")).hexdigest()[:10]
    backup_path = backup_root / f"{path.name}.{digest}.bak"
    backup_path.write_text(_read_text(path), encoding="utf-8")
    return backup_path


def prepend_daos_coexistence_rule(path: Path, backup_root: Path | None = None) -> Path | None:
    """Prepend the DAOS coexistence rule after explicit approval.

    Returns the backup path when the file changed. This function does not ask for
    approval; callers are responsible for collecting approval before calling it.
    """
    current = _read_text(path)
    if "DAOS coexistence rule" in current:
        return None
    backup_path = _backup_instruction_carrier(path, backup_root) if backup_root else None
    path.write_text(DAOS_COEXISTENCE_BLOCK.rstrip() + "\n\n" + current, encoding="utf-8")
    return backup_path


def write_instruction_scan_report(
    pack_dir: str | Path,
    scan_paths: list[Path],
    applied_paths: list[Path] | None = None,
    backup_paths: dict[Path, Path] | None = None,
) -> Path:
    root = Path(pack_dir).expanduser().resolve()
    report_dir = root / "import-stage"
    report_dir.mkdir(parents=True, exist_ok=True)
    report_path = report_dir / "instruction-scan.md"

    carriers = find_instruction_carriers(scan_paths)
    applied = sorted(set(applied_paths or []))
    backups = backup_paths or {}
    unapplied = [path for path in carriers if path not in applied and instruction_carrier_needs_daos_rule(path)]
    already_aligned = [path for path in carriers if path not in applied and not instruction_carrier_needs_daos_rule(path)]

    lines = [
        "# DAOS Instruction Scan",
        "",
        "DAOS always installs the mandatory wiki/cache baseline. Existing agent-private memory can remain in place.",
        "",
        "DAOS coexistence rule should be placed at the top/front of existing instruction carriers before older private-memory rules.",
        "",
        "## Scan roots",
    ]
    lines.extend(f"- {path}" for path in scan_paths)
    lines.extend(["", "## Instruction carriers found"])
    if carriers:
        lines.extend(f"- {path}" for path in carriers)
    else:
        lines.append("- none")
    lines.extend(["", "## Edits applied"])
    if applied:
        for path in applied:
            backup = backups.get(path)
            if backup:
                lines.append(f"- prepended DAOS coexistence rule to `{path}`; backup: `{backup}`")
            else:
                lines.append(f"- prepended DAOS coexistence rule to `{path}`")
    else:
        lines.append("- none")
    lines.extend(["", "## Edits needing approval"])
    if unapplied:
        lines.extend(f"- prepend DAOS coexistence rule to `{path}`" for path in unapplied)
    else:
        lines.append("- none")
    if already_aligned:
        lines.extend(["", "## Already aligned"])
        lines.extend(f"- `{path}` already contains DAOS coexistence rule" for path in already_aligned)
    lines.extend(
        [
            "",
            "## Suggested coexistence rule",
            DAOS_COEXISTENCE_BLOCK.rstrip(),
            "",
            "## Safety posture",
            "- no arbitrary old memory content was imported",
            "- instruction files are edited only after explicit approval",
            "- approved instruction edits are backed up under `.daos/backups/instructions/`",
            "- preserve existing private-memory rules below the DAOS coexistence rule",
        ]
    )
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report_path


def _is_placeholder_bullet(line: str) -> bool:
    clean = line[2:].strip() if line.startswith("- ") else line.strip()
    return any(marker in clean for marker in PLACEHOLDER_MARKERS)


def _real_bullets(lines: list[str]) -> list[str]:
    return [line for line in lines if not _is_placeholder_bullet(line)]


def _first_bullet_summary(lines: list[str], fallback: str) -> str:
    real = _real_bullets(lines)
    if not real:
        return fallback
    return real[0][2:].strip() if real[0].startswith("- ") else real[0].strip()


def _agent_continuity_summary(path: Path) -> str:
    if not path.is_file():
        return "agent-continuity.md is missing"
    text = _read_text(path)
    status = _label_value(text, "**Status:**")
    if status and not _looks_placeholder_text(status):
        return status
    bullets = _real_bullets([line for line in text.splitlines() if line.startswith("- ")])
    if bullets:
        return bullets[0][2:].strip()
    return "No agent continuity set yet."


def _looks_placeholder_text(text: str) -> bool:
    return any(marker in text for marker in PLACEHOLDER_MARKERS)


def _compact_validation_errors(errors: list[str]) -> list[str]:
    if not errors:
        return []
    empty_by_file: dict[str, int] = {}
    other: list[str] = []
    for error in errors:
        if " has an empty required field:" in error:
            filename = error.split(" has an empty required field:", 1)[0]
            empty_by_file[filename] = empty_by_file.get(filename, 0) + 1
        else:
            other.append(error)

    compact = [f"{filename} has {count} empty required fields" for filename, count in sorted(empty_by_file.items())]
    compact.extend(other)
    return compact


def build_state_report(pack_dir: str | Path, *, heading: str = "DAOS Status") -> tuple[int, str, str]:
    root = Path(pack_dir).expanduser().resolve()
    validation = validate_pack_dir(root)
    if any(error.startswith("Pack directory does not exist") or error.startswith("Pack path is not a directory") for error in validation.errors):
        return (
            1,
            "",
            f"DAOS Status unavailable: {root}\n- run `use-daos init` to create a DAOS home, or set DAOS_HOME to an existing pack\n",
        )

    hot_cache = root / "wiki" / "cache" / "hot-cache.md"
    hot_cache_log = root / "wiki" / "cache" / "hot-cache-log.md"
    reset_handoff = root / "wiki" / "cache" / "reset-handoff.md"
    agent_continuity = root / "wiki" / "cache" / "agent-continuity.md"
    raw_dir = root / "wiki" / "raw"
    source_dir = root / "wiki" / "sources"
    instruction_scan = root / "import-stage" / "instruction-scan.md"

    current: list[str] = []
    corrections: list[str] = []
    if hot_cache.is_file():
        hot_text = _read_text(hot_cache)
        current = _real_bullets(_section_bullets(hot_text, "## Current Focus"))[:4]
        corrections = _real_bullets(_section_bullets(hot_text, "## Current Corrections"))[:3]

    recent: list[str] = []
    if hot_cache_log.is_file():
        recent = _recent_log_entries(_read_text(hot_cache_log), limit=4)

    reset_summary = "No exact next move set."
    next_move = "Set current focus in `wiki/cache/hot-cache.md`; create a reset handoff when real work begins."
    if reset_handoff.is_file():
        value = _label_value(_read_text(reset_handoff), "- Exact next move:")
        if value:
            reset_summary = value
            next_move = value

    setup_required: list[str] = []
    if validation.errors:
        compact_errors = _compact_validation_errors(validation.errors)
        setup_required.extend(compact_errors[:5])
        if len(compact_errors) > 5:
            setup_required.append(f"{len(compact_errors) - 5} more validation issues; run `use-daos check` for details")

    continuity_missing: list[str] = []
    if not current:
        continuity_missing.append("hot-cache.md has no real current focus yet")
    if reset_handoff.is_file():
        handoff_text = _read_text(reset_handoff)
        if not _label_value(handoff_text, "- Exact next move:"):
            continuity_missing.append("reset-handoff.md has no filled Exact next move")
        if not _label_value(handoff_text, "- First verification:"):
            continuity_missing.append("reset-handoff.md has no filled First verification")
    else:
        continuity_missing.append("reset-handoff.md is missing")

    raw_count = 0
    source_count = 0
    if raw_dir.is_dir():
        raw_count = len([path for path in raw_dir.rglob("*") if path.is_file() and path.name != "README.md"])
    if source_dir.is_dir():
        source_count = len([path for path in source_dir.rglob("*") if path.is_file() and path.name != "README.md"])
    instruction_count = _count_instruction_carriers(instruction_scan)
    instruction_applied_count = _count_report_section_items(instruction_scan, "## Edits applied")
    instruction_pending_count = _count_report_section_items(instruction_scan, "## Edits needing approval")

    lines = [
        heading,
        f"Pack: {root}",
        "",
        "Setup",
        "- DAOS baseline present.",
    ]
    if instruction_scan.is_file():
        lines.append("- instruction bridge review present inside DAOS home: import-stage/instruction-scan.md")
    else:
        lines.append("- no instruction bridge review present")
    hot_cache_summary = _first_bullet_summary(current, "No current focus set yet.")
    hot_cache_log_summary = recent[0] if recent else "No recent hot-cache-log entries found."
    agent_summary = _agent_continuity_summary(agent_continuity)

    lines.extend(
        [
            "",
            "DAOS On",
            f"- Hot Cache: {hot_cache_summary}",
            f"- Hot Cache Log: {hot_cache_log_summary}",
            f"- Reset Handoff: {reset_summary}",
            f"- Agent Continuity: {agent_summary}",
        ]
    )
    lines.extend([
        "",
        "Current",
    ])
    lines.extend(current or ["- No current focus set yet."])
    if corrections:
        lines.extend(["", "Corrections"])
        lines.extend(corrections)
    lines.extend(["", "Recent Activity"])
    lines.extend([f"- {entry}" for entry in recent] or ["- No recent hot-cache-log entries found."])
    lines.extend(["", "Memory Surfaces", f"- raw notes beyond README: {raw_count}", f"- source notes beyond README: {source_count}"])
    if instruction_scan.is_file():
        lines.extend(
            [
                "",
                "Bridge",
                f"- instruction carriers found: {instruction_count}",
                f"- instruction edits applied: {instruction_applied_count}",
                f"- instruction edits needing approval: {instruction_pending_count}",
                "- review inside DAOS home: import-stage/instruction-scan.md",
            ]
        )
    bridge_review: list[str] = []
    if instruction_scan.is_file() and instruction_pending_count:
        bridge_review.append(f"{instruction_pending_count} instruction edits need approval; review `import-stage/instruction-scan.md` inside DAOS home")
    elif instruction_scan.is_file():
        bridge_review.append("None")
    else:
        bridge_review.append("No instruction bridge review present")

    lines.extend(["", "Setup Required"])
    if setup_required:
        lines.append("- This DAOS home is readable, but it still needs personalization before it is operational.")
        lines.extend([f"- {item}" for item in setup_required])
    else:
        lines.append("- None")
    lines.extend(["", "Continuity Missing"])
    lines.extend([f"- {item}" for item in continuity_missing] or ["- None"])
    lines.extend(["", "Bridge Review"])
    lines.extend([f"- {item}" for item in bridge_review])
    lines.extend(["", "Next", f"- {next_move}"])
    return 0, "\n".join(lines) + "\n", ""


def _status_line(label: str, status: str) -> str:
    return f"{label:<24}{status}"


def _load_runtime_fixture(runtime_file: str | Path | None) -> tuple[dict, list[str]]:
    if not runtime_file:
        return {}, []
    path = Path(runtime_file).expanduser().resolve()
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"runtime fixture unreadable: {path}: {exc}"]


def _path_from_env(name: str) -> str:
    return str(Path(os.environ[name]).expanduser().resolve()) if os.environ.get(name) else ""


def _hermes_home() -> Path:
    return Path(os.environ.get("HERMES_HOME", "~/.hermes")).expanduser()


def _detect_hermes_runtime(pack_dir: Path) -> tuple[dict, list[str]]:
    """Collect conservative, read-only Hermes evidence for `use-daos doctor`.

    This does not claim a live one-shot proof. It only reports wiring that can be
    checked from files/env without mutating the runtime.
    """
    warnings: list[str] = []
    evidence: dict = {"runtime": "hermes", "unexpected_writes": False}

    startup_root = _path_from_env("HERMES_STARTUP_ROOT") or _path_from_env("PWD") or str(Path.cwd().resolve())
    daos_home = _path_from_env("DAOS_HOME")
    evidence["startup_root"] = startup_root
    evidence["daos_home"] = daos_home or str(pack_dir)
    if not daos_home:
        warnings.append("Hermes runtime detection used pack_dir as daos_home because DAOS_HOME is not set")

    plugin_path = _hermes_home() / "plugins" / "daos-session-handoff" / "__init__.py"
    plugin_text = ""
    try:
        plugin_text = plugin_path.read_text(encoding="utf-8")
    except OSError as exc:
        warnings.append(f"Hermes reset/wake plugin unreadable: {plugin_path}: {exc}")

    prompt_markers = (
        "current user message",
        "hot-cache",
        "reset-handoff",
        "agent-continuity",
        "private",
    )
    if plugin_text and all(marker in plugin_text.lower() for marker in prompt_markers):
        evidence["prompt_precedence"] = [
            "current user message / local thread",
            "DAOS hot-cache / reset-handoff",
            "DAOS agent-continuity fallback",
            "private memory",
        ]
    else:
        evidence["prompt_precedence"] = []
        warnings.append("Hermes prompt precedence could not be proven from the DAOS session handoff plugin")

    signal_wired = bool(
        plugin_text
        and "pre_llm_call" in plugin_text
        and "is_first_turn" in plugin_text
        and "on_session_finalize" in plugin_text
        and "reset-handoff.md" in plugin_text
    )
    evidence["reset_wake"] = {
        "signal_wired": signal_wired,
        "one_shot_proven": False,
    }
    if not signal_wired:
        warnings.append("Hermes reset/wake signal wiring was not detected")
    return evidence, warnings


def collect_runtime_evidence(
    pack_dir: Path,
    runtime: str | None = None,
    detect: bool = False,
) -> tuple[dict, list[str]]:
    """Return runtime evidence in the shape `build_doctor_report` understands.

    `runtime` can name a supported detector (currently `hermes`) or point to a
    JSON fixture. `detect=True` enables automatic conservative detection.
    """
    warnings: list[str] = []
    if runtime:
        runtime_path = Path(runtime).expanduser()
        if runtime_path.is_file():
            return _load_runtime_fixture(runtime_path)

    runtime_name = (runtime or "").strip().lower()
    if detect and not runtime_name:
        hermes_plugin = _hermes_home() / "plugins" / "daos-session-handoff" / "__init__.py"
        if hermes_plugin.exists() or os.environ.get("HERMES_HOME"):
            runtime_name = "hermes"

    if runtime_name in {"", "none"}:
        return {}, warnings
    if runtime_name == "hermes":
        return _detect_hermes_runtime(pack_dir)
    return {}, [f"unsupported runtime detector: {runtime}"]


def _normalise_platform_message(text: str) -> str:
    """Return user content with common chat wrappers removed.

    Discord gateway session logs often store user messages as:
    `[Replying to: "..."] [crltn] proof text`. Doctor proofs should
    validate the human content, not fail because transport metadata is present.
    """
    cleaned = text.strip()
    if cleaned.startswith("[Replying to:"):
        closing = cleaned.find("]")
        if closing != -1:
            cleaned = cleaned[closing + 1 :].strip()
    if cleaned.startswith("["):
        closing = cleaned.find("]")
        if closing != -1:
            cleaned = cleaned[closing + 1 :].strip()
    return cleaned


def _runtime_anchor_status(root: Path, runtime: dict) -> tuple[str, str]:
    if not runtime:
        return "UNPROVEN", "no runtime fixture provided"
    expected = str(root)
    startup_root = str(runtime.get("startup_root", ""))
    daos_home = str(runtime.get("daos_home", ""))
    if startup_root == expected or daos_home == expected:
        return "PASS", "runtime fixture points at DAOS home/project root"
    return "WARN", "runtime fixture root does not match DAOS home"


def _source_precedence_status(runtime: dict) -> tuple[str, str]:
    if not runtime:
        return "UNPROVEN", "no prompt precedence evidence provided"
    precedence = [str(item).lower() for item in runtime.get("prompt_precedence", [])]
    if not precedence:
        return "UNPROVEN", "runtime fixture has no prompt_precedence list"
    private_index = next((i for i, item in enumerate(precedence) if "private" in item or "memory" in item), None)
    daos_index = next((i for i, item in enumerate(precedence) if "daos" in item or "hot-cache" in item or "project" in item), None)
    if daos_index is not None and (private_index is None or daos_index < private_index):
        return "PASS", "DAOS/project context precedes private memory"
    return "WARN", "private memory may outrank DAOS current truth"


def _reset_signal_status(runtime: dict) -> tuple[str, str]:
    if not runtime:
        return "UNPROVEN", "no reset/wake runtime evidence provided"
    reset_wake = runtime.get("reset_wake", {}) if isinstance(runtime.get("reset_wake", {}), dict) else {}
    session_proof = runtime.get("session_proof", {}) if isinstance(runtime.get("session_proof", {}), dict) else {}
    if reset_wake.get("signal_wired") is True or session_proof:
        return "PASS", "reset/wake evidence present"
    return "UNPROVEN", "runtime fixture does not prove reset/wake signal wiring"


def _one_shot_status(runtime: dict) -> tuple[str, str]:
    if not runtime:
        return "UNPROVEN", "no one-shot proof evidence provided"
    reset_wake = runtime.get("reset_wake", {}) if isinstance(runtime.get("reset_wake", {}), dict) else {}
    if reset_wake.get("one_shot_proven") is True:
        return "PASS", "runtime fixture reports one-shot reset/wake proof"
    session_proof = runtime.get("session_proof", {}) if isinstance(runtime.get("session_proof", {}), dict) else {}
    if session_proof:
        first = _normalise_platform_message(str(session_proof.get("first_user_message", "")))
        second = _normalise_platform_message(str(session_proof.get("second_user_message", "")))
        first_ok = "proof one after reset" in first and session_proof.get("first_orientation_present") is True
        second_ok = "proof two normal followup" in second and session_proof.get("second_orientation_present") is False
        if first_ok and second_ok:
            return "PASS", "platform wrappers normalized; reset orientation was one-shot"
        return "WARN", "session proof did not show first-turn orientation and second-turn absence"
    return "UNPROVEN", "no one-shot reset/wake proof provided"


def build_doctor_report(
    pack_dir: str | Path,
    runtime_file: str | Path | None = None,
    runtime: str | None = None,
    detect_runtime: bool = False,
) -> tuple[int, str, str]:
    """Build a read-only DAOS proof-ladder receipt."""
    root = Path(pack_dir).expanduser().resolve()
    validation = validate_pack_dir(root)
    if runtime_file:
        runtime, runtime_errors = _load_runtime_fixture(runtime_file)
    else:
        runtime, runtime_errors = collect_runtime_evidence(root, runtime=runtime, detect=detect_runtime)

    if any(error.startswith("Pack directory does not exist") or error.startswith("Pack path is not a directory") for error in validation.errors):
        return 1, "", f"DAOS Doctor unavailable: {root}\n- run `use-daos init` to create a DAOS home, or set DAOS_HOME to an existing pack\n"

    baseline_files = [
        root / "assistant-charter.md",
        root / "operating-profile.md",
        root / "wiki" / "cache" / "hot-cache.md",
        root / "wiki" / "cache" / "reset-handoff.md",
    ]
    pack_status = "PASS" if all(path.is_file() for path in baseline_files) else "FAIL"
    instruction_scan = root / "import-stage" / "instruction-scan.md"
    pending = _count_report_section_items(instruction_scan, "## Edits needing approval")
    applied = _count_report_section_items(instruction_scan, "## Edits applied")
    if instruction_scan.is_file() and pending == 0:
        bridge_status = "PASS"
        bridge_detail = f"instruction bridge review present; applied={applied}, pending=0"
    elif instruction_scan.is_file():
        bridge_status = "WARN"
        bridge_detail = f"instruction bridge review present; pending edits={pending}"
    else:
        bridge_status = "PASS"
        bridge_detail = "no instruction bridge review present; treating as greenfield/unscanned for read-only v0"

    runtime_status, runtime_detail = _runtime_anchor_status(root, runtime)
    precedence_status, precedence_detail = _source_precedence_status(runtime)
    reset_status, reset_detail = _reset_signal_status(runtime)
    one_shot_status, one_shot_detail = _one_shot_status(runtime)
    writes_status = "WARN" if runtime.get("unexpected_writes") is True else "PASS"
    writes_detail = "runtime fixture reported unexpected writes" if writes_status == "WARN" else "no unexpected writes reported by doctor inputs"

    statuses = [pack_status, bridge_status, runtime_status, precedence_status, reset_status, one_shot_status, writes_status]
    if all(status == "PASS" for status in statuses):
        verdict = "DAOS obeyed"
    elif "FAIL" in statuses or "WARN" in (runtime_status, precedence_status, writes_status):
        verdict = "conflict detected"
    else:
        verdict = "installed, not proven"

    lines = [
        "DAOS Doctor",
        f"Pack: {root}",
        "Read-only: no files modified",
        "",
        "Proof ladder",
        _status_line("Pack structure", pack_status),
        _status_line("Instruction bridge", bridge_status),
        _status_line("Runtime anchor", runtime_status),
        _status_line("Source precedence", precedence_status),
        _status_line("Reset/wake signal", reset_status),
        _status_line("One-shot reset proof", one_shot_status),
        _status_line("Unexpected writes", writes_status),
        "",
        f"Verdict: {verdict}",
        "",
        "Evidence",
        f"- pack structure: {'baseline files present' if pack_status == 'PASS' else 'baseline files missing'}",
        f"- instruction bridge: {bridge_detail}",
        f"- runtime anchor: {runtime_detail}",
        f"- source precedence: {precedence_detail}",
        f"- reset/wake signal: {reset_detail}",
        f"- one-shot reset proof: {one_shot_detail}",
        f"- unexpected writes: {writes_detail}",
    ]
    if runtime_errors:
        lines.extend(["", "Runtime fixture warnings"])
        lines.extend(f"- {error}" for error in runtime_errors)
    if verdict != "DAOS obeyed":
        next_steps = ["", "Next"]
        if bridge_status == "WARN":
            next_steps.append("- Review bridge warnings before claiming overlay obedience.")
        next_steps.append(
            "- Provide runtime evidence with `--runtime-file` or `--runtime hermes --detect-runtime` "
            "to prove anchor, source precedence, and reset/wake one-shot behavior."
        )
        lines.extend(next_steps)
    return 0, "\n".join(lines) + "\n", ""


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
