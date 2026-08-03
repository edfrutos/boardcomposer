"""Remember last successful CSV/Excel import folder."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_suggested_import_directory_uses_existing(qapp, tmp_path):
    del qapp
    import_dir = tmp_path / "imports"
    import_dir.mkdir()
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(language="es", last_import_directory=str(import_dir))
    )

    assert window._suggested_import_directory() == str(import_dir)


def test_suggested_import_directory_falls_back_when_missing(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(
            language="es",
            last_import_directory=str(tmp_path / "gone"),
        )
    )

    assert window._suggested_import_directory() == ""


def test_remember_import_directory_persists(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    target = tmp_path / "imports" / "boards.csv"
    target.parent.mkdir()
    target.write_text("id,width,height\n", encoding="utf-8")

    window._remember_import_directory(target)

    assert window.services.preferences.current.last_import_directory == str(
        target.parent.resolve()
    )
    reloaded = PreferencesManager(tmp_path / "preferences.json").current
    assert reloaded.last_import_directory == str(target.parent.resolve())


def test_open_tabular_import_remembers_after_load(qapp, tmp_path, monkeypatch):
    from studio import main_window as mw
    from studio.tabular_file import TabularLoadResult

    del qapp
    window = _window(tmp_path)
    csv_path = tmp_path / "stock" / "pieces.csv"
    csv_path.parent.mkdir()
    csv_path.write_text("id,width,height\nA,10,10\n", encoding="utf-8")

    monkeypatch.setattr(
        mw.QFileDialog,
        "getOpenFileName",
        lambda *args, **kwargs: (str(csv_path), "CSV"),
    )
    monkeypatch.setattr(window, "_prompt_xlsx_sheet", lambda path: None)
    monkeypatch.setattr(
        mw,
        "load_tabular_file",
        lambda path, sheet=None: TabularLoadResult(
            fieldnames=("id", "width", "height"),
            rows=({"id": "A", "width": "10", "height": "10"},),
        ),
    )

    loaded = window._open_tabular_import(
        dialog_key="dialog.import_pieces_csv",
        short_key="action.import_pieces_csv",
    )

    assert loaded is not None
    assert loaded.ok
    remembered = window.services.preferences.current.last_import_directory
    assert remembered == str(csv_path.parent.resolve())
