from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosCliTests(unittest.TestCase):
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

    def test_help_lists_only_shipped_commands_without_previewing_unshipped_commands(self) -> None:
        result = self.run_cli("--help")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("check", result.stdout)
        self.assertIn("orient", result.stdout)
        self.assertIn("reset-test", result.stdout)
        self.assertNotIn("handoff", result.stdout)
        self.assertNotIn("memory-audit", result.stdout)

    def test_check_passes_on_filled_example_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "filled-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_cli("check", str(destination))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS check passed", result.stdout)
        self.assertIn("errors: 0", result.stdout)
        self.assertIn("warnings:", result.stdout)

    def test_check_fails_on_unfilled_starter_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "blank-pack"
            bootstrap = self.run_bootstrap(str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_cli("check", str(destination))

        self.assertNotEqual(result.returncode, 0)
        combined_output = result.stdout + result.stderr
        self.assertIn("DAOS check failed", combined_output)
        self.assertIn("empty required field", combined_output)
        self.assertIn("next:", combined_output)


if __name__ == "__main__":
    unittest.main()
