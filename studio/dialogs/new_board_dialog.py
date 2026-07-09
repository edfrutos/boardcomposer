"""Dialog for creating a Studio board."""

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QSpinBox,
    QVBoxLayout,
)


class NewBoardDialog(QDialog):
    """Dialogo para crear un tablero."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Nuevo tablero")

        self.board_id = QLineEdit("TAB-001")
        self.length_mm = QSpinBox()
        self.width_mm = QSpinBox()
        self.thickness_mm = QSpinBox()
        self.material = QLineEdit("Melamina blanca")

        for field in (self.length_mm, self.width_mm, self.thickness_mm):
            field.setRange(1, 100_000)

        self.length_mm.setValue(3000)
        self.width_mm.setValue(1200)
        self.thickness_mm.setValue(19)

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
        return {
            "board_id": self.board_id.text().strip(),
            "length_mm": float(self.length_mm.value()),
            "width_mm": float(self.width_mm.value()),
            "thickness_mm": float(self.thickness_mm.value()),
            "material": self.material.text().strip(),
        }
