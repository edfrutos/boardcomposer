"""Tests for recent-files persistence and the welcome screen (SCR-001)."""

from studio.recent_files import RecentFilesManager
from studio.welcome_screen import WelcomeScreen


def test_recent_files_manager_persists_and_filters_missing(tmp_path):
    path = tmp_path / "recent.json"
    existing = tmp_path / "demo.bcproj"
    existing.write_text("{}", encoding="utf-8")
    missing = tmp_path / "gone.bcproj"

    manager = RecentFilesManager(path=path)
    manager.add(str(missing))
    manager.add(str(existing))

    reloaded = RecentFilesManager(path=path)

    assert reloaded.files[0] == str(existing)
    assert str(missing) in reloaded.files
    assert reloaded.existing_files() == [str(existing)]


def test_welcome_screen_lists_recent_paths(qapp):
    del qapp
    screen = WelcomeScreen()
    screen.set_recent_files(["/tmp/proyecto-a.bcproj", "/tmp/proyecto-b.bcproj"])

    assert screen.recent_list.count() == 2
    assert "proyecto-a.bcproj" in screen.recent_list.item(0).text()


def test_welcome_screen_shows_empty_state(qapp):
    del qapp
    screen = WelcomeScreen()
    screen.set_recent_files([])

    assert screen.recent_list.count() == 1
    assert "Sin proyectos recientes" in screen.recent_list.item(0).text()


def test_welcome_screen_brand_and_primary_object_names(qapp):
    del qapp
    from PySide6.QtWidgets import QLabel, QPushButton

    screen = WelcomeScreen()

    assert screen.objectName() == "welcomeRoot"
    brand = screen.findChild(QLabel, "welcomeBrand")
    assert brand is not None
    assert brand.text() == "BoardComposer"
    assert screen.new_button.objectName() == "primaryButton"
    assert isinstance(screen.new_button, QPushButton)
