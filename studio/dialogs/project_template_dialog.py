"""Dialog to pick a stored project template."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
)

from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.project_templates import ProjectTemplateInfo


class ProjectTemplatePickerDialog(QDialog):
    """List project templates and return the selected name."""

    def __init__(
        self,
        templates: list[ProjectTemplateInfo],
        *,
        language: str = DEFAULT_LANGUAGE,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self.setWindowTitle(tr("template.pick_title", language))
        self.setMinimumSize(420, 320)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("template.pick_intro", language)))

        self.list = QListWidget()
        for template in templates:
            label = tr(
                "template.pick_item",
                language,
                name=template.name,
                boards=template.board_count,
                pieces=template.piece_count,
            )
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, template.name)
            self.list.addItem(item)
        self.list.itemDoubleClicked.connect(self.accept)
        layout.addWidget(self.list)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        if self.list.count():
            self.list.setCurrentRow(0)

    def selected_name(self) -> str | None:
        item = self.list.currentItem()
        if item is None:
            return None
        name = item.data(Qt.ItemDataRole.UserRole)
        return str(name) if name else None
