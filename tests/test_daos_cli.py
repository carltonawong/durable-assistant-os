from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosCliTests(unittest.TestCase):
    def run_cli(self, *args: str, input_text: str | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(CLI_SCRIPT), *args],
            cwd=cwd or REPO_ROOT,
            text=True,
            input=input_text,
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
        self.assertIn("status", result.stdout)
        self.assertNotIn("state", result.stdout)
        self.assertIn("check", result.stdout)
        self.assertIn("orient", result.stdout)
        self.assertIn("reset-test", result.stdout)
        self.assertIn("handoff", result.stdout)
        self.assertIn("memory-audit", result.stdout)

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

    def test_init_scans_given_working_directory_and_stages_instruction_review(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            workspace = root / "workspace"
            workspace.mkdir()
            agents = workspace / "AGENTS.md"
            agents.write_text("# Existing agent rules\nUse local memory.\n", encoding="utf-8")
            destination = root / "daos-home"

            result = self.run_cli("init", str(destination), "--scan", str(workspace))

            report = destination / ".daos" / "import-stage" / "instruction-scan.md"
            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(report.is_file())
            report_text = report.read_text(encoding="utf-8")
            self.assertIn(str(agents), report_text)
            self.assertIn("prepend DAOS coexistence rule", report_text)
            self.assertEqual(agents.read_text(encoding="utf-8"), "# Existing agent rules\nUse local memory.\n")

    def test_init_with_interactive_approval_prepends_instruction_rule(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            workspace = root / "workspace"
            workspace.mkdir()
            agents = workspace / "AGENTS.md"
            agents.write_text("# Existing agent rules\nUse local memory.\n", encoding="utf-8")
            destination = root / "daos-home"

            # Run through a tiny pseudo-terminal so sys.stdin.isatty() is true.
            command = (
                f"printf 'y\n' | script -q -c \"python {CLI_SCRIPT} init {destination} --scan {workspace}\" /dev/null"
            )
            result = subprocess.run(command, cwd=REPO_ROOT, shell=True, text=True, capture_output=True, check=False)

            self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
            updated = agents.read_text(encoding="utf-8")
            self.assertTrue(updated.startswith("## DAOS coexistence rule"))
            backups = list((destination / ".daos" / "backups" / "instructions").rglob("*.bak"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "# Existing agent rules\nUse local memory.\n")
            report = destination / ".daos" / "import-stage" / "instruction-scan.md"
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("Edits applied", report_text)
            self.assertIn("backup:", report_text)
            self.assertIn("instruction backups", result.stdout)

    def test_state_report_hides_fresh_starter_pack_placeholders(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "blank-pack"
            init = self.run_cli("init", str(destination), "--blank")
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            result = self.run_cli("status", str(destination))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("- No current focus set yet.", result.stdout)
            self.assertNotIn("Fill with the current shared foreground lane", result.stdout)
            self.assertIn("hot-cache.md has no real current focus yet", result.stdout)


if __name__ == "__main__":
    unittest.main()
