from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"


class DaosFirstRunFlowTests(unittest.TestCase):
    def run_cli(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        input_text: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            ["python", str(CLI_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            input=input_text,
            capture_output=True,
            check=False,
            env=run_env,
        )

    def test_first_run_flow_defaults_to_daos_home_and_ends_complete(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "fresh-home"
            pack = home / ".daos"
            workdir = Path(tmpdir) / "hermes-agent"
            workdir.mkdir(parents=True)
            env = {"HOME": str(home)}

            init = self.run_cli("init", "--blank", env=env)
            setup = self.run_cli(
                "setup",
                "--active-lane",
                "Hermes Agent local setup",
                "--working-directory",
                str(workdir),
                "--primary-outcome",
                "Help the user make concrete progress while preserving continuity.",
                "--approval-boundary",
                "Ask before destructive, credential, publishing, or production changes.",
                "--uncertainty-behavior",
                "verify first, act on low-risk defaults, ask before risky changes",
                "--live-sources",
                "current thread, repo files/git status, logs/runtime state",
                "--durable-context",
                "project conventions, preferred tools, recurring setup details",
                "--reset-recovery",
                "current project status, exact next step, first verification",
                "--week-success",
                "remembers where we left off, verifies before acting, keeps work moving",
                env=env,
            )
            check = self.run_cli("check", env=env)
            on = self.run_cli("on", env=env)
            reset = self.run_cli("reset-test", env=env)

            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn("next: run `use-daos setup`", init.stdout)

            self.assertEqual(setup.returncode, 0, msg=setup.stderr)
            self.assertIn("DAOS setup", setup.stdout)
            self.assertIn("Step 1: assistant charter", setup.stdout)
            self.assertIn("Step 2: operating profile", setup.stdout)
            self.assertIn("Step 3: current focus", setup.stdout)
            self.assertIn("Step 4: reset handoff", setup.stdout)
            self.assertIn("1/8 What do you want this assistant to help you make progress on first?", setup.stdout)
            self.assertIn("Examples: coding projects, business operations, personal admin", setup.stdout)
            self.assertIn("Default: my current active project", setup.stdout)
            self.assertIn("5/8 What live sources should the assistant check before trusting memory?", setup.stdout)
            self.assertIn("Default: current thread, repo files/git status, logs/runtime state", setup.stdout)
            self.assertIn("8/8 What would make this assistant feel genuinely useful after one week?", setup.stdout)
            self.assertIn("next: run `use-daos check`", setup.stdout)

            self.assertTrue((pack / "assistant-charter.md").exists())
            self.assertTrue((pack / "operating-profile.md").exists())
            self.assertIn("Hermes Agent local setup", (pack / "operating-profile.md").read_text(encoding="utf-8"))
            self.assertIn(str(workdir), (pack / "wiki" / "cache" / "hot-cache.md").read_text(encoding="utf-8"))
            self.assertIn("Ask before destructive, credential, publishing, or production changes.", (pack / "assistant-charter.md").read_text(encoding="utf-8"))
            self.assertIn("current thread, repo files/git status, logs/runtime state", (pack / "operating-profile.md").read_text(encoding="utf-8"))

            self.assertEqual(check.returncode, 0, msg=check.stderr)
            self.assertIn(f"DAOS check passed: {pack.resolve()}", check.stdout)
            self.assertIn("warnings: 0", check.stdout)
            self.assertIn("notes: 1", check.stdout)
            self.assertIn("cadence-review.md is intentionally left for later", check.stdout)

            self.assertEqual(on.returncode, 0, msg=on.stderr)
            self.assertTrue(on.stdout.startswith("DAOS On\n"), on.stdout)
            self.assertIn("Hermes Agent local setup", on.stdout)

            self.assertEqual(reset.returncode, 0, msg=reset.stderr)
            self.assertIn("DAOS reset test passed", reset.stdout)
            self.assertIn("You're complete!", reset.stdout)

    def test_setup_refuses_non_interactive_defaulting_without_explicit_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "fresh-home"
            env = {"HOME": str(home)}
            init = self.run_cli("init", "--blank", env=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            setup = self.run_cli("setup", env=env)

        self.assertNotEqual(setup.returncode, 0)
        self.assertIn("DAOS setup needs an interactive terminal", setup.stderr)
        self.assertIn("Run `use-daos setup` yourself", setup.stderr)
        self.assertIn("--accept-defaults", setup.stderr)

    def test_setup_can_accept_defaults_when_explicitly_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "fresh-home"
            env = {"HOME": str(home)}
            init = self.run_cli("init", "--blank", env=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            setup = self.run_cli("setup", "--accept-defaults", env=env)

        self.assertEqual(setup.returncode, 0, msg=setup.stderr)
        self.assertIn("non-interactive defaults explicitly accepted", setup.stdout)
        self.assertIn("1/8 What do you want this assistant to help you make progress on first?", setup.stdout)

    def test_setup_refuses_to_overwrite_personalized_files_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "fresh-home"
            pack = home / ".daos"
            env = {"HOME": str(home)}
            init = self.run_cli("init", "--blank", env=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            first_setup = self.run_cli("setup", "--accept-defaults", env=env)
            self.assertEqual(first_setup.returncode, 0, msg=first_setup.stderr)
            charter_path = pack / "assistant-charter.md"
            original = charter_path.read_text(encoding="utf-8")
            personalized = original + "\n<!-- user personalization -->\n"
            charter_path.write_text(personalized, encoding="utf-8")

            second_setup = self.run_cli("setup", "--accept-defaults", env=env)

            self.assertNotEqual(second_setup.returncode, 0)
            self.assertIn("refused to overwrite existing personalized setup files", second_setup.stderr)
            self.assertIn("assistant-charter.md", second_setup.stderr)
            self.assertIn("use-daos setup --force", second_setup.stderr)
            self.assertEqual(charter_path.read_text(encoding="utf-8"), personalized)

    def test_setup_force_backs_up_before_overwriting_personalized_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            home = Path(tmpdir) / "fresh-home"
            pack = home / ".daos"
            env = {"HOME": str(home)}
            init = self.run_cli("init", "--blank", env=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            first_setup = self.run_cli("setup", "--accept-defaults", env=env)
            self.assertEqual(first_setup.returncode, 0, msg=first_setup.stderr)
            charter_path = pack / "assistant-charter.md"
            personalized = charter_path.read_text(encoding="utf-8") + "\n<!-- user personalization -->\n"
            charter_path.write_text(personalized, encoding="utf-8")

            forced = self.run_cli("setup", "--accept-defaults", "--force", env=env)
            backups = list((pack / ".daos" / "backups" / "setup").glob("*/assistant-charter.md"))

            self.assertEqual(forced.returncode, 0, msg=forced.stderr)
            self.assertIn("backed up existing setup files", forced.stdout)
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), personalized)
            self.assertNotEqual(charter_path.read_text(encoding="utf-8"), personalized)


if __name__ == "__main__":
    unittest.main()
