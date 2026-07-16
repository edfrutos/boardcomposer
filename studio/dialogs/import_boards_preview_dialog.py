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

_COLUMNS = ("Fila", "Id", "Largo", "Ancho", "Espesor", "Cantidad", "Material", "Estado")
_ERROR_BACKGROUND = QColor(255, 214, 214)


class ImportBoardsPreviewDialog(QDialog):
    """Shows a preview table of a parsed CSV import, before it's applied."""

    def __init__(self, result: ImportBoardsResult, parent=None) -> None:
        super().__init__(parent)

        self.result = result
        self.setWindowTitle("Importar inventario de tableros (CSV)")
        self.setMinimumSize(640, 400)

        layout = QVBoxLayout(self)

        summary = QLabel(self._summary_text())
        layout.addWidget(summary)

        if result.file_errors:
            errors_label = QLabel(
                "No se pudo procesar el archivo:\n"
                + "\n".join(f"- {error}" for error in result.file_errors)
            )
            layout.addWidget(errors_label)

        self.table = QTableWidget(len(result.rows), len(_COLUMNS))
        self.table.setHorizontalHeaderLabels(_COLUMNS)
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
            return "El archivo no se pudo importar."

        return (
            f"{valid_count} tablero(s) válido(s), {invalid_count} fila(s) con errores."
        )

    def _populate_row(self, row_index: int, row) -> None:
        board = row.board
        values = (
            str(row.row_number),
            board.board_id if board else row.raw.get("board_id", ""),
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
