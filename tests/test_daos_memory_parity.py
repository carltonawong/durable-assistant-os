from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.daos_core.parity import audit_memory_parity

REPO_ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"
PARITY_SCRIPT = REPO_ROOT / "scripts" / "daos_memory_parity.py"


class DaosMemoryParityTests(unittest.TestCase):
    def bootstrap_filled_pack(self, destination: Path) -> None:
        result = subprocess.run(
            ["python", str(BOOTSTRAP_SCRIPT), "--filled-example", str(destination)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)

    def run_parity(self, pack_dir: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(PARITY_SCRIPT), str(pack_dir)],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_filled_pack_is_parity_healthy(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "filled-pack"
            self.bootstrap_filled_pack(destination)

            result = audit_memory_parity(destination)

            self.assertEqual(result.status, "healthy")
            self.assertEqual(result.findings, [])

    def test_missing_baseline_memory_file_is_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "missing-memory-pack"
            self.bootstrap_filled_pack(destination)
            (destination / "wiki" / "cache" / "hot-cache.md").unlink()

            result = audit_memory_parity(destination)

            self.assertEqual(result.status, "drift")
            self.assertTrue(any("missing baseline memory files" in finding.message for finding in result.findings))

    def test_wiki_log_must_be_chronological_append_order(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "log-order-pack"
            self.bootstrap_filled_pack(destination)
            (destination / "wiki" / "log.md").write_text(
                "# Log\n\n## 2026-04-23\n- newer\n\n## 2026-04-21\n- older\n",
                encoding="utf-8",
            )

            result = audit_memory_parity(destination)

            self.assertEqual(result.status, "watch")
            self.assertTrue(any("wiki/log.md" in finding.message for finding in result.findings))

    def test_hot_cache_log_must_be_reverse_chronological(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "hot-cache-log-order-pack"
            self.bootstrap_filled_pack(destination)
            (destination / "wiki" / "cache" / "hot-cache-log.md").write_text(
                "# Hot Cache Log\n\n## 2026-04-21\n- older\n\n## 2026-04-23\n- newer\n",
                encoding="utf-8",
            )

            result = audit_memory_parity(destination)

            self.assertEqual(result.status, "watch")
            self.assertTrue(any("hot-cache-log.md" in finding.message for finding in result.findings))

    def test_hot_cache_requires_exact_five_sections(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "hot-cache-shape-pack"
            self.bootstrap_filled_pack(destination)
            (destination / "wiki" / "cache" / "hot-cache.md").write_text(
                "# Hot Cache\n\n## Current Focus\n- ok\n\n## Extra Section\n- drift\n",
                encoding="utf-8",
            )

            result = audit_memory_parity(destination)

            self.assertEqual(result.status, "watch")
            self.assertTrue(any("section shape" in finding.message for finding in result.findings))

    def test_cli_outputs_report_shape(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            destination = Path(tmpdir) / "cli-pack"
            self.bootstrap_filled_pack(destination)

            result = self.run_parity(destination)

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("Status: healthy", result.stdout)
            self.assertIn("Findings:", result.stdout)
            self.assertIn("Repairs made:", result.stdout)
            self.assertIn("Recommended next move:", result.stdout)


if __name__ == "__main__":
    unittest.main()
