from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
PORTABILITY_SCRIPT = REPO_ROOT / "scripts" / "daos_portability.py"
BOOTSTRAP_SCRIPT = REPO_ROOT / "scripts" / "daos_bootstrap.py"


class DaosPortabilityScriptTests(unittest.TestCase):
    def run_bootstrap(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(BOOTSTRAP_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def run_portability(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["python", str(PORTABILITY_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )

    def seed_wiki(self, root: Path) -> None:
        (root / "pages").mkdir(parents=True)
        (root / "sources").mkdir(parents=True)
        (root / "index.md").write_text("# Durable Wiki\n", encoding="utf-8")
        (root / "pages" / "ops.md").write_text("# Ops\nDurable note\n", encoding="utf-8")
        (root / "sources" / "lane-model.md").write_text("# Lane Model\n", encoding="utf-8")
        (root / "log.md").write_text("# Log\n", encoding="utf-8")

    def bootstrap_pack_and_bundle(
        self,
        tmp: Path,
        *,
        include_active_memory: bool = False,
    ) -> tuple[Path, Path, Path, Path | None, Path | None]:
        pack_dir = tmp / "pack"
        wiki_root = tmp / "wiki"
        bundle_dir = tmp / "bundle"
        self.seed_wiki(wiki_root)
        bootstrap = self.run_bootstrap("--filled-example", str(pack_dir))
        self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

        hot_cache = None
        continuity = None
        export_args = ["export", "--pack-dir", str(pack_dir), "--wiki-root", str(wiki_root), "--out", str(bundle_dir)]
        if include_active_memory:
            hot_cache = tmp / "hot-cache.md"
            continuity = tmp / "agent-continuity.md"
            hot_cache.write_text("# Hot Cache\n", encoding="utf-8")
            continuity.write_text("# Continuity\n", encoding="utf-8")
            export_args.extend([
                "--include-active-memory",
                "--hot-cache",
                str(hot_cache),
                "--agent-continuity",
                str(continuity),
            ])

        export = self.run_portability(*export_args)
        self.assertEqual(export.returncode, 0, msg=export.stderr)
        return pack_dir, wiki_root, bundle_dir, hot_cache, continuity

    def test_export_builds_bundle_with_manifest_and_durable_wiki(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            pack_dir = tmp / "pack"
            wiki_root = tmp / "wiki"
            bundle_dir = tmp / "bundle"
            self.seed_wiki(wiki_root)
            bootstrap = self.run_bootstrap("--filled-example", str(pack_dir))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            result = self.run_portability("export", "--pack-dir", str(pack_dir), "--wiki-root", str(wiki_root), "--out", str(bundle_dir))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            manifest = json.loads((bundle_dir / "portability-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["bundle_version"], "1")
            self.assertEqual(manifest["payload"]["durable_wiki"]["included"], True)
            self.assertEqual(manifest["payload"]["active_memory"]["included"], False)
            self.assertTrue((bundle_dir / "pack" / "daos-pack.json").exists())
            self.assertTrue((bundle_dir / "durable" / "wiki" / "index.md").exists())
            self.assertTrue((bundle_dir / "durable" / "wiki" / "pages" / "ops.md").exists())

    def test_export_excludes_active_memory_by_default_and_can_include_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            pack_dir = tmp / "pack"
            wiki_root = tmp / "wiki"
            bundle_dir = tmp / "bundle"
            hot_cache = tmp / "hot-cache.md"
            continuity = tmp / "agent-continuity.md"
            self.seed_wiki(wiki_root)
            hot_cache.write_text("# Hot Cache\n", encoding="utf-8")
            continuity.write_text("# Continuity\n", encoding="utf-8")
            bootstrap = self.run_bootstrap("--filled-example", str(pack_dir))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)

            default_export = self.run_portability("export", "--pack-dir", str(pack_dir), "--wiki-root", str(wiki_root), "--out", str(bundle_dir))
            self.assertEqual(default_export.returncode, 0, msg=default_export.stderr)
            self.assertFalse((bundle_dir / "active").exists())

            bundle_with_active = tmp / "bundle-active"
            active_export = self.run_portability(
                "export",
                "--pack-dir",
                str(pack_dir),
                "--wiki-root",
                str(wiki_root),
                "--out",
                str(bundle_with_active),
                "--include-active-memory",
                "--hot-cache",
                str(hot_cache),
                "--agent-continuity",
                str(continuity),
            )
            self.assertEqual(active_export.returncode, 0, msg=active_export.stderr)
            self.assertTrue((bundle_with_active / "active" / "hot-cache.md").exists())
            self.assertTrue((bundle_with_active / "active" / "agent-continuity.md").exists())

    def test_inspect_reports_bundle_payload_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            pack_dir = tmp / "pack"
            wiki_root = tmp / "wiki"
            bundle_dir = tmp / "bundle"
            self.seed_wiki(wiki_root)
            bootstrap = self.run_bootstrap("--filled-example", str(pack_dir))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            export = self.run_portability("export", "--pack-dir", str(pack_dir), "--wiki-root", str(wiki_root), "--out", str(bundle_dir))
            self.assertEqual(export.returncode, 0, msg=export.stderr)

            result = self.run_portability("inspect", str(bundle_dir))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("bundle_version: 1", result.stdout)
            self.assertIn("durable_wiki_files:", result.stdout)
            self.assertIn("active_memory_included: no", result.stdout)
            self.assertIn("schema_version: 1", result.stdout)

    def test_plan_reports_staged_actions_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            pack_dir = tmp / "pack"
            wiki_root = tmp / "wiki"
            bundle_dir = tmp / "bundle"
            target_wiki = tmp / "target-wiki"
            self.seed_wiki(wiki_root)
            bootstrap = self.run_bootstrap("--filled-example", str(pack_dir))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            export = self.run_portability("export", "--pack-dir", str(pack_dir), "--wiki-root", str(wiki_root), "--out", str(bundle_dir))
            self.assertEqual(export.returncode, 0, msg=export.stderr)

            result = self.run_portability("plan", str(bundle_dir), "--target-wiki-root", str(target_wiki))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertIn("would copy durable wiki files", result.stdout)
            self.assertIn("would restore pack metadata anchors", result.stdout)
            self.assertFalse(target_wiki.exists())

    def test_apply_restores_durable_wiki_and_metadata_into_empty_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            pack_dir = tmp / "pack"
            wiki_root = tmp / "wiki"
            bundle_dir = tmp / "bundle"
            target_wiki = tmp / "target-wiki"
            target_pack = tmp / "target-pack"
            self.seed_wiki(wiki_root)
            bootstrap = self.run_bootstrap("--filled-example", str(pack_dir))
            self.assertEqual(bootstrap.returncode, 0, msg=bootstrap.stderr)
            export = self.run_portability("export", "--pack-dir", str(pack_dir), "--wiki-root", str(wiki_root), "--out", str(bundle_dir))
            self.assertEqual(export.returncode, 0, msg=export.stderr)

            result = self.run_portability("apply", str(bundle_dir), "--target-wiki-root", str(target_wiki), "--target-pack-dir", str(target_pack))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertTrue((target_wiki / "index.md").exists())
            self.assertTrue((target_wiki / "pages" / "ops.md").exists())
            self.assertTrue((target_pack / "daos-pack.json").exists())
            self.assertTrue((target_pack / ".daos" / "manifest.json").exists())
            self.assertIn("copied durable wiki files", result.stdout)

    def test_apply_refuses_silent_overwrite_on_durable_wiki_conflict(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            _, _, bundle_dir, _, _ = self.bootstrap_pack_and_bundle(tmp)
            target_wiki = tmp / "target-wiki"
            target_pack = tmp / "target-pack"
            target_wiki.mkdir(parents=True)
            (target_wiki / "index.md").write_text("# Other durable root\n", encoding="utf-8")

            result = self.run_portability("apply", str(bundle_dir), "--target-wiki-root", str(target_wiki), "--target-pack-dir", str(target_pack))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual((target_wiki / "index.md").read_text(encoding="utf-8"), "# Other durable root\n")
            staged_conflicts = list((target_pack / ".daos" / "portability-review").glob("*.md"))
            self.assertEqual(len(staged_conflicts), 1)
            self.assertIn("collision", staged_conflicts[0].read_text(encoding="utf-8"))
            self.assertIn("collision review", result.stdout)

    def test_apply_stages_active_memory_sidecars_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            _, _, bundle_dir, _, _ = self.bootstrap_pack_and_bundle(tmp, include_active_memory=True)
            target_wiki = tmp / "target-wiki"
            target_pack = tmp / "target-pack"

            result = self.run_portability("apply", str(bundle_dir), "--target-wiki-root", str(target_wiki), "--target-pack-dir", str(target_pack))

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            staged_active = target_pack / ".daos" / "portability-stage" / "active-memory"
            self.assertTrue((staged_active / "hot-cache.md").exists())
            self.assertTrue((staged_active / "agent-continuity.md").exists())
            self.assertIn("active-memory stage", result.stdout)

    def test_apply_can_stage_incoming_durable_conflicts_for_manual_merge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            _, _, bundle_dir, _, _ = self.bootstrap_pack_and_bundle(tmp)
            target_wiki = tmp / "target-wiki"
            target_pack = tmp / "target-pack"
            target_wiki.mkdir(parents=True)
            (target_wiki / "index.md").write_text("# Other durable root\n", encoding="utf-8")

            result = self.run_portability(
                "apply",
                str(bundle_dir),
                "--target-wiki-root",
                str(target_wiki),
                "--target-pack-dir",
                str(target_pack),
                "--durable-conflicts",
                "stage",
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual((target_wiki / "index.md").read_text(encoding="utf-8"), "# Other durable root\n")
            staged_conflict = target_pack / ".daos" / "portability-stage" / "durable-conflicts" / "index.md"
            self.assertTrue(staged_conflict.exists())
            self.assertEqual(staged_conflict.read_text(encoding="utf-8"), "# Durable Wiki\n")
            self.assertIn("staged incoming durable conflicts", result.stdout)

    def test_apply_can_overwrite_durable_conflicts_with_backup_when_explicitly_requested(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)
            _, _, bundle_dir, _, _ = self.bootstrap_pack_and_bundle(tmp)
            target_wiki = tmp / "target-wiki"
            target_pack = tmp / "target-pack"
            target_wiki.mkdir(parents=True)
            (target_wiki / "index.md").write_text("# Other durable root\n", encoding="utf-8")

            result = self.run_portability(
                "apply",
                str(bundle_dir),
                "--target-wiki-root",
                str(target_wiki),
                "--target-pack-dir",
                str(target_pack),
                "--durable-conflicts",
                "overwrite",
            )

            self.assertEqual(result.returncode, 0, msg=result.stderr)
            self.assertEqual((target_wiki / "index.md").read_text(encoding="utf-8"), "# Durable Wiki\n")
            backups = list((target_pack / ".daos" / "portability-backups").glob("*/durable-wiki/index.md"))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(encoding="utf-8"), "# Other durable root\n")
            self.assertIn("overwrote durable wiki conflicts", result.stdout)


if __name__ == "__main__":
    unittest.main()
