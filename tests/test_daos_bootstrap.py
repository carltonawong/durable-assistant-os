from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosBootstrapScriptTests(unittest.TestCase):
    def run_script(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(SCRIPT_PATH), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_blank_starter_pack_copy_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "blank-pack"
            result = self.run_script(str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((destination / "README.md").exists())
            self.assertTrue((destination / "assistant-charter.md").exists())
            self.assertIn("blank starter-pack", result.stdout)

    def test_filled_example_copy_succeeds(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "filled-pack"
            result = self.run_script("--filled-example", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((destination / "operating-profile.md").exists())
            self.assertTrue((destination / "wiki" / "cache" / "HOT-CACHE-SPEC.md").exists())
            self.assertTrue((destination / "AGENTS.md").exists())
            self.assertIn("filled starter-pack example", result.stdout)

    def test_generated_pack_includes_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "manifest-pack"

            result = self.run_script(str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            manifest = json.loads((destination / "daos-pack.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["schema_version"], "1")
            self.assertEqual(manifest["pack_kind"], "starter-pack")
            self.assertEqual(manifest["generator"], "scripts/daos_bootstrap.py")
            self.assertEqual(manifest["framework_version"], "v0.2.3")
            self.assertTrue(manifest["pack_id"])

    def test_non_empty_destination_fails_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "occupied"
            destination.mkdir()
            (destination / "keep.txt").write_text("leave me", encoding="utf-8")

            result = self.run_script(str(destination))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Use --force to replace it", result.stderr)
            self.assertTrue((destination / "keep.txt").exists())

    def test_force_replaces_existing_destination(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "replace-me"
            destination.mkdir()
            (destination / "assistant-charter.md").write_text("# old charter\n", encoding="utf-8")
            (destination / "operating-profile.md").write_text("# old profile\n", encoding="utf-8")
            (destination / "old.txt").write_text("old", encoding="utf-8")

            result = self.run_script("--force", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertFalse((destination / "old.txt").exists())
            self.assertTrue((destination / "README.md").exists())

    def test_force_refuses_non_daos_directory_without_explicit_override(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "ordinary-folder"
            destination.mkdir()
            (destination / "keep.txt").write_text("keep", encoding="utf-8")

            result = self.run_script("--force", str(destination))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("refusing to delete a non-DAOS directory", result.stderr)
            self.assertTrue((destination / "keep.txt").exists())


if __name__ == "__main__":
    unittest.main()
