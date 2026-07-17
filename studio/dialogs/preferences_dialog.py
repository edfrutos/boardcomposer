"""Preferences dialog for Studio appearance, workspace and scoring (SCR-006)."""

from __future__ import annotations

from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)

from boardcomposer.solver.strategies import strategy_by_name
from studio.preferences import (
    DEFAULT_GRID_SIZE_MM,
    MAX_GRID_SIZE_MM,
    MIN_GRID_SIZE_MM,
    VALID_STRATEGIES,
    StudioPreferences,
    WeightPreferences,
)
from studio.theme import DEFAULT_THEME, VALID_THEMES

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

        self.setWindowTitle("Preferencias")
        self.setMinimumWidth(440)
        self._preferences = preferences

        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                "Estas opciones se aplican a todos los proyectos y no forman "
                "parte del fichero `.bcproj`."
            )
        )

        general = QGroupBox("General")
        general_form = QFormLayout(general)
        self.theme = QComboBox()
        for key in VALID_THEMES:
            self.theme.addItem(_THEME_LABELS[key], key)
        theme_index = self.theme.findData(preferences.theme)
        self.theme.setCurrentIndex(theme_index if theme_index >= 0 else 0)
        general_form.addRow("Tema:", self.theme)
        layout.addWidget(general)

        workspace = QGroupBox("Workspace")
        workspace_form = QFormLayout(workspace)
        self.show_grid = QCheckBox("Mostrar cuadrícula")
        self.show_grid.setChecked(preferences.show_grid)
        workspace_form.addRow("", self.show_grid)
        self.grid_size_mm = QSpinBox()
        self.grid_size_mm.setRange(MIN_GRID_SIZE_MM, MAX_GRID_SIZE_MM)
        self.grid_size_mm.setSuffix(" mm")
        self.grid_size_mm.setSingleStep(10)
        self.grid_size_mm.setValue(preferences.grid_size_mm)
        workspace_form.addRow("Tamaño de cuadrícula:", self.grid_size_mm)
        layout.addWidget(workspace)

        algorithms = QGroupBox("Algoritmos")
        form = QFormLayout(algorithms)

        self.strategy = QComboBox()
        for key in VALID_STRATEGIES:
            self.strategy.addItem(_STRATEGY_LABELS[key], key)
        index = self.strategy.findData(preferences.strategy_name)
        self.strategy.setCurrentIndex(index if index >= 0 else 0)
        self.strategy.currentIndexChanged.connect(self._on_strategy_changed)
        form.addRow("Estrategia:", self.strategy)

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
        layout.addWidget(algorithms)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.RestoreDefaults
            | QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.StandardButton.RestoreDefaults).clicked.connect(
            self._restore_defaults
        )
        layout.addWidget(buttons)

        self._apply_weights_to_spins(preferences.weights)
        self._on_custom_weights_toggled(preferences.use_custom_weights)

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
        self.theme.setCurrentIndex(self.theme.findData(DEFAULT_THEME))
        self.show_grid.setChecked(True)
        self.grid_size_mm.setValue(DEFAULT_GRID_SIZE_MM)
        self.strategy.setCurrentIndex(self.strategy.findData("material"))
        self.use_custom_weights.setChecked(False)
        self._on_strategy_changed(self.strategy.currentIndex())

    def preferences(self) -> StudioPreferences:
        return StudioPreferences(
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
        )
