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
    assert "solutionsOutdatedBanner" in sheet
    assert LIGHT.danger in sheet
    assert LIGHT.window in sheet
    assert "QWidget#welcomeRoot QPushButton#welcomeClearRecent" in sheet
    assert LIGHT.accent in sheet
    assert LIGHT.alternate in sheet
    assert "welcomeRecentList" in sheet
    assert "welcomeRecentLabel" in sheet
    assert "uppercase" in sheet
    assert "welcomeRoot" in sheet
    assert "QWidget#welcomeRoot QLabel#welcomeBrand" in sheet
    assert "QWidget#welcomeRoot QLabel#welcomeSubtitle" in sheet
    assert "QWidget#welcomeRoot QLabel#welcomeTagline" in sheet
    assert "QWidget#welcomeRoot QPushButton#primaryButton" in sheet
    assert "QWidget#workspaceEmptyOverlay QPushButton#primaryButton" in sheet
    assert "QWidget#aboutRoot QPushButton#primaryButton" in sheet
    assert "QWidget#whatsNewRoot QPushButton#primaryButton" in sheet
    assert "QWidget#shortcutsRoot QPushButton#primaryButton" in sheet
    assert "QWidget#welcomeRoot QPushButton {" in sheet
    assert "QWidget#workspaceEmptyOverlay QPushButton {" in sheet
    assert "aboutRoot" in sheet
    assert "QWidget#aboutRoot QLabel#welcomeBrand" in sheet
    assert "QWidget#aboutRoot QLabel#welcomeSubtitle" in sheet
    assert "QWidget#aboutRoot QLabel#welcomeTagline" in sheet
    assert "whatsNewRoot" in sheet
    assert "shortcutsRoot" in sheet
    assert "whatsNewBody" in sheet
    assert "shortcutsTable" in sheet
    assert "helpDialogHeading" in sheet
    assert "QWidget#shortcutsRoot QHeaderView::section" in sheet
    assert LIGHT.panel in sheet
    assert LIGHT.accent in sheet
    assert LIGHT.accent_text in sheet
    assert LIGHT.accent_hover in sheet
    assert "welcomeRecentList::item:selected" in sheet
    assert LIGHT.accent_text in sheet
