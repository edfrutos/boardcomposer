"""Shared pytest fixtures for headless Qt tests (DT-0004).

Tests that instantiate real PySide6 widgets need a single, session-wide
`QApplication`. Setting `QT_QPA_PLATFORM=offscreen` (before Qt is imported
anywhere) lets the full widget/graphics-scene stack run without a display
server, which is what makes these tests runnable in CI and in sandboxed
agent environments alike.
"""

import atexit
import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# First QWidget/QDialog on Linux can block on AT-SPI/DBus or fontconfig
# with no session bus (GitHub ubuntu-latest). Disable a11y bridge and
# keep offscreen tests from waiting until the job timeout.
os.environ.setdefault("QT_ACCESSIBILITY", "0")
os.environ.setdefault("NO_AT_BRIDGE", "1")

import pytest  # noqa: E402
from PySide6.QtWidgets import QApplication  # noqa: E402


def _save_coverage() -> None:
    try:
        import coverage
    except ImportError:
        return
    current = getattr(coverage.Coverage, "current", None)
    if current is None:
        return
    cov = current()
    if cov is not None:
        cov.save()


@pytest.fixture(scope="session")
def qapp():
    """Provide a single QApplication instance for the whole test session."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app


def pytest_sessionfinish(session, exitstatus):
    """Leave before PySide tears down QObjects at interpreter shutdown.

    A green suite still segfaults (exit 139) when Python deletes shared
    styles, fonts and leftover windows. The result is already recorded.
    """
    del session
    code = int(exitstatus)

    def _finish() -> None:
        _save_coverage()
        sys.stdout.flush()
        sys.stderr.flush()
        os._exit(code)

    atexit.register(_finish)
