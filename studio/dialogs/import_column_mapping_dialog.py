"""Manual column-mapping dialog for CSV/Excel import (FLW-002)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.import_headers import sanitize_header_map
from studio.import_templates import ImportMappingTemplate, ImportTemplatesManager

_UNMAPPED = ""


class ImportColumnMappingDialog(QDialog):
    """Let the user assign file headers to canonical import fields."""

    def __init__(
        self,
        *,
        fieldnames: list[str] | tuple[str, ...],
        field_order: tuple[str, ...],
        required_fields: tuple[str, ...],
        initial_map: dict[str, str],
        missing_fields: list[str] | tuple[str, ...],
        templates: list[ImportMappingTemplate] | tuple[ImportMappingTemplate, ...] = (),
        templates_manager: ImportTemplatesManager | None = None,
        kind: str = "boards",
        language: str = DEFAULT_LANGUAGE,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._fieldnames = list(fieldnames)
        self._field_order = field_order
        self._required = set(required_fields)
        self._templates_manager = templates_manager
        self._kind = kind
        self._templates = (
            list(templates_manager.for_kind(kind))
            if templates_manager is not None
            else list(templates)
        )
        self._combos: dict[str, QComboBox] = {}

        self.setWindowTitle(tr("import.mapping_title", language))
        layout = QVBoxLayout(self)

        intro = QLabel(
            tr(
                "import.mapping_intro",
                language,
                fields=", ".join(missing_fields),
            )
        )
        intro.setWordWrap(True)
        layout.addWidget(intro)

        self._template_combo: QComboBox | None = None
        self._delete_template_button: QPushButton | None = None
        if self._templates or self._templates_manager is not None:
            template_row = QHBoxLayout()
            template_row.addWidget(QLabel(tr("import.mapping_template", language)))
            self._template_combo = QComboBox()
            self._reload_template_combo()
            self._template_combo.currentIndexChanged.connect(self._on_template_changed)
            template_row.addWidget(self._template_combo, stretch=1)

            if self._templates_manager is not None:
                self._delete_template_button = QPushButton(
                    tr("import.mapping_delete", language)
                )
                self._delete_template_button.clicked.connect(
                    self._delete_selected_template
                )
                template_row.addWidget(self._delete_template_button)
                self._update_delete_button()

            layout.addLayout(template_row)

        form = QFormLayout()
        for canonical in field_order:
            combo = QComboBox()
            combo.addItem(tr("import.mapping_none", language), _UNMAPPED)
            for header in fieldnames:
                combo.addItem(header, header)
            prefill = initial_map.get(canonical)
            if prefill:
                index = combo.findData(prefill)
                if index >= 0:
                    combo.setCurrentIndex(index)
            label_key = f"import.mapping.field.{canonical}"
            label = tr(label_key, language)
            if canonical in self._required:
                label = f"{label} *"
            form.addRow(label, combo)
            self._combos[canonical] = combo
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _reload_template_combo(self) -> None:
        if self._template_combo is None:
            return
        if self._templates_manager is not None:
            self._templates = list(self._templates_manager.for_kind(self._kind))
        self._template_combo.blockSignals(True)
        self._template_combo.clear()
        self._template_combo.addItem(tr("import.mapping_none", self._language), None)
        for template in self._templates:
            self._template_combo.addItem(template.name, template)
        self._template_combo.setCurrentIndex(0)
        self._template_combo.blockSignals(False)
        self._update_delete_button()

    def _on_template_changed(self) -> None:
        self._update_delete_button()
        self._apply_selected_template()

    def _update_delete_button(self) -> None:
        if self._delete_template_button is None or self._template_combo is None:
            return
        template = self._template_combo.currentData()
        self._delete_template_button.setEnabled(
            isinstance(template, ImportMappingTemplate)
        )

    def _delete_selected_template(self) -> None:
        if self._templates_manager is None or self._template_combo is None:
            return
        template = self._template_combo.currentData()
        if not isinstance(template, ImportMappingTemplate):
            return
        answer = QMessageBox.question(
            self,
            tr("import.mapping_delete_title", self._language),
            tr("import.mapping_delete_confirm", self._language, name=template.name),
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._templates_manager.delete(template.kind, template.name)
        self._reload_template_combo()

    def _apply_selected_template(self) -> None:
        if self._template_combo is None:
            return
        template = self._template_combo.currentData()
        if not isinstance(template, ImportMappingTemplate):
            return
        mapping = sanitize_header_map(template.header_map, self._fieldnames)
        for canonical, combo in self._combos.items():
            header = mapping.get(canonical, _UNMAPPED)
            index = combo.findData(header)
            if index >= 0:
                combo.setCurrentIndex(index)
            else:
                combo.setCurrentIndex(0)

    def header_map(self) -> dict[str, str]:
        """Return canonical → file-header assignments (skip unmapped)."""
        result: dict[str, str] = {}
        for canonical, combo in self._combos.items():
            value = combo.currentData()
            if isinstance(value, str) and value:
                result[canonical] = value
        return result
