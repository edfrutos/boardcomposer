"""Dialog for creating a Studio piece."""

from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)

from studio.units import display_to_mm, mm_to_display, unit_label


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
        units: str = "mm",
    ):
        super().__init__(parent)

        self._units = units
        self.setWindowTitle(title)
        suffix = f" {unit_label(units)}"

        self.piece_id = QLineEdit(piece_id)
        self.length = QDoubleSpinBox()
        self.width = QDoubleSpinBox()
        self.thickness = QDoubleSpinBox()
        self.quantity = QSpinBox()
        self.material = QLineEdit(material)
        self.rotatable = QCheckBox()
        self.rotatable.setChecked(True)

        decimals = 0 if units == "mm" else 2
        for field in (self.length, self.width, self.thickness):
            field.setRange(0.01, 100_000)
            field.setDecimals(decimals)
            field.setSuffix(suffix)

        self.length.setValue(mm_to_display(length_mm, units))
        self.width.setValue(mm_to_display(width_mm, units))
        self.thickness.setValue(mm_to_display(thickness_mm, units))
        self.quantity.setRange(1, 10_000)
        self.quantity.setValue(quantity)

        form = QFormLayout()
        form.addRow("Identificador:", self.piece_id)
        form.addRow(f"Largo ({unit_label(units)}):", self.length)
        form.addRow(f"Ancho ({unit_label(units)}):", self.width)
        form.addRow(f"Espesor ({unit_label(units)}):", self.thickness)
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
            "length_mm": display_to_mm(self.length.value(), self._units),
            "width_mm": display_to_mm(self.width.value(), self._units),
            "thickness_mm": display_to_mm(self.thickness.value(), self._units),
            "quantity": self.quantity.value(),
            "material": self.material.text().strip(),
            "rotatable": self.rotatable.isChecked(),
        }
