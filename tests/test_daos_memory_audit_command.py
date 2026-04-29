from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosMemoryAuditCommandTests(unittest.TestCase):
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

    def test_memory_audit_reports_core_memory_surfaces(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_filled_pack(tmpdir)

            result = self.run_cli("memory-audit", str(pack))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS memory audit", result.stdout)
        self.assertIn("wiki/cache/hot-cache.md: present", result.stdout)
        self.assertIn("wiki/cache/hot-cache-log.md: present", result.stdout)
        self.assertIn("wiki/cache/reset-handoff.md: present", result.stdout)
        self.assertIn("wiki/cache/agent-continuity.md: present", result.stdout)
        self.assertIn("wiki/index.md: present", result.stdout)
        self.assertIn("wiki/raw/: present", result.stdout)
        self.assertIn("wiki/sources/: present", result.stdout)

    def test_memory_audit_warns_when_reset_handoff_is_missing(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_filled_pack(tmpdir)
            (pack / "wiki" / "cache" / "reset-handoff.md").unlink()

            result = self.run_cli("memory-audit", str(pack))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("warnings:", result.stdout)
        self.assertIn("wiki/cache/reset-handoff.md is missing", result.stdout)

    def test_memory_audit_fails_for_missing_pack(self) -> None:
        result = self.run_cli("memory-audit", "/tmp/daos-memory-audit-missing-pack")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS memory audit failed", result.stderr)
        self.assertIn("Pack directory does not exist", result.stderr)


if __name__ == "__main__":
    unittest.main()
