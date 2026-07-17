"""Help dialogs: What's New and About."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)

from studio.i18n import DEFAULT_LANGUAGE, tr
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

        layout = QVBoxLayout(self)
        brand = QLabel("BoardComposer Studio")
        brand.setObjectName("welcomeBrand")
        layout.addWidget(brand)
        layout.addWidget(
            QLabel(tr("help.about_version", language, version=STUDIO_VERSION))
        )
        blurb = QLabel(tr("help.about_blurb", language))
        blurb.setWordWrap(True)
        layout.addWidget(blurb)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)
