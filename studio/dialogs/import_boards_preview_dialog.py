"""Preview dialog for the CSV board-inventory import flow (FLW-002)."""

from __future__ import annotations

from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from studio.board_csv_importer import ImportBoardsResult
from studio.i18n import DEFAULT_LANGUAGE, tr

_ERROR_BACKGROUND = QColor(255, 214, 214)
_COLUMN_KEYS = (
    "import.col.row",
    "import.col.id",
    "import.col.length",
    "import.col.width",
    "import.col.thickness",
    "import.col.quantity",
    "import.col.material",
    "import.col.status",
)


class ImportBoardsPreviewDialog(QDialog):
    """Shows a preview table of a parsed CSV import, before it's applied."""

    def __init__(
        self,
        result: ImportBoardsResult,
        parent=None,
        *,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__(parent)

        self.result = result
        self._language = language
        self.setWindowTitle(tr("import.boards_title", language))
        self.setMinimumSize(640, 400)

        layout = QVBoxLayout(self)

        summary = QLabel(self._summary_text())
        layout.addWidget(summary)

        if result.file_errors:
            errors_label = QLabel(
                tr("import.file_error_header", language)
                + "\n"
                + "\n".join(f"- {error}" for error in result.file_errors)
            )
            layout.addWidget(errors_label)

        columns = [tr(key, language) for key in _COLUMN_KEYS]
        self.table = QTableWidget(len(result.rows), len(columns))
        self.table.setHorizontalHeaderLabels(columns)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

        for row_index, row in enumerate(result.rows):
            self._populate_row(row_index, row)

        layout.addWidget(self.table)

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(result.valid_rows)
        )
        layout.addWidget(self.buttons)

    def _summary_text(self) -> str:
        valid_count = len(self.result.valid_rows)
        invalid_count = len(self.result.invalid_rows)

        if self.result.file_errors:
            return tr("import.file_failed", self._language)

        return tr(
            "import.boards_summary",
            self._language,
            valid=valid_count,
            invalid=invalid_count,
        )

    def _populate_row(self, row_index: int, row) -> None:
        board = row.board
        values = (
            str(row.row_number),
            board.board_id if board else row.display_id,
            f"{board.length_mm:g}" if board else "",
            f"{board.width_mm:g}" if board else "",
            f"{board.thickness_mm:g}" if board else "",
            str(board.quantity) if board else "",
            board.material if board else "",
            "OK" if row.is_valid else "; ".join(row.errors),
        )

        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            if not row.is_valid:
                item.setBackground(_ERROR_BACKGROUND)
            self.table.setItem(row_index, column, item)
