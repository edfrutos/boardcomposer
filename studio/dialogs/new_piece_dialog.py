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
        thickness_mm: int = 19,
        quantity: int = 1,
        material: str = "Melamina blanca",
        title: str = "Nueva pieza",
        show_quantity: bool = True,
    ):
        super().__init__(parent)

        self.setWindowTitle(title)

        self.piece_id = QLineEdit(piece_id)
        self.length_mm = QSpinBox()
        self.width_mm = QSpinBox()
        self.thickness_mm = QSpinBox()
        self.quantity = QSpinBox()
        self.material = QLineEdit(material)
        self.rotatable = QCheckBox()
        self.rotatable.setChecked(True)

        for field in (self.length_mm, self.width_mm, self.thickness_mm):
            field.setRange(1, 100000)

        self.length_mm.setValue(length_mm)
        self.width_mm.setValue(width_mm)
        self.thickness_mm.setValue(thickness_mm)
        self.quantity.setRange(1, 10_000)
        self.quantity.setValue(quantity)

        form = QFormLayout()
        form.addRow("Identificador:", self.piece_id)
        form.addRow("Largo (mm):", self.length_mm)
        form.addRow("Ancho (mm):", self.width_mm)
        form.addRow("Espesor (mm):", self.thickness_mm)
        if show_quantity:
            form.addRow("Cantidad:", self.quantity)
        else:
            self.quantity.setEnabled(False)
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
            "thickness_mm": float(self.thickness_mm.value()),
            "quantity": self.quantity.value(),
            "material": self.material.text().strip(),
            "rotatable": self.rotatable.isChecked(),
        }
