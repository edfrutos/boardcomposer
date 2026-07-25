"""Dialog for creating a new Studio project (FLW-001)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
)

from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.units import DEFAULT_UNITS, VALID_UNITS, normalize_units


class NewProjectDialog(QDialog):
    """Ask for project name and preferred display units."""

    def __init__(
        self,
        parent=None,
        *,
        name: str = "",
        units: str = DEFAULT_UNITS,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self.setWindowTitle(tr("form.new_project", language))

        self.name = QLineEdit(name)
        self.name.setPlaceholderText(tr("form.project_name_placeholder", language))

        self.units = QComboBox()
        for key in VALID_UNITS:
            self.units.addItem(tr(f"units.{key}", language), key)
        index = self.units.findData(normalize_units(units))
        self.units.setCurrentIndex(index if index >= 0 else 0)

        form = QFormLayout()
        form.addRow(tr("form.project_name", language), self.name)
        form.addRow(tr("prefs.units", language), self.units)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.name.setFocus()
        self.name.selectAll()

    def project_data(self) -> dict[str, str]:
        """Return cleaned name and selected units."""
        return {
            "name": self.name.text().strip(),
            "units": normalize_units(self.units.currentData() or DEFAULT_UNITS),
        }
