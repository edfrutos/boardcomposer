"""Help dialogs: What's New, About, and keyboard shortcuts."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QTextEdit,
    QVBoxLayout,
)

from studio.branding import app_icon
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.keyboard_shortcuts import STUDIO_SHORTCUTS, format_shortcut_label
from studio.whats_new import load_whats_new
from studio.welcome_screen import STUDIO_VERSION


class WhatsNewDialog(QDialog):
    """Show recent Unreleased changelog highlights."""

    def __init__(self, *, language: str = DEFAULT_LANGUAGE, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("help.whats_new_title", language))
        self.setMinimumSize(520, 420)

        title, bullets = load_whats_new()
        layout = QVBoxLayout(self)
        heading = QLabel(tr("help.whats_new_heading", language, section=title))
        heading.setWordWrap(True)
        layout.addWidget(heading)

        body = QTextEdit()
        body.setReadOnly(True)
        body.setPlainText("\n".join(f"• {item}" for item in bullets))
        layout.addWidget(body)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


class AboutDialog(QDialog):
    """Simple About box for BoardComposer Studio."""

    def __init__(self, *, language: str = DEFAULT_LANGUAGE, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("help.about_title", language))
        self.setMinimumWidth(360)

        icon = app_icon()
        if not icon.isNull():
            self.setWindowIcon(icon)

        layout = QVBoxLayout(self)
        if not icon.isNull():
            icon_label = QLabel()
            icon_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            icon_label.setPixmap(icon.pixmap(96, 96))
            layout.addWidget(icon_label)

        brand = QLabel("BoardComposer Studio")
        brand.setObjectName("welcomeBrand")
        brand.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(brand)
        version = QLabel(tr("help.about_version", language, version=STUDIO_VERSION))
        version.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(version)
        blurb = QLabel(tr("help.about_blurb", language))
        blurb.setWordWrap(True)
        blurb.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(blurb)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)


class ShortcutsDialog(QDialog):
    """Read-only table of Studio keyboard shortcuts."""

    def __init__(self, *, language: str = DEFAULT_LANGUAGE, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("help.shortcuts_title", language))
        self.setMinimumSize(420, 360)

        layout = QVBoxLayout(self)
        intro = QLabel(tr("help.shortcuts_intro", language))
        intro.setWordWrap(True)
        layout.addWidget(intro)

        table = QTableWidget(len(STUDIO_SHORTCUTS), 2)
        table.setHorizontalHeaderLabels(
            [
                tr("help.shortcuts_col_action", language),
                tr("help.shortcuts_col_keys", language),
            ]
        )
        table.verticalHeader().setVisible(False)
        table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        table.setSelectionMode(QTableWidget.SelectionMode.NoSelection)
        table.setShowGrid(False)
        for row, binding in enumerate(STUDIO_SHORTCUTS):
            table.setItem(
                row,
                0,
                QTableWidgetItem(tr(f"action.{binding.action_key}", language)),
            )
            table.setItem(
                row,
                1,
                QTableWidgetItem(format_shortcut_label(binding)),
            )
        table.resizeColumnsToContents()
        table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(table)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
