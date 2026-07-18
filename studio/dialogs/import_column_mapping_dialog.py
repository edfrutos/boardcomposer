"""Manual column-mapping dialog for CSV/Excel import (FLW-002)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
)

from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.import_headers import sanitize_header_map
from studio.import_templates import ImportMappingTemplate

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
        language: str = DEFAULT_LANGUAGE,
        parent=None,
    ) -> None:
        super().__init__(parent)
        self._language = language
        self._fieldnames = list(fieldnames)
        self._field_order = field_order
        self._required = set(required_fields)
        self._templates = list(templates)
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

        if self._templates:
            template_row = QHBoxLayout()
            template_row.addWidget(QLabel(tr("import.mapping_template", language)))
            self._template_combo = QComboBox()
            self._template_combo.addItem(tr("import.mapping_none", language), None)
            for template in self._templates:
                self._template_combo.addItem(template.name, template)
            self._template_combo.currentIndexChanged.connect(
                self._apply_selected_template
            )
            template_row.addWidget(self._template_combo, stretch=1)
            layout.addLayout(template_row)
        else:
            self._template_combo = None

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
