"""User-level material / thickness catalog (IDE-0028)."""

from PySide6.QtWidgets import QComboBox

from studio.dialogs.material_catalog_dialog import MaterialCatalogDialog
from studio.dialogs.new_board_dialog import NewBoardDialog
from studio.dialogs.new_piece_dialog import NewPieceDialog
from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.i18n import tr
from studio.keyboard_shortcuts import STUDIO_SHORTCUTS
from studio.main_window import MainWindow
from studio.material_catalog import (
    CatalogMaterial,
    MaterialCatalog,
    MaterialCatalogManager,
    default_catalog,
    normalize_thickness,
)
from studio.models import StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def test_normalize_thickness_rounds_to_tenth():
    assert normalize_thickness(19.0000001) == 19.0
    assert normalize_thickness(19.06) == 19.1


def test_default_catalog_includes_workshop_stock():
    names = default_catalog().names()
    assert names == ["Contrachapado", "Demo", "MDF", "Melamina blanca"]
    assert "Melamina blanca" in names
    assert "MDF" in names
    assert "Contrachapado" in names
    assert default_catalog().thicknesses_for("Melamina blanca") == (16.0, 19.0, 22.0)


def test_remember_adds_name_and_extra_thickness(tmp_path):
    path = tmp_path / "material_catalog.json"
    manager = MaterialCatalogManager(path=path)
    assert manager.remember("Haya", 18)
    assert manager.remember("Haya", 22)
    assert not manager.remember("Haya", 18)

    reloaded = MaterialCatalogManager(path=path)
    found = reloaded.catalog.find("haya")
    assert found is not None
    assert found.name == "Haya"
    assert found.thicknesses_mm == (18.0, 22.0)


def test_empty_and_corrupt_files_fall_back_to_defaults(tmp_path):
    empty = tmp_path / "empty.json"
    empty.write_text('{"version": 1, "materials": []}\n', encoding="utf-8")
    assert (
        MaterialCatalogManager(path=empty).catalog.names() == default_catalog().names()
    )

    corrupt = tmp_path / "corrupt.json"
    corrupt.write_text("{not json", encoding="utf-8")
    assert MaterialCatalogManager(path=corrupt).catalog.names() == (
        default_catalog().names()
    )


def test_restore_defaults_rewrites_file(tmp_path):
    path = tmp_path / "material_catalog.json"
    manager = MaterialCatalogManager(path=path)
    manager.replace_all([CatalogMaterial("Haya", (18.0,))])
    manager.restore_defaults()
    assert manager.catalog.names() == default_catalog().names()
    reloaded = MaterialCatalogManager(path=path)
    assert reloaded.catalog.names() == default_catalog().names()


def test_new_board_dialog_keeps_custom_thickness_on_open(qapp):
    del qapp
    catalog = MaterialCatalog(
        materials=[CatalogMaterial("Melamina blanca", (16.0, 19.0, 22.0))]
    )
    dialog = NewBoardDialog(
        thickness_mm=18,
        material="Melamina blanca",
        catalog=catalog,
    )
    assert isinstance(dialog.material, QComboBox)
    assert dialog.material.isEditable()
    assert dialog.material.currentText() == "Melamina blanca"
    assert dialog.thickness.value() == 18
    assert dialog.board_data()["material"] == "Melamina blanca"
    assert dialog.board_data()["thickness_mm"] == 18


def test_selecting_catalog_material_fills_first_thickness(qapp):
    del qapp
    dialog = NewPieceDialog(thickness_mm=18, material="Melamina blanca")
    index = dialog.material.findText("MDF")
    assert index >= 0
    dialog.material.setCurrentIndex(index)
    assert dialog.piece_data()["material"] == "MDF"
    assert dialog.piece_data()["thickness_mm"] == 16


def test_price_persists_and_zero_is_omitted(tmp_path):
    path = tmp_path / "material_catalog.json"
    manager = MaterialCatalogManager(path=path)
    manager.replace_all([CatalogMaterial("Haya", (18.0,), price_per_m2=25.5)])
    payload = manager.catalog.to_payload()
    assert payload["materials"][0]["price_per_m2"] == 25.5
    assert manager.catalog.price_for("haya") == 25.5
    assert manager.price_map() == {"haya": 25.5}

    unpriced = CatalogMaterial("MDF", (16.0,))
    assert "price_per_m2" not in unpriced.to_dict()
    assert unpriced.price_per_m2 == 0.0


