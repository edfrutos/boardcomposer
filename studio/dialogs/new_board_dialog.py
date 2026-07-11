"""Dialog for creating or editing a Studio board."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)


class NewBoardDialog(QDialog):
    """Dialog for creating or editing a board."""

    def __init__(
        self,
        parent=None,
        *,
        board_id: str = "TAB-001",
        length_mm: int = 3000,
        width_mm: int = 1200,
        thickness_mm: int = 19,
        material: str = "Melamina blanca",
        title: str = "Nuevo tablero",
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(title)

        self.board_id = QLineEdit(board_id)
        self.length_mm = QSpinBox()
        self.width_mm = QSpinBox()
        self.thickness_mm = QSpinBox()
        self.material = QLineEdit(material)

        for field in (
            self.length_mm,
            self.width_mm,
            self.thickness_mm,
        ):
            field.setRange(1, 100_000)

        self.length_mm.setValue(length_mm)
        self.width_mm.setValue(width_mm)
        self.thickness_mm.setValue(thickness_mm)

        form = QFormLayout()
        form.addRow("Identificador:", self.board_id)
        form.addRow("Largo (mm):", self.length_mm)
        form.addRow("Ancho (mm):", self.width_mm)
        form.addRow("Espesor (mm):", self.thickness_mm)
        form.addRow("Material:", self.material)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def board_data(self) -> dict:
        """Return the values entered in the dialog."""
        return {
            "board_id": self.board_id.text().strip(),
            "length_mm": float(self.length_mm.value()),
            "width_mm": float(self.width_mm.value()),
            "thickness_mm": float(self.thickness_mm.value()),
            "material": self.material.text().strip(),
        }
