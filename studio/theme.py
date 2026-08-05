"""Apply Studio appearance preferences (theme) to the Qt application."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtGui import QColor, QFont, QFontDatabase, QPalette
from PySide6.QtWidgets import QApplication

from studio.theme_tokens import LIGHT, ThemeTokens, tokens_for

VALID_THEMES = ("system", "light", "dark")
DEFAULT_THEME = "system"

_FONTS_REGISTERED = False
_FONTS_DIR = Path(__file__).resolve().parent / "assets" / "fonts"

# Families reported by QFontDatabase for the bundled static TTFs.
_UI_FAMILY = "Source Sans 3"
_UI_SEMIBOLD_FAMILY = "Source Sans 3 SemiBold"
_BRAND_CANDIDATES = ("Archivo SemiBold", "Archivo")


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
    QDockWidget {{
        color: {tokens.text};
    }}
    QDockWidget::title {{
        background-color: {tokens.panel};
        color: {tokens.text};
        text-align: left;
        padding: 7px 10px;
        border-bottom: 1px solid {tokens.border};
        font-family: "{_UI_SEMIBOLD_FAMILY}";
    }}
    QSplitter::handle {{
        background-color: {tokens.border};
    }}
    QSplitter::handle:horizontal {{
        width: 2px;
    }}
    QSplitter::handle:vertical {{
        height: 2px;
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
    QPushButton:focus {{
        border: 2px solid {tokens.accent};
        padding: 5px 13px;
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
        min-height: 44px;
    }}
    QPushButton#primaryButton:focus {{
        border: 2px solid {tokens.text};
        padding: 5px 13px;
    }}
    QToolBar#mainToolbar {{
        background-color: {tokens.window};
        border: none;
        border-bottom: 1px solid {tokens.border};
        spacing: 4px;
        padding: 2px 6px;
    }}
    QToolBar#mainToolbar QToolButton {{
        color: {tokens.text};
        background: transparent;
        border: 1px solid transparent;
        border-radius: 4px;
        padding: 5px 10px;
        min-height: 28px;
        font-family: "{ui}";
        font-size: 12px;
    }}
    QToolBar#mainToolbar QToolButton:hover {{
        background-color: {tokens.alternate};
        border: 1px solid {tokens.border};
    }}
    QToolBar#mainToolbar QToolButton:checked {{
        background-color: {tokens.alternate};
        border: 1px solid {tokens.accent};
    }}
    QToolBar#mainToolbar QToolButton:focus {{
        border: 1px solid {tokens.accent};
        background-color: {tokens.alternate};
    }}
    QPushButton#primaryButton:hover {{
        background-color: {tokens.accent_hover};
    }}
    QDialogButtonBox QPushButton {{
        min-height: 36px;
        min-width: 80px;
    }}
    QCheckBox {{
        color: {tokens.text};
        spacing: 8px;
    }}
    QCheckBox:focus {{
        color: {tokens.text};
    }}
    QCheckBox::indicator {{
        width: 16px;
        height: 16px;
        border: 1px solid {tokens.border};
        border-radius: 3px;
        background-color: {tokens.base};
    }}
    QCheckBox::indicator:checked {{
        background-color: {tokens.accent};
        border-color: {tokens.accent_hover};
    }}
    QCheckBox::indicator:focus {{
        border: 2px solid {tokens.accent};
    }}
    QTextEdit#inspectorPanel {{
        background-color: {tokens.base};
        color: {tokens.text};
        border: none;
        padding: 8px 10px;
        font-family: "{ui}";
        font-size: 13px;
        selection-background-color: {tokens.accent};
        selection-color: {tokens.accent_text};
    }}
    QLabel#exportGraphicPreview {{
        background-color: {tokens.alternate};
        color: {tokens.muted};
        border: 1px solid {tokens.border};
        border-radius: 4px;
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
    }}
    QListWidget:focus, QTreeWidget:focus, QTableWidget:focus, QTableView:focus {{
        border: 1px solid {tokens.accent};
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
    QLabel#solutionsOutdatedBanner {{
        background-color: {tokens.window};
        color: {tokens.danger};
        border: 1px solid {tokens.danger};
        border-radius: 4px;
        padding: 6px 8px;
        font-family: "{ui}";
        font-size: 12px;
    }}
    QWidget#welcomeRoot {{
        background-color: {tokens.window};
    }}
    QPushButton#welcomeClearRecent {{
        color: {tokens.muted};
        background: transparent;
        border: 1px solid transparent;
        min-height: 32px;
        padding: 4px 8px;
    }}
    QPushButton#welcomeClearRecent:hover {{
        color: {tokens.text};
        border: 1px solid {tokens.border};
        background-color: {tokens.alternate};
    }}
    QPushButton#welcomeClearRecent:focus {{
        border: 2px solid {tokens.accent};
        padding: 3px 7px;
    }}
    QWidget#workspaceEmptyOverlay {{
        background-color: {tokens.base};
        border: 1px solid {tokens.border};
        border-radius: 8px;
    }}
    QWidget#workspaceEmptyOverlay QPushButton {{
        text-align: center;
    }}
    QLabel#workspaceEmptyTitle {{
        font-family: "{_UI_SEMIBOLD_FAMILY}";
        font-size: 18px;
        font-weight: 600;
        color: {tokens.text};
    }}
    QLabel#workspaceEmptyBlurb {{
        font-family: "{ui}";
        font-size: 13px;
        color: {tokens.muted};
        margin-bottom: 4px;
    }}
    QListWidget#welcomeRecentList {{
        background-color: {tokens.base};
        border: 1px solid {tokens.border};
        border-radius: 6px;
        padding: 6px;
    }}
    """


