from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "daos_validate.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosValidateScriptTests(unittest.TestCase):
    def run_validate(self, pack_dir: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(VALIDATE_SCRIPT), str(pack_dir)],
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

    def test_blank_starter_pack_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "blank-pack"
            bootstrap = self.run_bootstrap(str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_validate(destination)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("empty required field", result.stderr)

    def test_filled_example_passes_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "filled-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_validate(destination)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("validation passed", result.stdout)

    def test_missing_required_file_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack_dir = Path(tmpdir) / "broken-pack"
            pack_dir.mkdir()
            (pack_dir / "assistant-charter.md").write_text("# Assistant Charter\n", encoding="utf-8")

            result = self.run_validate(pack_dir)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Missing required file: operating-profile.md", result.stderr)

    def test_lane_with_empty_required_fields_fails_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "lane-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            (destination / "operating-profile.md").write_text(
                """# Operating Profile

## 1. Assistant charter

- Primary outcome: Stay oriented.
- Primary failure mode: Drift.
- Uncertainty behavior: Ask when needed.
- Safety / approval boundary: Destructive actions require approval.
- Master list source: One list.
- Memory front door: Hot cache.
- Durable memory home: Wiki.
- Ask-vs-act rule: Ask when intent changes.
- Escalation / approval rule: Ask first.

## 2. Top-level lane map

- Ops

## 3. Per-lane snapshot

### Lane: Ops
- Status:
- Foreground:
- Pressure:
- Short note:
""",
                encoding="utf-8",
            )

            result = self.run_validate(destination)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("operating-profile.md lane 'Ops' has an empty required field: - Status:", result.stderr)
            self.assertIn("operating-profile.md lane 'Ops' has an empty required field: - Foreground:", result.stderr)
            self.assertIn("operating-profile.md lane 'Ops' has an empty required field: - Pressure:", result.stderr)
            self.assertIn("operating-profile.md lane 'Ops' has an empty required field: - Short note:", result.stderr)

    def test_validation_can_succeed_with_warnings_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "warning-pack"
            bootstrap = self.run_bootstrap("--filled-example", str(destination))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            (destination / "cadence-review.md").write_text("# Cadence Review\n", encoding="utf-8")

            result = self.run_validate(destination)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("warnings: 1", result.stdout)
            self.assertIn("cadence-review.md looks blank", result.stdout)


if __name__ == "__main__":
    unittest.main()
