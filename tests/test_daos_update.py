from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
UPDATE_SCRIPT = REPO_ROOT / "scripts" / "daos_update.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosUpdateScriptTests(unittest.TestCase):
    def run_bootstrap(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(BOOTSTRAP_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_update(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(UPDATE_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_check_reports_manifest_and_metadata_gaps_for_manifestless_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "legacy-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            (destination / "daos-pack.json").unlink()

            result = self.run_update("check", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("manifest: missing", result.stdout)
            self.assertIn("upgrade_ready: yes", result.stdout)
            self.assertIn("missing managed metadata anchor", result.stdout)

    def test_check_reports_metadata_status_for_generated_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "generated-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_update("check", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("manifest: present", result.stdout)
            self.assertIn("schema_version: 1", result.stdout)
            self.assertIn("framework_version: 0.1.0-alpha3", result.stdout)
            self.assertRegex(result.stdout, r"pack_id: [0-9a-f-]+")
            self.assertIn("upgrade_ready: stable", result.stdout)

    def test_plan_never_proposes_overwriting_user_owned_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "plan-pack"
            bootstrap = self.run_bootstrap(str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_update("plan", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("do not overwrite assistant-charter.md", result.stdout)
            self.assertIn("do not overwrite operating-profile.md", result.stdout)
            self.assertIn("managed metadata only", result.stdout)


if __name__ == "__main__":
    unittest.main()
