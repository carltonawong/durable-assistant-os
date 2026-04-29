from __future__ import annotations

import os
import pty
import select
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
WRAPPER = REPO_ROOT / "bin" / "use-daos.js"


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

    def run_wrapper_in_pty(self, *args: str, input_after_prompt: str = "y\n") -> tuple[int, str]:
        master, slave = pty.openpty()
        proc = subprocess.Popen(
            ["node", str(WRAPPER), *args],
            cwd=REPO_ROOT,
            stdin=slave,
            stdout=slave,
            stderr=slave,
            env=os.environ.copy(),
        )
        os.close(slave)
        output = bytearray()
        sent = False
        start = time.time()
        while True:
            if time.time() - start > 10:
                proc.kill()
                break
            readable, _, _ = select.select([master], [], [], 0.1)
            if master in readable:
                try:
                    chunk = os.read(master, 4096)
                except OSError:
                    break
                if not chunk:
                    break
                output.extend(chunk)
                if not sent and b"Apply these approved instruction edits now?" in output:
                    os.write(master, input_after_prompt.encode())
                    sent = True
            if proc.poll() is not None:
                break
        try:
            os.close(master)
        except OSError:
            pass
        return proc.wait(), output.decode(errors="replace")

    def test_wrapper_help_delegates_to_python_cli(self) -> None:
        result = self.run_wrapper("--help")

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("usage: use-daos", result.stdout)
        self.assertNotIn("usage: use-daos.py", result.stdout)
        self.assertIn("DAOS local harness commands", result.stdout)
        self.assertIn("status", result.stdout)
        self.assertIn("init", result.stdout)

    def test_wrapper_init_and_status_flow(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "daos-home"

            init = self.run_wrapper("init", str(destination), "--blank")
            self.assertEqual(init.returncode, 0, msg=init.stderr)
            self.assertIn("DAOS initialized", init.stdout)
            self.assertIn("use-daos setup", init.stdout)

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
        self.assertIn("npx use-daos init", result.stderr)

    def test_wrapper_rejects_python_that_is_too_old(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_python = Path(tmpdir) / "python"
            fake_python.write_text("#!/usr/bin/env sh\nexit 1\n", encoding="utf-8")
            fake_python.chmod(0o755)

            result = self.run_wrapper("--help", env={"DAOS_PYTHON": str(fake_python)})

        self.assertEqual(result.returncode, 1)
        self.assertIn("DAOS needs Python 3", result.stderr)

    def test_wrapper_preserves_interactive_instruction_approval(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            workspace = root / "workspace"
            workspace.mkdir()
            agents = workspace / "AGENTS.md"
            agents.write_text("# Existing agent rules\nUse local memory.\n", encoding="utf-8")
            destination = root / "daos-home"

            code, output = self.run_wrapper_in_pty("init", str(destination), "--scan", str(workspace))

            self.assertEqual(code, 0, msg=output)
            self.assertIn("DAOS wants approval", output)
            self.assertIn("instruction edits: applied with approval (1)", output)
            self.assertIn("DAOS coexistence rule", agents.read_text(encoding="utf-8"))
            backups = list((destination / ".daos" / "backups" / "instructions").rglob("AGENTS.md*.bak"))
            self.assertEqual(len(backups), 1)


if __name__ == "__main__":
    unittest.main()
