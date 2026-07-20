"""Application entry point for BoardComposer Studio."""

import sys

from PySide6.QtWidgets import QApplication

from studio.branding import app_icon
from studio.main_window import MainWindow
from studio.services import StudioServices
from studio.theme import apply_theme


def main() -> int:
    """Run BoardComposer Studio."""
    app = QApplication(sys.argv)
    app.setApplicationName("BoardComposer Studio")
    app.setOrganizationName("EDF Developer")
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
