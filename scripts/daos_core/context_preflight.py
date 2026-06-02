"""Read-only adapter preflight helpers for DAOS context continuity.

These helpers are intentionally small and runtime-agnostic. They do not fetch
messages, open browsers, call networks, or mutate memory. Adapters can call
them after collecting their own local payload/evidence to make reply-anchor
recovery and durable preference enforcement testable.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


SENSITIVE_ACTION_CLASSES = {
    "login-sensitive",
    "public-posting",
    "social-posting",
    "browser-login",
}


@dataclass(frozen=True)
class ContextAnchor:
    """Platform-supplied pointer to the message/thread being answered."""

    platform: str = "unknown"
    channel_id: str | None = None
    thread_id: str | None = None
    message_id: str | None = None
    quoted_text: str | None = None

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> "ContextAnchor | None":
        if not value:
            return None
        message_id = _clean(value.get("message_id") or value.get("id"))
        quoted_text = _clean(value.get("quoted_text") or value.get("quoted_summary") or value.get("summary"))
        if not message_id and not quoted_text:
            return None
        return cls(
            platform=_clean(value.get("platform")) or "unknown",
            channel_id=_clean(value.get("channel_id")),
            thread_id=_clean(value.get("thread_id")),
            message_id=message_id,
            quoted_text=quoted_text,
        )

    def as_dict(self) -> dict[str, str | None]:
        return {
            "platform": self.platform,
            "channel_id": self.channel_id,
            "thread_id": self.thread_id,
            "message_id": self.message_id,
            "quoted_text": self.quoted_text,
        }


@dataclass(frozen=True)
class ContextRecoveryResult:
    context_anchor: ContextAnchor | None
    session_boundary: str
    recovered_context: str
    confidence: str
    active_lane: str | None
    resume_receipt: str
    ask_for_reorientation: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "context_anchor": self.context_anchor.as_dict() if self.context_anchor else None,
            "session_boundary": self.session_boundary,
            "recovered_context": self.recovered_context,
            "confidence": self.confidence,
            "active_lane": self.active_lane,
            "resume_receipt": self.resume_receipt,
            "ask_for_reorientation": self.ask_for_reorientation,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class ActionPolicyResult:
    task_class: str
    preference: str | None
    selected_action: str | None
    default_action: str | None
    exception_rule: str | None
    receipt: str
    blocked: bool = False
    needs_confirmation: bool = False
    notes: tuple[str, ...] = field(default_factory=tuple)

    def as_dict(self) -> dict[str, Any]:
        return {
            "task_class": self.task_class,
            "preference": self.preference,
            "selected_action": self.selected_action,
            "default_action": self.default_action,
            "exception_rule": self.exception_rule,
            "receipt": self.receipt,
            "blocked": self.blocked,
            "needs_confirmation": self.needs_confirmation,
            "notes": list(self.notes),
        }


def recover_reply_anchor_context(
    payload: Mapping[str, Any],
    local_context_index: Mapping[str, Mapping[str, Any]],
    *,
    current_lane: str | None = None,
) -> ContextRecoveryResult:
    """Resolve a platform reply/thread anchor before broader memory fallback.

    ``payload`` is the adapter-collected event. If it contains a ``reply_anchor``
    with a message id, the local index is checked first. If the anchor resolves
    to a different lane than the current hot lane, the explicit reply anchor wins
    for this turn and the result records a conflict.
    """

    session_boundary = _clean(payload.get("session_boundary")) or "none"
    anchor = ContextAnchor.from_mapping(_mapping(payload.get("reply_anchor") or payload.get("context_anchor")))

    if anchor is None:
        fallback_lane = _clean(payload.get("channel_lane")) or current_lane
        return ContextRecoveryResult(
            context_anchor=None,
            session_boundary=session_boundary,
            recovered_context="missing",
            confidence="low" if session_boundary != "none" else "medium",
            active_lane=fallback_lane,
            resume_receipt="No reply anchor was available; using channel/lane context only.",
            ask_for_reorientation=session_boundary != "none",
            notes=("anchor-missing",),
        )

    recovered = local_context_index.get(anchor.message_id or "") if anchor.message_id else None
    if recovered is None:
        if anchor.quoted_text:
            return ContextRecoveryResult(
                context_anchor=anchor,
                session_boundary=session_boundary,
                recovered_context="quoted-only",
                confidence="medium",
                active_lane=current_lane,
                resume_receipt="Recovered the quoted reply text, but not the full prior local context.",
                ask_for_reorientation=False,
                notes=("full-anchor-context-missing",),
            )
        return ContextRecoveryResult(
            context_anchor=anchor,
            session_boundary=session_boundary,
            recovered_context="missing",
            confidence="low",
            active_lane=current_lane,
            resume_receipt="The reply anchor was present but the prior local context was not available.",
            ask_for_reorientation=True,
            notes=("anchor-unresolved",),
        )

    recovered_lane = _clean(recovered.get("lane")) or current_lane
    summary = _clean(recovered.get("summary")) or _clean(recovered.get("text")) or "the anchored prior message"
    conflict = bool(current_lane and recovered_lane and recovered_lane != current_lane)
    if conflict:
        return ContextRecoveryResult(
            context_anchor=anchor,
            session_boundary=session_boundary,
            recovered_context="conflict",
            confidence="medium",
            active_lane=recovered_lane,
            resume_receipt=f"Recovered reply-anchor context for {recovered_lane}; using it over the current lane for this turn.",
            ask_for_reorientation=False,
            notes=("reply-anchor-overrode-current-lane", summary),
        )

    return ContextRecoveryResult(
        context_anchor=anchor,
        session_boundary=session_boundary,
        recovered_context="found",
        confidence="high",
        active_lane=recovered_lane,
        resume_receipt=f"Recovered reply-anchor context for {recovered_lane or 'this lane'}: {summary}",
        ask_for_reorientation=False,
    )


def evaluate_action_preflight_policy(
    task_class: str,
    policies: Mapping[str, Mapping[str, Any]],
    *,
    requested_action: str | None = None,
    explicit_override: bool = False,
    read_only: bool = False,
    memory_evidence: str | None = None,
) -> ActionPolicyResult:
    """Convert a durable action preference into a tool-selection preflight.

    Policies are keyed by task class and remain user/runtime supplied. DAOS does
    not hardcode one person's browser or posting preference as a universal rule.
    A policy may include ``preference``, ``default_action``, and
    ``exception_rule`` fields.

    ``memory_evidence`` is context, not permission; sensitive deviations still
    require explicit override or a read-only exception.
    """

    task_class = _clean(task_class) or "unknown"
    memory_evidence = _clean(memory_evidence)
    policy = policies.get(task_class) or policies.get("*") or {}
    preference = _clean(policy.get("preference"))
    default_action = _clean(policy.get("default_action"))
    exception_rule = _clean(policy.get("exception_rule"))
    selected = _clean(requested_action) or default_action

    if not policy:
        return ActionPolicyResult(
            task_class=task_class,
            preference=None,
            selected_action=selected,
            default_action=None,
            exception_rule=None,
            receipt=f"No durable action policy matched {task_class}; using the requested/default path.",
            notes=("policy-missing",),
        )

    violating = bool(default_action and selected and selected != default_action)
    sensitive = task_class in SENSITIVE_ACTION_CLASSES or bool(policy.get("sensitive"))

    if violating and sensitive and not explicit_override and not read_only:
        extra_notes = ("memory-evidence-not-permission",) if memory_evidence else ()
        evidence_clause = " Memory evidence was context, not permission." if memory_evidence else ""
        return ActionPolicyResult(
            task_class=task_class,
            preference=preference,
            selected_action=selected,
            default_action=default_action,
            exception_rule=exception_rule,
            receipt=f"Blocked {selected}; durable policy for {task_class} defaults to {default_action}.{evidence_clause}",
            blocked=True,
            needs_confirmation=True,
            notes=("durable-policy-violation", *extra_notes),
        )

    if violating and not explicit_override and read_only:
        return ActionPolicyResult(
            task_class=task_class,
            preference=preference,
            selected_action=selected,
            default_action=default_action,
            exception_rule=exception_rule,
            receipt=f"Using read-only exception for {selected}; durable default remains {default_action}.",
            blocked=False,
            needs_confirmation=False,
            notes=("read-only-exception",),
        )

    if violating and explicit_override:
        return ActionPolicyResult(
            task_class=task_class,
            preference=preference,
            selected_action=selected,
            default_action=default_action,
            exception_rule=exception_rule,
            receipt=f"Using explicit override {selected}; durable default is {default_action}.",
            blocked=False,
            needs_confirmation=False,
            notes=("explicit-override",),
        )

    return ActionPolicyResult(
        task_class=task_class,
        preference=preference,
        selected_action=selected,
        default_action=default_action,
        exception_rule=exception_rule,
        receipt=f"Using durable policy for {task_class}: {selected}.",
        blocked=False,
        needs_confirmation=False,
    )


def _mapping(value: Any) -> Mapping[str, Any] | None:
    return value if isinstance(value, Mapping) else None


def _clean(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
