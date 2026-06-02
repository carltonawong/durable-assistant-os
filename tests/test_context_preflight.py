from __future__ import annotations

import unittest

from scripts.daos_core.context_preflight import (
    evaluate_action_preflight_policy,
    recover_reply_anchor_context,
)


class ContextPreflightTests(unittest.TestCase):
    def test_reply_anchor_recovers_context_after_session_rollover(self) -> None:
        result = recover_reply_anchor_context(
            {
                "session_boundary": "idle-expiry",
                "reply_anchor": {
                    "platform": "messaging-adapter",
                    "channel_id": "lane-a",
                    "message_id": "m-123",
                },
            },
            {
                "m-123": {
                    "lane": "release-work",
                    "summary": "fix the doctor runtime-proof next-step receipt",
                }
            },
            current_lane="general-chat",
        )

        self.assertEqual(result.recovered_context, "conflict")
        self.assertEqual(result.active_lane, "release-work")
        self.assertEqual(result.confidence, "medium")
        self.assertFalse(result.ask_for_reorientation)
        self.assertIn("using it over the current lane", result.resume_receipt)
        self.assertIn("reply-anchor-overrode-current-lane", result.notes)

    def test_missing_reply_anchor_after_rollover_requests_one_reorientation(self) -> None:
        result = recover_reply_anchor_context(
            {"session_boundary": "process-restart", "channel_lane": "support"},
            {},
            current_lane=None,
        )

        self.assertEqual(result.recovered_context, "missing")
        self.assertEqual(result.active_lane, "support")
        self.assertEqual(result.confidence, "low")
        self.assertTrue(result.ask_for_reorientation)
        self.assertIn("No reply anchor", result.resume_receipt)

    def test_unresolved_reply_anchor_reports_low_confidence_without_private_paths(self) -> None:
        result = recover_reply_anchor_context(
            {
                "session_boundary": "compression",
                "reply_anchor": {"platform": "messaging-adapter", "message_id": "missing"},
            },
            {},
            current_lane="ops",
        )

        self.assertEqual(result.recovered_context, "missing")
        self.assertEqual(result.confidence, "low")
        self.assertTrue(result.ask_for_reorientation)
        self.assertNotIn("local-cache-path", result.resume_receipt)
        self.assertNotIn("private-transcript-store", result.resume_receipt)

    def test_durable_action_policy_blocks_silent_sensitive_violation(self) -> None:
        result = evaluate_action_preflight_policy(
            "login-sensitive",
            {
                "login-sensitive": {
                    "preference": "Use the signed-in visible profile by default.",
                    "default_action": "visible-browser-profile",
                    "exception_rule": "Headless requires explicit override unless read-only and known safe.",
                    "sensitive": True,
                }
            },
            requested_action="headless-browser",
        )

        self.assertTrue(result.blocked)
        self.assertTrue(result.needs_confirmation)
        self.assertEqual(result.default_action, "visible-browser-profile")
        self.assertEqual(result.selected_action, "headless-browser")
        self.assertIn("Blocked", result.receipt)

    def test_durable_action_policy_survives_reset_as_data_not_warm_session_state(self) -> None:
        policies = {
            "public-posting": {
                "preference": "Use the operator-approved browser/profile path before public posts.",
                "default_action": "approved-public-posting-path",
                "exception_rule": "Alternate mode needs explicit approval.",
                "sensitive": True,
            }
        }

        first_turn = evaluate_action_preflight_policy("public-posting", policies)
        after_rollover = evaluate_action_preflight_policy(
            "public-posting",
            policies,
            requested_action="unapproved-fallback",
        )

        self.assertEqual(first_turn.selected_action, "approved-public-posting-path")
        self.assertFalse(first_turn.blocked)
        self.assertTrue(after_rollover.blocked)
        self.assertIn("durable-policy-violation", after_rollover.notes)

    def test_memory_evidence_does_not_grant_sensitive_action_permission(self) -> None:
        result = evaluate_action_preflight_policy(
            "public-posting",
            {
                "public-posting": {
                    "preference": "Use approved visible/publication path for public posts.",
                    "default_action": "approved-publication-path",
                    "exception_rule": "Alternate publication path needs explicit approval.",
                    "sensitive": True,
                }
            },
            requested_action="remembered-shortcut-path",
            memory_evidence="Prior memory says the shortcut was okay last time.",
        )

        self.assertTrue(result.blocked)
        self.assertTrue(result.needs_confirmation)
        self.assertIn("Memory evidence was context, not permission.", result.receipt)
        self.assertIn("memory-evidence-not-permission", result.notes)

    def test_read_only_exception_is_explicit_and_non_mutating(self) -> None:
        result = evaluate_action_preflight_policy(
            "login-sensitive",
            {
                "login-sensitive": {
                    "preference": "Use approved interactive path for mutations.",
                    "default_action": "interactive-profile",
                    "exception_rule": "Read-only inspection may use a non-interactive path.",
                    "sensitive": True,
                }
            },
            requested_action="read-only-adapter",
            read_only=True,
        )

        self.assertFalse(result.blocked)
        self.assertFalse(result.needs_confirmation)
        self.assertIn("read-only exception", result.receipt)


if __name__ == "__main__":
    unittest.main()
