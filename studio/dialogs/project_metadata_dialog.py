"""Dialog for project client / reference / notes (IDE-0024)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QPlainTextEdit,
    QVBoxLayout,
)

from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.i18n import DEFAULT_LANGUAGE, tr


class ProjectMetadataDialog(QDialog):
    """Edit optional project metadata stored in the ``.bcproj``."""

    def __init__(
        self,
        parent=None,
        *,
        client: str = "",
        reference: str = "",
        notes: str = "",
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self.setWindowTitle(tr("dialog.project_metadata_title", language))

        self.client = QLineEdit(client)
        self.reference = QLineEdit(reference)
        self.notes = QPlainTextEdit(notes)
        self.notes.setPlaceholderText(tr("form.project_notes_placeholder", language))
        self.notes.setMinimumHeight(96)

        form = QFormLayout()
        form.addRow(tr("form.project_client", language), self.client)
        form.addRow(tr("form.project_reference", language), self.reference)
        form.addRow(tr("form.project_notes", language), self.notes)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout(self)
        layout.addLayout(form)
        layout.addWidget(buttons)

        self.client.setFocus()
        self.client.selectAll()

    def metadata(self) -> dict[str, str]:
        """Return cleaned client, reference and notes."""
        return {
            "client": self.client.text().strip(),
            "reference": self.reference.text().strip(),
            "notes": self.notes.toPlainText().strip(),
        }
