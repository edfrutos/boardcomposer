"""Shared material combo wiring for board/piece dialogs (IDE-0028)."""

from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QDoubleSpinBox

from studio.i18n import DEFAULT_LANGUAGE, tr
from studio.material_catalog import (
    MaterialCatalog,
    default_catalog,
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
