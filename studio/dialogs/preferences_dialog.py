"""Preferences dialog for Studio appearance, workspace and scoring (SCR-006)."""

from __future__ import annotations

from dataclasses import replace

from PySide6.QtCore import QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
)

from boardcomposer.solver.strategies import strategy_by_name
from studio.dialogs.dialog_chrome import polish_dialog_button_box
from studio.export_options import VALID_EXPORT_FORMATS, format_label
from studio.i18n import DEFAULT_LANGUAGE, VALID_LANGUAGES, tr
from studio.preferences import (
    DEFAULT_GRID_SIZE_MM,
    DEFAULT_MAX_SOLUTIONS,
    MAX_GRID_SIZE_MM,
    MAX_MAX_SOLUTIONS,
    MIN_GRID_SIZE_MM,
    MIN_MAX_SOLUTIONS,
    VALID_STRATEGIES,
    StudioPreferences,
    WeightPreferences,
    default_preferences_path,
)
from studio.theme import DEFAULT_THEME, VALID_THEMES
from studio.units import DEFAULT_UNITS, VALID_UNITS

_STRATEGY_LABELS = {
    "balanced": "Equilibrada",
    "material": "Material primero",
    "compact": "Compacta primero",
    "exact": "Exacta (MaxRects + CP-SAT)",
}

_THEME_LABELS = {
    "system": "Sistema",
    "light": "Claro",
    "dark": "Oscuro",
}