def _resolved_ui_and_brand_families() -> tuple[str | None, str | None]:
    """Return bundled UI / brand family names when registered, else None."""
    families = set(QFontDatabase.families())
    ui = _UI_FAMILY if _UI_FAMILY in families else None
    brand = next((name for name in _BRAND_CANDIDATES if name in families), None)
    return ui, brand


def _welcome_typography_qss(*, brand: str | None, ui: str | None) -> str:
    """Minimal Welcome/About/help typography + empty-overlay + outdated banner
    + Clear Recent + recent column + Welcome/About/WhatsNew/Shortcuts/Explain
    roots + scoped button chrome under ``system``.

    Empty overlay, outdated banner, Clear Recent, recent label/list (ink +
    selection), ``#welcomeRoot``, ``#aboutRoot``, ``#whatsNewRoot``,
    ``#shortcutsRoot``, and ``#explainSolutionRoot`` sit on light (taller)
    surfaces even when the OS palette is dark, so ink/background use LIGHT
    tokens for contrast. Brand ink plus primary buttons are scoped under
    Welcome/About/WhatsNew/Shortcuts/Explain/empty roots; secondary chrome
    stays on Welcome/empty/Explain so Preferences keep platform chrome
    (intentional: no ``#preferencesRoot`` / no LIGHT-scoped prefs form).
    ``#welcomeClearRecent`` keeps its own transparent/hover rules (more
    specific ID).
    """
    parts: list[str] = []
    if brand:
        parts.append(
            f"QLabel#welcomeBrand {{"
            f' font-family: "{brand}";'
            f" font-size: 42px;"
            f" font-weight: 800;"
            f" letter-spacing: -1px;"
            f" }}"
        )
    if ui:
        parts.append(
            f'QLabel#welcomeSubtitle {{ font-family: "{ui}"; font-size: 13px; }}'
        )
        parts.append(
            f'QLabel#welcomeTagline {{ font-family: "{ui}"; font-size: 16px; }}'
        )
        families = set(QFontDatabase.families())
        title_family = _UI_SEMIBOLD_FAMILY if _UI_SEMIBOLD_FAMILY in families else ui
        parts.append(
            f"QLabel#workspaceEmptyTitle {{"
            f' font-family: "{title_family}";'
            f" font-size: 18px;"
            f" font-weight: 600;"
            f" color: {LIGHT.text};"
            f" }}"
        )
        parts.append(
            f"QLabel#workspaceEmptyBlurb {{"
            f' font-family: "{ui}";'
            f" font-size: 13px;"
            f" color: {LIGHT.muted};"
            f" margin-bottom: 4px;"
            f" }}"
        )
        label_family = title_family
    else:
        parts.append(
            f"QLabel#workspaceEmptyTitle {{"
            f" font-size: 18px;"
            f" font-weight: 600;"
            f" color: {LIGHT.text};"
            f" }}"
        )
        parts.append(
            f"QLabel#workspaceEmptyBlurb {{"
            f" font-size: 13px;"
            f" color: {LIGHT.muted};"
            f" margin-bottom: 4px;"
            f" }}"
        )
        label_family = None
    parts.append(
        f"QWidget#workspaceEmptyOverlay {{"
        f" background-color: {LIGHT.base};"
        f" border: 1px solid {LIGHT.border};"
        f" border-radius: 8px;"
        f" }}"
    )
    banner_font = f' font-family: "{ui}";' if ui else ""
    parts.append(
        f"QLabel#solutionsOutdatedBanner {{"
        f" background-color: {LIGHT.window};"
        f" color: {LIGHT.danger};"
        f" border: 1px solid {LIGHT.danger};"
        f" border-radius: 4px;"
        f" padding: 6px 8px;"
        f"{banner_font}"
        f" font-size: 12px;"
        f" }}"
    )
    clear_font = f' font-family: "{ui}";' if ui else ""
    # More specific than scoped ``QWidget#welcomeRoot QPushButton`` so Clear
    # Recent keeps transparent/flat chrome instead of panel secondary fill.
    parts.append(
        f"QWidget#welcomeRoot QPushButton#welcomeClearRecent {{"
        f" color: {LIGHT.muted};"
        f" background: transparent;"
        f" border: 1px solid transparent;"
        f" min-height: 32px;"
        f" padding: 4px 8px;"
        f"{clear_font}"
        f" }}"
    )
    parts.append(
        f"QWidget#welcomeRoot QPushButton#welcomeClearRecent:hover {{"
        f" color: {LIGHT.text};"
        f" border: 1px solid {LIGHT.border};"
        f" background-color: {LIGHT.alternate};"
        f" }}"
    )
    parts.append(
        f"QWidget#welcomeRoot QPushButton#welcomeClearRecent:focus {{"
        f" border: 2px solid {LIGHT.accent};"
        f" padding: 3px 7px;"
        f" }}"
    )
    label_font = f' font-family: "{label_family}";' if label_family else ""
    parts.append(
        f"QLabel#welcomeRecentLabel {{"
        f"{label_font}"
        f" font-size: 12px;"
        f" font-weight: 600;"
        f" color: {LIGHT.muted};"
        f" letter-spacing: 0.6px;"
        f" text-transform: uppercase;"
        f" }}"
    )
    parts.append(
        f"QListWidget#welcomeRecentList {{"
        f" background-color: {LIGHT.base};"
        f" color: {LIGHT.text};"
        f" border: 1px solid {LIGHT.border};"
        f" border-radius: 6px;"
        f" padding: 6px;"
        f" }}"
    )
    parts.append(
        f"QListWidget#welcomeRecentList:focus {{ border: 1px solid {LIGHT.accent}; }}"
    )
    parts.append(
        f"QListWidget#welcomeRecentList::item:selected {{"
        f" background-color: {LIGHT.accent};"
        f" color: {LIGHT.accent_text};"
        f" }}"
    )
    parts.append(f"QWidget#welcomeRoot {{ background-color: {LIGHT.window}; }}")
    parts.append(f"QWidget#welcomeRoot QLabel#welcomeBrand {{ color: {LIGHT.text}; }}")
    parts.append(
        f"QWidget#welcomeRoot QLabel#welcomeSubtitle {{ color: {LIGHT.muted}; }}"
    )
    parts.append(
        f"QWidget#welcomeRoot QLabel#welcomeTagline {{ color: {LIGHT.text}; }}"
    )
    parts.append(f"QWidget#aboutRoot {{ background-color: {LIGHT.window}; }}")
    parts.append(f"QWidget#aboutRoot QLabel#welcomeBrand {{ color: {LIGHT.text}; }}")
    parts.append(
        f"QWidget#aboutRoot QLabel#welcomeSubtitle {{ color: {LIGHT.muted}; }}"
    )
    parts.append(f"QWidget#aboutRoot QLabel#welcomeTagline {{ color: {LIGHT.text}; }}")
    heading_font = f' font-family: "{ui}";' if ui else ""
    for root in ("whatsNewRoot", "shortcutsRoot", "explainSolutionRoot"):
        parts.append(f"QWidget#{root} {{ background-color: {LIGHT.window}; }}")
        parts.append(
            f"QWidget#{root} QLabel#helpDialogHeading {{"
            f" color: {LIGHT.text};"
            f"{heading_font}"
            f" }}"
        )
    for body_id in ("whatsNewBody", "explainSolutionBody"):
        parts.append(
            f"QTextEdit#{body_id} {{"
            f" background-color: {LIGHT.base};"
            f" color: {LIGHT.text};"
            f" border: 1px solid {LIGHT.border};"
            f" border-radius: 4px;"
            f" padding: 4px 8px;"
            f" selection-background-color: {LIGHT.accent};"
            f" selection-color: {LIGHT.accent_text};"
            f" }}"
        )
        parts.append(
            f"QTextEdit#{body_id}:focus {{ border: 1px solid {LIGHT.accent}; }}"
        )
    parts.append(
        f"QTableWidget#shortcutsTable {{"
        f" background-color: {LIGHT.base};"
        f" alternate-background-color: {LIGHT.alternate};"
        f" color: {LIGHT.text};"
        f" border: 1px solid {LIGHT.border};"
        f" border-radius: 4px;"
        f" }}"
    )
    parts.append(
        f"QTableWidget#shortcutsTable:focus {{ border: 1px solid {LIGHT.accent}; }}"
    )
    header_font = f' font-family: "{label_family}";' if label_family else ""
    parts.append(
        f"QWidget#shortcutsRoot QHeaderView::section {{"
        f" background-color: {LIGHT.panel};"
        f" color: {LIGHT.muted};"
        f" border: none;"
        f" border-bottom: 1px solid {LIGHT.border};"
        f" border-right: 1px solid {LIGHT.border};"
        f" padding: 6px 8px;"
        f"{header_font}"
        f" }}"
    )
    primary_font = f' font-family: "{label_family}";' if label_family else ""
    for root in ("welcomeRoot", "workspaceEmptyOverlay", "explainSolutionRoot"):
        align = " text-align: center;" if root == "workspaceEmptyOverlay" else ""
        parts.append(
            f"QWidget#{root} QPushButton {{"
            f" background-color: {LIGHT.panel};"
            f" color: {LIGHT.text};"
            f" border: 1px solid {LIGHT.border};"
            f" border-radius: 4px;"
            f" padding: 6px 14px;"
            f" min-height: 28px;"
            f"{align}"
            f" }}"
        )
        parts.append(
            f"QWidget#{root} QPushButton:hover {{"
            f" background-color: {LIGHT.alternate};"
            f" border-color: {LIGHT.accent};"
            f" }}"
        )
        parts.append(
            f"QWidget#{root} QPushButton:focus {{"
            f" border: 2px solid {LIGHT.accent};"
            f" padding: 5px 13px;"
            f" }}"
        )
        parts.append(
            f"QWidget#{root} QPushButton:pressed {{"
            f" background-color: {LIGHT.border};"
            f" }}"
        )
        parts.append(
            f"QWidget#{root} QPushButton:disabled {{"
            f" color: {LIGHT.muted};"
            f" background-color: {LIGHT.alternate};"
            f" }}"
        )
    for root in (
        "welcomeRoot",
        "workspaceEmptyOverlay",
        "aboutRoot",
        "whatsNewRoot",
        "shortcutsRoot",
        "explainSolutionRoot",
    ):
        parts.append(
            f"QWidget#{root} QPushButton#primaryButton {{"
            f" background-color: {LIGHT.accent};"
            f" color: {LIGHT.accent_text};"
            f" border: 1px solid {LIGHT.accent_hover};"
            f"{primary_font}"
            f" font-weight: 600;"
            f" min-height: 44px;"
            f" }}"
        )
        parts.append(
            f"QWidget#{root} QPushButton#primaryButton:hover {{"
            f" background-color: {LIGHT.accent_hover};"
            f" }}"
        )
        parts.append(
            f"QWidget#{root} QPushButton#primaryButton:focus {{"
            f" border: 2px solid {LIGHT.text};"
            f" padding: 5px 13px;"
            f" }}"
        )
    return "\n".join(parts)


