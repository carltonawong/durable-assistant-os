from __future__ import annotations

import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class HotCacheWriterDocsTests(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (REPO_ROOT / relative_path).read_text(encoding="utf-8")

    def test_starter_pack_defines_single_writer_boundary(self) -> None:
        agents = self.read("starter-pack/AGENTS.md")
        spec = self.read("starter-pack/wiki/cache/HOT-CACHE-SPEC.md")
        model = self.read("starter-pack/wiki/cache/MEMORY-OPERATING-MODEL.md")
        wiki = self.read("starter-pack/wiki/WIKI.md")
        harness = self.read("harness/mandatory-baseline.md")
        combined = agents + "\n" + spec + "\n" + model + "\n" + wiki + "\n" + harness

        required_phrases = [
            "many-reader / single-writer",
            "configured hot-cache maintainer",
            "durable ingress",
            "untrusted evidence",
            "whole-file",
            "cursor unchanged",
            "non-blocking",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in combined]
        self.assertEqual(missing, [])

    def test_schedule_is_optional_and_retry_safe(self) -> None:
        maintenance = self.read("docs/maintenance.md")
        model = self.read("starter-pack/wiki/cache/MEMORY-OPERATING-MODEL.md")
        combined = maintenance + "\n" + model

        required_phrases = [
            "15-minute",
            "7,22,37,52",
            "not a universal",
            "deterministic no-work precheck",
            "committed cursor",
            "leave cache, log, and cursor unchanged",
            "must never delay an interactive response",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in combined]
        self.assertEqual(missing, [])

    def test_hermes_guard_is_generic_and_behavior_verified(self) -> None:
        integrations = self.read("docs/agent-integrations.md")

        required_phrases = [
            "pre_tool_call",
            "writer identity predicate",
            "file writes, patches, shell commands, or code execution",
            "needs_llm: false",
            "wakeAgent: false",
            "plugin enabled and discovered",
            "behavior proven through real dispatch",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in integrations]
        self.assertEqual(missing, [])
        private_patterns = [
            r"/mnt/c/Users/[^/<]+",
            r"C:\\Users\\[^\\<]+",
            r"\b[0-9a-f]{12}\b",
        ]
        for pattern in private_patterns:
            self.assertIsNone(re.search(pattern, integrations))


if __name__ == "__main__":
    unittest.main()
