"""Preview dialog for importing pieces from CSV (FLW-002)."""

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

from studio.piece_csv_importer import ImportPiecesResult

_COLUMNS = (
    "Fila",
    "Id base",
    "Cantidad",
    "Ids generados",
    "Largo",
    "Ancho",
    "Espesor",
    "Material",
    "Estado",
)
_ERROR_BACKGROUND = QColor(255, 214, 214)


class ImportPiecesPreviewDialog(QDialog):
    """Shows a preview table of a parsed pieces CSV import."""

    def __init__(self, result: ImportPiecesResult, parent=None) -> None:
        super().__init__(parent)

        self.result = result
        self.setWindowTitle("Importar piezas (CSV)")
        self.setMinimumSize(720, 400)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(self._summary_text()))

        if result.file_errors:
            layout.addWidget(
                QLabel(
                    "No se pudo procesar el archivo:\n"
                    + "\n".join(f"- {error}" for error in result.file_errors)
                )
            )

        self.table = QTableWidget(len(result.rows), len(_COLUMNS))
        self.table.setHorizontalHeaderLabels(_COLUMNS)
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
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setEnabled(
            bool(result.valid_rows)
        )
        layout.addWidget(buttons)

    def _summary_text(self) -> str:
        if self.result.file_errors:
            return "El archivo no se pudo importar."
        return (
            f"{len(self.result.valid_pieces)} pieza(s) válida(s) "
            f"en {len(self.result.valid_rows)} fila(s); "
            f"{len(self.result.invalid_rows)} fila(s) con errores."
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
                item.setBackground(_ERROR_BACKGROUND)
            self.table.setItem(row_index, column, item)
