from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
WIZARD_SCRIPT = REPO_ROOT / "scripts" / "daos_wizard.py"
VALIDATE_SCRIPT = REPO_ROOT / "scripts" / "daos_validate.py"


class DaosWizardScriptTests(unittest.TestCase):
    ANSWERS = "\n".join(
        [
            "Help me stay oriented across active work and personal lanes.",
            "Noise, bad assumptions, and repeated re-steering.",
            "Ask when ambiguity changes the action; otherwise act on likely intent.",
            "Urgent blockers, deadline drift, and wrong-foreground issues.",
            "Destructive, public, costly, or socially consequential actions.",
            "Grounded, concise, chief-of-staff-like.",
            "Operations, Client work, Personal",
            "Operations, Client work",
            "Waiting-on follow-ups and deep work.",
            "One durable task list.",
            "yes",
        ]
    ) + "\n"

    def run_wizard(self, destination: Path, *args: str, input_text: str | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(WIZARD_SCRIPT), *args, str(destination)],
            cwd=REPO_ROOT,
            text=True,
            input=input_text,
            capture_output=True,
            check=False,
        )

    def run_validate(self, destination: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(VALIDATE_SCRIPT), str(destination)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_wizard_generates_filled_pack_that_passes_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "wizard-pack"
            result = self.run_wizard(destination, input_text=self.ANSWERS)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((destination / "assistant-charter.md").exists())
            self.assertTrue((destination / "operating-profile.md").exists())
            self.assertIn("Generated DAOS starter pack", result.stdout)

            validation = self.run_validate(destination)
            self.assertEqual(validation.returncode, 0, msg=validation.stderr)

    def test_non_empty_target_fails_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "occupied"
            destination.mkdir()
            (destination / "old.txt").write_text("old", encoding="utf-8")

            result = self.run_wizard(destination, input_text=self.ANSWERS)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Use --force to replace it", result.stderr)
            self.assertTrue((destination / "old.txt").exists())

    def test_force_replaces_existing_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "replace-me"
            destination.mkdir()
            (destination / "old.txt").write_text("old", encoding="utf-8")

            result = self.run_wizard(destination, "--force", input_text=self.ANSWERS)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertFalse((destination / "old.txt").exists())
            self.assertTrue((destination / "assistant-charter.md").exists())


if __name__ == "__main__":
    unittest.main()
