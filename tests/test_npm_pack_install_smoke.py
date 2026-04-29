from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


class DaosNpmPackInstallSmokeTests(unittest.TestCase):
    def run_cmd(
        self,
        args: list[str],
        *,
        cwd: Path,
        env: dict[str, str] | None = None,
        timeout: int = 120,
    ) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            args,
            cwd=cwd,
            env=merged_env,
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )

    def pack_tarball(self, tmpdir: Path) -> Path:
        result = self.run_cmd(["npm", "pack", "--pack-destination", str(tmpdir)], cwd=REPO_ROOT)
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        filename = result.stdout.strip().splitlines()[-1]
        tarball = tmpdir / filename
        self.assertTrue(tarball.is_file(), f"npm pack did not create {tarball}")
        return tarball

    def install_package_in_consumer(self, tarball: Path, consumer: Path) -> Path:
        consumer.mkdir(parents=True)
        init = self.run_cmd(["npm", "init", "-y"], cwd=consumer)
        self.assertEqual(init.returncode, 0, msg=init.stderr)
        install = self.run_cmd(["npm", "install", str(tarball)], cwd=consumer)
        self.assertEqual(install.returncode, 0, msg=install.stderr)
        binary = consumer / "node_modules" / ".bin" / "use-daos"
        self.assertTrue(binary.exists(), f"installed package did not expose {binary}")
        return binary

    def test_packed_tarball_installs_and_runs_init_status_from_consumer_project(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tarball = self.pack_tarball(root)
            daos = self.install_package_in_consumer(tarball, root / "consumer")
            pack_home = root / "pack-home"

            init = self.run_cmd([str(daos), "init", str(pack_home), "--blank"], cwd=root / "consumer")
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn("DAOS initialized", init.stdout)
            self.assertIn("baseline: installed mandatory wiki/cache framework", init.stdout)
            self.assertTrue((pack_home / "wiki" / "cache" / "hot-cache.md").is_file())

            status = self.run_cmd([str(daos)], cwd=root / "consumer", env={"DAOS_HOME": str(pack_home)})
            self.assertEqual(status.returncode, 0, msg=status.stderr)
            self.assertIn("DAOS Status", status.stdout)
            self.assertIn("DAOS On", status.stdout)
            self.assertIn("Hot Cache: No current focus set yet.", status.stdout)
            self.assertIn("Next", status.stdout)

    def test_packed_tarball_supports_documented_no_arg_init_then_no_arg_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tarball = self.pack_tarball(root)
            consumer = root / "consumer"
            daos = self.install_package_in_consumer(tarball, consumer)
            workspace = root / "workspace"
            workspace.mkdir()
            agents = workspace / "AGENTS.md"
            agents.write_text("# Existing agent instructions\nUse local memory.\n", encoding="utf-8")
            pack_home = root / "documented-daos-home"
            env = {"DAOS_HOME": str(pack_home)}

            init = self.run_cmd([str(daos), "init"], cwd=workspace, env=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn(f"DAOS initialized: {pack_home}", init.stdout)
            self.assertIn("instruction scan: wrote review report inside DAOS home: .daos/import-stage/instruction-scan.md", init.stdout)
            self.assertNotIn(".daos/.daos/import-stage", init.stdout)
            self.assertIn("instruction edits: none applied", init.stdout)
            self.assertTrue((pack_home / "wiki" / "cache" / "hot-cache.md").is_file())
            self.assertNotIn("DAOS coexistence rule", agents.read_text(encoding="utf-8"))
            report = pack_home / ".daos" / "import-stage" / "instruction-scan.md"
            self.assertTrue(report.is_file())
            self.assertIn("AGENTS.md", report.read_text(encoding="utf-8"))

            status = self.run_cmd([str(daos)], cwd=workspace, env=env)
            self.assertEqual(status.returncode, 0, msg=status.stderr)
            self.assertIn("DAOS Status", status.stdout)
            self.assertIn("DAOS On", status.stdout)
            self.assertIn("Bridge Review", status.stdout)

    def test_packed_tarball_no_arg_init_uses_home_daos_when_no_daos_home_is_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tarball = self.pack_tarball(root)
            consumer = root / "consumer"
            daos = self.install_package_in_consumer(tarball, consumer)
            fake_home = root / "fake-home"
            fake_home.mkdir()
            workspace = root / "workspace"
            workspace.mkdir()
            env = {"HOME": str(fake_home), "DAOS_HOME": ""}
            expected_home = fake_home / ".daos"

            init = self.run_cmd([str(daos), "init", "--blank"], cwd=workspace, env=env)
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn(f"DAOS initialized: {expected_home}", init.stdout)
            self.assertTrue((expected_home / "wiki" / "cache" / "hot-cache.md").is_file())

            status = self.run_cmd([str(daos)], cwd=workspace, env=env)
            self.assertEqual(status.returncode, 0, msg=status.stderr)
            self.assertIn("DAOS Status", status.stdout)
            self.assertIn("DAOS On", status.stdout)
            self.assertIn("Hot Cache: No current focus set yet.", status.stdout)

    def test_packed_tarball_on_command_shows_populated_daos_on_surface(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tarball = self.pack_tarball(root)
            consumer = root / "consumer"
            daos = self.install_package_in_consumer(tarball, consumer)
            workspace = root / "workspace"
            workspace.mkdir()
            pack_home = root / "daos-home"
            init = self.run_cmd([str(daos), "init", str(pack_home), "--blank"], cwd=workspace)
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            hot_cache = pack_home / "wiki" / "cache" / "hot-cache.md"
            hot_cache.write_text(
                "# Hot Cache\n\n"
                "**Updated:** 2026-04-27 17:30 PDT  \n"
                "**Updated by:** DAOS package smoke test  \n"
                "**Scope:** Demo workspace onboarding\n\n"
                "> Shared volatile front door: short-horizon context.\n\n"
                "## Current Focus\n"
                "- Evaluate DAOS in an existing Hermes-style workspace.\n\n"
                "## Current Corrections\n"
                "- Existing Hermes private memory stays private.\n\n"
                "## Current State\n"
                "- DAOS baseline installed under the user's home directory.\n\n"
                "## Open Problems\n"
                "- Assistant charter and operating profile still need user-specific filling.\n\n"
                "## System Priorities\n"
                "- Keep install non-destructive.\n",
                encoding="utf-8",
            )

            result = self.run_cmd([str(daos), "on", str(pack_home)], cwd=workspace)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue(result.stdout.startswith("DAOS On\n"), result.stdout)
            self.assertNotIn("DAOS Status\n", result.stdout)
            self.assertIn("Evaluate DAOS in an existing Hermes-style workspace.", result.stdout)

    def test_packed_tarball_can_read_existing_openclaw_style_home_without_creating_default_daos(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tarball = self.pack_tarball(root)
            consumer = root / "consumer"
            daos = self.install_package_in_consumer(tarball, consumer)
            package_root = consumer / "node_modules" / "use-daos"
            existing_home = root / ".openclaw"
            fake_home = root / "fake-home"
            fake_home.mkdir()
            shutil.copytree(package_root / "starter-pack", existing_home)
            hot_cache = existing_home / "wiki" / "cache" / "hot-cache.md"
            hot_cache.write_text(
                "# Hot Cache\n\n"
                "**Updated:** 2026-04-27 18:00 PDT  \n"
                "**Updated by:** Existing assistant home smoke test  \n"
                "**Scope:** Existing OpenClaw-style home\n\n"
                "> Shared volatile front door: short-horizon context.\n\n"
                "## Current Focus\n"
                "- Use an existing .openclaw-style assistant home as the DAOS home.\n\n"
                "## Current Corrections\n"
                "- DAOS home is a structure, not a required folder name.\n\n"
                "## Current State\n"
                "- Wiki/cache surfaces already exist in the assistant home.\n\n"
                "## Open Problems\n"
                "- No separate ~/.daos home should be created for this explicit path check.\n\n"
                "## System Priorities\n"
                "- Read explicit pack paths without side effects.\n",
                encoding="utf-8",
            )

            result = self.run_cmd(
                [str(daos), "on", str(existing_home)],
                cwd=root,
                env={"HOME": str(fake_home), "DAOS_HOME": ""},
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("DAOS On", result.stdout)
            self.assertIn("Use an existing .openclaw-style assistant home", result.stdout)
            self.assertFalse((fake_home / ".daos").exists(), "explicit existing home should not create ~/.daos")

    def test_packed_tarball_stages_instruction_review_without_importing_memory_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tarball = self.pack_tarball(root)
            daos = self.install_package_in_consumer(tarball, root / "consumer")
            workspace = root / "workspace"
            workspace.mkdir()
            (workspace / "AGENTS.md").write_text("# Existing agent instructions\nUse local memory.\n", encoding="utf-8")
            (workspace / "MEMORY.md").write_text("# Existing memory\nDo not import me by default.\n", encoding="utf-8")
            pack_home = root / "daos-home"

            init = self.run_cmd([str(daos), "init", str(pack_home), "--scan", str(workspace)], cwd=root / "consumer")
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn("instruction scan: wrote review report inside DAOS home: .daos/import-stage/instruction-scan.md", init.stdout)
            self.assertNotIn(".daos/.daos/import-stage", init.stdout)
            self.assertIn("instruction edits: none applied", init.stdout)
            self.assertNotIn("DAOS coexistence rule", (workspace / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual(list(pack_home.rglob("MEMORY.md")), [])

            report = pack_home / ".daos" / "import-stage" / "instruction-scan.md"
            self.assertTrue(report.is_file())
            report_text = report.read_text(encoding="utf-8")
            self.assertIn("AGENTS.md", report_text)
            self.assertNotIn("MEMORY.md", report_text)

            status = self.run_cmd([str(daos), "status", str(pack_home)], cwd=root / "consumer")
            self.assertEqual(status.returncode, 0, msg=status.stderr)
            self.assertIn("Bridge Review", status.stdout)
            self.assertIn("instruction edits need approval", status.stdout)


if __name__ == "__main__":
    unittest.main()
