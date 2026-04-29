from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosHandoffTests(unittest.TestCase):
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

    def test_handoff_overwrites_reset_handoff_with_canonical_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_filled_pack(tmpdir)
            handoff_path = pack / "wiki" / "cache" / "reset-handoff.md"
            handoff_path.write_text("old diary entry that should be replaced\n", encoding="utf-8")

            result = self.run_cli(
                "handoff",
                str(pack),
                "--lane",
                "Harness",
                "--status",
                "fresh",
                "--why",
                "Need exact recovery point.",
                "--next",
                "Run reset-test against the pack.",
                "--verify",
                "python scripts/daos.py reset-test /path/to/pack",
            )
            content = handoff_path.read_text(encoding="utf-8")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS handoff written", result.stdout)
        self.assertNotIn("old diary entry", content)
        self.assertIn("# Reset Handoff", content)
        self.assertIn("**Lane:** Harness", content)
        self.assertIn("**Status:** fresh", content)
        self.assertIn("- Why this handoff exists: Need exact recovery point.", content)
        self.assertIn("- Exact next move: Run reset-test against the pack.", content)
        self.assertIn("- First verification: python scripts/daos.py reset-test /path/to/pack", content)
        self.assertIn("- If stale or contradicted: Re-read the current thread, hot cache, and verified files before continuing.", content)

    def test_handoff_rejects_blank_required_values(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_filled_pack(tmpdir)

            result = self.run_cli(
                "handoff",
                str(pack),
                "--lane",
                "Harness",
                "--status",
                "fresh",
                "--why",
                "Need exact recovery point.",
                "--next",
                "   ",
                "--verify",
                "python scripts/daos.py reset-test /path/to/pack",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS handoff failed", result.stderr)
        self.assertIn("--next must not be blank", result.stderr)

    def test_handoff_refuses_directory_that_does_not_look_like_daos_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "not-a-pack"
            target.mkdir()

            result = self.run_cli(
                "handoff",
                str(target),
                "--lane",
                "Harness",
                "--status",
                "fresh",
                "--why",
                "Need exact recovery point.",
                "--next",
                "Run reset-test against the pack.",
                "--verify",
                "python scripts/daos.py reset-test /path/to/pack",
            )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS handoff failed", result.stderr)
        self.assertIn("does not look like a DAOS pack", result.stderr)


if __name__ == "__main__":
    unittest.main()
