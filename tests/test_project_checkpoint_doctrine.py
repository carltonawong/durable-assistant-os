from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class ProjectCheckpointDoctrineTests(unittest.TestCase):
    REQUIRED_PHRASES = [
        "project checkpoint",
        "infrastructure",
        "data ownership",
        "provider/tool/account choice",
        "deployment/runtime mode",
        "live-vs-dry-run",
        "source of truth",
        "what not to assume",
        "next blocker",
    ]

    REQUIRED_FILES = [
        "harness/mandatory-baseline.md",
        "harness/core-setup.md",
        "docs/memory.md",
        "docs/public-memory-page.md",
        "templates/operating-profile-template.md",
        "templates/cadence-review-template.md",
        "starter-pack/AGENTS.md",
        "starter-pack/wiki/WIKI.md",
        "starter-pack/wiki/cache/MEMORY-OPERATING-MODEL.md",
        "starter-pack/operating-profile.md",
        "starter-pack/cadence-review.md",
        "examples/starter-pack-example/operating-profile.md",
        "examples/starter-pack-example/cadence-review.md",
    ]

    def test_project_checkpoint_doctrine_is_installed_across_public_surfaces(self) -> None:
        for relative_path in self.REQUIRED_FILES:
            with self.subTest(path=relative_path):
                text = (REPO_ROOT / relative_path).read_text(encoding="utf-8").lower()
                self.assertIn("project checkpoint", text)

    def test_mandatory_baseline_defines_checkpoint_contract(self) -> None:
        text = (REPO_ROOT / "harness" / "mandatory-baseline.md").read_text(encoding="utf-8").lower()
        for phrase in self.REQUIRED_PHRASES:
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, text)

    def test_checkpoint_doctrine_stays_generic(self) -> None:
        public_paths = [
            "harness/mandatory-baseline.md",
            "harness/core-setup.md",
            "docs/memory.md",
            "docs/public-memory-page.md",
            "templates/operating-profile-template.md",
            "templates/cadence-review-template.md",
            "starter-pack/AGENTS.md",
            "starter-pack/wiki/WIKI.md",
            "starter-pack/wiki/cache/MEMORY-OPERATING-MODEL.md",
        ]
        forbidden_project_specific_terms = ["restoreline", "supabase", "render"]
        for relative_path in public_paths:
            text = (REPO_ROOT / relative_path).read_text(encoding="utf-8").lower()
            for term in forbidden_project_specific_terms:
                with self.subTest(path=relative_path, term=term):
                    self.assertNotIn(term, text)


if __name__ == "__main__":
    unittest.main()
