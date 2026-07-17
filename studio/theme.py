"""Apply Studio appearance preferences (theme) to the Qt application."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

from studio.theme_tokens import ThemeTokens, tokens_for

VALID_THEMES = ("system", "light", "dark")
DEFAULT_THEME = "system"

_FONTS_REGISTERED = False
_FONTS_DIR = Path(__file__).resolve().parent / "assets" / "fonts"

# Families reported by QFontDatabase for the bundled static TTFs.
_UI_FAMILY = "Source Sans 3"
_UI_SEMIBOLD_FAMILY = "Source Sans 3 SemiBold"
_BRAND_CANDIDATES = ("Archivo ExtraBold", "Archivo SemiBold", "Archivo")


def _register_bundled_fonts() -> None:
    """Load OFL fonts from studio/assets/fonts/ once per process."""
    global _FONTS_REGISTERED
    if _FONTS_REGISTERED:
        return
    if not _FONTS_DIR.is_dir():
        _FONTS_REGISTERED = True
        return
    for path in sorted(_FONTS_DIR.glob("*.ttf")):
        QFontDatabase.addApplicationFont(str(path))
    _FONTS_REGISTERED = True


def _palette_from_tokens(tokens: ThemeTokens) -> QPalette:
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(tokens.window))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(tokens.text))
    palette.setColor(QPalette.ColorRole.Base, QColor(tokens.base))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(tokens.alternate))
    palette.setColor(QPalette.ColorRole.Text, QColor(tokens.text))
    palette.setColor(QPalette.ColorRole.Button, QColor(tokens.panel))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(tokens.text))
    palette.setColor(QPalette.ColorRole.Highlight, QColor(tokens.accent))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor(tokens.accent_text))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(tokens.panel))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor(tokens.tooltip))
    palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(tokens.muted))
    palette.setColor(QPalette.ColorRole.Light, QColor(tokens.base))
    palette.setColor(QPalette.ColorRole.Midlight, QColor(tokens.alternate))
    palette.setColor(QPalette.ColorRole.Mid, QColor(tokens.border))
    palette.setColor(QPalette.ColorRole.Dark, QColor(tokens.border))
    palette.setColor(QPalette.ColorRole.Shadow, QColor(tokens.text))
    palette.setColor(QPalette.ColorRole.Link, QColor(tokens.accent))
    palette.setColor(QPalette.ColorRole.LinkVisited, QColor(tokens.accent_hover))
    return palette


def build_stylesheet(tokens: ThemeTokens) -> str:
    """Build application QSS from design tokens."""
    ui = tokens.font_ui
    brand = tokens.font_brand
    return f"""
    * {{
        font-family: "{ui}";
        font-size: 13px;
    }}
    QWidget {{
        color: {tokens.text};
    }}
    QMainWindow, QDialog {{
        background-color: {tokens.window};
    }}
    QMenuBar {{
        background-color: {tokens.panel};
        color: {tokens.text};
        border-bottom: 1px solid {tokens.border};
        padding: 2px 4px;
    }}
    QMenuBar::item:selected {{
        background-color: {tokens.alternate};
    }}
    QMenu {{
        background-color: {tokens.base};
        color: {tokens.text};
        border: 1px solid {tokens.border};
        padding: 4px;
    }}
    QMenu::item:selected {{
        background-color: {tokens.accent};
        color: {tokens.accent_text};
    }}
    QStatusBar {{
        background-color: {tokens.panel};
        color: {tokens.muted};
        border-top: 1px solid {tokens.border};
    }}
    QToolTip {{
        background-color: {tokens.panel};
        color: {tokens.tooltip};
        border: 1px solid {tokens.border};
        padding: 4px 8px;
    }}
    QPushButton {{
        background-color: {tokens.panel};
        color: {tokens.text};
        border: 1px solid {tokens.border};
        border-radius: 4px;
        padding: 6px 14px;
        min-height: 28px;
    }}
    QPushButton:hover {{
        background-color: {tokens.alternate};
        border-color: {tokens.accent};
    }}
    QPushButton:pressed {{
        background-color: {tokens.border};
    }}
    QPushButton:disabled {{
        color: {tokens.muted};
        background-color: {tokens.alternate};
    }}
    QPushButton#primaryButton {{
        background-color: {tokens.accent};
        color: {tokens.accent_text};
        border: 1px solid {tokens.accent_hover};
        font-family: "{_UI_SEMIBOLD_FAMILY}";
        font-weight: 600;
    }}
    QPushButton#primaryButton:hover {{
        background-color: {tokens.accent_hover};
    }}
    QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox, QTextEdit, QPlainTextEdit {{
        background-color: {tokens.base};
        color: {tokens.text};
        border: 1px solid {tokens.border};
        border-radius: 4px;
        padding: 4px 8px;
        selection-background-color: {tokens.accent};
        selection-color: {tokens.accent_text};
    }}
    QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus,
    QTextEdit:focus, QPlainTextEdit:focus {{
        border: 1px solid {tokens.accent};
    }}
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    QComboBox QAbstractItemView {{
        background-color: {tokens.base};
        color: {tokens.text};
        border: 1px solid {tokens.border};
        selection-background-color: {tokens.accent};
        selection-color: {tokens.accent_text};
    }}
    QListWidget, QTreeWidget, QTableWidget, QTableView {{
        background-color: {tokens.base};
        alternate-background-color: {tokens.alternate};
        color: {tokens.text};
        border: 1px solid {tokens.border};
        border-radius: 4px;
        outline: none;
    }}
    QListWidget::item:selected, QTreeWidget::item:selected,
    QTableWidget::item:selected, QTableView::item:selected {{
        background-color: {tokens.accent};
        color: {tokens.accent_text};
    }}
    QHeaderView::section {{
        background-color: {tokens.panel};
        color: {tokens.muted};
        border: none;
        border-bottom: 1px solid {tokens.border};
        border-right: 1px solid {tokens.border};
        padding: 6px 8px;
        font-family: "{_UI_SEMIBOLD_FAMILY}";
    }}
    QGroupBox {{
        background-color: {tokens.panel};
        border: 1px solid {tokens.border};
        border-radius: 6px;
        margin-top: 12px;
        padding: 12px 10px 10px 10px;
        font-family: "{_UI_SEMIBOLD_FAMILY}";
    }}
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 4px;
        color: {tokens.muted};
    }}
    QTabWidget::pane {{
        border: 1px solid {tokens.border};
        background-color: {tokens.base};
        border-radius: 4px;
    }}
    QTabBar::tab {{
        background-color: {tokens.panel};
        color: {tokens.muted};
        border: 1px solid {tokens.border};
        border-bottom: none;
        padding: 6px 14px;
        margin-right: 2px;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }}
    QTabBar::tab:selected {{
        background-color: {tokens.base};
        color: {tokens.text};
        border-bottom: 2px solid {tokens.accent};
    }}
    QScrollBar:vertical {{
        background: {tokens.scroll};
        width: 10px;
        margin: 0;
    }}
    QScrollBar::handle:vertical {{
        background: {tokens.scroll_handle};
        border-radius: 4px;
        min-height: 24px;
    }}
    QScrollBar:horizontal {{
        background: {tokens.scroll};
        height: 10px;
        margin: 0;
    }}
    QScrollBar::handle:horizontal {{
        background: {tokens.scroll_handle};
        border-radius: 4px;
        min-width: 24px;
    }}
    QScrollBar::add-line, QScrollBar::sub-line {{
        width: 0;
        height: 0;
    }}
    QLabel#welcomeBrand {{
        font-family: "{brand}";
        font-size: 42px;
        font-weight: 800;
        letter-spacing: -1px;
        color: {tokens.text};
    }}
    QLabel#welcomeSubtitle {{
        font-family: "{ui}";
        font-size: 13px;
        color: {tokens.muted};
    }}
    QLabel#welcomeTagline {{
        font-family: "{ui}";
        font-size: 16px;
        color: {tokens.text};
        margin-top: 4px;
    }}
    QLabel#welcomeRecentLabel {{
        font-family: "{_UI_SEMIBOLD_FAMILY}";
        font-size: 12px;
        color: {tokens.muted};
        letter-spacing: 0.6px;
        text-transform: uppercase;
    }}
    QWidget#welcomeRoot {{
        background-color: {tokens.window};
    }}
    QListWidget#welcomeRecentList {{
        background-color: {tokens.base};
        border: 1px solid {tokens.border};
        border-radius: 6px;
        padding: 6px;
    }}
    """


def apply_theme(app: QApplication, theme: str) -> None:
    """Apply a Studio theme to `app`.

    `system` restores the platform default style/palette and clears QSS.
    """
    _register_bundled_fonts()
    name = theme if theme in VALID_THEMES else DEFAULT_THEME
    app.setStyle("Fusion")

    if name == "system":
        app.setStyleSheet("")
        app.setPalette(app.style().standardPalette())
        app.setFont(QFont())
        return

    tokens = tokens_for(name)
    if tokens is None:
        app.setStyleSheet("")
        app.setPalette(app.style().standardPalette())
        return

    families = set(QFontDatabase.families())
    ui_family = _UI_FAMILY if _UI_FAMILY in families else tokens.font_ui
    brand_family = next(
        (name for name in _BRAND_CANDIDATES if name in families),
        tokens.font_brand,
    )
    resolved = ThemeTokens(
        window=tokens.window,
        base=tokens.base,
        alternate=tokens.alternate,
        panel=tokens.panel,
        text=tokens.text,
        muted=tokens.muted,
        border=tokens.border,
        accent=tokens.accent,
        accent_hover=tokens.accent_hover,
        accent_text=tokens.accent_text,
        danger=tokens.danger,
        tooltip=tokens.tooltip,
        scroll=tokens.scroll,
        scroll_handle=tokens.scroll_handle,
        font_ui=ui_family,
        font_brand=brand_family,
    )

    app.setPalette(_palette_from_tokens(resolved))
    app.setFont(QFont(ui_family, 13))
    app.setStyleSheet(build_stylesheet(resolved))