class PreferencesDialog(QDialog):
    """Edit user-level Studio preferences."""

    def __init__(self, preferences: StudioPreferences, parent=None) -> None:
        super().__init__(parent)

        self._preferences = preferences
        self._language = preferences.language
        self.setMinimumWidth(460)

        layout = QVBoxLayout(self)
        self._intro = QLabel()
        layout.addWidget(self._intro)

        self.general = QGroupBox()
        general_form = QFormLayout(self.general)

        self.language = QComboBox()
        for key in VALID_LANGUAGES:
            self.language.addItem(tr(f"language.{key}", preferences.language), key)
        language_index = self.language.findData(preferences.language)
        self.language.setCurrentIndex(language_index if language_index >= 0 else 0)
        self.language.currentIndexChanged.connect(self._on_language_changed)
        general_form.addRow(tr("prefs.language", preferences.language), self.language)

        self.theme = QComboBox()
        for key in VALID_THEMES:
            self.theme.addItem(_THEME_LABELS[key], key)
        theme_index = self.theme.findData(preferences.theme)
        self.theme.setCurrentIndex(theme_index if theme_index >= 0 else 0)
        general_form.addRow(tr("prefs.theme", preferences.language), self.theme)

        self.units = QComboBox()
        for key in VALID_UNITS:
            self.units.addItem(tr(f"units.{key}", preferences.language), key)
        units_index = self.units.findData(preferences.units)
        self.units.setCurrentIndex(units_index if units_index >= 0 else 0)
        general_form.addRow(tr("prefs.units", preferences.language), self.units)
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
        workspace_form.addRow(
            tr("prefs.grid_size", preferences.language), self.grid_size_mm
        )
        layout.addWidget(self.workspace)

        self.algorithms = QGroupBox()
        form = QFormLayout(self.algorithms)

        self.strategy = QComboBox()
        for key in VALID_STRATEGIES:
            self.strategy.addItem(_STRATEGY_LABELS[key], key)
        index = self.strategy.findData(preferences.strategy_name)
        self.strategy.setCurrentIndex(index if index >= 0 else 0)
        self.strategy.currentIndexChanged.connect(self._on_strategy_changed)
        form.addRow(tr("prefs.strategy", preferences.language), self.strategy)

        self.use_custom_weights = QCheckBox("Usar pesos personalizados")
        self.use_custom_weights.setChecked(preferences.use_custom_weights)
        self.use_custom_weights.toggled.connect(self._on_custom_weights_toggled)
        form.addRow("", self.use_custom_weights)

        self.material_utilization = self._weight_spin()
        self.placed_boards = self._weight_spin()
        self.compactness = self._weight_spin()
        self.rotation_penalty = self._weight_spin()

        form.addRow("Aprovechamiento de material:", self.material_utilization)
        form.addRow("Piezas colocadas:", self.placed_boards)
        form.addRow("Compacidad:", self.compactness)
        form.addRow("Penalización por rotación:", self.rotation_penalty)
        layout.addWidget(self.algorithms)

        self.export_group = QGroupBox()
        export_form = QFormLayout(self.export_group)
        self.export_format = QComboBox()
        for key in VALID_EXPORT_FORMATS:
            self.export_format.addItem(format_label(key), key)
        export_index = self.export_format.findData(preferences.export_format)
        self.export_format.setCurrentIndex(export_index if export_index >= 0 else 0)
        export_form.addRow(
            tr("prefs.export_format", preferences.language), self.export_format
        )
        self.export_include_metrics = QCheckBox("Incluir métricas (JSON)")
        self.export_include_metrics.setChecked(preferences.export_include_metrics)
        export_form.addRow("", self.export_include_metrics)
        self.export_include_explanation = QCheckBox("Incluir explicación (JSON)")
        self.export_include_explanation.setChecked(
            preferences.export_include_explanation
        )
        export_form.addRow("", self.export_include_explanation)
        self.export_include_offcuts = QCheckBox("Incluir retales")
        self.export_include_offcuts.setChecked(preferences.export_include_offcuts)
        export_form.addRow("", self.export_include_offcuts)
        layout.addWidget(self.export_group)

        self.advanced = QGroupBox()
        advanced_form = QFormLayout(self.advanced)
        self.max_solutions = QSpinBox()
        self.max_solutions.setRange(MIN_MAX_SOLUTIONS, MAX_MAX_SOLUTIONS)
        self.max_solutions.setValue(preferences.max_solutions)
        advanced_form.addRow(
            tr("prefs.max_solutions", preferences.language), self.max_solutions
        )
        self.open_config_folder = QPushButton(
            tr("prefs.open_config_folder", preferences.language)
        )
        self.open_config_folder.clicked.connect(self._open_config_folder)
        advanced_form.addRow("", self.open_config_folder)
        layout.addWidget(self.advanced)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.RestoreDefaults
            | QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        polish_dialog_button_box(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self._restore_defaults
        )
        layout.addWidget(buttons)

        self._apply_weights_to_spins(preferences.weights)
        self._on_custom_weights_toggled(preferences.use_custom_weights)
        self._retranslate()

    def _retranslate(self) -> None:
        language = self.language.currentData() or DEFAULT_LANGUAGE
        self._language = language
        self.setWindowTitle(tr("prefs.title", language))
        self._intro.setText(
            "Estas opciones se aplican a todos los proyectos y no forman "
            "parte del fichero `.bcproj`."
            if language == "es"
            else "These options apply to all projects and are not part of "
            "the `.bcproj` file."
        )
        self.general.setTitle(tr("prefs.general", language))
        self.workspace.setTitle(tr("prefs.workspace", language))
        self.algorithms.setTitle(tr("prefs.algorithms", language))
        self.export_group.setTitle(tr("prefs.export", language))
        self.advanced.setTitle(tr("prefs.advanced", language))
        self.show_grid.setText(tr("prefs.show_grid", language))
        self.open_config_folder.setText(tr("prefs.open_config_folder", language))

        for index, key in enumerate(VALID_LANGUAGES):
            self.language.setItemText(index, tr(f"language.{key}", language))
        for index, key in enumerate(VALID_UNITS):
            self.units.setItemText(index, tr(f"units.{key}", language))

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
        self.max_solutions.setValue(DEFAULT_MAX_SOLUTIONS)
        self._on_strategy_changed(self.strategy.currentIndex())
        self._retranslate()

    def _open_config_folder(self) -> None:
        folder = default_preferences_path().parent
        folder.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(folder.resolve())))

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
            max_solutions=self.max_solutions.value(),
        )
