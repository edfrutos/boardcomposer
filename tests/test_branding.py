"""Tests for BoardComposer Studio branding assets."""

from studio.branding import APP_ICON_PATH, app_icon
from studio.dialogs.help_dialogs import AboutDialog


def test_app_icon_asset_exists():
    assert APP_ICON_PATH.is_file()


def test_app_icon_loads(qapp):
    del qapp
    icon = app_icon()
    assert not icon.isNull()
    assert icon.availableSizes()


def test_about_dialog_shows_app_icon(qapp):
    del qapp
    dialog = AboutDialog(language="es")
    assert not dialog.windowIcon().isNull()
