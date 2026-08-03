"""System theme must not force the fictional Sans Serif font family."""

from PySide6.QtWidgets import QApplication

from studio.theme import _BRAND_CANDIDATES, _UI_FAMILY, apply_theme
from studio.theme_tokens import LIGHT


def test_system_theme_uses_bundled_ui_font_when_available(qapp):
    del qapp
    app = QApplication.instance()
    assert app is not None

    apply_theme(app, "system")
    family = app.font().family()
    assert family != "Sans Serif"
    assert family == _UI_FAMILY


def test_light_theme_keeps_source_sans(qapp):
    del qapp
    app = QApplication.instance()
    assert app is not None

    apply_theme(app, "light")
    assert app.font().family() == _UI_FAMILY


def test_system_theme_keeps_welcome_brand_typography(qapp):
    del qapp
    app = QApplication.instance()
    assert app is not None

    apply_theme(app, "system")
    sheet = app.styleSheet()
    assert "welcomeBrand" in sheet
    assert "42px" in sheet
    assert any(name in sheet for name in _BRAND_CANDIDATES)
    assert "welcomeSubtitle" in sheet
    assert "welcomeTagline" in sheet
    assert "workspaceEmptyTitle" in sheet
    assert "18px" in sheet
    assert "workspaceEmptyBlurb" in sheet
    assert "workspaceEmptyOverlay" in sheet
    assert LIGHT.text in sheet
    assert LIGHT.muted in sheet
    assert LIGHT.base in sheet
    assert LIGHT.border in sheet
