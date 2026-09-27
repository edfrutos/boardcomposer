"""Preferences dialog stays within the screen (scroll, buttons pinned)."""

from PySide6.QtGui import QGuiApplication
from PySide6.QtWidgets import QScrollArea

from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.preferences import StudioPreferences


def test_preferences_dialog_scrolls_within_screen(qapp):
    del qapp
    dialog = PreferencesDialog(StudioPreferences(language="es"))
    scroll = dialog.findChild(QScrollArea)
    assert scroll is not None
    assert scroll.widget() is dialog._body
    assert dialog.general.parentWidget() is dialog._body
    assert dialog._buttons.parentWidget() is dialog
    screen = QGuiApplication.primaryScreen()
    assert screen is not None
    available = screen.availableGeometry().height()
    assert dialog.height() <= dialog.maximumHeight() <= available
    if dialog._body.sizeHint().height() > dialog._scroll.sizeHint().height():
        assert dialog.height() > dialog._scroll.sizeHint().height()
