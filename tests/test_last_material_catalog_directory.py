"""Remember last successful material-catalog pack folder."""

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    return MainWindow(services)


def test_suggested_material_catalog_directory_uses_existing(qapp, tmp_path):
    del qapp
    pack_dir = tmp_path / "packs"
    pack_dir.mkdir()
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(language="es", last_material_catalog_directory=str(pack_dir))
    )

    assert window._suggested_material_catalog_directory() == str(pack_dir)


def test_suggested_material_catalog_directory_falls_back_when_missing(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.preferences.update(
        StudioPreferences(
            language="es",
            last_material_catalog_directory=str(tmp_path / "gone"),
        )
    )

    assert window._suggested_material_catalog_directory() == ""


def test_remember_material_catalog_directory_persists(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    target = tmp_path / "packs" / "boardcomposer-material-catalog.json"
    target.parent.mkdir()
    target.write_text("{}", encoding="utf-8")

    window._remember_material_catalog_directory(target)

    assert window.services.preferences.current.last_material_catalog_directory == str(
        target.parent.resolve()
    )
    reloaded = PreferencesManager(tmp_path / "preferences.json").current
    assert reloaded.last_material_catalog_directory == str(target.parent.resolve())
