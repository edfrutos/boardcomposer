"""Export dialog with format options and preview (SCR-007)."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from boardcomposer.domain import AssemblySolution, Project
from boardcomposer.export import (
    MAX_PDF_MARGIN_MM,
    MIN_PDF_MARGIN_MM,
    VALID_PDF_ORIENTATIONS,
    VALID_PDF_PAPERS,
    VALID_PDF_SCALES,
)
from studio.dialogs.dialog_chrome import (
    polish_dialog_button_box,
    polish_secondary_button,
)
from studio.export_options import (
    MAX_JPEG_QUALITY,
    MAX_RASTER_DPI,
    MIN_JPEG_QUALITY,
    MIN_RASTER_DPI,
    VALID_EXPORT_FORMATS,
    ExportOptions,
    format_label,
    preview_svg,
    preview_text,
)
from studio.export_templates import ExportTemplatesManager, normalize_client
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.solution_thumbnail import svg_to_pixmap

_GRAPHIC_PREVIEW_SIZE = QSize(520, 280)
_NO_TEMPLATE = ""
_ALL_CLIENTS = "*"
_KEY_SEP = "\x1e"


def _template_key(client: str, name: str) -> str:
    return f"{normalize_client(client)}{_KEY_SEP}{name}"


def _split_template_key(key: str) -> tuple[str, str]:
    if _KEY_SEP not in key:
        return "", key
    client, name = key.split(_KEY_SEP, 1)
    return client, name


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
        language: str = DEFAULT_LANGUAGE,
        templates_directory: str | None = None,
        on_templates_directory: Callable[[str | Path], None] | None = None,
        material_prices: dict[str, float] | None = None,
        ranked_count: int = 1,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._language = language
        self._solution = solution
        self._project = project
        self._strategy_name = strategy_name
        self._solution_index = solution_index
        self._templates_directory = templates_directory or ""
        self._on_templates_directory = on_templates_directory
        self._material_prices = material_prices
        self._ranked_count = max(int(ranked_count), 1)
        self._templates = (
            templates
            if templates is not None
            else ExportTemplatesManager(autoload=False)
        )

        self.setWindowTitle(self._tr("export.title"))
        self.setMinimumSize(640, 700)

        layout = QVBoxLayout(self)
        self.intro = QLabel(self._tr("export.intro"))
        layout.addWidget(self.intro)

        form = QFormLayout()

        self.client = QComboBox()
        self.client.setEditable(True)
        self.client.currentIndexChanged.connect(self._on_client_changed)
        self.client.editTextChanged.connect(self._on_client_edited)
        form.addRow(self._tr("export.client"), self.client)

        template_row = QHBoxLayout()
        self.template = QComboBox()
        self.template.currentIndexChanged.connect(self._on_template_selected)
        template_row.addWidget(self.template, stretch=1)

        self.save_template_button = polish_secondary_button(
            QPushButton(self._tr("export.save")),
            tip=self._tr("tip.export_save_template"),
        )
        self.save_template_button.clicked.connect(self._save_template)
        template_row.addWidget(self.save_template_button)

        self.delete_template_button = polish_secondary_button(
            QPushButton(self._tr("export.delete")),
            tip=self._tr("tip.export_delete_template"),
        )
        self.delete_template_button.clicked.connect(self._delete_template)
        template_row.addWidget(self.delete_template_button)
        form.addRow(self._tr("export.template"), template_row)

        share_row = QHBoxLayout()
        self.export_templates_button = polish_secondary_button(
            QPushButton(self._tr("export.share_export")),
            tip=self._tr("tip.export_share_export"),
        )
        self.export_templates_button.clicked.connect(self._export_templates_pack)
        share_row.addWidget(self.export_templates_button)
        self.import_templates_button = polish_secondary_button(
            QPushButton(self._tr("export.share_import")),
            tip=self._tr("tip.export_share_import"),
        )
        self.import_templates_button.clicked.connect(self._import_templates_pack)
        share_row.addWidget(self.import_templates_button)
        share_row.addStretch(1)
        form.addRow("", share_row)

        self.format = QComboBox()
        for key in VALID_EXPORT_FORMATS:
            self.format.addItem(format_label(key), key)
        index = self.format.findData(options.format)
        self.format.setCurrentIndex(index if index >= 0 else 0)
        self.format.currentIndexChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.format"), self.format)

        self.include_metrics = QCheckBox(self._tr("export.metrics"))
        self.include_metrics.setChecked(options.include_metrics)
        self.include_metrics.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_metrics)

        self.include_explanation = QCheckBox(self._tr("export.explanation"))
        self.include_explanation.setChecked(options.include_explanation)
        self.include_explanation.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_explanation)

        self.include_offcuts = QCheckBox(self._tr("export.offcuts"))
        self.include_offcuts.setChecked(options.include_offcuts)
        self.include_offcuts.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_offcuts)

        self.include_piece_labels = QCheckBox(self._tr("export.labels"))
        self.include_piece_labels.setChecked(options.include_piece_labels)
        self.include_piece_labels.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_piece_labels)

        self.include_offcut_labels = QCheckBox(self._tr("export.offcut_labels"))
        self.include_offcut_labels.setChecked(options.include_offcut_labels)
        self.include_offcut_labels.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_offcut_labels)

        self.include_panel_dimensions = QCheckBox(self._tr("export.panel_dimensions"))
        self.include_panel_dimensions.setChecked(options.include_panel_dimensions)
        self.include_panel_dimensions.toggled.connect(self._on_options_edited)
        form.addRow("", self.include_panel_dimensions)

        self.pdf_paper = QComboBox()
        for key in VALID_PDF_PAPERS:
            self.pdf_paper.addItem(self._tr(f"export.paper_{key}"), key)
        paper_index = self.pdf_paper.findData(options.pdf_paper)
        self.pdf_paper.setCurrentIndex(paper_index if paper_index >= 0 else 0)
        self.pdf_paper.currentIndexChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.pdf_paper"), self.pdf_paper)

        self.pdf_orientation = QComboBox()
        for key in VALID_PDF_ORIENTATIONS:
            self.pdf_orientation.addItem(self._tr(f"export.orientation_{key}"), key)
        orientation_index = self.pdf_orientation.findData(options.pdf_orientation)
        self.pdf_orientation.setCurrentIndex(
            orientation_index if orientation_index >= 0 else 0
        )
        self.pdf_orientation.currentIndexChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.pdf_orientation"), self.pdf_orientation)

        self.pdf_scale = QComboBox()
        for key in VALID_PDF_SCALES:
            self.pdf_scale.addItem(
                self._tr(f"export.scale_{key.replace(':', '_')}"), key
            )
        scale_index = self.pdf_scale.findData(options.pdf_scale)
        self.pdf_scale.setCurrentIndex(scale_index if scale_index >= 0 else 0)
        self.pdf_scale.currentIndexChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.pdf_scale"), self.pdf_scale)

        self.pdf_margin_mm = QDoubleSpinBox()
        self.pdf_margin_mm.setRange(MIN_PDF_MARGIN_MM, MAX_PDF_MARGIN_MM)
        self.pdf_margin_mm.setDecimals(1)
        self.pdf_margin_mm.setSingleStep(1.0)
        self.pdf_margin_mm.setSuffix(" mm")
        self.pdf_margin_mm.setValue(options.pdf_margin_mm)
        self.pdf_margin_mm.valueChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.pdf_margin"), self.pdf_margin_mm)

        self.raster_dpi = QSpinBox()
        self.raster_dpi.setRange(MIN_RASTER_DPI, MAX_RASTER_DPI)
        self.raster_dpi.setSingleStep(12)
        self.raster_dpi.setSuffix(" DPI")
        self.raster_dpi.setValue(options.raster_dpi)
        self.raster_dpi.valueChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.raster_dpi"), self.raster_dpi)

        self.jpeg_quality = QSpinBox()
        self.jpeg_quality.setRange(MIN_JPEG_QUALITY, MAX_JPEG_QUALITY)
        self.jpeg_quality.setSingleStep(5)
        self.jpeg_quality.setSuffix(" %")
        self.jpeg_quality.setValue(options.jpeg_quality)
        self.jpeg_quality.valueChanged.connect(self._on_options_edited)
        form.addRow(self._tr("export.jpeg_quality"), self.jpeg_quality)

        self.export_batch = QCheckBox(
            self._tr("export.batch", count=self._ranked_count)
        )
        can_batch = self._ranked_count >= 2
        self.export_batch.setChecked(bool(options.export_batch) and can_batch)
        self.export_batch.setEnabled(can_batch)
        self.export_batch.toggled.connect(self._on_options_edited)
        form.addRow("", self.export_batch)
        layout.addLayout(form)

        layout.addWidget(QLabel(self._tr("export.graphic")))
        self.graphic_preview = QLabel()
        self.graphic_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.graphic_preview.setMinimumHeight(200)
        self.graphic_preview.setFrameShape(QFrame.Shape.StyledPanel)
        self.graphic_preview.setObjectName("exportGraphicPreview")
        graphic_scroll = QScrollArea()
        graphic_scroll.setWidgetResizable(True)
        graphic_scroll.setFrameShape(QFrame.Shape.NoFrame)
        graphic_scroll.setMinimumHeight(220)
        graphic_scroll.setWidget(self.graphic_preview)
        layout.addWidget(graphic_scroll)

        layout.addWidget(QLabel(self._tr("export.summary")))
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumHeight(120)
        layout.addWidget(self.preview)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.button(QDialogButtonBox.StandardButton.Ok).setText(
            self._tr("export.export_btn")
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self._reload_clients()
        self._reload_templates()
        self._refresh_preview()

    def _tr(self, key: str, **kwargs: object) -> str:
        return tr(key, self._language, **kwargs)

    def options(self) -> ExportOptions:
        return ExportOptions(
            format=self.format.currentData() or "svg",
            include_metrics=self.include_metrics.isChecked(),
            include_explanation=self.include_explanation.isChecked(),
            include_offcuts=self.include_offcuts.isChecked(),
            include_piece_labels=self.include_piece_labels.isChecked(),
            include_offcut_labels=self.include_offcut_labels.isChecked(),
            include_panel_dimensions=self.include_panel_dimensions.isChecked(),
            pdf_paper=self.pdf_paper.currentData() or "drawing",
            pdf_orientation=self.pdf_orientation.currentData() or "auto",
            pdf_scale=self.pdf_scale.currentData() or "1:1",
            pdf_margin_mm=self.pdf_margin_mm.value(),
            raster_dpi=self.raster_dpi.value(),
            jpeg_quality=self.jpeg_quality.value(),
            export_batch=self.export_batch.isChecked() and self._ranked_count >= 2,
        ).normalized()

    def _client_filter(self) -> str | None:
        """Return client filter: None=all, ''=general, or a client name."""
        data = self.client.currentData()
        if data == _ALL_CLIENTS:
            return None
        if data is not None:
            return str(data)
        text = normalize_client(self.client.currentText())
        general = self._tr("export.client_general")
        all_label = self._tr("export.client_all")
        if text in {general, all_label}:
            return None if text == all_label else ""
        return text

    def _client_for_save(self) -> str:
        """Client name used when saving a profile (never the 'all' sentinel)."""
        data = self.client.currentData()
        if data == _ALL_CLIENTS:
            return ""
        if data is not None:
            return normalize_client(str(data))
        text = normalize_client(self.client.currentText())
        if text in {
            self._tr("export.client_general"),
            self._tr("export.client_all"),
        }:
            return ""
        return text

    def _reload_clients(self, selected: str | None = _ALL_CLIENTS) -> None:
        current = selected if selected is not None else self._client_filter()
        if current is None:
            current = _ALL_CLIENTS

        self.client.blockSignals(True)
        self.client.clear()
        self.client.addItem(self._tr("export.client_all"), _ALL_CLIENTS)
        self.client.addItem(self._tr("export.client_general"), "")
        for name in self._templates.clients():
            self.client.addItem(name, name)

        index = self.client.findData(current)
        if index < 0 and current not in {_ALL_CLIENTS, ""}:
            self.client.addItem(str(current), str(current))
            index = self.client.findData(current)
        self.client.setCurrentIndex(index if index >= 0 else 0)
        self.client.blockSignals(False)

    def _reload_templates(self, selected_key: str | None = None) -> None:
        current = (
            selected_key if selected_key is not None else self.template.currentData()
        )
        client_filter = self._client_filter()
        general_label = self._tr("export.client_general")

        self.template.blockSignals(True)
        self.template.clear()
        self.template.addItem(self._tr("export.no_template"), _NO_TEMPLATE)

        for template in self._templates.templates_for(client_filter):
            key = _template_key(template.client, template.name)
            label = template.display_label(
                general_label=general_label if client_filter is None else ""
            )
            self.template.addItem(label, key)

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
        self.include_piece_labels.blockSignals(True)
        self.include_offcut_labels.blockSignals(True)
        self.include_panel_dimensions.blockSignals(True)
        self.pdf_paper.blockSignals(True)
        self.pdf_orientation.blockSignals(True)
        self.pdf_scale.blockSignals(True)
        self.pdf_margin_mm.blockSignals(True)
        self.raster_dpi.blockSignals(True)
        self.jpeg_quality.blockSignals(True)
        self.export_batch.blockSignals(True)

        index = self.format.findData(options.format)
        self.format.setCurrentIndex(index if index >= 0 else 0)
        self.include_metrics.setChecked(options.include_metrics)
        self.include_explanation.setChecked(options.include_explanation)
        self.include_offcuts.setChecked(options.include_offcuts)
        self.include_piece_labels.setChecked(options.include_piece_labels)
        self.include_offcut_labels.setChecked(options.include_offcut_labels)
        self.include_panel_dimensions.setChecked(options.include_panel_dimensions)
        paper_index = self.pdf_paper.findData(options.pdf_paper)
        self.pdf_paper.setCurrentIndex(paper_index if paper_index >= 0 else 0)
        orientation_index = self.pdf_orientation.findData(options.pdf_orientation)
        self.pdf_orientation.setCurrentIndex(
            orientation_index if orientation_index >= 0 else 0
        )
        scale_index = self.pdf_scale.findData(options.pdf_scale)
        self.pdf_scale.setCurrentIndex(scale_index if scale_index >= 0 else 0)
        self.pdf_margin_mm.setValue(options.pdf_margin_mm)
        self.raster_dpi.setValue(options.raster_dpi)
        self.jpeg_quality.setValue(options.jpeg_quality)
        self.export_batch.setChecked(
            bool(options.export_batch) and self._ranked_count >= 2
        )

        self.format.blockSignals(False)
        self.include_metrics.blockSignals(False)
        self.include_explanation.blockSignals(False)
        self.include_offcuts.blockSignals(False)
        self.include_piece_labels.blockSignals(False)
        self.include_offcut_labels.blockSignals(False)
        self.include_panel_dimensions.blockSignals(False)
        self.pdf_paper.blockSignals(False)
        self.pdf_orientation.blockSignals(False)
        self.pdf_scale.blockSignals(False)
        self.pdf_margin_mm.blockSignals(False)
        self.raster_dpi.blockSignals(False)
        self.jpeg_quality.blockSignals(False)
        self.export_batch.blockSignals(False)
        self._refresh_preview()

    def _on_client_changed(self, index: int) -> None:
        del index
        self._reload_templates(selected_key=_NO_TEMPLATE)

    def _on_client_edited(self, text: str) -> None:
        del text
        # Typing a custom client name: keep template list for exact data match
        # when the combo still points at a known item; otherwise show all.
        if self.client.findText(self.client.currentText()) < 0:
            return

    def _on_template_selected(self, index: int) -> None:
        del index
        self._update_template_buttons()
        key = self.template.currentData() or _NO_TEMPLATE
        if not key:
            return
        client, name = _split_template_key(key)
        template = self._templates.get(name, client=client)
        if template is None:
            return
        if self.client.currentData() == _ALL_CLIENTS and template.client:
            # Keep "all clients" filter but still apply options.
            pass
        self._apply_options(template.options)

    def _on_options_edited(self, *_args) -> None:
        if self.template.currentData():
            self.template.blockSignals(True)
            self.template.setCurrentIndex(0)
            self.template.blockSignals(False)
            self._update_template_buttons()
        self._refresh_preview()

    def _save_template(self) -> None:
        client = self._client_for_save()
        suggested_key = self.template.currentData() or ""
        suggested = ""
        if suggested_key:
            _, suggested = _split_template_key(suggested_key)

        name, accepted = QInputDialog.getText(
            self,
            self._tr("export.save_template_title"),
            self._tr("export.save_template_prompt"),
            text=suggested,
        )
        if not accepted:
            return
        name = name.strip()
        if not name:
            QMessageBox.warning(
                self,
                self._tr("export.save_template_title"),
                self._tr("export.empty_name"),
            )
            return

        # If filter is "all" and user typed a client in the editable field
        # that isn't a sentinel, prefer that text.
        if self.client.currentData() == _ALL_CLIENTS:
            typed = normalize_client(self.client.currentText())
            if typed and typed not in {
                self._tr("export.client_all"),
                self._tr("export.client_general"),
            }:
                client = typed

        self._templates.save_template(name, self.options(), client=client)
        self._reload_clients(selected=client or "")
        self._reload_templates(selected_key=_template_key(client, name))

    def _delete_template(self) -> None:
        key = self.template.currentData() or _NO_TEMPLATE
        if not key:
            return
        client, name = _split_template_key(key)
        label = self.template.currentText()
        answer = QMessageBox.question(
            self,
            self._tr("export.delete_title"),
            self._tr("export.delete_confirm", name=label),
        )
        if answer != QMessageBox.StandardButton.Yes:
            return
        self._templates.delete(name, client=client)
        self._reload_clients(selected=self.client.currentData())
        self._reload_templates(selected_key=_NO_TEMPLATE)

    def _suggested_templates_path(self, default_filename: str = "") -> str:
        """Prefer last pack folder when it still exists."""
        directory = self._templates_directory.strip()
        if directory:
            folder = Path(directory).expanduser()
            if folder.is_dir():
                if default_filename:
                    return str(folder / default_filename)
                return str(folder)
        return default_filename

    def _remember_templates_directory(self, path: str | Path) -> None:
        if self._on_templates_directory is None:
            return
        folder = str(Path(path).expanduser().resolve().parent)
        self._templates_directory = folder
        self._on_templates_directory(path)

    def _export_templates_pack(self) -> None:
        client_filter = self._client_filter()
        path, _ = QFileDialog.getSaveFileName(
            self,
            self._tr("export.share_export_title"),
            self._suggested_templates_path("boardcomposer-export-templates.json"),
            self._tr("export.share_filter"),
        )
        if not path:
            return
        try:
            count = self._templates.export_pack(path, client=client_filter)
        except OSError as exc:
            QMessageBox.warning(
                self,
                self._tr("export.share_export_title"),
                self._tr("export.share_error", error=str(exc)),
            )
            return
        self._remember_templates_directory(path)
        QMessageBox.information(
            self,
            self._tr("export.share_export_title"),
            self._tr("export.share_export_done", count=count),
        )

    def _import_templates_pack(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            self._tr("export.share_import_title"),
            self._suggested_templates_path(),
            self._tr("export.share_filter"),
        )
        if not path:
            return

        choice = QMessageBox.question(
            self,
            self._tr("export.share_import_title"),
            self._tr("export.share_import_mode"),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Cancel,
        )
        if choice == QMessageBox.StandardButton.Cancel:
            return
        mode = "replace" if choice == QMessageBox.StandardButton.No else "merge"

        try:
            imported, total = self._templates.import_pack(path, mode=mode)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(
                self,
                self._tr("export.share_import_title"),
                self._tr("export.share_error", error=str(exc)),
            )
            return

        self._remember_templates_directory(path)
        self._reload_clients(selected=_ALL_CLIENTS)
        self._reload_templates(selected_key=_NO_TEMPLATE)
        QMessageBox.information(
            self,
            self._tr("export.share_import_title"),
            self._tr(
                "export.share_import_done",
                imported=imported,
                total=total,
                mode=self._tr(
                    "export.share_mode_replace"
                    if mode == "replace"
                    else "export.share_mode_merge"
                ),
            ),
        )

    def _refresh_preview(self) -> None:
        options = self.options()
        json_only = options.format == "json"
        self.include_metrics.setEnabled(json_only)
        self.include_explanation.setEnabled(json_only)
        plan = options.format in {"svg", "png", "jpeg", "dxf", "pdf"}
        self.include_piece_labels.setEnabled(plan)
        self.include_offcut_labels.setEnabled(plan and options.include_offcuts)
        self.include_panel_dimensions.setEnabled(plan)
        pdf = options.format == "pdf"
        self.pdf_paper.setEnabled(pdf)
        self.pdf_margin_mm.setEnabled(pdf)
        iso_paper = pdf and options.pdf_paper != "drawing"
        self.pdf_orientation.setEnabled(iso_paper)
        self.pdf_scale.setEnabled(iso_paper)
        raster = options.format in {"png", "jpeg"}
        self.raster_dpi.setEnabled(raster)
        self.jpeg_quality.setEnabled(options.format == "jpeg")

        svg = preview_svg(self._solution, self._project, options)
        pixmap = svg_to_pixmap(svg, box=_GRAPHIC_PREVIEW_SIZE)
        self.graphic_preview.setPixmap(pixmap)
        self.graphic_preview.setText(
            "" if not pixmap.isNull() else self._tr("export.no_preview")
        )

        self.preview.setPlainText(
            preview_text(
                self._solution,
                self._project,
                options,
                strategy_name=self._strategy_name,
                solution_index=self._solution_index,
                material_prices=self._material_prices,
                ranked_count=self._ranked_count,
            )
        )
