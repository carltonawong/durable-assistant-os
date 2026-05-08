from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosBootCheckTests(unittest.TestCase):
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

    def write_runtime_config(self, path: Path, payload: dict[str, object]) -> Path:
        config_path = path / "runtime.json"
        config_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        return config_path

    def test_boot_check_passes_for_daos_first_runtime_fixture(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack = root / "pack"
            bootstrap = self.run_bootstrap("--filled-example", str(pack))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            config = self.write_runtime_config(
                root,
                {
                    "startup_root": str(pack),
                    "daos_home": str(pack),
                    "prompt_precedence": ["local_thread", "daos_project", "hot_cache", "private_memory", "live_reality"],
                    "session_topology": {"shared_collaboration_lanes": True, "group_sessions_per_user": False},
                    "reset_handoff": {"enabled": True, "reads_reset_handoff": True, "reads_hot_cache": True},
                },
            )

            result = self.run_cli("boot-check", str(pack), "--runtime-config", str(config))

        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        self.assertIn("DAOS boot check passed", result.stdout)
        self.assertIn("Installed Structure", result.stdout)
        self.assertIn("Startup Root", result.stdout)
        self.assertIn("Prompt/Context Precedence", result.stdout)
        self.assertIn("Session Topology", result.stdout)
        self.assertIn("Reset/Handoff Wiring", result.stdout)
        self.assertIn("Cache Freshness", result.stdout)
        self.assertIn("errors: 0", result.stdout)

    def test_boot_check_fails_when_runtime_starts_outside_pack_and_memory_precedes_daos(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pack = root / "pack"
            bootstrap = self.run_bootstrap("--filled-example", str(pack))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            config = self.write_runtime_config(
                root,
                {
                    "startup_root": str(root / "wrong-root"),
                    "daos_home": str(pack),
                    "prompt_precedence": ["private_memory", "hot_cache", "daos_project", "live_reality"],
                    "session_topology": {"shared_collaboration_lanes": True, "group_sessions_per_user": True},
                    "reset_handoff": {"enabled": False, "reads_reset_handoff": False, "reads_hot_cache": False},
                },
            )

            result = self.run_cli("boot-check", str(pack), "--runtime-config", str(config))

        combined = result.stdout + result.stderr
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS boot check failed", combined)
        self.assertIn("startup root is outside the DAOS pack/home", combined)
        self.assertIn("private runtime memory appears before DAOS/project context", combined)
        self.assertIn("group sessions are split per user while shared DAOS lanes are expected", combined)
        self.assertIn("reset/handoff hook is not enabled", combined)
        self.assertIn("next moves:", combined)

    def test_boot_check_without_runtime_config_reports_structure_but_warns_runtime_unverified(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = Path(tmpdir) / "pack"
            bootstrap = self.run_bootstrap("--filled-example", str(pack))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_cli("doctor", str(pack))

        self.assertEqual(result.returncode, 0, msg=result.stderr + result.stdout)
        self.assertIn("DAOS boot check passed", result.stdout)
        self.assertIn("runtime config: not provided", result.stdout)
        self.assertIn("runtime boot order is unverified", result.stdout)
        self.assertIn("warnings:", result.stdout)


if __name__ == "__main__":
    unittest.main()
