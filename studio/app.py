"""Application entry point for BoardComposer Studio."""

from __future__ import annotations

import signal
import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from studio.branding import app_icon
from studio.main_window import MainWindow
from studio.services import StudioServices
from studio.theme import apply_theme, bootstrap_ui_font


def _install_sigint_handler(app: QApplication) -> QTimer:
    """Quit the Qt loop on Ctrl+C instead of interrupting a Python override."""

    def _quit(*_args: object) -> None:
        app.quit()

    signal.signal(signal.SIGINT, _quit)
    # Python only delivers signals between bytecode ops; a short timer lets
    # SIGINT reach the handler while Qt is blocking in C++.
    timer = QTimer(app)
    timer.setInterval(200)
    timer.timeout.connect(lambda: None)
    timer.start()
    return timer


def main() -> int:
    """Run BoardComposer Studio."""
    app = QApplication(sys.argv)
    bootstrap_ui_font(app)
    app.setApplicationName("BoardComposer Studio")
    app.setOrganizationName("EDF Developer")
    _install_sigint_handler(app)
    icon = app_icon()
    if not icon.isNull():
        app.setWindowIcon(icon)
    services = StudioServices()
    apply_theme(app, services.preferences.current.theme)
    window = MainWindow(services=services)
    if not icon.isNull():
        window.setWindowIcon(icon)
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
