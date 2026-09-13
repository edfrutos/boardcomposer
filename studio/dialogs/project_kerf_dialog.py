"""Dialog for project saw kerf (IDE-0020)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QVBoxLayout,
)

from boardcomposer.layout.kerf import MAX_KERF_MM
from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.i18n import DEFAULT_LANGUAGE, tr


class ProjectKerfDialog(QDialog):
    """Edit the saw-kerf stored on the current ``.bcproj``."""

    def __init__(
        self,
        parent=None,
        *,
        kerf_mm: float = 0.0,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self.setWindowTitle(tr("dialog.project_kerf_title", language))

        self.kerf_mm = QDoubleSpinBox()
        self.kerf_mm.setRange(0.0, MAX_KERF_MM)
        self.kerf_mm.setDecimals(1)
        self.kerf_mm.setSingleStep(0.5)
        self.kerf_mm.setSuffix(" mm")
        self.kerf_mm.setValue(kerf_mm)
        self.kerf_mm.setToolTip(tr("form.project_kerf_help", language))

        form = QFormLayout()
        form.addRow(tr("form.project_kerf", language), self.kerf_mm)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.kerf_mm.setFocus()
        self.kerf_mm.selectAll()

    def value(self) -> float:
        """Return the chosen kerf in millimetres."""
        return float(self.kerf_mm.value())
