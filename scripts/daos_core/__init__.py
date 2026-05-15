"""Shared DAOS schema, rendering, and validation helpers."""

# DAOS baseline note: current public framework baseline is v0.1.6; this module remains part of the current release surface.

from .schema import (
    AssistantCharter,
    DaosPack,
    FRAMEWORK_VERSION,
    LaneSnapshot,
    OperatingProfile,
    SCHEMA_VERSION,
    blank_starter_pack,
    filled_example_pack,
    wizard_pack,
)
from .render import render_pack_manifest, write_pack_core_files
from .parity import ParityFinding, ParityResult, audit_memory_parity
from .validate import ValidationResult, validate_pack_dir
from .boot_check import run_boot_check
from .context_preflight import evaluate_action_preflight_policy, recover_reply_anchor_context
from .harness import audit_memory_surfaces, build_doctor_report, build_orientation_bundle, build_state_report, collect_runtime_evidence, find_instruction_carriers, prepend_daos_coexistence_rule, run_reset_recovery_test, write_instruction_scan_report, write_reset_handoff

__all__ = [
    "AssistantCharter",
    "DaosPack",
    "FRAMEWORK_VERSION",
    "LaneSnapshot",
    "OperatingProfile",
    "SCHEMA_VERSION",
    "ParityFinding",
    "ParityResult",
    "ValidationResult",
    "audit_memory_parity",
    "audit_memory_surfaces",
    "build_doctor_report",
    "build_orientation_bundle",
    "build_state_report",
    "collect_runtime_evidence",
    "blank_starter_pack",
    "filled_example_pack",
    "find_instruction_carriers",
    "evaluate_action_preflight_policy",
    "recover_reply_anchor_context",
    "prepend_daos_coexistence_rule",
    "render_pack_manifest",
    "run_boot_check",
    "run_reset_recovery_test",
    "validate_pack_dir",
    "wizard_pack",
    "write_pack_core_files",
    "write_instruction_scan_report",
    "write_reset_handoff",
]
