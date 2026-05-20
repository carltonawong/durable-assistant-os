from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def npm_command() -> str:
    executable = shutil.which("npm.cmd") or shutil.which("npm")
    if executable is None:
        raise unittest.SkipTest("npm executable not found")
    return executable


class DaosNpmPackagePayloadTests(unittest.TestCase):
    def npm_pack_dry_run(self) -> dict:
        result = subprocess.run(
            [npm_command(), "pack", "--dry-run", "--json"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, msg=result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(len(payload), 1)
        return payload[0]

    def test_npm_package_contains_runtime_payload_without_test_or_cache_bloat(self) -> None:
        package = self.npm_pack_dry_run()
        paths = {entry["path"] for entry in package["files"]}

        required_paths = {
            "package.json",
            "README.md",
            "LICENSE",
            "NOTICE",
            "CHANGELOG.md",
            "bin/use-daos.js",
            "docs/memory-parity-auditor.md",
            "docs/releases/v0.2.0.md",
            "docs/releases/v0.2.1.md",
            "docs/releases/v0.2.2.md",
            "docs/releases/v0.2.3.md",
            "docs/releases/v0.2.4.md",
            "docs/releases/v0.2.5.md",
            "docs/script-safety.md",
            "docs/wiki-governance.md",
            "docs/reset-current-state-receipt.md",
            "examples/creative-studio-operating-profile-example.md",
            "harness/core-setup.md",
            "harness/first-week.md",
            "scripts/daos.py",
            "scripts/daos_bootstrap.py",
            "scripts/daos_memory_parity.py",
            "scripts/daos_portability.py",
            "scripts/daos_update.py",
            "scripts/daos_validate.py",
            "scripts/daos_wizard.py",
            "scripts/daos_core/__init__.py",
            "scripts/daos_core/boot_check.py",
            "scripts/daos_core/harness.py",
            "scripts/daos_core/render.py",
            "scripts/daos_core/schema.py",
            "scripts/daos_core/validate.py",
            "starter-pack/AGENTS.md",
            "starter-pack/wiki/cache/hot-cache.md",
            "starter-pack/wiki/cache/hot-cache-log.md",
            "starter-pack/wiki/cache/reset-handoff.md",
            "starter-pack/wiki/cache/agent-continuity.md",
        }
        missing = sorted(required_paths - paths)
        self.assertEqual(missing, [], "npm package is missing runtime payload files")

        forbidden_prefixes = ("tests/", "docs/assets/", "examples/evals/")
        forbidden_paths = {
            "docs/evals.md",
            "docs/eval-metric-stack.md",
            "docs/eval-results.md",
            "docs/eval-validity.md",
        }
        forbidden_fragments = (
            "__pycache__",
            ".pyc",
            "daos_adversarial_eval.py",
            "daos_eval.py",
            "daos_continuity_",
        )
        offenders = sorted(
            path
            for path in paths
            if path.startswith(forbidden_prefixes)
            or path in forbidden_paths
            or any(fragment in path for fragment in forbidden_fragments)
        )
        self.assertEqual(offenders, [], "npm package includes test/cache/asset/private eval bloat")


    def test_packaged_markdown_references_only_packaged_repo_files(self) -> None:
        package = self.npm_pack_dry_run()
        paths = {entry["path"] for entry in package["files"]}
        markdown_paths = sorted(
            path for path in paths if path.endswith(".md") and path != "CHANGELOG.md"
        )
        repo_prefixes = ("docs/", "examples/", "harness/", "scripts/", "starter-pack/", "templates/")
        tracked = subprocess.run(
            ["git", "ls-files"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(tracked.returncode, 0, msg=tracked.stderr)
        repo_files = set(tracked.stdout.splitlines())

        offenders: list[str] = []
        reference_pattern = re.compile(r"(?:\[[^\]]*\]\(([^)]+)\))|`([^`]+)`")
        for markdown_path in markdown_paths:
            text = (REPO_ROOT / markdown_path).read_text(encoding="utf-8")
            for match in reference_pattern.finditer(text):
                raw_reference = (match.group(1) or match.group(2) or "").strip()
                target = raw_reference.split("#", 1)[0].strip()
                if not target or "://" in target or target.startswith(("#", "mailto:")):
                    continue
                if target.startswith("./"):
                    target = target[2:]
                candidate_paths = [target]
                if not target.startswith(repo_prefixes) and not target.startswith("/"):
                    candidate_paths.append(
                        str((Path(markdown_path).parent / target).as_posix())
                    )
                for candidate in candidate_paths:
                    candidate = candidate.lstrip("/")
                    if candidate in repo_files and candidate not in paths:
                        offenders.append(f"{markdown_path} references unpackaged {candidate}")

        self.assertEqual(sorted(set(offenders)), [])

    def test_npm_package_stays_small_enough_for_release_distribution(self) -> None:
        package = self.npm_pack_dry_run()

        self.assertLessEqual(package["entryCount"], 70)
        # Current compact docs/proof surface stays below ~110 KB.
        self.assertLessEqual(package["size"], 109_200)


if __name__ == "__main__":
    unittest.main()
