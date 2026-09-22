"""Share Studio preferences via JSON pack (IDE-0049)."""

from PySide6.QtWidgets import QFileDialog, QMessageBox

from studio.dialogs.preferences_dialog import PreferencesDialog
from studio.preferences import (
    PREFS_PACK_KIND,
    PreferencesManager,
    StudioPreferences,
    export_preferences_pack,
    import_preferences_pack,
)


def test_export_pack_omits_local_paths_and_window(tmp_path):
    prefs = StudioPreferences(
        units="cm",
        theme="dark",
        last_export_directory="/tmp/exports",
        window_geometry="QUJDRA==",
        window_state="U1RBVEU=",
        last_preferences_directory="/packs",
    )
    pack = tmp_path / "prefs.json"
    export_preferences_pack(prefs, pack)
    text = pack.read_text(encoding="utf-8")
    assert PREFS_PACK_KIND in text
    assert '"units": "cm"' in text
    assert "last_export_directory" not in text
    assert "window_geometry" not in text
    assert "window_state" not in text
    assert "last_preferences_directory" not in text


def test_import_pack_merge_overlays_and_keeps_local(tmp_path):
    current = StudioPreferences(
        units="mm",
        theme="light",
        max_solutions=20,
        last_export_directory="/keep",
        window_geometry="QUJDRA==",
    )
    pack = tmp_path / "pack.json"
    export_preferences_pack(StudioPreferences(units="in", theme="dark"), pack)

    imported = import_preferences_pack(current, pack, mode="merge")
    assert imported.units == "in"
    assert imported.theme == "dark"
    assert imported.max_solutions == 20
    assert imported.last_export_directory == "/keep"
    assert imported.window_geometry == "QUJDRA=="


def test_import_pack_replace_uses_defaults_for_missing(tmp_path):
    current = StudioPreferences(
        units="cm",
        theme="dark",
        max_solutions=40,
        last_project_directory="/projects",
    )
    pack = tmp_path / "pack.json"
    export_preferences_pack(StudioPreferences(units="in"), pack)

    imported = import_preferences_pack(current, pack, mode="replace")
    assert imported.units == "in"
    assert imported.theme == "system"
    assert imported.max_solutions == 20
    assert imported.last_project_directory == "/projects"


def test_import_pack_accepts_raw_preferences_json(tmp_path):
    raw = tmp_path / "preferences.json"
    PreferencesManager(raw).update(StudioPreferences(units="cm", language="en"))
    imported = import_preferences_pack(StudioPreferences(), raw, mode="merge")
    assert imported.units == "cm"
    assert imported.language == "en"


def test_import_pack_rejects_wrong_kind_and_mode(tmp_path):
    wrong = tmp_path / "catalog.json"
    wrong.write_text(
        '{"kind": "boardcomposer.material_catalog", "materials": []}',
        encoding="utf-8",
    )
    try:
        import_preferences_pack(StudioPreferences(), wrong, mode="merge")
    except ValueError as exc:
        assert "preferencias" in str(exc)
    else:
        raise AssertionError("expected ValueError")

    try:
        import_preferences_pack(StudioPreferences(), wrong, mode="invalid")
    except ValueError as exc:
        assert "Modo" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_preferences_dialog_share_buttons_and_export(qapp, tmp_path, monkeypatch):
    del qapp
    target = tmp_path / "out" / "pack.json"
    target.parent.mkdir()
    remembered: list[str] = []
    dialog = PreferencesDialog(
        StudioPreferences(language="en", units="cm"),
        pack_directory=str(target.parent),
        on_pack_directory=lambda path: remembered.append(str(path)),
    )
    assert dialog.export_button.text() == "Export preferences…"
    assert dialog.import_button.text() == "Import preferences…"

    monkeypatch.setattr(
        QFileDialog,
        "getSaveFileName",
        lambda *args, **kwargs: (str(target), "json"),
    )
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)

    dialog._export_pack()

    assert target.is_file()
    assert PREFS_PACK_KIND in target.read_text(encoding="utf-8")
    assert remembered == [str(target)]
    assert dialog.preferences().last_preferences_directory == str(
        target.parent.resolve()
    )


def test_preferences_dialog_import_merge_updates_widgets(qapp, tmp_path, monkeypatch):
    del qapp
    pack = tmp_path / "pack.json"
    export_preferences_pack(
        StudioPreferences(units="in", theme="dark", max_solutions=8),
        pack,
    )
    dialog = PreferencesDialog(StudioPreferences(language="en", units="mm"))
    monkeypatch.setattr(
        QFileDialog,
        "getOpenFileName",
        lambda *args, **kwargs: (str(pack), "json"),
    )
    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )
    monkeypatch.setattr(QMessageBox, "information", lambda *args, **kwargs: None)

    dialog._import_pack()

    imported = dialog.preferences()
    assert imported.units == "in"
    assert imported.theme == "dark"
    assert imported.max_solutions == 8


def test_preferences_manager_round_trips_last_preferences_directory(tmp_path):
    path = tmp_path / "preferences.json"
    manager = PreferencesManager(path)
    manager.update(
        StudioPreferences(language="es", last_preferences_directory="/packs")
    )
    assert PreferencesManager(path).current.last_preferences_directory == "/packs"
