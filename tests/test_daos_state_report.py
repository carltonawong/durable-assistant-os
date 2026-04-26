from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CLI_SCRIPT = REPO_ROOT / "scripts" / "daos.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"

HOT_CACHE = """# Hot Cache

**Updated:** 2026-04-26 15:10 PDT  
**Updated by:** Test  
**Scope:** DAOS state report

## Current Focus
- Building no-args DAOS state report.
- Keeping public surface simple.

## Current Corrections
- DAOS coexists with private memory.

## Current State
- Harness commands are private proof surfaces.

## Open Problems
- Need bridge-aware init design.

## System Priorities
- Keep state report compact.
"""

HOT_CACHE_LOG = """# Hot Cache Log

## 2026-04-26 15:10 PDT - Test
- Built state report test fixture.
- Verified hot cache extraction.

## 2026-04-26 15:00 PDT - Test
- Captured mandatory baseline correction.
"""

RESET_HANDOFF = """# Reset Handoff

## Current Handoff
**Last updated:** 2026-04-26 15:10 PDT  
**Updated by:** Test  
**Lane:** DAOS  
**Status:** fresh

- Why this handoff exists: Resume state report work.
- Exact next move: Polish the no-args DAOS state report.
- First verification: python scripts/daos.py
- If stale or contradicted: Verify files first.
"""


class DaosStateReportTests(unittest.TestCase):
    def run_cli(self, *args: str, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
        run_env = os.environ.copy()
        if env:
            run_env.update(env)
        return subprocess.run(
            ["python", str(CLI_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
            env=run_env,
        )

    def run_bootstrap(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(BOOTSTRAP_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def make_state_pack(self, tmpdir: str) -> Path:
        pack = Path(tmpdir) / "pack"
        bootstrap = self.run_bootstrap("--filled-example", str(pack))
        self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
        cache_dir = pack / "wiki" / "cache"
        cache_dir.mkdir(parents=True, exist_ok=True)
        (cache_dir / "hot-cache.md").write_text(HOT_CACHE, encoding="utf-8")
        (cache_dir / "hot-cache-log.md").write_text(HOT_CACHE_LOG, encoding="utf-8")
        (cache_dir / "reset-handoff.md").write_text(RESET_HANDOFF, encoding="utf-8")
        return pack

    def test_state_command_outputs_compact_state_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_state_pack(tmpdir)

            result = self.run_cli("state", str(pack))

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS State", result.stdout)
        self.assertIn("Current", result.stdout)
        self.assertIn("- Building no-args DAOS state report.", result.stdout)
        self.assertIn("Recent Activity", result.stdout)
        self.assertIn("Built state report test fixture.", result.stdout)
        self.assertIn("Needs Attention", result.stdout)
        self.assertIn("Next", result.stdout)
        self.assertIn("Polish the no-args DAOS state report.", result.stdout)

    def test_no_args_uses_daos_home_environment_as_state_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            pack = self.make_state_pack(tmpdir)

            result = self.run_cli(env={"DAOS_HOME": str(pack)})

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assertIn("DAOS State", result.stdout)
        self.assertIn(str(pack), result.stdout)
        self.assertIn("Building no-args DAOS state report", result.stdout)

    def test_no_args_without_discoverable_pack_explains_init_next_step(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            result = self.run_cli(env={"DAOS_HOME": str(Path(tmpdir) / "missing")})

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DAOS State unavailable", result.stderr)
        self.assertIn("run `daos init`", result.stderr)


if __name__ == "__main__":
    unittest.main()
