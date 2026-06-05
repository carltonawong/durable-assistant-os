from __future__ import annotations

import unittest
from unittest import mock

import npm_command


class NpmCommandResolutionTests(unittest.TestCase):
    def test_non_windows_uses_native_npm_without_cmd_fallback(self) -> None:
        calls: list[str] = []

        def fake_which(name: str) -> str | None:
            calls.append(name)
            if name == "npm":
                return None
            if name == "npm.cmd":
                return "/mnt/c/Program Files/nodejs/npm.cmd"
            return None

        with mock.patch.object(npm_command.sys, "platform", "linux"), mock.patch.object(
            npm_command.shutil,
            "which",
            side_effect=fake_which,
        ):
            with self.assertRaises(unittest.SkipTest):
                npm_command.npm_command()

        self.assertEqual(calls, ["npm"])

    def test_windows_prefers_cmd_launcher(self) -> None:
        with mock.patch.object(npm_command.sys, "platform", "win32"), mock.patch.object(
            npm_command.shutil,
            "which",
            side_effect=lambda name: "C:/Program Files/nodejs/npm.cmd" if name == "npm.cmd" else "C:/Program Files/nodejs/npm",
        ):
            self.assertEqual(npm_command.npm_command(), "C:/Program Files/nodejs/npm.cmd")
