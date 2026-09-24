"""Preferences dialog for Studio appearance, workspace and scoring (SCR-006)."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from boardcomposer.export.pdf_page import (
    DEFAULT_PDF_MARGIN_MM,
    DEFAULT_PDF_ORIENTATION,
    DEFAULT_PDF_PAPER,
    DEFAULT_PDF_SCALE,
    MAX_PDF_MARGIN_MM,
    MIN_PDF_MARGIN_MM,
    VALID_PDF_ORIENTATIONS,
    VALID_PDF_PAPERS,
    VALID_PDF_SCALES,
)
from boardcomposer.export.quote import (
    DEFAULT_LABOR_EUR_PER_HOUR,
    DEFAULT_LABOR_MINUTES_PER_PIECE,
    MAX_LABOR_EUR_PER_HOUR,
    MAX_LABOR_MINUTES_PER_PIECE,
)
from boardcomposer.layout.kerf import DEFAULT_KERF_MM, MAX_KERF_MM
from boardcomposer.solver.strategies import strategy_by_name
from studio.dialogs.dialog_chrome import (
    polish_dialog_button_box,
    polish_secondary_button,
)
from studio.export_options import (
    DEFAULT_JPEG_QUALITY,
    DEFAULT_RASTER_DPI,
    MAX_JPEG_QUALITY,
    MAX_RASTER_DPI,
    MIN_JPEG_QUALITY,
    MIN_RASTER_DPI,
    VALID_EXPORT_FORMATS,
    format_label,
)
from studio.i18n import DEFAULT_LANGUAGE, VALID_LANGUAGES, tr
from studio.material_catalog import MaterialCatalogManager
from studio.material_fields import fill_material_combo
from studio.preferences import (
    DEFAULT_GRID_SIZE_MM,
    DEFAULT_MATERIAL,
    DEFAULT_MAX_SOLUTIONS,
    MAX_GRID_SIZE_MM,
    MAX_MAX_SOLUTIONS,
    MIN_GRID_SIZE_MM,
    MIN_MAX_SOLUTIONS,
    VALID_STRATEGIES,
    StudioPreferences,
    WeightPreferences,
    default_preferences_path,
    export_preferences_pack,
    import_preferences_pack,
)
from studio.theme import DEFAULT_THEME, VALID_THEMES
from studio.units import DEFAULT_UNITS, VALID_UNITS


class PreferencesDialog(QDialog):
    """Edit user-level Studio preferences."""

    def __init__(
        self,
        preferences: StudioPreferences,
        parent=None,
        *,
        catalog: MaterialCatalogManager | None = None,
        pack_directory: str = "",
        on_pack_directory: Callable[[str | Path], None] | None = None,
    ) -> None:
        super().__init__(parent)

        self._preferences = preferences
        self._language = preferences.language
        self._catalog = catalog
        self._pack_directory = pack_directory
        self._on_pack_directory = on_pack_directory
        self.setMinimumWidth(460)

        layout = QVBoxLayout(self)
        self._intro = QLabel()
        self._intro.setWordWrap(True)
        layout.addWidget(self._intro)

        self.general = QGroupBox()
        general_form = QFormLayout(self.general)

        self.language = QComboBox()
        for key in VALID_LANGUAGES:
            self.language.addItem(tr(f"language.{key}", preferences.language), key)
        language_index = self.language.findData(preferences.language)
        self.language.setCurrentIndex(language_index if language_index >= 0 else 0)
        self.language.currentIndexChanged.connect(self._on_language_changed)
        self._language_label = QLabel()
        general_form.addRow(self._language_label, self.language)

        self.theme = QComboBox()
        for key in VALID_THEMES:
            self.theme.addItem(tr(f"theme.{key}", preferences.language), key)
        theme_index = self.theme.findData(preferences.theme)
        self.theme.setCurrentIndex(theme_index if theme_index >= 0 else 0)
        self._theme_label = QLabel()
        general_form.addRow(self._theme_label, self.theme)

        self.units = QComboBox()
        for key in VALID_UNITS:
            self.units.addItem(tr(f"units.{key}", preferences.language), key)
        units_index = self.units.findData(preferences.units)
        self.units.setCurrentIndex(units_index if units_index >= 0 else 0)
        self._units_label = QLabel()
        general_form.addRow(self._units_label, self.units)
        layout.addWidget(self.general)

        self.workspace = QGroupBox()
        workspace_form = QFormLayout(self.workspace)
        self.show_grid = QCheckBox()
        self.show_grid.setChecked(preferences.show_grid)
        workspace_form.addRow("", self.show_grid)
        self.grid_size_mm = QSpinBox()
        self.grid_size_mm.setRange(MIN_GRID_SIZE_MM, MAX_GRID_SIZE_MM)
        self.grid_size_mm.setSuffix(" mm")
        self.grid_size_mm.setSingleStep(10)
        self.grid_size_mm.setValue(preferences.grid_size_mm)
        self._grid_size_label = QLabel()
        workspace_form.addRow(self._grid_size_label, self.grid_size_mm)
        layout.addWidget(self.workspace)

        self.algorithms = QGroupBox()
        algorithms_form = QFormLayout(self.algorithms)

        self.strategy = QComboBox()
        for key in VALID_STRATEGIES:
            self.strategy.addItem(tr(f"strategy.{key}", preferences.language), key)
        index = self.strategy.findData(preferences.strategy_name)
        self.strategy.setCurrentIndex(index if index >= 0 else 0)
        self.strategy.currentIndexChanged.connect(self._on_strategy_changed)
        self._strategy_label = QLabel()
        algorithms_form.addRow(self._strategy_label, self.strategy)

        self.use_custom_weights = QCheckBox()
        self.use_custom_weights.setChecked(preferences.use_custom_weights)
        self.use_custom_weights.toggled.connect(self._on_custom_weights_toggled)
        algorithms_form.addRow("", self.use_custom_weights)

        self.material_utilization = self._weight_spin()
        self.placed_boards = self._weight_spin()
        self.compactness = self._weight_spin()
        self.rotation_penalty = self._weight_spin()

        self._weight_material_label = QLabel()
        self._weight_placed_label = QLabel()
        self._weight_compactness_label = QLabel()
        self._weight_rotation_label = QLabel()
        algorithms_form.addRow(self._weight_material_label, self.material_utilization)
        algorithms_form.addRow(self._weight_placed_label, self.placed_boards)
        algorithms_form.addRow(self._weight_compactness_label, self.compactness)
        algorithms_form.addRow(self._weight_rotation_label, self.rotation_penalty)
        layout.addWidget(self.algorithms)

        self.export_group = QGroupBox()
        export_form = QFormLayout(self.export_group)
        self.export_format = QComboBox()
        for key in VALID_EXPORT_FORMATS:
            self.export_format.addItem(format_label(key), key)
        export_index = self.export_format.findData(preferences.export_format)
        self.export_format.setCurrentIndex(export_index if export_index >= 0 else 0)
        self._export_format_label = QLabel()
        export_form.addRow(self._export_format_label, self.export_format)
        self.export_include_metrics = QCheckBox()
        self.export_include_metrics.setChecked(preferences.export_include_metrics)
        export_form.addRow("", self.export_include_metrics)
        self.export_include_explanation = QCheckBox()
        self.export_include_explanation.setChecked(
            preferences.export_include_explanation
        )
        export_form.addRow("", self.export_include_explanation)
        self.export_include_offcuts = QCheckBox()
        self.export_include_offcuts.setChecked(preferences.export_include_offcuts)
        export_form.addRow("", self.export_include_offcuts)
        self.export_include_piece_labels = QCheckBox()
        self.export_include_piece_labels.setChecked(
            preferences.export_include_piece_labels
        )
        export_form.addRow("", self.export_include_piece_labels)
        self.export_include_offcut_labels = QCheckBox()
        self.export_include_offcut_labels.setChecked(
            preferences.export_include_offcut_labels
        )
        export_form.addRow("", self.export_include_offcut_labels)
        self.export_include_panel_dimensions = QCheckBox()
        self.export_include_panel_dimensions.setChecked(
            preferences.export_include_panel_dimensions
        )
        export_form.addRow("", self.export_include_panel_dimensions)
        self.export_include_plan_traceability = QCheckBox()
        self.export_include_plan_traceability.setChecked(
            preferences.export_include_plan_traceability
        )
        export_form.addRow("", self.export_include_plan_traceability)
        self.export_batch = QCheckBox()
        self.export_batch.setChecked(preferences.export_batch)
        export_form.addRow("", self.export_batch)
        self.export_pdf_paper = QComboBox()
        for key in VALID_PDF_PAPERS:
            self.export_pdf_paper.addItem(key, key)
        paper_index = self.export_pdf_paper.findData(preferences.export_pdf_paper)
        self.export_pdf_paper.setCurrentIndex(paper_index if paper_index >= 0 else 0)
        self._export_pdf_paper_label = QLabel()
        export_form.addRow(self._export_pdf_paper_label, self.export_pdf_paper)
        self.export_pdf_orientation = QComboBox()
        for key in VALID_PDF_ORIENTATIONS:
            self.export_pdf_orientation.addItem(key, key)
        orientation_index = self.export_pdf_orientation.findData(
            preferences.export_pdf_orientation
        )
        self.export_pdf_orientation.setCurrentIndex(
            orientation_index if orientation_index >= 0 else 0
        )
        self._export_pdf_orientation_label = QLabel()
        export_form.addRow(
            self._export_pdf_orientation_label, self.export_pdf_orientation
        )
        self.export_pdf_scale = QComboBox()
        for key in VALID_PDF_SCALES:
            self.export_pdf_scale.addItem(key, key)
        scale_index = self.export_pdf_scale.findData(preferences.export_pdf_scale)
        self.export_pdf_scale.setCurrentIndex(scale_index if scale_index >= 0 else 0)
        self._export_pdf_scale_label = QLabel()
        export_form.addRow(self._export_pdf_scale_label, self.export_pdf_scale)
        self.export_pdf_margin_mm = QDoubleSpinBox()
        self.export_pdf_margin_mm.setRange(MIN_PDF_MARGIN_MM, MAX_PDF_MARGIN_MM)
        self.export_pdf_margin_mm.setDecimals(1)
        self.export_pdf_margin_mm.setSingleStep(1.0)
        self.export_pdf_margin_mm.setSuffix(" mm")
        self.export_pdf_margin_mm.setValue(preferences.export_pdf_margin_mm)
        self._export_pdf_margin_label = QLabel()
        export_form.addRow(self._export_pdf_margin_label, self.export_pdf_margin_mm)
        self.export_raster_dpi = QSpinBox()
        self.export_raster_dpi.setRange(MIN_RASTER_DPI, MAX_RASTER_DPI)
        self.export_raster_dpi.setSingleStep(12)
        self.export_raster_dpi.setSuffix(" DPI")
        self.export_raster_dpi.setValue(preferences.export_raster_dpi)
        self._export_raster_dpi_label = QLabel()
        export_form.addRow(self._export_raster_dpi_label, self.export_raster_dpi)
        self.export_jpeg_quality = QSpinBox()
        self.export_jpeg_quality.setRange(MIN_JPEG_QUALITY, MAX_JPEG_QUALITY)
        self.export_jpeg_quality.setSingleStep(5)
        self.export_jpeg_quality.setSuffix(" %")
        self.export_jpeg_quality.setValue(preferences.export_jpeg_quality)
        self._export_jpeg_quality_label = QLabel()
        export_form.addRow(self._export_jpeg_quality_label, self.export_jpeg_quality)
        self.quote_labor_eur_per_hour = QDoubleSpinBox()
        self.quote_labor_eur_per_hour.setRange(0.0, MAX_LABOR_EUR_PER_HOUR)
        self.quote_labor_eur_per_hour.setDecimals(2)
        self.quote_labor_eur_per_hour.setSingleStep(1.0)
        self.quote_labor_eur_per_hour.setSuffix(" EUR/h")
        self.quote_labor_eur_per_hour.setValue(preferences.quote_labor_eur_per_hour)
        self._quote_labor_rate_label = QLabel()
        export_form.addRow(self._quote_labor_rate_label, self.quote_labor_eur_per_hour)
        self.quote_labor_minutes_per_piece = QDoubleSpinBox()
        self.quote_labor_minutes_per_piece.setRange(0.0, MAX_LABOR_MINUTES_PER_PIECE)
        self.quote_labor_minutes_per_piece.setDecimals(1)
        self.quote_labor_minutes_per_piece.setSingleStep(1.0)
        self.quote_labor_minutes_per_piece.setSuffix(" min")
        self.quote_labor_minutes_per_piece.setValue(
            preferences.quote_labor_minutes_per_piece
        )
        self._quote_labor_minutes_label = QLabel()
        export_form.addRow(
            self._quote_labor_minutes_label, self.quote_labor_minutes_per_piece
        )
        layout.addWidget(self.export_group)

        self.advanced = QGroupBox()
        advanced_form = QFormLayout(self.advanced)
        self.max_solutions = QSpinBox()
        self.max_solutions.setRange(MIN_MAX_SOLUTIONS, MAX_MAX_SOLUTIONS)
        self.max_solutions.setValue(preferences.max_solutions)
        self._max_solutions_label = QLabel()
        advanced_form.addRow(self._max_solutions_label, self.max_solutions)
        self.default_kerf_mm = QDoubleSpinBox()
        self.default_kerf_mm.setRange(0.0, MAX_KERF_MM)
        self.default_kerf_mm.setDecimals(1)
        self.default_kerf_mm.setSingleStep(0.5)
        self.default_kerf_mm.setSuffix(" mm")
        self.default_kerf_mm.setValue(preferences.default_kerf_mm)
        self._default_kerf_label = QLabel()
        advanced_form.addRow(self._default_kerf_label, self.default_kerf_mm)
        self.default_material = QComboBox()
        catalog_model = catalog.catalog if catalog is not None else None
        fill_material_combo(
            self.default_material,
            catalog_model,
            preferences.default_material,
        )
        self._default_material_label = QLabel()
        advanced_form.addRow(self._default_material_label, self.default_material)
        self.edit_catalog = polish_secondary_button(QPushButton())
        self.edit_catalog.clicked.connect(self._open_material_catalog)
        if catalog is None:
            self.edit_catalog.hide()
        advanced_form.addRow("", self.edit_catalog)
        self.open_config_folder = polish_secondary_button(QPushButton())
        self.open_config_folder.clicked.connect(self._open_config_folder)
        advanced_form.addRow("", self.open_config_folder)
        share_row = QHBoxLayout()
        self.export_button = polish_secondary_button(QPushButton())
        self.import_button = polish_secondary_button(QPushButton())
        self.export_button.clicked.connect(self._export_pack)
        self.import_button.clicked.connect(self._import_pack)
        share_row.addWidget(self.export_button)
        share_row.addWidget(self.import_button)
        advanced_form.addRow("", share_row)
        layout.addWidget(self.advanced)

        self._buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.RestoreDefaults
            | QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(self._buttons)
        self._buttons.accepted.connect(self.accept)
        self._buttons.rejected.connect(self.reject)
        self._buttons.button(
            QDialogButtonBox.StandardButton.RestoreDefaults
        ).clicked.connect(self._restore_defaults)
        layout.addWidget(self._buttons)

        self._apply_weights_to_spins(preferences.weights)
        self._on_custom_weights_toggled(preferences.use_custom_weights)
        self._retranslate()

    def _retranslate(self) -> None:
        language = self.language.currentData() or DEFAULT_LANGUAGE
        self._language = language
        self.setWindowTitle(tr("prefs.title", language))
        self._intro.setText(tr("prefs.intro", language))
        self.general.setTitle(tr("prefs.general", language))
        self.workspace.setTitle(tr("prefs.workspace", language))
        self.algorithms.setTitle(tr("prefs.algorithms", language))
        self.export_group.setTitle(tr("prefs.export", language))
        self.advanced.setTitle(tr("prefs.advanced", language))
        self.show_grid.setText(tr("prefs.show_grid", language))
        self.open_config_folder.setText(tr("prefs.open_config_folder", language))
        config_tip = tr("tip.open_config_folder", language)
        self.open_config_folder.setToolTip(config_tip)
        self.open_config_folder.setStatusTip(config_tip)
        self.edit_catalog.setText(tr("prefs.edit_catalog", language))
        catalog_tip = tr("tip.prefs_edit_catalog", language)
        self.edit_catalog.setToolTip(catalog_tip)
        self.edit_catalog.setStatusTip(catalog_tip)
        self.export_button.setText(tr("prefs.share_export", language))
        self.import_button.setText(tr("prefs.share_import", language))
        export_tip = tr("tip.prefs_share_export", language)
        import_tip = tr("tip.prefs_share_import", language)
        self.export_button.setToolTip(export_tip)
        self.export_button.setStatusTip(export_tip)
        self.import_button.setToolTip(import_tip)
        self.import_button.setStatusTip(import_tip)
        self.use_custom_weights.setText(tr("prefs.use_custom_weights", language))
        self.export_include_metrics.setText(tr("prefs.export_metrics", language))
        self.export_include_explanation.setText(
            tr("prefs.export_explanation", language)
        )
        self.export_include_offcuts.setText(tr("prefs.export_offcuts", language))
        self.export_include_piece_labels.setText(tr("prefs.export_labels", language))
        self.export_include_offcut_labels.setText(
            tr("prefs.export_offcut_labels", language)
        )
        self.export_include_panel_dimensions.setText(
            tr("prefs.export_panel_dimensions", language)
        )
        self.export_include_plan_traceability.setText(
            tr("prefs.export_plan_traceability", language)
        )
        self.export_batch.setText(tr("prefs.export_batch", language))
        self._export_pdf_paper_label.setText(tr("prefs.export_pdf_paper", language))
        self._export_pdf_orientation_label.setText(
            tr("prefs.export_pdf_orientation", language)
        )
        self._export_pdf_scale_label.setText(tr("prefs.export_pdf_scale", language))
        self._export_pdf_margin_label.setText(tr("prefs.export_pdf_margin", language))
        self._export_raster_dpi_label.setText(tr("prefs.export_raster_dpi", language))
        self._export_jpeg_quality_label.setText(
            tr("prefs.export_jpeg_quality", language)
        )
        self._quote_labor_rate_label.setText(tr("prefs.quote_labor_rate", language))
        self._quote_labor_minutes_label.setText(
            tr("prefs.quote_labor_minutes", language)
        )
        labor_tip = tr("tip.prefs_quote_labor", language)
        self.quote_labor_eur_per_hour.setToolTip(labor_tip)
        self.quote_labor_eur_per_hour.setStatusTip(labor_tip)
        self.quote_labor_minutes_per_piece.setToolTip(labor_tip)
        self.quote_labor_minutes_per_piece.setStatusTip(labor_tip)
        for index, key in enumerate(VALID_PDF_PAPERS):
            self.export_pdf_paper.setItemText(
                index, tr(f"export.paper_{key}", language)
            )
        for index, key in enumerate(VALID_PDF_ORIENTATIONS):
            self.export_pdf_orientation.setItemText(
                index, tr(f"export.orientation_{key}", language)
            )
        for index, key in enumerate(VALID_PDF_SCALES):
            self.export_pdf_scale.setItemText(
                index, tr(f"export.scale_{key.replace(':', '_')}", language)
            )

        self._language_label.setText(tr("prefs.language", language))
        self._theme_label.setText(tr("prefs.theme", language))
        self._units_label.setText(tr("prefs.units", language))
        self._grid_size_label.setText(tr("prefs.grid_size", language))
        self._strategy_label.setText(tr("prefs.strategy", language))
        self._weight_material_label.setText(tr("prefs.weight_material", language))
        self._weight_placed_label.setText(tr("prefs.weight_placed", language))
        self._weight_compactness_label.setText(tr("prefs.weight_compactness", language))
        self._weight_rotation_label.setText(tr("prefs.weight_rotation", language))
        self._export_format_label.setText(tr("prefs.export_format", language))
        self._max_solutions_label.setText(tr("prefs.max_solutions", language))
        self._default_kerf_label.setText(tr("prefs.default_kerf", language))
        self.default_kerf_mm.setToolTip(tr("tip.prefs_default_kerf", language))
        self.default_kerf_mm.setStatusTip(tr("tip.prefs_default_kerf", language))
        self._default_material_label.setText(tr("prefs.default_material", language))
        self.default_material.setToolTip(tr("tip.prefs_default_material", language))
        self.default_material.setStatusTip(tr("tip.prefs_default_material", language))

        for index, key in enumerate(VALID_LANGUAGES):
            self.language.setItemText(index, tr(f"language.{key}", language))
        for index, key in enumerate(VALID_THEMES):
            self.theme.setItemText(index, tr(f"theme.{key}", language))
        for index, key in enumerate(VALID_UNITS):
            self.units.setItemText(index, tr(f"units.{key}", language))
        for index, key in enumerate(VALID_STRATEGIES):
            self.strategy.setItemText(index, tr(f"strategy.{key}", language))

        restore = self._buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults)
        if restore is not None:
            restore.setText(tr("prefs.restore_defaults", language))
            restore_tip = tr("tip.restore_defaults", language)
            restore.setToolTip(restore_tip)
            restore.setStatusTip(restore_tip)

    def _on_language_changed(self, _index: int) -> None:
        self._retranslate()

    @staticmethod
    def _weight_spin() -> QDoubleSpinBox:
        spin = QDoubleSpinBox()
        spin.setRange(0.0, 100.0)
        spin.setDecimals(1)
        spin.setSingleStep(1.0)
        return spin

    def _apply_weights_to_spins(self, weights: WeightPreferences) -> None:
        self.material_utilization.setValue(weights.material_utilization)
        self.placed_boards.setValue(weights.placed_boards)
        self.compactness.setValue(weights.compactness)
        self.rotation_penalty.setValue(weights.rotation_penalty)

    def _on_strategy_changed(self, _index: int) -> None:
        if self.use_custom_weights.isChecked():
            return
        strategy = strategy_by_name(self.strategy.currentData())
        self._apply_weights_to_spins(
            WeightPreferences.from_scoring_weights(strategy.weights)
        )

    def _on_custom_weights_toggled(self, checked: bool) -> None:
        for spin in (
            self.material_utilization,
            self.placed_boards,
            self.compactness,
            self.rotation_penalty,
        ):
            spin.setEnabled(checked)
        if not checked:
            self._on_strategy_changed(self.strategy.currentIndex())

    def _restore_defaults(self) -> None:
        self.language.setCurrentIndex(self.language.findData(DEFAULT_LANGUAGE))
        self.theme.setCurrentIndex(self.theme.findData(DEFAULT_THEME))
        self.units.setCurrentIndex(self.units.findData(DEFAULT_UNITS))
        self.show_grid.setChecked(True)
        self.grid_size_mm.setValue(DEFAULT_GRID_SIZE_MM)
        self.strategy.setCurrentIndex(self.strategy.findData("material"))
        self.use_custom_weights.setChecked(False)
        self.export_format.setCurrentIndex(self.export_format.findData("svg"))
        self.export_include_metrics.setChecked(True)
        self.export_include_explanation.setChecked(True)
        self.export_include_offcuts.setChecked(True)
        self.export_include_piece_labels.setChecked(True)
        self.export_include_offcut_labels.setChecked(True)
        self.export_include_panel_dimensions.setChecked(True)
        self.export_include_plan_traceability.setChecked(True)
        self.export_batch.setChecked(False)
        paper_index = self.export_pdf_paper.findData(DEFAULT_PDF_PAPER)
        self.export_pdf_paper.setCurrentIndex(paper_index if paper_index >= 0 else 0)
        orientation_index = self.export_pdf_orientation.findData(
            DEFAULT_PDF_ORIENTATION
        )
        self.export_pdf_orientation.setCurrentIndex(
            orientation_index if orientation_index >= 0 else 0
        )
        scale_index = self.export_pdf_scale.findData(DEFAULT_PDF_SCALE)
        self.export_pdf_scale.setCurrentIndex(scale_index if scale_index >= 0 else 0)
        self.export_pdf_margin_mm.setValue(DEFAULT_PDF_MARGIN_MM)
        self.export_raster_dpi.setValue(DEFAULT_RASTER_DPI)
        self.export_jpeg_quality.setValue(DEFAULT_JPEG_QUALITY)
        self.quote_labor_eur_per_hour.setValue(DEFAULT_LABOR_EUR_PER_HOUR)
        self.quote_labor_minutes_per_piece.setValue(DEFAULT_LABOR_MINUTES_PER_PIECE)
        self.max_solutions.setValue(DEFAULT_MAX_SOLUTIONS)
        self.default_kerf_mm.setValue(DEFAULT_KERF_MM)
        self.default_material.setEditText(DEFAULT_MATERIAL)
        self._on_strategy_changed(self.strategy.currentIndex())
        self._retranslate()

    def _open_material_catalog(self) -> None:
        if self._catalog is None:
            return
        from studio.dialogs.material_catalog_dialog import MaterialCatalogDialog

        dialog = MaterialCatalogDialog(
            self._catalog,
            self,
            language=self._language,
        )
        dialog.exec()

    def _open_config_folder(self) -> None:
        folder = default_preferences_path().parent
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder.resolve())))

    def _suggested_pack_path(self, default_filename: str = "") -> str:
        directory = self._pack_directory.strip()
        if directory and Path(directory).is_dir():
            return (
                str(Path(directory) / default_filename)
                if default_filename
                else directory
            )
        return default_filename

    def _remember_pack_directory(self, path: str | Path) -> None:
        folder = str(Path(path).resolve().parent)
        self._pack_directory = folder
        self._preferences = replace(
            self._preferences, last_preferences_directory=folder
        )
        if self._on_pack_directory is not None:
            self._on_pack_directory(path)

    def _export_pack(self) -> None:
        path, _ = QFileDialog.getSaveFileName(
            self,
            tr("prefs.share_export_title", self._language),
            self._suggested_pack_path("boardcomposer-preferences.json"),
            tr("prefs.share_filter", self._language),
        )
        if not path:
            return
        if not path.lower().endswith(".json"):
            path = f"{path}.json"
        try:
            export_preferences_pack(self.preferences(), path)
        except OSError as exc:
            QMessageBox.warning(
                self,
                tr("prefs.share_export_title", self._language),
                tr("prefs.share_error", self._language, error=str(exc)),
            )
            return
        self._remember_pack_directory(path)
        QMessageBox.information(
            self,
            tr("prefs.share_export_title", self._language),
            tr("prefs.share_export_done", self._language),
        )

    def _import_pack(self) -> None:
        path, _ = QFileDialog.getOpenFileName(
            self,
            tr("prefs.share_import_title", self._language),
            self._suggested_pack_path(),
            tr("prefs.share_filter", self._language),
        )
        if not path:
            return
        choice = QMessageBox.question(
            self,
            tr("prefs.share_import_title", self._language),
            tr("prefs.share_import_mode", self._language),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
            | QMessageBox.StandardButton.Cancel,
        )
        if choice == QMessageBox.StandardButton.Cancel:
            return
        mode = "replace" if choice == QMessageBox.StandardButton.No else "merge"
        try:
            imported = import_preferences_pack(self.preferences(), path, mode=mode)
        except (OSError, ValueError) as exc:
            QMessageBox.warning(
                self,
                tr("prefs.share_import_title", self._language),
                tr("prefs.share_error", self._language, error=str(exc)),
            )
            return
        self._remember_pack_directory(path)
        self._apply_imported_preferences(imported)
        QMessageBox.information(
            self,
            tr("prefs.share_import_title", self._language),
            tr(
                "prefs.share_import_done",
                self._language,
                mode=tr(
                    "prefs.share_mode_replace"
                    if mode == "replace"
                    else "prefs.share_mode_merge",
                    self._language,
                ),
            ),
        )

    def _apply_imported_preferences(self, preferences: StudioPreferences) -> None:
        """Load imported shop settings into widgets; OK still persists."""
        language_index = self.language.findData(preferences.language)
        self.language.setCurrentIndex(language_index if language_index >= 0 else 0)
        theme_index = self.theme.findData(preferences.theme)
        self.theme.setCurrentIndex(theme_index if theme_index >= 0 else 0)
        units_index = self.units.findData(preferences.units)
        self.units.setCurrentIndex(units_index if units_index >= 0 else 0)
        self.show_grid.setChecked(preferences.show_grid)
        self.grid_size_mm.setValue(preferences.grid_size_mm)
        strategy_index = self.strategy.findData(preferences.strategy_name)
        self.strategy.setCurrentIndex(strategy_index if strategy_index >= 0 else 0)
        self.use_custom_weights.setChecked(preferences.use_custom_weights)
        self._apply_weights_to_spins(preferences.weights)
        export_index = self.export_format.findData(preferences.export_format)
        self.export_format.setCurrentIndex(export_index if export_index >= 0 else 0)
        self.export_include_metrics.setChecked(preferences.export_include_metrics)
        self.export_include_explanation.setChecked(
            preferences.export_include_explanation
        )
        self.export_include_offcuts.setChecked(preferences.export_include_offcuts)
        self.export_include_piece_labels.setChecked(
            preferences.export_include_piece_labels
        )
        self.export_include_offcut_labels.setChecked(
            preferences.export_include_offcut_labels
        )
        self.export_include_panel_dimensions.setChecked(
            preferences.export_include_panel_dimensions
        )
        self.export_include_plan_traceability.setChecked(
            preferences.export_include_plan_traceability
        )
        self.export_batch.setChecked(preferences.export_batch)
        paper_index = self.export_pdf_paper.findData(preferences.export_pdf_paper)
        self.export_pdf_paper.setCurrentIndex(paper_index if paper_index >= 0 else 0)
        orientation_index = self.export_pdf_orientation.findData(
            preferences.export_pdf_orientation
        )
        self.export_pdf_orientation.setCurrentIndex(
            orientation_index if orientation_index >= 0 else 0
        )
        scale_index = self.export_pdf_scale.findData(preferences.export_pdf_scale)
        self.export_pdf_scale.setCurrentIndex(scale_index if scale_index >= 0 else 0)
        self.export_pdf_margin_mm.setValue(preferences.export_pdf_margin_mm)
        self.export_raster_dpi.setValue(preferences.export_raster_dpi)
        self.export_jpeg_quality.setValue(preferences.export_jpeg_quality)
        self.quote_labor_eur_per_hour.setValue(preferences.quote_labor_eur_per_hour)
        self.quote_labor_minutes_per_piece.setValue(
            preferences.quote_labor_minutes_per_piece
        )
        self.max_solutions.setValue(preferences.max_solutions)
        self.default_kerf_mm.setValue(preferences.default_kerf_mm)
        self.default_material.setEditText(preferences.default_material)
        self._on_custom_weights_toggled(preferences.use_custom_weights)
        self._retranslate()

    def preferences(self) -> StudioPreferences:
        return replace(
            self._preferences,
            strategy_name=self.strategy.currentData() or "material",
            use_custom_weights=self.use_custom_weights.isChecked(),
            weights=WeightPreferences(
                material_utilization=self.material_utilization.value(),
                placed_boards=self.placed_boards.value(),
                compactness=self.compactness.value(),
                rotation_penalty=self.rotation_penalty.value(),
            ),
            theme=self.theme.currentData() or DEFAULT_THEME,
            show_grid=self.show_grid.isChecked(),
            grid_size_mm=self.grid_size_mm.value(),
            language=self.language.currentData() or DEFAULT_LANGUAGE,
            units=self.units.currentData() or DEFAULT_UNITS,
            export_format=self.export_format.currentData() or "svg",
            export_include_metrics=self.export_include_metrics.isChecked(),
            export_include_explanation=self.export_include_explanation.isChecked(),
            export_include_offcuts=self.export_include_offcuts.isChecked(),
            export_include_piece_labels=(self.export_include_piece_labels.isChecked()),
            export_include_offcut_labels=(
                self.export_include_offcut_labels.isChecked()
            ),
            export_include_panel_dimensions=(
                self.export_include_panel_dimensions.isChecked()
            ),
            export_include_plan_traceability=(
                self.export_include_plan_traceability.isChecked()
            ),
            export_batch=self.export_batch.isChecked(),
            export_pdf_paper=self.export_pdf_paper.currentData() or DEFAULT_PDF_PAPER,
            export_pdf_orientation=self.export_pdf_orientation.currentData()
            or DEFAULT_PDF_ORIENTATION,
            export_pdf_scale=self.export_pdf_scale.currentData() or DEFAULT_PDF_SCALE,
            export_pdf_margin_mm=self.export_pdf_margin_mm.value(),
            export_raster_dpi=self.export_raster_dpi.value(),
            export_jpeg_quality=self.export_jpeg_quality.value(),
            quote_labor_eur_per_hour=self.quote_labor_eur_per_hour.value(),
            quote_labor_minutes_per_piece=self.quote_labor_minutes_per_piece.value(),
            max_solutions=self.max_solutions.value(),
            default_kerf_mm=self.default_kerf_mm.value(),
            default_material=self.default_material.currentText().strip()
            or DEFAULT_MATERIAL,
        )
