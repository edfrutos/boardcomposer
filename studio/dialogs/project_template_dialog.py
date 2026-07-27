"""Dialog to pick a stored project template."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.project_templates import ProjectTemplateInfo, ProjectTemplatesManager


class ProjectTemplatePickerDialog(QDialog):
    """List project templates and return the selected name."""

    def __init__(
        self,
        templates: list[ProjectTemplateInfo],
        *,
        manager: ProjectTemplatesManager | None = None,
        language: str = DEFAULT_LANGUAGE,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._manager = manager
        self.setWindowTitle(tr("template.pick_title", language))
        self.setMinimumSize(420, 360)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel(tr("template.pick_intro", language)))

        self.list = QListWidget()
        self.list.itemDoubleClicked.connect(self.accept)
        self.list.currentItemChanged.connect(self._update_delete_enabled)
        layout.addWidget(self.list)

        row = QHBoxLayout()
        self.delete_button = QPushButton(tr("template.delete", language))
        self.delete_button.setEnabled(False)
        self.delete_button.clicked.connect(self._delete_selected)
        if manager is None:
            self.delete_button.hide()
        row.addWidget(self.delete_button)
        row.addStretch(1)
        layout.addLayout(row)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._reload_list(templates)

    def _reload_list(self, templates: list[ProjectTemplateInfo]) -> None:
        self.list.clear()
        for template in templates:
            if template.placement_count:
                label = tr(
                    "template.pick_item_with_placements",
                    self._language,
                    name=template.name,
                    boards=template.board_count,
                    pieces=template.piece_count,
                    placements=template.placement_count,
                )
            else:
                label = tr(
                    "template.pick_item",
                    self._language,
                    name=template.name,
                    boards=template.board_count,
                    pieces=template.piece_count,
                )
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, template.name)
            item.setData(Qt.ItemDataRole.UserRole + 1, template.placement_count)
            self.list.addItem(item)
        if self.list.count():
            self.list.setCurrentRow(0)
        self._update_delete_enabled()

    def _update_delete_enabled(self, *_args) -> None:
        self.delete_button.setEnabled(
            self._manager is not None and self.list.currentItem() is not None
        )

    def _delete_selected(self) -> None:
        if self._manager is None:
            return
        name = self.selected_name()
        if not name:
            return
        answer = QMessageBox.question(
            self,
            tr("template.delete_title", self._language),
            tr("template.delete_confirm", self._language, name=name),
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        if not self._manager.delete(name):
            QMessageBox.warning(
                self,
                tr("template.delete_title", self._language),
                tr("template.delete_failed", self._language, name=name),
            )
            return
        self._reload_list(self._manager.list())
        if self.list.count() == 0:
            self.reject()

    def selected_name(self) -> str | None:
        item = self.list.currentItem()
        if item is None:
            return None
        name = item.data(Qt.ItemDataRole.UserRole)
        return str(name) if name else None

    def selected_placement_count(self) -> int:
        item = self.list.currentItem()
        if item is None:
            return 0
        value = item.data(Qt.ItemDataRole.UserRole + 1)
        try:
            return int(value or 0)
        except (TypeError, ValueError):
            return 0
