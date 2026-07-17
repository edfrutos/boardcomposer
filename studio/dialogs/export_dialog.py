"""Export dialog with format options and preview (SCR-007)."""

from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QTextEdit,
    QVBoxLayout,
)

from boardcomposer.domain import AssemblySolution, Project
from studio.export_options import (
    VALID_EXPORT_FORMATS,
    ExportOptions,
    format_label,
    preview_svg,
    preview_text,
)
from studio.export_templates import ExportTemplatesManager
from studio.solution_thumbnail import svg_to_pixmap

_GRAPHIC_PREVIEW_SIZE = QSize(520, 280)
_NO_TEMPLATE = ""


class ExportDialog(QDialog):
    """Choose format/options and preview before exporting a solution."""

    def __init__(
        self,
        solution: AssemblySolution,
        project: Project | None,
        options: ExportOptions,
        *,
        templates: ExportTemplatesManager | None = None,
        strategy_name: str | None = None,
        solution_index: int | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("Exportar solución")
        self.setMinimumSize(640, 660)
        self._solution = solution
        self._project = project
        self._strategy_name = strategy_name
        self._solution_index = solution_index
        self._templates = (
            templates
            if templates is not None
            else ExportTemplatesManager(autoload=False)
        )

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "Elige el formato y el contenido. La vista previa refleja "
                "las opciones seleccionadas."
            )
        )

        form = QFormLayout()

        template_row = QHBoxLayout()
        self.template = QComboBox()
        self.template.currentIndexChanged.connect(self._on_template_selected)
        template_row.addWidget(self.template, stretch=1)

        self.save_template_button = QPushButton("Guardar…")
        self.save_template_button.clicked.connect(self._save_template)
        template_row.addWidget(self.save_template_button)

        self.delete_template_button = QPushButton("Eliminar")
        self.delete_template_button.clicked.connect(self._delete_template)
        template_row.addWidget(self.delete_template_button)
        form.addRow("Plantilla:", template_row)

        self.format = QComboBox()
        for key in VALID_EXPORT_FORMATS:
            self.format.addItem(format_label(key), key)
        index = self.format.findData(options.format)
        self.format.setCurrentIndex(index if index >= 0 else 0)
        self.format.currentIndexChanged.connect(self._on_options_edited)
        form.addRow("Formato:", self.format)

        self.include_metrics = QCheckBox("Incluir métricas (JSON)")
        self.include_metrics.setChecked(options.include_metrics)
        self.include_metrics.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_metrics)

        self.include_explanation = QCheckBox("Incluir explicación (JSON)")
        self.include_explanation.setChecked(options.include_explanation)
        self.include_explanation.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_explanation)

        self.include_offcuts = QCheckBox("Incluir retales")
        self.include_offcuts.setChecked(options.include_offcuts)
        self.include_offcuts.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_offcuts)
        layout.addLayout(form)

        layout.addWidget(QLabel("Vista previa gráfica"))
        self.graphic_preview = QLabel()
        self.graphic_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graphic_preview.setMinimumHeight(200)
        self.graphic_preview.setFrameShape(QFrame.Shape.StyledPanel)
        self.graphic_preview.setStyleSheet(
            "QLabel { background: white; color: #64748b; }"
        )
        graphic_scroll = QScrollArea()
        graphic_scroll.setWidgetResizable(True)
        graphic_scroll.setFrameShape(QFrame.Shape.NoFrame)
        graphic_scroll.setMinimumHeight(220)
        graphic_scroll.setWidget(self.graphic_preview)
        layout.addWidget(graphic_scroll)

        layout.addWidget(QLabel("Resumen / contenido"))
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumHeight(120)
        layout.addWidget(self.preview)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Exportar…")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._reload_templates()
        self._refresh_preview()

    def options(self) -> ExportOptions:
        return ExportOptions(
            format=self.format.currentData() or "svg",
            include_metrics=self.include_metrics.isChecked(),
            include_explanation=self.include_explanation.isChecked(),
            include_offcuts=self.include_offcuts.isChecked(),
        ).normalized()

    def _reload_templates(self, selected: str | None = None) -> None:
        current = selected if selected is not None else self.template.currentData()
        self.template.blockSignals(True)
        self.template.clear()
        self.template.addItem("(sin plantilla)", _NO_TEMPLATE)
        for name in self._templates.names():
            self.template.addItem(name, name)
        index = self.template.findData(current or _NO_TEMPLATE)
        self.template.setCurrentIndex(index if index >= 0 else 0)
        self.template.blockSignals(False)
        self._update_template_buttons()

    def _update_template_buttons(self) -> None:
        has_selection = bool(self.template.currentData())
        self.delete_template_button.setEnabled(has_selection)

    def _apply_options(self, options: ExportOptions) -> None:
        options = options.normalized()
        self.format.blockSignals(True)
        self.include_metrics.blockSignals(True)
        self.include_explanation.blockSignals(True)
        self.include_offcuts.blockSignals(True)

        index = self.format.findData(options.format)
        self.format.setCurrentIndex(index if index >= 0 else 0)
        self.include_metrics.setChecked(options.include_metrics)
        self.include_explanation.setChecked(options.include_explanation)
        self.include_offcuts.setChecked(options.include_offcuts)

        self.format.blockSignals(False)
        self.include_metrics.blockSignals(False)
        self.include_explanation.blockSignals(False)
        self.include_offcuts.blockSignals(False)
        self._refresh_preview()

    def _on_template_selected(self, index: int) -> None:
        del index
        self._update_template_buttons()
        name = self.template.currentData() or _NO_TEMPLATE
        if not name:
            return
        template = self._templates.get(name)
        if template is None:
            return
        self._apply_options(template.options)

    def _on_options_edited(self, *_args) -> None:
        if self.template.currentData():
            self.template.blockSignals(True)
            self.template.setCurrentIndex(0)
            self.template.blockSignals(False)
            self._update_template_buttons()
        self._refresh_preview()

    def _save_template(self) -> None:
        suggested = self.template.currentData() or ""
        name, accepted = QInputDialog.getText(
            self,
            "Guardar plantilla",
            "Nombre de la plantilla:",
            text=suggested,
        )
        if not accepted:
            return
        name = name.strip()
        if not name:
            QMessageBox.warning(
                self,
                "Guardar plantilla",
                "El nombre de la plantilla no puede estar vacío.",
            )
            return
        self._templates.save_template(name, self.options())
        self._reload_templates(selected=name)

    def _delete_template(self) -> None:
        name = self.template.currentData() or _NO_TEMPLATE
        if not name:
            return
        answer = QMessageBox.question(
            self,
            "Eliminar plantilla",
            f"¿Eliminar la plantilla «{name}»?",
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._templates.delete(name)
        self._reload_templates(selected=_NO_TEMPLATE)

    def _refresh_preview(self) -> None:
        options = self.options()
        json_only = options.format == "json"
        self.include_metrics.setEnabled(json_only)
        self.include_explanation.setEnabled(json_only)

        svg = preview_svg(self._solution, self._project, options)
        pixmap = svg_to_pixmap(svg, box=_GRAPHIC_PREVIEW_SIZE)
        self.graphic_preview.setPixmap(pixmap)
        self.graphic_preview.setText("" if not pixmap.isNull() else "Sin vista previa")

        self.preview.setPlainText(
            preview_text(
                self._solution,
                self._project,
                options,
                strategy_name=self._strategy_name,
                solution_index=self._solution_index,
            )
        )
