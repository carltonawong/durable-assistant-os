from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class DaosReleaseFrontDoorTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_readme_leads_with_v02_cli_product_loop(self) -> None:
        readme = self.read("README.md")
        first_window = readme[:2500]

        self.assertIn("npx use-daos init", first_window)
        self.assertIn("npx use-daos setup", first_window)
        self.assertIn("npx use-daos check", first_window)
        self.assertIn("npx use-daos on", first_window)
        self.assertIn("npx use-daos reset-test", first_window)
        self.assertIn("npx use-daos", first_window)
        self.assertIn("DAOS Status", first_window)
        self.assertIn("DAOS On", first_window)
        self.assertIn("does **not** import arbitrary memory files", readme)
        self.assertIn("DAOS home is the folder with the DAOS pack/wiki", readme)
        self.assertIn("existing assistant home", readme)
        self.assertLess(readme.index("npx use-daos init"), readme.index("## Manual path"))

    def test_quickstart_leads_with_v02_cli_product_loop(self) -> None:
        quickstart = self.read("docs/quickstart.md")
        first_window = quickstart[:1800]

        self.assertIn("npx use-daos init", first_window)
        self.assertIn("npx use-daos setup", first_window)
        self.assertIn("npx use-daos check", first_window)
        self.assertIn("npx use-daos on", first_window)
        self.assertIn("npx use-daos reset-test", first_window)
        self.assertIn("npx use-daos", first_window)
        self.assertIn("DAOS Status", first_window)
        self.assertIn("DAOS On", first_window)
        self.assertIn("DAOS does not import arbitrary old memory files", quickstart)
        self.assertIn("DAOS_HOME=/path/to/existing-assistant-home", quickstart)
        self.assertIn("use-daos on /path/to/existing-assistant-home", quickstart)
        self.assertLess(quickstart.index("npx use-daos init"), quickstart.index("## Manual path"))

    def test_release_docs_do_not_expose_private_draft_language(self) -> None:
        release_facing_files = [
            "README.md",
            "docs/quickstart.md",
            "CHANGELOG.md",
            "docs/releases/v0.2.0.md",
            "docs/releases/v0.2.1.md",
            "docs/releases/v0.2.2.md",
            "docs/releases/v0.2.3.md",
            "docs/releases/v0.2.4.md",
            "docs/releases/v0.2.5.md",
            "docs/releases/v0.2.6.md",
        ]
        forbidden_terms = [
            "private draft",
            "do not publish",
            "Carlton approves",
            "0.2.0-private",
            "DAOS Context",
            "DAOS Files",
            "state report",
            "view state",
        ]
        offenders: list[str] = []
        for relative in release_facing_files:
            text = self.read(relative)
            for term in forbidden_terms:
                if term in text:
                    offenders.append(f"{relative} contains {term!r}")
        self.assertEqual(offenders, [])

    def test_package_metadata_is_ready_for_v02_release(self) -> None:
        package = json.loads(self.read("package.json"))

        self.assertEqual(package["name"], "use-daos")
        self.assertEqual(package["version"], "0.2.6")
        self.assertEqual(package["bin"], {"use-daos": "bin/use-daos.js"})
        self.assertEqual(package["license"], "Apache-2.0")
        self.assertEqual(package["homepage"], "https://github.com/carltonawong/durable-assistant-os#readme")
        self.assertEqual(
            package["repository"],
            {"type": "git", "url": "git+https://github.com/carltonawong/durable-assistant-os.git"},
        )
        self.assertEqual(package["bugs"], {"url": "https://github.com/carltonawong/durable-assistant-os/issues"})
        for keyword in ["ai-agents", "agent-memory", "context-engineering", "local-first", "markdown"]:
            self.assertIn(keyword, package["keywords"])
        self.assertNotIn("private", package)

    def test_changelog_and_release_note_cover_v02_safety_contract(self) -> None:
        combined = (
            self.read("CHANGELOG.md")
            + "\n"
            + self.read("docs/releases/v0.2.0.md")
            + "\n"
            + self.read("docs/releases/v0.2.1.md")
            + "\n"
            + self.read("docs/releases/v0.2.2.md")
            + "\n"
            + self.read("docs/releases/v0.2.3.md")
            + "\n"
            + self.read("docs/releases/v0.2.4.md")
            + "\n"
            + self.read("docs/releases/v0.2.5.md")
            + "\n"
            + self.read("docs/releases/v0.2.6.md")
        )
        required_phrases = [
            "npx use-daos init",
            "npx use-daos setup",
            "npx use-daos check",
            "npx use-daos on",
            "npx use-daos reset-test",
            "You're complete!",
            "DAOS On",
            "does not silently edit existing instruction files",
            "Arbitrary old memory content",
            "Packed-tarball smoke",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in combined]
        self.assertEqual(missing, [])

    def test_memory_docs_define_freshness_sensitive_claims(self) -> None:
        combined = self.read("README.md") + "\n" + self.read("docs/memory.md")

        required_phrases = [
            "freshness-sensitive",
            "release versions",
            "publish status",
            "branch/tag state",
            "runtime health",
            "test results",
            "live authority",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in combined]
        self.assertEqual(missing, [])

    def test_agent_integration_docs_define_deterministic_compaction_floor(self) -> None:
        integrations = self.read("docs/agent-integrations.md")
        changelog = self.read("CHANGELOG.md")
        combined = integrations + "\n" + changelog

        required_phrases = [
            "Deterministic compaction fallback",
            "before any context window is discarded",
            "must not depend on a second LLM call",
            "recent user asks",
            "recent tool/action state",
            "file/path mentions",
            "last dropped turns",
            "bounded and redacted",
            "continuity is degraded",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in combined]
        self.assertEqual(missing, [])

    def test_release_surfaces_do_not_leak_local_paths_or_old_baseline_notes(self) -> None:
        checked_files = [
            "README.md",
            "CHANGELOG.md",
            "docs/agent-integrations.md",
            "docs/maintenance.md",
            "docs/quickstart.md",
            "scripts/daos_core/__init__.py",
            "scripts/daos_core/parity.py",
            "scripts/daos_memory_parity.py",
            "scripts/daos_portability.py",
            "scripts/daos_update.py",
            "scripts/daos_validate.py",
            "tests/test_daos_memory_parity.py",
            "tests/test_daos_portability.py",
            "tests/test_script_safety.py",
        ]
        forbidden_patterns = [
            "/mnt/c/Users/openq",
            "C:\\Users\\openq",
            "/home/openq",
            "/home/carlton",
            "current public framework baseline is v0.1.6",
        ]
        offenders: list[str] = []
        for relative in checked_files:
            text = self.read(relative)
            for pattern in forbidden_patterns:
                if pattern in text:
                    offenders.append(f"{relative} contains {pattern!r}")
        self.assertEqual(offenders, [])

    def test_repo_reconciliation_safety_doc_stays_read_only_and_general(self) -> None:
        doc = self.read("docs/repo-reconciliation-safety.md")
        maintenance = self.read("docs/maintenance.md")

        required_phrases = [
            "read-only",
            "git status --short --branch",
            "git rev-list --left-right --count HEAD...origin/main",
            "git worktree list",
            "duplicate checkout",
            "inspect diffs",
            "archive non-destructively",
            "Do not run `git reset --hard`",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in doc]
        self.assertEqual(missing, [])
        self.assertIn("docs/repo-reconciliation-safety.md", maintenance)
        for private_term in ["/mnt/c/Users", "C:\\Users", "Hermes", "OpenClaw"]:
            self.assertNotIn(private_term, doc)

    def test_semantic_handoff_receipt_template_documents_runtime_fields(self) -> None:
        receipt = self.read("docs/semantic-handoff-receipt.md")
        integrations = self.read("docs/agent-integrations.md")

        required_phrases = [
            "work_object_identity",
            "active_source_of_truth",
            "last_verified_state",
            "current_user_ask",
            "nearby_confusion_set",
            "required_reanchor_checks",
            "status",
            "verified",
            "generated_fallback",
            "use-daos doctor --json",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in receipt]
        self.assertEqual(missing, [])
        self.assertIn("docs/semantic-handoff-receipt.md", integrations)
        self.assertNotIn("/mnt/c/Users", receipt)
        self.assertNotIn("Hermes", receipt)
        self.assertNotIn("OpenClaw", receipt)

    def test_reset_current_state_receipt_stays_small_and_actionable(self) -> None:
        receipt = self.read("docs/reset-current-state-receipt.md")
        readme = self.read("README.md")

        required_phrases = [
            "Objective:",
            "Last verified result:",
            "Approval boundary:",
            "Stale risk:",
            "Next action:",
            "Treat remembered status as orientation, not proof.",
            "Recheck freshness-sensitive facts against live authority.",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in receipt]
        self.assertEqual(missing, [])
        self.assertIn("docs/reset-current-state-receipt.md", readme)
        for private_term in ["/mnt/c/Users", "C:\\Users"]:
            self.assertNotIn(private_term, receipt)


if __name__ == "__main__":
    unittest.main()
