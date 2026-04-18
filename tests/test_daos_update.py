from __future__ import annotations

import json
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

    def test_apply_creates_manifest_and_records_migration_for_manifestless_pack(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "legacy-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            (destination / "daos-pack.json").unlink()
            original_charter = (destination / "assistant-charter.md").read_text(encoding="utf-8")

            result = self.run_update("apply", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            manifest = json.loads((destination / "daos-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], "1")
            self.assertEqual(manifest["framework_version"], "0.1.0-alpha3")
            self.assertTrue(manifest["pack_id"])
            self.assertEqual((destination / "assistant-charter.md").read_text(encoding="utf-8"), original_charter)
            self.assertTrue((destination / ".daos" / "migrations").is_dir())
            migration_files = list((destination / ".daos" / "migrations").glob("*.json"))
            self.assertEqual(len(migration_files), 1)
            record = json.loads(migration_files[0].read_text(encoding="utf-8"))
            self.assertIn("created daos-pack.json", record["actions"])
            self.assertIn("wrote .daos/manifest.json", record["actions"])

    def test_apply_repairs_metadata_gaps_and_backs_up_existing_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "partial-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            manifest_path = destination / "daos-pack.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest.pop("framework_version", None)
            manifest.pop("pack_id", None)
            manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

            result = self.run_update("apply", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            updated_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(updated_manifest["framework_version"], "0.1.0-alpha3")
            self.assertTrue(updated_manifest["pack_id"])
            backup_files = list((destination / ".daos" / "backups").glob("**/daos-pack.json"))
            self.assertGreaterEqual(len(backup_files), 1)


if __name__ == "__main__":
    unittest.main()
