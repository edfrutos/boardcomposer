"""Preview dialog for importing pieces from CSV (FLW-002)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHeaderView,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.piece_csv_importer import ImportPiecesResult
from studio.workspace.canvas_style import color as canvas_color

_COLUMN_KEYS = (
    "import.col.row",
    "import.col.base_id",
    "import.col.quantity",
    "import.col.generated_ids",
    "import.col.length",
    "import.col.width",
    "import.col.thickness",
    "import.col.material",
    "import.col.status",
)


class ImportPiecesPreviewDialog(QDialog):
    """Shows a preview table of a parsed pieces CSV import."""

    def __init__(
        self,
        result: ImportPiecesResult,
        parent=None,
        *,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__(parent)

        self.result = result
        self._language = language
        self.setWindowTitle(tr("import.pieces_title", language))
        self.setMinimumSize(720, 400)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self._summary_text()))

        if result.file_errors:
            layout.addWidget(
                QLabel(
                    tr("import.file_error_header", language)
                    + "\n"
                    + "\n".join(f"- {error}" for error in result.file_errors)
                )
            )

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

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(result.valid_rows)
        )
        layout.addWidget(buttons)

    def _summary_text(self) -> str:
        if self.result.file_errors:
            return tr("import.file_failed", self._language)
        return tr(
            "import.pieces_summary",
            self._language,
            pieces=len(self.result.valid_pieces),
            rows=len(self.result.valid_rows),
            invalid=len(self.result.invalid_rows),
        )

    def _populate_row(self, row_index: int, row) -> None:
        first = row.pieces[0] if row.pieces else None
        values = (
            str(row.row_number),
            row.base_id or row.raw.get("piece_id", ""),
            str(row.quantity),
            ", ".join(piece.piece_id for piece in row.pieces),
            f"{first.length_mm:g}" if first else "",
            f"{first.width_mm:g}" if first else "",
            f"{first.thickness_mm:g}" if first else "",
            first.material if first else "",
            "OK" if row.is_valid else "; ".join(row.errors),
        )
        for column, value in enumerate(values):
            item = QTableWidgetItem(value)
            if not row.is_valid:
                item.setBackground(canvas_color("invalid_fill"))
            self.table.setItem(row_index, column, item)
