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

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nueva pieza")

        self.piece_id = QLineEdit("P-001")
        self.length_mm = QSpinBox()
        self.width_mm = QSpinBox()
        self.material = QLineEdit("Melamina blanca")
        self.rotatable = QCheckBox()
        self.rotatable.setChecked(True)

        for field in (self.length_mm, self.width_mm):
            field.setRange(1, 100000)

        self.length_mm.setValue(700)
        self.width_mm.setValue(300)

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
