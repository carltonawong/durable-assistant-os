from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class ArtifactRecallGuardDocsTests(unittest.TestCase):
    def test_public_memory_docs_include_artifact_recall_guard(self) -> None:
        text = (REPO_ROOT / "docs" / "memory.md").read_text(encoding="utf-8")

        self.assertIn("## Prior artifact recall", text)
        self.assertIn("the identifier is not in the local thread", text)
        self.assertIn("search targeted session/wiki/source records", text)
        self.assertIn("verify the live URL, repo, or file", text)
        self.assertIn("hot cache or familiar memory alone", text)

    def test_starter_pack_cache_spec_names_hot_cache_as_routing_hint(self) -> None:
        text = (REPO_ROOT / "starter-pack" / "wiki" / "cache" / "HOT-CACHE-SPEC.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("### Artifact recall guard", text)
        self.assertIn("Hot cache is a routing hint, not an artifact registry.", text)
        self.assertIn("demo/preview URLs", text)
        self.assertIn("answer with the verified identifier", text)


if __name__ == "__main__":
    unittest.main()
