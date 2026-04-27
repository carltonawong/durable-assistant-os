from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class DaosNpmPackagePayloadTests(unittest.TestCase):
    def npm_pack_dry_run(self) -> dict:
        result = subprocess.run(
            ["npm", "pack", "--dry-run", "--json"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 1)
        return payload[0]

    def test_npm_package_contains_runtime_payload_without_test_or_cache_bloat(self) -> None:
        package = self.npm_pack_dry_run()
        paths = {entry["path"] for entry in package["files"]}

        required_paths = {
            "package.json",
            "README.md",
            "LICENSE",
            "CHANGELOG.md",
            "bin/daos.js",
            "docs/memory-parity-auditor.md",
            "docs/releases/v0.2.0.md",
            "docs/script-safety.md",
            "examples/creative-studio-operating-profile-example.md",
            "harness/core-setup.md",
            "harness/first-week.md",
            "scripts/daos.py",
            "scripts/daos_bootstrap.py",
            "scripts/daos_core/__init__.py",
            "scripts/daos_core/harness.py",
            "scripts/daos_core/render.py",
            "scripts/daos_core/schema.py",
            "scripts/daos_core/validate.py",
            "starter-pack/AGENTS.md",
            "starter-pack/wiki/cache/hot-cache.md",
            "starter-pack/wiki/cache/hot-cache-log.md",
            "starter-pack/wiki/cache/reset-handoff.md",
            "starter-pack/wiki/cache/agent-continuity.md",
        }
        missing = sorted(required_paths - paths)
        self.assertEqual(missing, [], "npm package is missing runtime payload files")

        forbidden_prefixes = ("tests/", "docs/assets/")
        forbidden_fragments = ("__pycache__", ".pyc")
        offenders = sorted(
            path
            for path in paths
            if path.startswith(forbidden_prefixes) or any(fragment in path for fragment in forbidden_fragments)
        )
        self.assertEqual(offenders, [], "npm package includes test/cache/asset bloat")

    def test_npm_package_stays_small_enough_for_preview_distribution(self) -> None:
        package = self.npm_pack_dry_run()

        self.assertLessEqual(package["entryCount"], 70)
        self.assertLessEqual(package["size"], 100_000)


if __name__ == "__main__":
    unittest.main()
