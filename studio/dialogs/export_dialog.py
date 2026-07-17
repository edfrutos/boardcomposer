"""Export dialog with format options and preview (SCR-007)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QTextEdit,
    QVBoxLayout,
)

from boardcomposer.domain import AssemblySolution, Project
from studio.export_options import (
    VALID_EXPORT_FORMATS,
    ExportOptions,
    format_label,
    preview_text,
)


class ExportDialog(QDialog):
    """Choose format/options and preview before exporting a solution."""

    def __init__(
        self,
        solution: AssemblySolution,
        project: Project | None,
        options: ExportOptions,
        *,
        strategy_name: str | None = None,
        solution_index: int | None = None,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle("Exportar solución")
        self.setMinimumSize(560, 480)
        self._solution = solution
        self._project = project
        self._strategy_name = strategy_name
        self._solution_index = solution_index

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "Elige el formato y el contenido. La vista previa refleja "
                "las opciones seleccionadas."
            )
        )

        form = QFormLayout()
        self.format = QComboBox()
        for key in VALID_EXPORT_FORMATS:
            self.format.addItem(format_label(key), key)
        index = self.format.findData(options.format)
        self.format.setCurrentIndex(index if index >= 0 else 0)
        self.format.currentIndexChanged.connect(self._refresh_preview)
        form.addRow("Formato:", self.format)

        self.include_metrics = QCheckBox("Incluir métricas (JSON)")
        self.include_metrics.setChecked(options.include_metrics)
        self.include_metrics.toggled.connect(self._refresh_preview)
        form.addRow("", self.include_metrics)

        self.include_explanation = QCheckBox("Incluir explicación (JSON)")
        self.include_explanation.setChecked(options.include_explanation)
        self.include_explanation.toggled.connect(self._refresh_preview)
        form.addRow("", self.include_explanation)

        self.include_offcuts = QCheckBox("Incluir retales")
        self.include_offcuts.setChecked(options.include_offcuts)
        self.include_offcuts.toggled.connect(self._refresh_preview)
        form.addRow("", self.include_offcuts)
        layout.addLayout(form)

        layout.addWidget(QLabel("Vista previa"))
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        layout.addWidget(self.preview)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText("Exportar…")
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._refresh_preview()

    def options(self) -> ExportOptions:
        return ExportOptions(
            format=self.format.currentData() or "svg",
            include_metrics=self.include_metrics.isChecked(),
            include_explanation=self.include_explanation.isChecked(),
            include_offcuts=self.include_offcuts.isChecked(),
        ).normalized()

    def _refresh_preview(self) -> None:
        options = self.options()
        json_only = options.format == "json"
        self.include_metrics.setEnabled(json_only)
        self.include_explanation.setEnabled(json_only)

        self.preview.setPlainText(
            preview_text(
                self._solution,
                self._project,
                options,
                strategy_name=self._strategy_name,
                solution_index=self._solution_index,
            )
        )
