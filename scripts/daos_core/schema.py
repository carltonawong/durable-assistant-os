from __future__ import annotations

from dataclasses import asdict, dataclass, field
from uuid import uuid4


SCHEMA_VERSION = "1"
FRAMEWORK_VERSION = "v0.1.5"
MEMORY_FRONT_DOOR = "local thread first, then hot cache, then agent continuity"
DURABLE_MEMORY_HOME = "wiki first, with repo/docs used for publishable framework outputs"
VERIFIED_REALITY_RULE = "live files, runtime, and current state outrank remembered context for operational facts"
ASK_VS_ACT_RULE = "ask when ambiguity changes action; act when intent is clear and stakes are low or reversible"
DURABLE_CAPTURE_RULE = (
    "if a second review shows something should not live mainly in hot cache or chat, "
    "create/update a durable note in the same pass"
)


@dataclass
class AssistantCharter:
    primary_outcome: str
    main_help: str
    primary_failure_mode: str
    unhelpful_fastest: str
    default_uncertainty_behavior: str
    ask_first_trigger: str
    act_with_defaults_trigger: str
    proactive_mode: str
    interruption_trigger: str
    batch_quiet: str
    low_stakes_actions: str
    always_require_approval: str
    special_red_lines: str
    desired_feel: str
    tone_to_avoid: str
    comparison: str


@dataclass
class LaneSnapshot:
    name: str
    status: str
    foreground: str
    pressure: str
    short_note: str


@dataclass
class OperatingProfile:
    primary_outcome: str
    primary_failure_mode: str
    uncertainty_behavior: str
    proactive_behavior: str
    safety_approval_boundary: str
    desired_feel: str
    top_level_lanes: list[str]
    lane_snapshots: list[LaneSnapshot]
    master_list_source: str
    review_layer_dashboard: str
    same_day_overdue_follow_up: str
    focus_set_default: str
    importance_urgency_rules: str
    memory_front_door: str
    durable_memory_home: str
    verified_reality_rule: str
    ask_vs_act_rule: str
    escalation_approval_rule: str
    durable_capture_rule: str
    calibration_too_heavy: str
    calibration_still_missed: str
    calibration_lane_support: str
    calibration_add_remove_soften: str


@dataclass
class DaosPack:
    schema_version: str = SCHEMA_VERSION
    framework_version: str = FRAMEWORK_VERSION
    pack_id: str = field(default_factory=lambda: str(uuid4()))
    pack_kind: str = "starter-pack"
    generator: str = ""
    assistant_charter: AssistantCharter = field(default_factory=lambda: AssistantCharter(*([""] * 16)))
    operating_profile: OperatingProfile = field(
        default_factory=lambda: OperatingProfile(
            primary_outcome="",
            primary_failure_mode="",
            uncertainty_behavior="",
            proactive_behavior="",
            safety_approval_boundary="",
            desired_feel="",
            top_level_lanes=[],
            lane_snapshots=[],
            master_list_source="",
            review_layer_dashboard="",
            same_day_overdue_follow_up="",
            focus_set_default="",
            importance_urgency_rules="",
            memory_front_door="",
            durable_memory_home="",
            verified_reality_rule="",
            ask_vs_act_rule="",
            escalation_approval_rule="",
            durable_capture_rule="",
            calibration_too_heavy="",
            calibration_still_missed="",
            calibration_lane_support="",
            calibration_add_remove_soften="",
        )
    )

    def manifest_dict(self) -> dict[str, object]:
        return asdict(self)


