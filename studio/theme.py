"""Apply Studio appearance preferences (theme) to the Qt application."""

from __future__ import annotations

from PySide6.QtGui import QColor, QPalette
from PySide6.QtWidgets import QApplication

VALID_THEMES = ("system", "light", "dark")
DEFAULT_THEME = "system"


def _light_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(245, 245, 245))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.Text, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.Button, QColor(240, 240, 240))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(37, 99, 235))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(255, 255, 220))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(30, 30, 30))
    return palette


def _dark_palette() -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(55, 55, 55))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Button, QColor(55, 55, 55))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(37, 99, 235))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(60, 60, 60))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(150, 150, 150))
    return palette


def apply_theme(app: QApplication, theme: str) -> None:
    """Apply a Studio theme to `app`.

    `system` restores the platform default style/palette.
    """
    name = theme if theme in VALID_THEMES else DEFAULT_THEME
    if name == "system":
        app.setStyle("Fusion")
        app.setPalette(app.style().standardPalette())
        return

    app.setStyle("Fusion")
    if name == "dark":
        app.setPalette(_dark_palette())
    else:
        app.setPalette(_light_palette())
