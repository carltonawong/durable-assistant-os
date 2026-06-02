#!/usr/bin/env python3
"""Unified DAOS command-line front door."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from daos_bootstrap import bootstrap
from daos_core import audit_memory_surfaces, build_doctor_report, build_state_report, build_orientation_bundle, find_instruction_carriers, prepend_daos_coexistence_rule, run_boot_check, run_reset_recovery_test, validate_pack_dir, write_instruction_scan_report, write_reset_handoff


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        return argparse.Namespace(command="status", pack_dir=None)

    parser = argparse.ArgumentParser(
        prog="use-daos",
        description="DAOS local harness commands. Only shipped commands are listed here."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser(
        "status",
        help="show compact DAOS setup and continuity status",
        description="Show the current DAOS setup and continuity status. No files are modified.",
    )
    status.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")

    on = subparsers.add_parser(
        "on",
        help="show what DAOS is currently on",
        description="Alias for status: show the current DAOS setup and DAOS On continuity surface. No files are modified.",
    )
    on.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")


    init = subparsers.add_parser(
        "init",
        help="install the DAOS baseline",
        description="Install the mandatory DAOS baseline and optionally scan existing instruction carriers for coexistence review.",
    )
    init.add_argument("pack_dir", nargs="?", help="Destination DAOS home. Defaults to DAOS_HOME or ~/.daos.")
    init.add_argument("--blank", action="store_true", help="Install baseline without scanning existing instruction carriers")
    init.add_argument("--scan", action="append", default=[], help="Working directory to scan for existing agent instruction files")
    init.add_argument("--use-detected-home", action="store_true", help="Install additively into detected assistant home when no destination is given")
    init.add_argument("--force", action="store_true", help="Replace an existing non-empty DAOS destination")

    setup = subparsers.add_parser(
        "setup",
        help="guided first-run setup for the DAOS markdown files",
        description="Fill the minimum DAOS first-run markdown surfaces with brief guided explanations.",
    )
    setup.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")
    setup.add_argument("--active-lane", default=None, help="Current active project/lane name")
    setup.add_argument("--working-directory", default=None, help="Folder agents should treat as the current working directory")
    setup.add_argument("--primary-outcome", default=None, help="Main useful job this assistant should do")
    setup.add_argument("--approval-boundary", default=None, help="Actions that should require approval")
    setup.add_argument("--uncertainty-behavior", default=None, help="Ask-vs-act behavior when the assistant is unsure")
    setup.add_argument("--live-sources", default=None, help="Live sources to verify before trusting memory")
    setup.add_argument("--durable-context", default=None, help="Recurring context DAOS should preserve durably")
    setup.add_argument("--reset-recovery", default=None, help="What the assistant should recover first after reset or long idle")
    setup.add_argument("--week-success", default=None, help="What would make the assistant useful after one week")
    setup.add_argument("--accept-defaults", action="store_true", help="Allow non-interactive setup to accept all defaults explicitly")
    setup.add_argument("--force", action="store_true", help="Overwrite existing setup-managed files after backing them up")

    check = subparsers.add_parser(
        "check",
        help="read-only pack health check",
        description="Run a read-only DAOS pack health check. No files are modified.",
    )
    check.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory to check. Defaults to DAOS_HOME or ~/.daos.")

    boot_check = subparsers.add_parser(
        "boot-check",
        help="read-only boot-order/runtime hierarchy check",
        description="Verify whether an assistant runtime is likely to operate DAOS-first. No files are modified.",
    )
    boot_check.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")
    boot_check.add_argument("--runtime-config", help="Optional JSON fixture/export with startup_root, prompt_precedence, session_topology, and reset_handoff facts")

    doctor = subparsers.add_parser(
        "doctor",
        help="prove whether DAOS is installed, bridged, activated, and obeyed",
        description="Run a read-only DAOS proof ladder. No files are modified.",
    )
    doctor.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory. Defaults to DAOS_HOME or ~/.daos.")
    doctor.add_argument("--runtime-file", default=None, help="Optional JSON runtime evidence fixture for anchor/source-order/reset proof")
    doctor.add_argument("--runtime", default=None, help="Optional runtime detector name (currently: hermes) or path to a JSON evidence fixture")
    doctor.add_argument("--detect-runtime", action="store_true", help="Read-only best-effort runtime evidence detection")
    doctor.add_argument("--json", action="store_true", dest="json_output")

    orient = subparsers.add_parser(
        "orient",
        help="build a read-only assistant orientation bundle",
        description="Build a deterministic DAOS orientation bundle for an assistant. No files are modified and no LLM is called.",
    )
    orient.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory to orient from. Defaults to DAOS_HOME or ~/.daos.")
    orient.add_argument("--task", default=None, help="Current task to include in the orientation bundle")

    reset_test = subparsers.add_parser(
        "reset-test",
        help="run deterministic reset recovery checks",
        description="Check whether a DAOS pack can support fresh-session reset recovery. No files are modified and no LLM is called.",
    )
    reset_test.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory to test. Defaults to DAOS_HOME or ~/.daos.")

    handoff = subparsers.add_parser(
        "handoff",
        help="overwrite the reset handoff artifact",
        description="Write the current exact reset handoff into a DAOS pack. This overwrites wiki/cache/reset-handoff.md.",
    )
    handoff.add_argument("pack_dir", help="Path to a DAOS pack directory to update")
    handoff.add_argument("--lane", required=True, help="Current lane for the handoff")
    handoff.add_argument("--status", required=True, help="Current status for the handoff")
    handoff.add_argument("--why", required=True, help="Why this handoff exists")
    handoff.add_argument("--next", required=True, help="Exact next move after reset or idle")
    handoff.add_argument("--verify", required=True, help="First verification to run before continuing")

    memory_audit = subparsers.add_parser(
        "memory-audit",
        help="audit DAOS memory surfaces",
        description="Read-only audit of DAOS active and durable memory surfaces. No files are modified.",
    )
    memory_audit.add_argument("pack_dir", nargs="?", help="Path to a DAOS pack directory to audit. Defaults to DAOS_HOME or ~/.daos.")

    return parser.parse_args(argv)


def resolve_default_pack_dir(pack_dir_arg: str | None) -> Path:
    if pack_dir_arg:
        return Path(pack_dir_arg).expanduser().resolve()
    configured = os.environ.get("DAOS_HOME")
    if configured:
        return Path(configured).expanduser().resolve()
    return (Path.home() / ".daos").resolve()


ASSISTANT_HOME_MARKERS = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    "HERMES.md",
    "OPENCLAW.md",
    "QUINN.md",
    ".cursorrules",
)
ASSISTANT_HOME_DIR_MARKERS = (".openclaw", ".hermes", ".cursor", ".claude")


def _looks_like_daos_home(path: Path) -> bool:
    return (path / "assistant-charter.md").exists() and (path / "operating-profile.md").exists() and (path / "wiki" / "cache").is_dir()


def _looks_like_assistant_operating_home(path: Path) -> bool:
    if _looks_like_daos_home(path):
        return True
    if any((path / marker).exists() for marker in ASSISTANT_HOME_MARKERS):
        return True
    if any((path / marker).is_dir() for marker in ASSISTANT_HOME_DIR_MARKERS):
        return True
    return False


def detect_assistant_operating_home(scan_paths: list[Path]) -> Path | None:
    candidates: list[Path] = []
    for raw_path in scan_paths:
        path = raw_path.expanduser().resolve()
        current = path if path.is_dir() else path.parent
        for parent in (current, *current.parents):
            if _looks_like_assistant_operating_home(parent):
                candidates.append(parent)
                break
    if not candidates:
        return None
    for candidate in candidates:
        if _looks_like_daos_home(candidate):
            return candidate
    return candidates[0]


def run_status(pack_dir_arg: str | None, *, heading: str = "DAOS Status") -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = build_state_report(pack_dir, heading=heading)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def _resolve_init_scan_paths(args: argparse.Namespace) -> list[Path]:
    if args.blank:
        return []
    if args.scan:
        return [Path(path).expanduser().resolve() for path in args.scan]
    if sys.stdin.isatty():
        default = Path.cwd()
        response = input(f"Working directory to scan for agent instructions [{default}]: ").strip()
        return [Path(response).expanduser().resolve() if response else default.resolve()]
    return [Path.cwd().resolve()]


def _approve_instruction_edits(carriers: list[Path], backup_root: Path) -> dict[Path, Path]:
    if not carriers or not sys.stdin.isatty():
        return {}
    pending = []
    for carrier in carriers:
        try:
            text = carrier.read_text(encoding="utf-8")
        except OSError:
            continue
        if "DAOS coexistence rule" not in text:
            pending.append(carrier)
    if not pending:
        return {}

    print("DAOS found existing agent instruction files.")
    for carrier in pending:
        print(f"DAOS wants approval to prepend the coexistence rule to: {carrier}")
    response = input("Apply these approved instruction edits now? [y/N]: ").strip().lower()
    if response not in {"y", "yes"}:
        return {}

    applied: dict[Path, Path] = {}
    for carrier in pending:
        backup_path = prepend_daos_coexistence_rule(carrier, backup_root=backup_root)
        if backup_path:
            applied[carrier] = backup_path
    return applied


def run_init(args: argparse.Namespace) -> int:
    explicit_destination = bool(args.pack_dir or os.environ.get("DAOS_HOME"))
    try:
        scan_paths = _resolve_init_scan_paths(args)
        detected_home = detect_assistant_operating_home(scan_paths) if scan_paths else None
        use_detected_home = bool(args.use_detected_home and not explicit_destination and detected_home)
        pack_dir = detected_home if use_detected_home else resolve_default_pack_dir(args.pack_dir)
        destination = bootstrap(pack_dir, force=args.force, overlay=use_detected_home)
        report_path = None
        applied_backups: dict[Path, Path] = {}
        carriers = find_instruction_carriers(scan_paths) if scan_paths else []
        if carriers:
            timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
            backup_root = destination / ".daos" / "backups" / "instructions" / timestamp
            applied_backups = _approve_instruction_edits(carriers, backup_root)
        if scan_paths:
            report_path = write_instruction_scan_report(
                destination,
                scan_paths,
                applied_paths=list(applied_backups.keys()),
                backup_paths=applied_backups,
            )
    except (FileNotFoundError, ValueError, OSError) as exc:
        print(f"DAOS init failed: {exc}", file=sys.stderr)
        return 1

    print(f"DAOS initialized: {destination}")
    print("purpose: shared continuity baseline for agents; existing instruction files are edited only with approval")
    print("baseline: installed mandatory wiki/cache framework")
    if 'detected_home' in locals() and detected_home:
        print(f"assistant home scan: detected {detected_home}")
        if 'use_detected_home' in locals() and use_detected_home:
            print("assistant home install: used detected home additively; preserved existing files")
        elif not explicit_destination:
            print("assistant home install: defaulted to ~/.daos; use --use-detected-home to install into detected home")
    if args.blank:
        print("instruction scan: skipped (--blank)")
    elif report_path:
        display_report_path = report_path
        try:
            display_report_path = report_path.relative_to(destination)
        except ValueError:
            pass
        print(f"instruction scan: wrote review report inside DAOS home: {display_report_path}")
        if applied_backups:
            print(f"instruction edits: applied with approval ({len(applied_backups)})")
            print("instruction backups: .daos/backups/instructions/")
        else:
            print("instruction edits: none applied; review report lists any proposed edits")
    print("next: run `use-daos setup` to fill the minimum assistant charter, operating profile, current focus, and reset handoff")
    return 0


def _setup_answer(
    index: int,
    question: str,
    examples: str,
    default: str,
    value: str | None,
) -> str:
    print(f"{index}/8 {question}")
    print(f"Examples: {examples}")
    print(f"Default: {default}")
    if value:
        print(f"> {value.strip()}")
        return value.strip()
    if sys.stdin.isatty():
        response = input("> ").strip()
        return response or default
    print("> ")
    return default


SETUP_MANAGED_FILES = (
    Path("assistant-charter.md"),
    Path("operating-profile.md"),
    Path("wiki/cache/hot-cache.md"),
    Path("wiki/cache/reset-handoff.md"),
)


SETUP_STARTER_MARKERS = {
    Path("assistant-charter.md"): (("Starter-pack working copy", "- Primary outcome:", "- Actions that always require approval:"),),
    Path("operating-profile.md"): (("Starter-pack working copy", "- Primary outcome:", "- Durable capture rule:"),),
    Path("wiki/cache/hot-cache.md"): (
        ("**Updated:** YYYY-MM-DD HH:MM TZ", "Fill with compact Current Focus entries only."),
        ("**Updated:** YYYY-MM-DD HH:MM TZ", "Fill with the current shared foreground lane."),
    ),
    Path("wiki/cache/reset-handoff.md"): (("**Status:** empty | fresh | stale | blocked", "- Exact next move:"),),
}


def _is_setup_starter_file(path: Path, relative_path: Path) -> bool:
    if not path.exists():
        return True
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return any(all(marker in text for marker in markers) for markers in SETUP_STARTER_MARKERS[relative_path])


def _setup_dirty_files(pack_dir: Path) -> list[Path]:
    dirty: list[Path] = []
    for relative_path in SETUP_MANAGED_FILES:
        target = pack_dir / relative_path
        if target.exists() and not _is_setup_starter_file(target, relative_path):
            dirty.append(relative_path)
    return dirty


def _backup_setup_files(pack_dir: Path, relative_paths: tuple[Path, ...]) -> Path | None:
    existing = [relative_path for relative_path in relative_paths if (pack_dir / relative_path).exists()]
    if not existing:
        return None
    timestamp = datetime.now().astimezone().strftime("%Y%m%d-%H%M%S")
    backup_root = pack_dir / ".daos" / "backups" / "setup" / timestamp
    for relative_path in existing:
        source = pack_dir / relative_path
        destination = backup_root / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return backup_root


def run_setup(args: argparse.Namespace) -> int:
    pack_dir = resolve_default_pack_dir(args.pack_dir)
    if not pack_dir.exists():
        print(f"DAOS setup failed: pack directory does not exist: {pack_dir}", file=sys.stderr)
        print("next: run `use-daos init` first", file=sys.stderr)
        return 1

    dirty_files = _setup_dirty_files(pack_dir)
    if dirty_files and not args.force:
        print("DAOS setup refused to overwrite existing personalized setup files.", file=sys.stderr)
        for relative_path in dirty_files:
            print(f"- {relative_path}", file=sys.stderr)
        print("next: review those files, then rerun with `use-daos setup --force` only if you want DAOS to back them up and overwrite them.", file=sys.stderr)
        return 1

    provided_answers = [
        args.active_lane,
        args.working_directory,
        args.uncertainty_behavior,
        args.approval_boundary,
        args.live_sources,
        args.durable_context,
        args.reset_recovery,
        args.week_success,
    ]
    if not sys.stdin.isatty() and not args.accept_defaults and not all(provided_answers):
        print("DAOS setup needs an interactive terminal so it does not silently answer personalization questions for you.", file=sys.stderr)
        print("Run `use-daos setup` yourself in a terminal to answer the 8 setup questions.", file=sys.stderr)
        print("For automation only, pass all setup flags or explicitly use `use-daos setup --accept-defaults`.", file=sys.stderr)
        return 1

    print("DAOS setup")
    print(f"Pack: {pack_dir}")
    if args.accept_defaults and not sys.stdin.isatty():
        print("non-interactive defaults explicitly accepted")
    print("Answer 8 quick questions. Press Enter to accept a default.")
    active_lane = _setup_answer(
        1,
        "What do you want this assistant to help you make progress on first?",
        "coding projects, business operations, personal admin",
        "my current active project",
        args.active_lane or args.primary_outcome,
    )
    working_directory = _setup_answer(
        2,
        "What folder, project, or operating home should the assistant treat as the live workspace for this setup?",
        "current repo, company workspace, assistant home folder",
        str(Path.cwd().resolve()),
        args.working_directory,
    )
    uncertainty_behavior = _setup_answer(
        3,
        "When the assistant is unsure, should it inspect/verify first, act on obvious low-risk defaults, or ask before moving?",
        "verify first, act on low-risk defaults, always ask",
        "verify first, act on low-risk defaults, ask before risky changes",
        args.uncertainty_behavior,
    )
    approval_boundary = _setup_answer(
        4,
        "What actions should always require your approval?",
        "deleting files, publishing/sending messages, changing credentials",
        "destructive changes, external actions, credentials/production changes",
        args.approval_boundary,
    )
    live_sources = _setup_answer(
        5,
        "What live sources should the assistant check before trusting memory?",
        "current thread, repo files/git status, logs/runtime state",
        "current thread, repo files/git status, logs/runtime state",
        args.live_sources,
    )
    durable_context = _setup_answer(
        6,
        "What context are you tired of repeating and want DAOS to preserve durably?",
        "project conventions, preferred tools, business rules",
        "project conventions, preferred tools, recurring setup details",
        args.durable_context,
    )
    reset_recovery = _setup_answer(
        7,
        "If the assistant resets or comes back tomorrow, what should it recover first?",
        "current project status, exact next step, open blockers",
        "current project status, exact next step, first verification",
        args.reset_recovery,
    )
    week_success = _setup_answer(
        8,
        "What would make this assistant feel genuinely useful after one week?",
        "remembers where we left off, catches stale assumptions, keeps work moving",
        "remembers where we left off, verifies before acting, keeps work moving",
        args.week_success,
    )
    primary_outcome = active_lane
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")

    assistant_charter = dedent(f"""
        # Assistant Charter

        > DAOS setup working draft. Review and personalize this after first use.

        ## 1. Core outcome

        - Primary outcome: {primary_outcome}
        - The main kind of help this assistant should provide: Make progress on {active_lane}; preserve durable context for {durable_context}.

        ## 2. Main failure mode

        - Primary failure mode: Acting on stale or assumed context instead of verified current files/runtime state.
        - What would make the assistant feel unhelpful, unsafe, noisy, or trust-reducing fastest: Claiming setup or commands worked without checking them, or changing important files without scope awareness.

        ## 3. Uncertainty behavior

        - Default uncertainty behavior: {uncertainty_behavior}
        - Ask-first trigger: Ask when missing information would materially change the target, side effect, irreversible action, or user-facing result.
        - Act-with-defaults trigger: Proceed when the request has an obvious low-risk default and the result can be checked or reversed.

        ## 4. Proactive behavior

        - Proactive by default or mostly reactive: Mostly reactive, with proactive verification and compact continuity updates when they prevent repeated setup or confusion.
        - What should trigger interruption: Potential destructive changes, credential/security boundaries, ambiguous targets, or actions covered by approval boundaries.
        - What should usually be batched or left quiet: Routine logs, repeated status details, and non-blocking cleanup suggestions.

        ## 5. Safety / approval boundary

        - Low-stakes reversible actions that can proceed: Read-only inspection, local status checks, creating temporary test directories, and updating DAOS cache/handoff for the active lane.
        - Actions that always require approval: {approval_boundary}
        - Any special red lines: Do not treat DAOS memory as truth when live files/runtime contradict it; do not silently modify external instruction carriers.

        ## 6. Desired feel

        - Desired feel in daily use: Direct, practical, low-friction, and grounded in verified actions.
        - Tone to avoid: Overly verbose, performative, evasive, or pretending certainty without evidence.
        - Comparison or metaphor if helpful: {week_success}

        ## Minimum good first pass

        This file is ready for first use. Revisit after a week of real work.
        """).strip() + "\n"

    operating_profile = dedent(f"""
        # Operating Profile

        > DAOS setup working draft. Keep this compact; deepen it through use.

        ## 1. Assistant charter

        - Primary outcome: {primary_outcome}
        - Primary failure mode: Acting on stale or assumed context instead of verified current files/runtime state.
        - Uncertainty behavior: {uncertainty_behavior}
        - Proactive behavior: Mostly reactive, with proactive verification and compact continuity updates.
        - Safety / approval boundary: {approval_boundary}
        - Desired feel: Direct, practical, low-friction, and grounded in verified actions.

        ## 2. Top-level lane map

        - {active_lane}
        - Other:

        ## 3. Per-lane snapshot

        ### Lane: {active_lane}
        - Status: active
        - Foreground: yes
        - Pressure: low
        - Short note: Work from `{working_directory}` until the user changes the active lane.

        ## 4. Reminder / planning defaults

        - Master list source: Current thread plus DAOS cache files for this setup.
        - Review layer / dashboard: `use-daos on` and `use-daos status`.
        - Same-day overdue follow-up: Not configured yet.
        - Focus-set default: Keep the foreground lane pointed at `{active_lane}` until the user changes it.
        - Importance / urgency rules: Prioritize verified command outcomes and continuity health over speculative personalization.

        ## 5. Memory / trust defaults

        - Memory front door: current thread/session first, then `wiki/cache/hot-cache.md`, then `wiki/cache/reset-handoff.md` when resuming.
        - Durable memory home: `{pack_dir / 'wiki'}`.
        - Verified reality rule: Check {live_sources} before trusting remembered notes.
        - Ask-vs-act rule: {uncertainty_behavior}
        - Escalation / approval rule: Require approval for {approval_boundary}
        - Durable capture rule: Preserve {durable_context} when it would be annoying or risky to rediscover.
        - Project checkpoint rule: Capture changes to infrastructure, data ownership, provider/tool/account choice, auth, deployment/runtime mode, live-vs-dry-run posture, risk, money, customer impact, or operator setup.

        ## 6. Calibration later

        - What feels too heavy? Review after real use.
        - What still gets missed? Review after real use.
        - Which lane needs more support? Review after real use.
        - What should be added, removed, or softened? Review after real use.
        """).strip() + "\n"

    hot_cache = dedent(f"""
        # Hot Cache

        **Updated:** {timestamp}
        **Updated by:** DAOS setup
        **Scope:** {active_lane}

        > Shared volatile front door. If this feels mismatched, check `hot-cache-log.md`, then `reset-handoff.md`.

        ## Current Focus
        - {active_lane}
        - Working directory: `{working_directory}`.

        ## Current Corrections
        - This is a first-run setup draft; verify {live_sources} before acting on memory.

        ## Current State
        - DAOS setup has filled the minimum charter, profile, current focus, and reset handoff.
        - Durable context to preserve: {durable_context}.

        ## Open Problems
        - Personalize deeper after a week of real use.

        ## System Priorities
        - Keep the first setup lightweight and verified.
        - Use `use-daos check`, `use-daos on`, and `use-daos reset-test` to confirm readiness.
        """).strip() + "\n"

    reset_handoff = dedent(f"""
        # Reset Handoff

        Use this as the named DAOS reset/wake-up continuity artifact.

        If anything here conflicts with verified files, runtime state, or durable wiki pages, verify first and prefer reality.

        ## Current Handoff
        **Last updated:** {timestamp}
        **Updated by:** DAOS setup
        **Lane:** {active_lane}
        **Status:** fresh

        - Why this handoff exists: First-run DAOS setup created an initial recovery point.
        - Exact next move: Recover {reset_recovery}; then work from `{working_directory}` and run `use-daos on` to confirm current continuity.
        - First verification: Check {live_sources}; then run `use-daos check` and `use-daos reset-test` from the active DAOS environment.
        - If stale or contradicted: Re-read the current thread, then `wiki/cache/hot-cache.md`, then verify live files/runtime before continuing.

        ## Editing rules
        - overwrite instead of append
        - keep one resumable handoff, not a diary
        - point to durable notes instead of duplicating them
        - clear or rewrite when the exact handoff changes
        """).strip() + "\n"

    backup_root = _backup_setup_files(pack_dir, SETUP_MANAGED_FILES) if args.force else None

    (pack_dir / "assistant-charter.md").write_text(assistant_charter, encoding="utf-8")
    (pack_dir / "operating-profile.md").write_text(operating_profile, encoding="utf-8")
    cache_dir = pack_dir / "wiki" / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    (cache_dir / "hot-cache.md").write_text(hot_cache, encoding="utf-8")
    (cache_dir / "reset-handoff.md").write_text(reset_handoff, encoding="utf-8")

    print("Step 1: assistant charter — defines what the assistant is for, how it handles uncertainty, and what requires approval.")
    print("Step 2: operating profile — defines the active lane, working directory, and memory/trust defaults.")
    print("Step 3: current focus — writes the hot cache so agents know what DAOS is on right now.")
    print("Step 4: reset handoff — writes the exact recovery note for resets or long idle gaps.")
    if backup_root:
        print(f"backed up existing setup files: {backup_root}")
    print("wrote: assistant-charter.md")
    print("wrote: operating-profile.md")
    print("wrote: wiki/cache/hot-cache.md")
    print("wrote: wiki/cache/reset-handoff.md")
    print("next: run `use-daos check`")
    return 0


def run_check(pack_dir_arg: str | None) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    result = validate_pack_dir(pack_dir)

    if result.errors:
        print(f"DAOS check failed: {pack_dir}", file=sys.stderr)
        print(f"errors: {len(result.errors)}", file=sys.stderr)
        for issue in result.errors:
            print(f"- {issue}", file=sys.stderr)
        print(f"warnings: {len(result.warnings)}", file=sys.stderr)
        for warning in result.warnings:
            print(f"- {warning}", file=sys.stderr)
        print("next: fill required fields or restore missing required files, then run check again", file=sys.stderr)
        return 1

    print(f"DAOS check passed: {pack_dir}")
    print("errors: 0")
    later_use_notes = [
        warning for warning in result.warnings
        if warning == "cadence-review.md looks blank; keep it for later or fill it after real use"
    ]
    actionable_warnings = [warning for warning in result.warnings if warning not in later_use_notes]
    print(f"warnings: {len(actionable_warnings)}")
    for warning in actionable_warnings:
        print(f"- {warning}")
    if later_use_notes:
        print(f"notes: {len(later_use_notes)}")
        print("- cadence-review.md is intentionally left for later first-use calibration; fill it after real use.")
    if actionable_warnings:
        print("next: review warnings before relying on this pack operationally")
    else:
        print("next: run `use-daos on`, then `use-daos reset-test`")
    return 0


def run_boot_check_command(pack_dir_arg: str | None, runtime_config: str | None) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = run_boot_check(str(pack_dir), runtime_config=runtime_config)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_orient(pack_dir_arg: str | None, task: str | None) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = build_orientation_bundle(str(pack_dir), task=task)
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_doctor(
    pack_dir_arg: str | None,
    runtime_file: str | None,
    runtime: str | None,
    detect_runtime: bool,
    json_output: bool = False,
) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = build_doctor_report(
        str(pack_dir),
        runtime_file=runtime_file,
        runtime=runtime,
        detect_runtime=detect_runtime,
        json_output=json_output,
    )
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_reset_test(pack_dir_arg: str | None) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = run_reset_recovery_test(str(pack_dir))
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    if exit_code == 0:
        print("You're complete!")
    return exit_code


def run_handoff(args: argparse.Namespace) -> int:
    exit_code, stdout, stderr = write_reset_handoff(
        args.pack_dir,
        lane=args.lane,
        status=args.status,
        why=args.why,
        next_move=args.next,
        verify=args.verify,
    )
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def run_memory_audit(pack_dir_arg: str | None) -> int:
    pack_dir = resolve_default_pack_dir(pack_dir_arg)
    exit_code, stdout, stderr = audit_memory_surfaces(str(pack_dir))
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, end="", file=sys.stderr)
    return exit_code


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "on":
        return run_status(args.pack_dir, heading="DAOS On")
    if args.command == "status":
        return run_status(args.pack_dir)
    if args.command == "init":
        return run_init(args)
    if args.command == "setup":
        return run_setup(args)
    if args.command == "check":
        return run_check(args.pack_dir)
    if args.command == "boot-check":
        return run_boot_check_command(args.pack_dir, args.runtime_config)
    if args.command == "doctor":
        return run_doctor(args.pack_dir, args.runtime_file, args.runtime, args.detect_runtime, args.json_output)
    if args.command == "orient":
        return run_orient(args.pack_dir, args.task)
    if args.command == "reset-test":
        return run_reset_test(args.pack_dir)
    if args.command == "handoff":
        return run_handoff(args)
    if args.command == "memory-audit":
        return run_memory_audit(args.pack_dir)
    raise AssertionError(f"unhandled command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
