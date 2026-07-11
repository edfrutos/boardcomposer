"""Dialog for creating a Studio piece."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
    QCheckBox,
)


class NewPieceDialog(QDialog):
    """Diálogo para crear una pieza."""

    def __init__(
        self,
        parent=None,
        *,
        piece_id: str = "P-001",
        length_mm: int = 700,
        width_mm: int = 300,
        material: str = "Melamina blanca",
        title: str = "Nueva pieza",
    ):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.piece_id = QLineEdit(piece_id)
        self.length_mm = QSpinBox()
        self.width_mm = QSpinBox()
        self.material = QLineEdit(material)
        self.rotatable = QCheckBox()
        self.rotatable.setChecked(True)

        for field in (self.length_mm, self.width_mm):
            field.setRange(1, 100000)

        self.length_mm.setValue(length_mm)
        self.width_mm.setValue(width_mm)

        form = QFormLayout()
        form.addRow("Identificador:", self.piece_id)
        form.addRow("Largo (mm):", self.length_mm)
        form.addRow("Ancho (mm):", self.width_mm)
        form.addRow("Material:", self.material)
        form.addRow("Permitir rotación:", self.rotatable)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def piece_data(self) -> dict:
        return {
            "piece_id": self.piece_id.text().strip(),
            "length_mm": float(self.length_mm.value()),
            "width_mm": float(self.width_mm.value()),
            "material": self.material.text().strip(),
            "rotatable": self.rotatable.isChecked(),
        }
