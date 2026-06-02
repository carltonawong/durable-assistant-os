from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"


class DaosInitCommandTests(unittest.TestCase):
    def run_cli(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            ["python", str(CLI_SCRIPT), *args],
            cwd=cwd or REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=run_env,
        )

    def test_init_installs_mandatory_daos_baseline(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "daos-home"

            result = self.run_cli("init", str(target), "--blank")

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("DAOS initialized", result.stdout)
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / "assistant-charter.md").is_file())
            self.assertTrue((target / "operating-profile.md").is_file())
            self.assertTrue((target / "wiki" / "WIKI.md").is_file())
            self.assertTrue((target / "wiki" / "cache" / "hot-cache.md").is_file())
            self.assertTrue((target / "wiki" / "cache" / "reset-handoff.md").is_file())

    def test_init_scans_existing_instruction_carriers_without_overwriting_them(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "daos-home"
            project = Path(tmpdir) / "project"
            project.mkdir()
            existing_agents = project / "AGENTS.md"
            existing_agents.write_text("# Existing Agent Rules\n\nUse local memory.\n", encoding="utf-8")

            result = self.run_cli("init", str(target), "--scan", str(project))
            report = target / "import-stage" / "instruction-scan.md"

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(report.is_file())
            self.assertFalse((target / ".daos" / "import-stage" / "instruction-scan.md").exists())
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("AGENTS.md", report_text)
            self.assertIn("DAOS coexistence rule should be placed at the top/front", report_text)
            self.assertEqual(existing_agents.read_text(encoding="utf-8"), "# Existing Agent Rules\n\nUse local memory.\n")

    def test_init_uses_daos_home_environment_when_target_omitted(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "env-daos-home"

            result = self.run_cli("init", "--blank", env={"DAOS_HOME": str(target)})

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((target / "wiki" / "cache" / "hot-cache.md").is_file())

    def test_init_can_install_additively_into_detected_assistant_home(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_home = Path(tmpdir) / "fake-home"
            assistant_home = Path(tmpdir) / "assistant-home"
            assistant_home.mkdir()
            existing_agents = assistant_home / "AGENTS.md"
            existing_agents.write_text("# Existing Agent Rules\n\nKeep this file.\n", encoding="utf-8")

            result = self.run_cli(
                "init",
                "--use-detected-home",
                "--scan",
                str(assistant_home),
                env={"HOME": str(fake_home)},
                cwd=assistant_home,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn(f"assistant home scan: detected {assistant_home}", result.stdout)
            self.assertIn("assistant home install: used detected home additively", result.stdout)
            self.assertTrue((assistant_home / "assistant-charter.md").is_file())
            self.assertTrue((assistant_home / "operating-profile.md").is_file())
            self.assertTrue((assistant_home / "wiki" / "cache" / "hot-cache.md").is_file())
            self.assertEqual(existing_agents.read_text(encoding="utf-8"), "# Existing Agent Rules\n\nKeep this file.\n")
            self.assertFalse((fake_home / ".daos").exists())

    def test_init_detects_assistant_home_but_keeps_default_without_opt_in(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_home = Path(tmpdir) / "fake-home"
            assistant_home = Path(tmpdir) / "assistant-home"
            assistant_home.mkdir()
            (assistant_home / "AGENTS.md").write_text("# Existing Agent Rules\n", encoding="utf-8")

            result = self.run_cli(
                "init",
                "--scan",
                str(assistant_home),
                env={"HOME": str(fake_home)},
                cwd=assistant_home,
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("assistant home install: defaulted to ~/.daos", result.stdout)
            self.assertTrue((fake_home / ".daos" / "wiki" / "cache" / "hot-cache.md").is_file())
            self.assertFalse((assistant_home / "wiki" / "cache" / "hot-cache.md").exists())

    def test_init_refuses_non_empty_non_daos_target_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            target = Path(tmpdir) / "occupied"
            target.mkdir()
            (target / "keep.txt").write_text("keep", encoding="utf-8")

            result = self.run_cli("init", str(target), "--blank")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("DAOS init failed", result.stderr)
            self.assertTrue((target / "keep.txt").is_file())


if __name__ == "__main__":
    unittest.main()