def bootstrap_ui_font(app: QApplication) -> None:
    """Register bundled fonts and set UI face before widgets are built.

    Calling this right after ``QApplication(...)`` avoids the transient
    ``Sans Serif`` alias warning that Qt emits while the default font is still
    the fictional family name.
    """
    _register_bundled_fonts()
    ui, _brand = _resolved_ui_and_brand_families()
    if ui:
        app.setFont(QFont(ui, 13))


def apply_theme(app: QApplication, theme: str) -> None:
    """Apply a Studio theme to `app`.

    ``system`` restores the platform palette and keeps Welcome/About brand
    typography plus Welcome/About/WhatsNew/Shortcuts/Explain roots,
    empty-workspace, outdated-banner, Clear Recent, recent label/list, and
    scoped primary/secondary button chrome on LIGHT tokens (canvas is always
    taller-diurno under system; no full Industrial chrome).
    """
    from studio.workspace.canvas_style import set_active_canvas_theme

    _register_bundled_fonts()
    name = theme if theme in VALID_THEMES else DEFAULT_THEME
    app.setStyle("Fusion")
    set_active_canvas_theme(name)

    if name == "system":
        app.setPalette(app.style().standardPalette())
        # QFont() resolves to the fictional "Sans Serif" family on many
        # platforms (esp. offscreen CI) and spams qt.qpa.fonts warnings.
        # Prefer the bundled UI face when registered; otherwise keep the
        # platform default without forcing that alias.
        ui, brand = _resolved_ui_and_brand_families()
        if ui:
            app.setFont(QFont(ui, 13))
        # Keep Welcome brand chrome + empty-overlay without full Industrial QSS.
        app.setStyleSheet(_welcome_typography_qss(brand=brand, ui=ui))
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