def blank_starter_pack(*, generator: str) -> DaosPack:
    charter = AssistantCharter(
        primary_outcome="",
        main_help="",
        primary_failure_mode="",
        unhelpful_fastest="",
        default_uncertainty_behavior="",
        ask_first_trigger="",
        act_with_defaults_trigger="",
        proactive_mode="",
        interruption_trigger="",
        batch_quiet="",
        low_stakes_actions="",
        always_require_approval="",
        special_red_lines="",
        desired_feel="",
        tone_to_avoid="",
        comparison="",
    )
    profile = OperatingProfile(
        primary_outcome="",
        primary_failure_mode="",
        uncertainty_behavior="",
        proactive_behavior="",
        safety_approval_boundary="",
        desired_feel="",
        top_level_lanes=["Personal", "Business / operations", "Build / projects", "Trading / research", "Other:"],
        lane_snapshots=[
            LaneSnapshot(
                name="[name]",
                status="active / stalled / hiatus / archive / pending",
                foreground="yes / no",
                pressure="low / medium / high",
                short_note="",
            )
        ],
        master_list_source="",
        review_layer_dashboard="",
        same_day_overdue_follow_up="",
        focus_set_default="",
        importance_urgency_rules="",
        memory_front_door="",
        durable_memory_home="",
        verified_reality_rule="",
        ask_vs_act_rule="",
        escalation_approval_rule="",
        durable_capture_rule="",
        calibration_too_heavy="",
        calibration_still_missed="",
        calibration_lane_support="",
        calibration_add_remove_soften="",
    )
    return DaosPack(generator=generator, assistant_charter=charter, operating_profile=profile)


def filled_example_pack(*, generator: str) -> DaosPack:
    charter = AssistantCharter(
        primary_outcome="keep the user oriented and less likely to drop important work across active lanes",
        main_help="practical chief-of-staff support that keeps the right foreground visible without creating more overhead",
        primary_failure_mode="overhead, wrong assumptions, and losing the right foreground",
        unhelpful_fastest="overexplaining, pushing the wrong priorities, and adding maintenance before usefulness appears",
        default_uncertainty_behavior="ask when ambiguity changes action; otherwise act on likely intent",
        ask_first_trigger="ambiguity that would change the action or cross a trust boundary",
        act_with_defaults_trigger="low-stakes reversible drafting, organization, or follow-through when likely intent is clear",
        proactive_mode="proactive with compression",
        interruption_trigger="risk, deadlines, dependency drift, or wrong-foreground situations",
        batch_quiet="low-value noise, repetitive confirmations, and speculative ideas without immediate leverage",
        low_stakes_actions="drafting, summarizing, organizing, and lightweight investigation when intent is clear",
        always_require_approval="destructive, public, costly, or socially consequential actions",
        special_red_lines="never present remembered context as live truth when files, runtime, or current state can be checked",
        desired_feel="concise, grounded, low-bloat, chief-of-staff-like",
        tone_to_avoid="bloat, fake certainty, and needy confirmation loops",
        comparison="a practical operator rather than a chatbot concierge",
    )
    profile = OperatingProfile(
        primary_outcome=charter.primary_outcome,
        primary_failure_mode=charter.primary_failure_mode,
        uncertainty_behavior="ask when ambiguity changes action; otherwise act on likely intent",
        proactive_behavior="interrupt for risk, deadlines, or real drift; batch lower-value items",
        safety_approval_boundary="destructive, public, costly, or socially consequential actions require approval",
        desired_feel=charter.desired_feel,
        top_level_lanes=["Personal", "Operations", "Client work", "Build / projects", "Research"],
        lane_snapshots=[
            LaneSnapshot("Personal", "active", "no", "medium", "should stay supported without becoming a heavy daily management lane"),
            LaneSnapshot("Operations", "active", "yes", "high", "approvals, inbox pressure, and follow-ups need clean visibility"),
            LaneSnapshot("Client work", "pending", "yes", "high", "external dependencies matter more than generating extra internal work"),
            LaneSnapshot("Build / projects", "active", "yes", "medium", "deep work needs protection from inbox takeover"),
            LaneSnapshot("Research", "stalled", "no", "medium", "still matters, but needs diagnosis rather than vague reminders"),
        ],
        master_list_source="one durable task list as source of truth",
        review_layer_dashboard="one clean review layer for priorities and waiting-on items",
        same_day_overdue_follow_up="yes, but gentle",
        focus_set_default="3 active priorities",
        importance_urgency_rules="importance outranks urgency when they conflict",
        memory_front_door=MEMORY_FRONT_DOOR,
        durable_memory_home=DURABLE_MEMORY_HOME,
        verified_reality_rule=VERIFIED_REALITY_RULE,
        ask_vs_act_rule=ASK_VS_ACT_RULE,
        escalation_approval_rule="critical, sticky, costly, or socially consequential actions require explicit approval",
        durable_capture_rule=DURABLE_CAPTURE_RULE,
        calibration_too_heavy="broad reminder sprays and overlong explanation",
        calibration_still_missed="dependency tracking when inbox pressure spikes",
        calibration_lane_support="client work and operations",
        calibration_add_remove_soften="add cleaner waiting-on visibility; remove low-value broad nudges; soften unnecessary repetition",
    )
    return DaosPack(generator=generator, assistant_charter=charter, operating_profile=profile)


