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

        self.assertIn("npx daos init", first_window)
        self.assertIn("npx daos setup", first_window)
        self.assertIn("npx daos check", first_window)
        self.assertIn("npx daos on", first_window)
        self.assertIn("npx daos reset-test", first_window)
        self.assertIn("npx daos", first_window)
        self.assertIn("DAOS Status", first_window)
        self.assertIn("DAOS On", first_window)
        self.assertIn("does **not** import arbitrary memory files", readme)
        self.assertIn("DAOS home is the folder with the DAOS pack/wiki", readme)
        self.assertIn("existing assistant home", readme)
        self.assertLess(readme.index("npx daos init"), readme.index("## Manual path"))

    def test_quickstart_leads_with_v02_cli_product_loop(self) -> None:
        quickstart = self.read("docs/quickstart.md")
        first_window = quickstart[:1800]

        self.assertIn("npx daos init", first_window)
        self.assertIn("npx daos setup", first_window)
        self.assertIn("npx daos check", first_window)
        self.assertIn("npx daos on", first_window)
        self.assertIn("npx daos reset-test", first_window)
        self.assertIn("npx daos", first_window)
        self.assertIn("DAOS Status", first_window)
        self.assertIn("DAOS On", first_window)
        self.assertIn("DAOS does not import arbitrary old memory files", quickstart)
        self.assertIn("DAOS_HOME=/path/to/existing-assistant-home", quickstart)
        self.assertIn("daos on /path/to/existing-assistant-home", quickstart)
        self.assertLess(quickstart.index("npx daos init"), quickstart.index("## Manual path"))

    def test_release_docs_do_not_expose_private_draft_language(self) -> None:
        release_facing_files = [
            "README.md",
            "docs/quickstart.md",
            "CHANGELOG.md",
            "docs/releases/v0.2.0.md",
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

        self.assertEqual(package["version"], "0.2.0")
        self.assertNotIn("private", package)

    def test_changelog_and_release_note_cover_v02_safety_contract(self) -> None:
        combined = self.read("CHANGELOG.md") + "\n" + self.read("docs/releases/v0.2.0.md")
        required_phrases = [
            "npx daos init",
            "npx daos setup",
            "npx daos check",
            "npx daos on",
            "npx daos reset-test",
            "You're complete!",
            "DAOS On",
            "does not silently edit existing instruction files",
            "Arbitrary old memory content",
            "Packed-tarball smoke",
        ]
        missing = [phrase for phrase in required_phrases if phrase not in combined]
        self.assertEqual(missing, [])


if __name__ == "__main__":
    unittest.main()
