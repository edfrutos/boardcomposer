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

from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.units import display_to_mm, mm_to_display, unit_label


class NewPieceDialog(QDialog):
    """Dialog for creating or editing a piece."""

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
        title: str | None = None,
        show_quantity: bool = True,
        units: str = "mm",
        language: str = DEFAULT_LANGUAGE,
    ):
        super().__init__(parent)

        self._units = units
        self._language = language
        self.setWindowTitle(title or tr("form.new_piece", language))
        suffix = f" {unit_label(units)}"
        unit = unit_label(units)

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
        form.addRow(tr("form.id", language), self.piece_id)
        form.addRow(tr("form.length", language, unit=unit), self.length)
        form.addRow(tr("form.width", language, unit=unit), self.width)
        form.addRow(tr("form.thickness", language, unit=unit), self.thickness)
        if show_quantity:
            form.addRow(tr("form.quantity", language), self.quantity)
        else:
            self.quantity.setEnabled(False)
        form.addRow(tr("form.material", language), self.material)
        form.addRow(tr("form.allow_rotation", language), self.rotatable)

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
