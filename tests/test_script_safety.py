
# DAOS baseline note: current public framework baseline is v0.2.7; this module remains part of the current release surface.
from __future__ import annotations

import ast
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_ROOT = REPO_ROOT / "scripts"
NETWORK_MODULES = {"requests", "urllib", "socket", "http", "ftplib", "smtplib"}
BANNED_MODULES = NETWORK_MODULES | {"subprocess"}


class DaosScriptSafetyTests(unittest.TestCase):
    def python_script_paths(self) -> list[Path]:
        return sorted(SCRIPTS_ROOT.rglob("*.py"))

    def imported_roots(self, path: Path) -> set[str]:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        roots: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    roots.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom) and node.module:
                roots.add(node.module.split(".")[0])
        return roots

    def test_scripts_do_not_use_network_or_shell_execution_modules(self) -> None:
        offenders: list[str] = []
        for path in self.python_script_paths():
            imported = self.imported_roots(path)
            banned = sorted(imported.intersection(BANNED_MODULES))
            if banned:
                offenders.append(f"{path.relative_to(REPO_ROOT)} imports {', '.join(banned)}")

        self.assertEqual(
            offenders,
            [],
            "DAOS scripts should stay local/stdlib-safe; document and review before adding network or subprocess use. Offenders: "
            + "; ".join(offenders),
        )

    def test_advanced_write_capable_scripts_are_not_front_door_commands(self) -> None:
        front_door_docs = [REPO_ROOT / "README.md", REPO_ROOT / "docs" / "quickstart.md"]
        advanced_commands = {"scripts/daos_update.py", "scripts/daos_portability.py"}
        offenders: list[str] = []
        for doc in front_door_docs:
            content = doc.read_text(encoding="utf-8")
            for command in advanced_commands:
                if command in content:
                    offenders.append(f"{doc.relative_to(REPO_ROOT)} advertises {command}")

        self.assertEqual(
            offenders,
            [],
            "Front-door docs should keep write-capable maintenance/portability scripts out of first-run command lists; link advanced docs instead. Offenders: "
            + "; ".join(offenders),
        )


if __name__ == "__main__":
    unittest.main()
