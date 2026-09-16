"""Edit the user-level material / thickness catalog (IDE-0028)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from studio.dialogs.dialog_chrome import (
    polish_dialog_button_box,
    polish_secondary_button,
)
from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.material_catalog import (
    CatalogMaterial,
    MaterialCatalogManager,
    format_catalog_size,
)


def _parse_thicknesses(text: str) -> tuple[float, ...]:
    values: list[float] = []
    for chunk in text.replace(";", ",").split(","):
        cleaned = chunk.strip().replace(",", ".")
        if not cleaned:
            continue
        try:
            values.append(float(cleaned))
        except ValueError:
            continue
    return tuple(values)


def _parse_sizes(text: str) -> tuple[tuple[float, float], ...]:
    pairs: list[tuple[float, float]] = []
    for chunk in text.replace(";", ",").split(","):
        cleaned = chunk.strip().lower().replace("×", "x").replace("*", "x")
        if "x" not in cleaned:
            continue
        left, right = cleaned.split("x", 1)
        try:
            pairs.append(
                (
                    float(left.strip().replace(",", ".")),
                    float(right.strip().replace(",", ".")),
                )
            )
        except ValueError:
            continue
    return tuple(pairs)


class MaterialCatalogDialog(QDialog):
    """Add, update or remove typed materials used across projects."""

    def __init__(
        self,
        manager: MaterialCatalogManager,
        parent=None,
        *,
        language: str = DEFAULT_LANGUAGE,
    ) -> None:
        super().__init__(parent)
        self._manager = manager
        self._language = language
        self.setMinimumWidth(460)

        self._intro = QLabel()
        self._intro.setWordWrap(True)
        self.list = QListWidget()
        self.list.currentRowChanged.connect(self._on_row_changed)

        self.name = QLineEdit()
        self.thicknesses = QLineEdit()
        self.sizes = QLineEdit()
        self.price = QDoubleSpinBox()
        self.price.setRange(0.0, 1_000_000.0)
        self.price.setDecimals(2)
        self.price.setSingleStep(1.0)

        form = QFormLayout()
        self._name_label = QLabel()
        self._thickness_label = QLabel()
        self._sizes_label = QLabel()
        self._price_label = QLabel()
        form.addRow(self._name_label, self.name)
        form.addRow(self._thickness_label, self.thicknesses)
        form.addRow(self._sizes_label, self.sizes)
        form.addRow(self._price_label, self.price)

        buttons_row = QHBoxLayout()
        self.add_button = polish_secondary_button(QPushButton())
        self.update_button = polish_secondary_button(QPushButton())
        self.remove_button = polish_secondary_button(QPushButton())
        self.restore_button = polish_secondary_button(QPushButton())
        self.add_button.clicked.connect(self._add)
        self.update_button.clicked.connect(self._update_selected)
        self.remove_button.clicked.connect(self._remove)
        self.restore_button.clicked.connect(self._restore)
        buttons_row.addWidget(self.add_button)
        buttons_row.addWidget(self.update_button)
        buttons_row.addWidget(self.remove_button)
        buttons_row.addWidget(self.restore_button)

        box = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        polish_dialog_button_box(box)
        box.rejected.connect(self.accept)
        box.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self._intro)
        layout.addWidget(self.list)
        layout.addLayout(form)
        layout.addLayout(buttons_row)
        layout.addWidget(box)

        self._retranslate()
        self._reload_list()

    def _retranslate(self) -> None:
        language = self._language
        self.setWindowTitle(tr("catalog.title", language))
        self._intro.setText(tr("catalog.intro", language))
        self._name_label.setText(tr("catalog.name", language))
        self._thickness_label.setText(tr("catalog.thicknesses", language))
        self._sizes_label.setText(tr("catalog.sizes", language))
        self._price_label.setText(tr("catalog.price", language))
        self.thicknesses.setPlaceholderText(tr("catalog.thickness_hint", language))
        self.sizes.setPlaceholderText(tr("catalog.sizes_hint", language))
        self.sizes.setToolTip(tr("tip.catalog_sizes_edit", language))
        self.sizes.setStatusTip(tr("tip.catalog_sizes_edit", language))
        self.price.setSuffix(tr("catalog.price_suffix", language))
        self.price.setToolTip(tr("tip.catalog_price", language))
        self.price.setStatusTip(tr("tip.catalog_price", language))
        self.add_button.setText(tr("catalog.add", language))
        self.update_button.setText(tr("catalog.update", language))
        self.remove_button.setText(tr("catalog.remove", language))
        self.restore_button.setText(tr("catalog.restore", language))

    def _reload_list(self, select: str | None = None) -> None:
        self.list.clear()
        wanted = (select or self.name.text()).strip().casefold()
        selected_row = 0
        for index, item in enumerate(self._manager.catalog.materials):
            thicknesses = ", ".join(
                str(int(value) if value == int(value) else value)
                for value in item.thicknesses_mm
            )
            label = item.name if not thicknesses else f"{item.name} — {thicknesses} mm"
            if item.sizes_mm:
                sheets = ", ".join(format_catalog_size(*pair) for pair in item.sizes_mm)
                label = f"{label} · {sheets}"
            if item.price_per_m2 > 0:
                label = f"{label} · {item.price_per_m2:.2f} €/m²"
            row = QListWidgetItem(label)
            row.setData(int(Qt.ItemDataRole.UserRole), item.name)
            self.list.addItem(row)
            if item.name.casefold() == wanted:
                selected_row = index
        if self.list.count():
            self.list.setCurrentRow(selected_row)

    def _on_row_changed(self, row: int) -> None:
        if row < 0 or row >= len(self._manager.catalog.materials):
            return
        item = self._manager.catalog.materials[row]
        self.name.setText(item.name)
        self.thicknesses.setText(
            ", ".join(
                str(int(value) if value == int(value) else value)
                for value in item.thicknesses_mm
            )
        )
        self.sizes.setText(
            ", ".join(format_catalog_size(*pair) for pair in item.sizes_mm)
        )
        self.price.setValue(item.price_per_m2)

    def _current_material(self) -> CatalogMaterial | None:
        name = self.name.text().strip()
        if not name:
            return None
        return CatalogMaterial(
            name=name,
            thicknesses_mm=_parse_thicknesses(self.thicknesses.text()),
            price_per_m2=self.price.value(),
            sizes_mm=_parse_sizes(self.sizes.text()),
        )

    def _add(self) -> None:
        material = self._current_material()
        if material is None:
            return
        materials = list(self._manager.catalog.materials)
        existing = self._manager.catalog.find(material.name)
        if existing is not None:
            materials.remove(existing)
        materials.append(material)
        self._manager.replace_all(materials)
        self._reload_list(select=material.name)

    def _update_selected(self) -> None:
        self._add()

    def _remove(self) -> None:
        row = self.list.currentRow()
        materials = list(self._manager.catalog.materials)
        if 0 <= row < len(materials):
            del materials[row]
            self._manager.replace_all(materials)
            self.name.clear()
            self.thicknesses.clear()
            self.sizes.clear()
            self.price.setValue(0)
            self._reload_list()

    def _restore(self) -> None:
        self._manager.restore_defaults()
        self._reload_list()
