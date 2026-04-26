from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"

FILLED_RESET_HANDOFF = """# Reset Handoff

Use this as the named DAOS reset/wake-up continuity artifact.

If anything here conflicts with verified files, runtime state, or durable wiki pages, verify first and prefer reality.

## Current Handoff
**Last updated:** 2026-04-26 14:30 PDT  
**Updated by:** Test  
**Lane:** Harness  
**Status:** fresh

- Why this handoff exists: Verify deterministic reset recovery.
- Exact next move: Run the DAOS check command against the active pack.
- First verification: python scripts/daos.py check /path/to/pack
- If stale or contradicted: Re-read hot cache and verify files before continuing.

## Editing rules
- overwrite instead of append
"""


class DaosResetTestTests(unittest.TestCase):
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

    def make_filled_pack(self, tmpdir: str) -> Path:
        destination = Path(tmpdir) / "filled-pack"
        bootstrap = self.run_bootstrap("--filled-example", str(destination))
        self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
        return destination

    def test_reset_test_passes_when_exact_handoff_and_front_door_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_filled_pack(tmpdir)
            (pack / "wiki" / "cache" / "reset-handoff.md").write_text(FILLED_RESET_HANDOFF, encoding="utf-8")

            result = self.run_cli("reset-test", str(pack))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS reset test passed", result.stdout)
        self.assertIn("exact next move: Run the DAOS check command against the active pack.", result.stdout)
        self.assertIn("first verification: python scripts/daos.py check /path/to/pack", result.stdout)
        self.assertIn("Verify live reality before acting on stale memory", result.stdout)

    def test_reset_test_fails_when_reset_handoff_has_no_exact_next_move(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_filled_pack(tmpdir)
            (pack / "wiki" / "cache" / "reset-handoff.md").write_text(
                FILLED_RESET_HANDOFF.replace(
                    "- Exact next move: Run the DAOS check command against the active pack.",
                    "- Exact next move:",
                ),
                encoding="utf-8",
            )

            result = self.run_cli("reset-test", str(pack))

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS reset test failed", result.stderr)
        self.assertIn("reset-handoff.md has no filled Exact next move", result.stderr)

    def test_reset_test_fails_when_pack_is_missing(self) -> None:
        result = self.run_cli("reset-test", "/tmp/daos-reset-test-missing-pack")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS reset test failed", result.stderr)
        self.assertIn("Pack directory does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
