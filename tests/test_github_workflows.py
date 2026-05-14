from __future__ import annotations

import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "ci.yml"


class GithubWorkflowTests(unittest.TestCase):
    def test_ci_workflow_enforces_core_daos_gates(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8")

        self.assertIn("pull_request:", text)
        self.assertIn("branches: [main]", text)
        self.assertIn("permissions:", text)
        self.assertIn("contents: read", text)
        self.assertIn("python -m unittest discover -s tests -v", text)
        self.assertIn("npm run test:wrapper", text)
        self.assertIn("npm run test:package", text)
        self.assertIn("npm run test:pack-install", text)
        self.assertIn("npm run test:release-front-door", text)
        self.assertIn("npm pack --dry-run --json", text)

    def test_ci_workflow_does_not_publish_or_request_write_permissions(self) -> None:
        text = WORKFLOW.read_text(encoding="utf-8").lower()

        forbidden = [
            "npm publish",
            "gh release create",
            "contents: write",
            "packages: write",
            "id-token: write",
        ]
        for phrase in forbidden:
            self.assertNotIn(phrase, text)


if __name__ == "__main__":
    unittest.main()