def test_remember_keeps_existing_price():
    catalog = MaterialCatalog(
        materials=[CatalogMaterial("Haya", (18.0,), price_per_m2=12.5)]
    )
    assert catalog.remember("Haya", 22)
    found = catalog.find("Haya")
    assert found is not None
    assert found.thicknesses_mm == (18.0, 22.0)
    assert found.price_per_m2 == 12.5


def test_catalog_dialog_adds_and_persists(qapp, tmp_path):
    del qapp
    path = tmp_path / "material_catalog.json"
    manager = MaterialCatalogManager(path=path)
    dialog = MaterialCatalogDialog(manager, language="en")
    assert dialog.windowTitle() == "Material catalog"
    assert "€/m²" in dialog._price_label.text()
    dialog.name.setText("Haya")
    dialog.thicknesses.setText("18, 22")
    dialog.price.setValue(25.5)
    dialog._add()
    found = manager.catalog.find("Haya")
    assert found is not None
    assert found.price_per_m2 == 25.5
    reloaded = MaterialCatalogManager(path=path)
    assert reloaded.catalog.thicknesses_for("Haya") == (18.0, 22.0)
    assert reloaded.catalog.price_for("Haya") == 25.5
    assert any(
        "25.50 €/m²" in dialog.list.item(i).text() for i in range(dialog.list.count())
    )


def test_add_board_remembers_custom_material(qapp, tmp_path, monkeypatch):
    del qapp
    import studio.main_window as mw

    path = tmp_path / "material_catalog.json"
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        material_catalog=MaterialCatalogManager(path=path),
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(StudioProject(project_id="PRJ-1", name="Cat"))
    window = MainWindow(services)

    class _AcceptCustom:
        DialogCode = type("DialogCode", (), {"Accepted": 1})()

        def __init__(self, *args, **kwargs):
            del args, kwargs

        def exec(self):
            return self.DialogCode.Accepted

        def board_data(self):
            return {
                "board_id": "TAB-HAYA",
                "length_mm": 2800,
                "width_mm": 2070,
                "thickness_mm": 18,
                "quantity": 1,
                "material": "Haya",
            }

    monkeypatch.setattr(mw, "NewBoardDialog", _AcceptCustom)
    window._add_board()

    found = MaterialCatalogManager(path=path).catalog.find("Haya")
    assert found is not None
    assert found.thicknesses_mm == (18.0,)
    assert window.services.projects.current_project.boards[0].material == "Haya"


def test_material_catalog_shortcut_is_ctrl_alt_t():
    assert any(
        binding.action_key == "material_catalog" and binding.sequence == "Ctrl+Alt+T"
        for binding in STUDIO_SHORTCUTS
    )


def test_preferences_dialog_shows_catalog_button_when_manager_passed(qapp, tmp_path):
    del qapp
    manager = MaterialCatalogManager(path=tmp_path / "material_catalog.json")
    dialog = PreferencesDialog(StudioPreferences(language="es"), catalog=manager)
    assert not dialog.edit_catalog.isHidden()
    assert "catálogo" in dialog.edit_catalog.text().lower()

    bare = PreferencesDialog(StudioPreferences(language="es"))
    assert bare.edit_catalog.isHidden()


def test_main_window_catalog_action_stays_enabled_without_project(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    action = window._actions["material_catalog"]
    assert action.isEnabled()
    assert action.text() == "Catálogo de materiales…"
    tip = action.statusTip()
    assert "Ctrl+Alt+T" in tip or "⌥" in tip or "⌘" in tip


def test_material_catalog_tip_mentions_user_file_and_shortcut():
    es = tr("tip.material_catalog", "es").casefold()
    en = tr("tip.material_catalog", "en").casefold()
    assert "Ctrl+Alt+T" in tr("tip.material_catalog", "es")
    assert "Ctrl+Alt+T" in tr("tip.material_catalog", "en")
    assert ".bcproj" in es and "proyectos" in es
    assert ".bcproj" in en and "projects" in en
    assert "€/m²" in tr("catalog.intro", "es")
    assert "€/m²" in tr("catalog.intro", "en")


def test_format_material_cost_shows_dash_amount_and_partial(qapp, tmp_path):
    del qapp
    from boardcomposer.inventory.material_cost import MaterialCostEstimate

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)

    empty = MaterialCostEstimate()
    assert window._format_material_cost(empty) == "—"

    full = MaterialCostEstimate(total=12.5, priced_area_m2=0.5)
    assert window._format_material_cost(full) == "12.50 €"

    mixed = MaterialCostEstimate(
        total=12.5,
        priced_area_m2=0.5,
        unpriced_area_m2=0.3,
        missing_materials=("MDF",),
    )
    assert window._format_material_cost(mixed) == "12.50 €*"
