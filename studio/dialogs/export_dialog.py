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
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._language = language
        self._solution = solution
        self._project = project
        self._strategy_name = strategy_name
        self._solution_index = solution_index
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

        self.save_template_button = QPushButton(self._tr("export.save"))
        self.save_template_button.clicked.connect(self._save_template)
        template_row.addWidget(self.save_template_button)

        self.delete_template_button = QPushButton(self._tr("export.delete"))
        self.delete_template_button.clicked.connect(self._delete_template)
        template_row.addWidget(self.delete_template_button)
        form.addRow(self._tr("export.template"), template_row)

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
        layout.addLayout(form)

        layout.addWidget(QLabel(self._tr("export.graphic")))
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

        layout.addWidget(QLabel(self._tr("export.summary")))
        self.preview = QTextEdit()
        self.preview.setReadOnly(True)
        self.preview.setMinimumHeight(120)
        layout.addWidget(self.preview)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
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

    def _refresh_preview(self) -> None:
        options = self.options()
        json_only = options.format == "json"
        self.include_metrics.setEnabled(json_only)
        self.include_explanation.setEnabled(json_only)

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
            )
        )
