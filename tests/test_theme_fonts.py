"""System theme must not force the fictional Sans Serif font family."""

from PySide6.QtWidgets import QApplication

from studio.theme import apply_theme, _UI_FAMILY


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
