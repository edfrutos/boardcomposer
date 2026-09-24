"""Shop default material for new boards and pieces (IDE-0053)."""

from studio.dialogs.new_board_dialog import NewBoardDialog
from studio.dialogs.new_piece_dialog import NewPieceDialog
from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import (
    DEFAULT_MATERIAL,
    PreferencesManager,
    StudioPreferences,
    normalize_default_material,
    preferences_from_payload,
    preferences_payload,
)
from studio.services import StudioServices


def test_blank_default_material_falls_back_to_catalog_seed():
    assert normalize_default_material("  ") == DEFAULT_MATERIAL
    assert normalize_default_material(None) == DEFAULT_MATERIAL
    loaded = preferences_from_payload({})
    assert loaded.default_material == "Melamina blanca"


def test_default_material_roundtrip_in_preferences_payload():
    payload = preferences_payload(StudioPreferences(default_material="MDF"))
    assert payload["default_material"] == "MDF"
    assert preferences_from_payload(payload).default_material == "MDF"


def test_restore_defaults_resets_material(qapp):
    del qapp
    dialog = PreferencesDialog(StudioPreferences(default_material="Roble"))
    dialog._restore_defaults()
    assert dialog.preferences().default_material == "Melamina blanca"


def _window(tmp_path, material: str) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(
        StudioPreferences(language="es", default_material=material)
    )
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Taller",
            boards=[StudioBoard("B1", 1000, 500, "Roble", 19, 1)],
            pieces=[StudioPiece("A", 400, 300, "Roble", 19)],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    return window


def test_new_board_and_piece_use_shop_default(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path, "MDF")
    seen: list[str] = []

    def _board(*args, **kwargs):
        seen.append(kwargs["material"])
        dialog = NewBoardDialog(*args, **kwargs)
        dialog.exec = lambda: NewBoardDialog.DialogCode.Rejected
        return dialog

    def _piece(*args, **kwargs):
        seen.append(kwargs["material"])
        dialog = NewPieceDialog(*args, **kwargs)
        dialog.exec = lambda: NewPieceDialog.DialogCode.Rejected
        return dialog

    monkeypatch.setattr("studio.main_window.NewBoardDialog", _board)
    monkeypatch.setattr("studio.main_window.NewPieceDialog", _piece)
    window._add_board()
    window._add_piece()
    assert seen == ["MDF", "MDF"]


def test_edit_keeps_item_material(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path, "MDF")
    seen: list[str] = []

    def _board(*args, **kwargs):
        seen.append(kwargs["material"])
        dialog = NewBoardDialog(*args, **kwargs)
        dialog.exec = lambda: NewBoardDialog.DialogCode.Rejected
        return dialog

    monkeypatch.setattr("studio.main_window.NewBoardDialog", _board)
    window._edit_board("B1")
    assert seen == ["Roble"]
