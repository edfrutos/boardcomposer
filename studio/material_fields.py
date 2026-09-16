"""Shared material combo wiring for board/piece dialogs (IDE-0028)."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QDoubleSpinBox

from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.material_catalog import (
    MaterialCatalog,
    default_catalog,
    format_catalog_size,
    normalize_size,
    normalize_thickness,
)
from studio.units import display_to_mm, mm_to_display


def fill_material_combo(
    combo: QComboBox,
    catalog: MaterialCatalog | None,
    current: str,
) -> None:
    """Populate an editable combo with catalog names and the current value."""
    source = catalog if catalog is not None else default_catalog()
    combo.setEditable(True)
    combo.clear()
    names = list(source.names())
    cleaned = current.strip()
    if cleaned and all(name.casefold() != cleaned.casefold() for name in names):
        names.append(cleaned)
    for name in names:
        combo.addItem(name)
    combo.setEditText(cleaned or (names[0] if names else ""))


def bind_thickness_suggestions(
    combo: QComboBox,
    spin: QDoubleSpinBox,
    catalog: MaterialCatalog | None,
    *,
    units: str,
    language: str = DEFAULT_LANGUAGE,
) -> None:
    """Hint typical thicknesses; jumping only when the user picks a name."""
    source = catalog if catalog is not None else default_catalog()

    def _refresh_tips() -> None:
        name = combo.currentText()
        thicknesses = source.thicknesses_for(name)
        if thicknesses:
            labels = ", ".join(
                str(int(value) if value == int(value) else value)
                for value in thicknesses
            )
            tip = tr("tip.catalog_thickness", language, thicknesses=labels)
        else:
            tip = tr("tip.catalog_thickness_custom", language)
        spin.setToolTip(tip)
        spin.setStatusTip(tip)
        combo.setToolTip(tr("tip.catalog_material", language))

    def _on_material_selected(index: int) -> None:
        _refresh_tips()
        if index < 0:
            return
        thicknesses = source.thicknesses_for(combo.currentText())
        current_mm = normalize_thickness(display_to_mm(spin.value(), units))
        if thicknesses and current_mm not in thicknesses:
            spin.setValue(mm_to_display(thicknesses[0], units))

    combo.currentTextChanged.connect(lambda _text: _refresh_tips())
    combo.currentIndexChanged.connect(_on_material_selected)
    _refresh_tips()


def bind_board_size_suggestions(
    combo: QComboBox,
    length_spin: QDoubleSpinBox,
    width_spin: QDoubleSpinBox,
    size_combo: QComboBox,
    catalog: MaterialCatalog | None,
    *,
    units: str,
    language: str = DEFAULT_LANGUAGE,
    suggest_catalog_size: bool = False,
) -> None:
    """Fill typical sheet sizes; jump L×W only on a catalog name pick."""
    source = catalog if catalog is not None else default_catalog()

    def _current_size() -> tuple[float, float] | None:
        return normalize_size(
            display_to_mm(length_spin.value(), units),
            display_to_mm(width_spin.value(), units),
        )

    def _apply_size(pair: tuple[float, float]) -> None:
        length_spin.setValue(mm_to_display(pair[0], units))
        width_spin.setValue(mm_to_display(pair[1], units))

    def _reload_size_combo(*, apply_if_unknown: bool) -> None:
        sizes = source.sizes_for(combo.currentText())
        current = _current_size()
        size_combo.blockSignals(True)
        size_combo.clear()
        size_combo.addItem(tr("form.size_custom", language), None)
        selected = 0
        for pair in sizes:
            size_combo.addItem(format_catalog_size(*pair), pair)
            if current == pair:
                selected = size_combo.count() - 1
        if apply_if_unknown and sizes and selected == 0:
            _apply_size(sizes[0])
            selected = 1
        size_combo.setCurrentIndex(selected)
        size_combo.blockSignals(False)
        size_combo.setEnabled(bool(sizes))
        if sizes:
            labels = ", ".join(format_catalog_size(*pair) for pair in sizes)
            tip = tr("tip.catalog_size", language, sizes=labels)
        else:
            tip = tr("tip.catalog_size_custom", language)
        size_combo.setToolTip(tip)
        size_combo.setStatusTip(tip)
        length_spin.setToolTip(tip)
        length_spin.setStatusTip(tip)
        width_spin.setToolTip(tip)
        width_spin.setStatusTip(tip)

    def _on_material_selected(index: int) -> None:
        if index < 0:
            _reload_size_combo(apply_if_unknown=False)
            return
        _reload_size_combo(apply_if_unknown=True)

    def _on_size_selected(index: int) -> None:
        pair = size_combo.itemData(index)
        if pair is None:
            return
        _apply_size(pair)

    combo.currentIndexChanged.connect(_on_material_selected)
    combo.currentTextChanged.connect(
        lambda _text: _reload_size_combo(apply_if_unknown=False)
    )
    size_combo.currentIndexChanged.connect(_on_size_selected)
    _reload_size_combo(apply_if_unknown=suggest_catalog_size)
