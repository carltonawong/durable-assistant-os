from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "bin" / "daos.js"


class DaosNpmWrapperTests(unittest.TestCase):
    def run_wrapper(
        self,
        *args: str,
        env: dict[str, str] | None = None,
        cwd: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        merged_env = os.environ.copy()
        if env:
            merged_env.update(env)
        return subprocess.run(
            ["node", str(WRAPPER), *args],
            cwd=cwd or REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=merged_env,
        )

    def test_wrapper_help_delegates_to_python_cli(self) -> None:
        result = self.run_wrapper("--help")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS local harness commands", result.stdout)
        self.assertIn("status", result.stdout)
        self.assertIn("init", result.stdout)

    def test_wrapper_init_and_status_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "daos-home"

            init = self.run_wrapper("init", str(destination), "--blank")
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn("DAOS initialized", init.stdout)
            self.assertIn("daos status", init.stdout)

            status = self.run_wrapper("status", str(destination))

        self.assertEqual(status.returncode, 0, msg=status.stderr)
        self.assertIn("DAOS Status", status.stdout)
        self.assertIn("DAOS On", status.stdout)
        self.assertIn("Hot Cache:", status.stdout)

    def test_wrapper_no_args_uses_daos_home_for_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "daos-home"
            init = self.run_wrapper("init", str(destination), "--blank")
            self.assertEqual(init.returncode, 0, msg=init.stderr)

            result = self.run_wrapper(env={"DAOS_HOME": str(destination)})

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS Status", result.stdout)
        self.assertIn("DAOS On", result.stdout)

    def test_wrapper_preserves_python_cli_exit_code_and_stderr(self) -> None:
        result = self.run_wrapper("check", "/definitely/missing/daos-pack")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS check failed", result.stderr)

    def test_wrapper_prints_clear_message_when_python_is_missing(self) -> None:
        result = self.run_wrapper("--help", env={"DAOS_PYTHON": "/definitely/missing/python"})

        self.assertEqual(result.returncode, 1)
        self.assertIn("DAOS needs Python 3", result.stderr)
        self.assertIn("npx daos init", result.stderr)


if __name__ == "__main__":
    unittest.main()
