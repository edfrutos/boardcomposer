"""Empty-state CTA overlay for the Workspace canvas."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QPushButton, QVBoxLayout, QWidget

from studio.dialogs.dialog_chrome import (
    polish_primary_button,
    polish_secondary_button,
)
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.keyboard_shortcuts import with_native_shortcuts


class EmptyWorkspaceOverlay(QWidget):
    """Centered first-steps panel when the project has no boards or pieces."""

    add_board_requested = Signal()
    add_piece_requested = Signal()
    import_boards_requested = Signal()
    import_pieces_requested = Signal()

    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("workspaceEmptyOverlay")
        self._language = DEFAULT_LANGUAGE

        layout = QVBoxLayout(self)
        layout.setContentsMargins(32, 28, 32, 28)
        layout.setSpacing(10)

        self.title = QLabel()
        self.title.setObjectName("workspaceEmptyTitle")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setWordWrap(True)
        layout.addWidget(self.title)

        self.blurb = QLabel()
        self.blurb.setObjectName("workspaceEmptyBlurb")
        self.blurb.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blurb.setWordWrap(True)
        layout.addWidget(self.blurb)

        layout.addSpacing(8)

        self.add_board_button = polish_primary_button(QPushButton())
        self.add_board_button.clicked.connect(self.add_board_requested.emit)
        layout.addWidget(self.add_board_button)

        self.add_piece_button = polish_secondary_button(QPushButton())
        self.add_piece_button.clicked.connect(self.add_piece_requested.emit)
        layout.addWidget(self.add_piece_button)

        self.import_boards_button = polish_secondary_button(QPushButton())
        self.import_boards_button.clicked.connect(self.import_boards_requested.emit)
        layout.addWidget(self.import_boards_button)

        self.import_pieces_button = polish_secondary_button(QPushButton())
        self.import_pieces_button.clicked.connect(self.import_pieces_requested.emit)
        layout.addWidget(self.import_pieces_button)

        self.setMinimumWidth(340)
        self.setMaximumWidth(420)
        self.apply_language(DEFAULT_LANGUAGE)

    def apply_language(self, language: str) -> None:
        """Refresh CTA strings for the selected language."""
        self._language = language
        self.title.setText(tr("workspace.empty_title", language))
        self.blurb.setText(tr("workspace.empty_blurb", language))
        self.add_board_button.setText(tr("action.add_board", language))
        self.add_piece_button.setText(tr("action.add_piece", language))
        self.import_boards_button.setText(tr("action.import_boards_csv", language))
        self.import_pieces_button.setText(tr("action.import_pieces_csv", language))
        tip_pairs = (
            (self.add_board_button, "tip.add_board"),
            (self.add_piece_button, "tip.add_piece"),
            (self.import_boards_button, "tip.import_boards_csv"),
            (self.import_pieces_button, "tip.import_pieces_csv"),
        )
        for button, tip_key in tip_pairs:
            tip = with_native_shortcuts(tr(tip_key, language))
            button.setToolTip(tip)
            button.setStatusTip(tip)
