from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosOrientTests(unittest.TestCase):
    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(CLI_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_bootstrap(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(BOOTSTRAP_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_orient_outputs_read_order_and_live_reality_rule(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "filled-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_cli("orient", str(destination), "--task", "resume DAOS harness build")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("# DAOS Orientation Bundle", result.stdout)
        self.assertIn("Current task: resume DAOS harness build", result.stdout)
        self.assertIn("1. Local thread / current user request", result.stdout)
        self.assertIn("2. `wiki/cache/hot-cache.md`", result.stdout)
        self.assertIn("3. `wiki/cache/reset-handoff.md`", result.stdout)
        self.assertIn("4. `wiki/cache/agent-continuity.md`", result.stdout)
        self.assertIn("assistant-charter.md", result.stdout)
        self.assertIn("operating-profile.md", result.stdout)
        self.assertIn("Verify live reality before acting on stale memory", result.stdout)

    def test_orient_warns_but_still_outputs_when_pack_has_validation_warnings(self) -> None:
        result = self.run_cli("orient", "examples/starter-pack-example")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("validation warnings:", result.stdout)
        self.assertIn("daos-pack.json is missing", result.stdout)
        self.assertIn("# DAOS Orientation Bundle", result.stdout)

    def test_orient_fails_for_missing_pack(self) -> None:
        result = self.run_cli("orient", "/tmp/daos-pack-that-does-not-exist")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS orient failed", result.stderr)
        self.assertIn("Pack directory does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
