from __future__ import annotations

import shutil
import sys
import unittest


def npm_command() -> str:
    """Return a platform-native npm executable for subprocess tests.

    On Windows, the npm launcher is normally ``npm.cmd``. On Linux/macOS/WSL,
    executing a Windows ``npm.cmd`` shim directly can fail with ``Exec format
    error``, so prefer the native ``npm`` binary and do not fall back to the
    Windows launcher there.
    """

    if sys.platform == "win32":
        executable = shutil.which("npm.cmd") or shutil.which("npm")
    else:
        executable = shutil.which("npm")
    if executable is None:
        raise unittest.SkipTest("npm executable not found")
    return executable