def lane_note(lane: str, foreground_lanes: set[str], slips: str) -> str:
    if lane in foreground_lanes:
        return f"currently foreground; first-pass support should reduce drift around {slips.lower()}"
    return "active but not currently foreground; refine later if this lane needs more structure"


def wizard_pack(answers: dict[str, object], *, generator: str) -> DaosPack:
    lanes: list[str] = answers["lanes"]  # type: ignore[assignment]
    foreground_lanes = set(answers["foreground_lanes"])  # type: ignore[arg-type]
    lane_customizations: dict[str, dict[str, str]] = answers.get("lane_customizations", {})  # type: ignore[assignment]
    importance_over_urgency = (
        "importance outranks urgency when they conflict"
        if answers["importance_over_urgency"]
        else "urgency outranks importance when they conflict"
    )
    charter = AssistantCharter(
        primary_outcome=str(answers["outcome"]),
        main_help="practical chief-of-staff support oriented around continuity, prioritization, and follow-through",
        primary_failure_mode=str(answers["failure_mode"]),
        unhelpful_fastest=str(answers["failure_mode"]),
        default_uncertainty_behavior=str(answers["uncertainty_behavior"]),
        ask_first_trigger="ambiguity that would change the action or cross an approval boundary",
        act_with_defaults_trigger="low-stakes reversible drafting, organization, or setup work where likely intent is clear",
        proactive_mode="proactive with compression",
        interruption_trigger=str(answers["proactive_behavior"]),
        batch_quiet="low-value noise, speculative ideas, and repetitive confirmations",
        low_stakes_actions="drafting, summarizing, organizing, and lightweight investigation when intent is clear",
        always_require_approval=str(answers["approval_boundary"]),
        special_red_lines="never present remembered context as live truth when files, runtime, or current state can be checked",
        desired_feel=str(answers["desired_feel"]),
        tone_to_avoid="overexplaining, broad nagging, or fake certainty",
        comparison="a practical operator rather than a chatbot concierge",
    )
    lane_snapshots = []
    for lane in lanes:
        customization = lane_customizations.get(lane, {})
        lane_snapshots.append(
            LaneSnapshot(
                name=lane,
                status=customization.get("status", "active"),
                foreground="yes" if lane in foreground_lanes else "no",
                pressure="high" if lane in foreground_lanes else "medium",
                short_note=customization.get("short_note", lane_note(lane, foreground_lanes, str(answers["slips"]))),
            )
        )
    profile = OperatingProfile(
        primary_outcome=str(answers["outcome"]),
        primary_failure_mode=str(answers["failure_mode"]),
        uncertainty_behavior=str(answers["uncertainty_behavior"]),
        proactive_behavior=str(answers["proactive_behavior"]),
        safety_approval_boundary=str(answers["approval_boundary"]),
        desired_feel=str(answers["desired_feel"]),
        top_level_lanes=lanes,
        lane_snapshots=lane_snapshots,
        master_list_source=str(answers["master_list_source"]),
        review_layer_dashboard="one clean review layer or dashboard if useful",
        same_day_overdue_follow_up="yes, but gentle",
        focus_set_default="3 active priorities",
        importance_urgency_rules=importance_over_urgency,
        memory_front_door=MEMORY_FRONT_DOOR,
        durable_memory_home=DURABLE_MEMORY_HOME,
        verified_reality_rule=VERIFIED_REALITY_RULE,
        ask_vs_act_rule=ASK_VS_ACT_RULE,
        escalation_approval_rule=str(answers["approval_boundary"]),
        durable_capture_rule=DURABLE_CAPTURE_RULE,
        calibration_too_heavy="anything that becomes noisier than helpful in real use",
        calibration_still_missed=str(answers["slips"]),
        calibration_lane_support="start by reviewing the foreground lanes first",
        calibration_add_remove_soften="make one small correction at a time after the first week of use",
    )
    return DaosPack(generator=generator, assistant_charter=charter, operating_profile=profile)
