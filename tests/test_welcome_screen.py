"""Tests for recent-files persistence and the welcome screen (SCR-001)."""

from PySide6.QtWidgets import QApplication

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.recent_files import RecentFilesManager
from studio.services import StudioServices
from studio.theme import apply_theme
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


def test_recent_files_manager_clear(tmp_path):
    path = tmp_path / "recent.json"
    existing = tmp_path / "demo.bcproj"
    existing.write_text("{}", encoding="utf-8")

    manager = RecentFilesManager(path=path)
    manager.add(str(existing))
    manager.clear()

    assert manager.files == []
    assert RecentFilesManager(path=path).files == []


def test_recent_files_manager_prune_and_remove(tmp_path):
    path = tmp_path / "recent.json"
    existing = tmp_path / "demo.bcproj"
    existing.write_text("{}", encoding="utf-8")
    missing = tmp_path / "gone.bcproj"

    manager = RecentFilesManager(path=path)
    manager.add(str(missing))
    manager.add(str(existing))

    assert manager.prune_missing() == 1
    assert manager.files == [str(existing)]
    assert RecentFilesManager(path=path).files == [str(existing)]

    assert manager.remove(str(existing)) is True
    assert manager.files == []
    assert manager.remove(str(existing)) is False


def test_welcome_screen_lists_recent_paths(qapp):
    del qapp
    screen = WelcomeScreen()
    screen.set_recent_files(["/tmp/proyecto-a.bcproj", "/tmp/proyecto-b.bcproj"])

    assert screen.recent_list.count() == 2
    assert "proyecto-a.bcproj" in screen.recent_list.item(0).text()
    assert screen.clear_recent_button.isEnabled()
    tip = screen.clear_recent_button.toolTip()
    assert "Ctrl+Shift+X" in tip or "⇧⌘X" in tip


def test_welcome_screen_shows_empty_state(qapp):
    del qapp
    screen = WelcomeScreen()
    screen.set_recent_files([])

    assert screen.recent_list.count() == 1
    assert "Sin proyectos recientes" in screen.recent_list.item(0).text()
    assert not screen.clear_recent_button.isEnabled()
    assert "Sin proyectos recientes" in screen.clear_recent_button.toolTip()


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
    assert screen.new_button.minimumHeight() >= 44
    assert screen.open_button.minimumHeight() >= 44
    assert screen.demo_button.minimumHeight() >= 36
    assert screen.shortcuts_button.minimumHeight() >= 36
    assert screen.about_button.minimumHeight() >= 36
    assert screen.clear_recent_button.minimumHeight() >= 32
    assert screen.clear_recent_button.objectName() == "welcomeClearRecent"
    tip_shortcuts = screen.shortcuts_button.toolTip()
    assert "F1" in tip_shortcuts
    tip_about = screen.about_button.toolTip()
    assert "Ctrl+Shift+A" in tip_about or "⇧⌘A" in tip_about


def test_welcome_help_ctas_emit_signals(qapp):
    del qapp
    screen = WelcomeScreen()
    shortcuts: list[int] = []
    about: list[int] = []
    screen.shortcuts_requested.connect(lambda: shortcuts.append(1))
    screen.about_requested.connect(lambda: about.append(1))

    screen.shortcuts_button.click()
    screen.about_button.click()

    assert shortcuts == [1]
    assert about == [1]


def test_welcome_and_empty_ctas_survive_theme_switch(qapp, tmp_path):
    """light → system must not wipe Welcome / empty-overlay CTA heights."""
    del qapp
    app = QApplication.instance()
    assert app is not None
    apply_theme(app, "light")
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    window = MainWindow(services)
    assert window.welcome.new_button.minimumHeight() >= 44
    assert window.welcome.open_button.minimumHeight() >= 44
    assert window.welcome.demo_button.minimumHeight() >= 36
    assert window.welcome.shortcuts_button.minimumHeight() >= 36
    assert window.welcome.about_button.minimumHeight() >= 36
    assert window.welcome.clear_recent_button.minimumHeight() >= 32
    overlay = window.workspace.empty_overlay
    assert overlay.add_board_button.minimumHeight() >= 44
    assert overlay.add_piece_button.minimumHeight() >= 36
    assert overlay.import_boards_button.minimumHeight() >= 36


def test_welcome_recent_activation_ignores_null_item(qapp):
    del qapp
    screen = WelcomeScreen()
    opened: list[str] = []
    screen.open_recent_requested.connect(opened.append)

    screen._on_recent_activated(None)
    assert opened == []

    screen.set_recent_files([])
    empty = screen.recent_list.item(0)
    assert empty is not None
    screen._on_recent_activated(empty)
    assert opened == []


def test_welcome_recent_single_click_opens(qapp):
    del qapp
    screen = WelcomeScreen()
    opened: list[str] = []
    screen.open_recent_requested.connect(opened.append)
    screen.set_recent_files(["/tmp/proyecto-a.bcproj"])

    item = screen.recent_list.item(0)
    assert item is not None
    screen.recent_list.itemClicked.emit(item)

    assert opened == ["/tmp/proyecto-a.bcproj"]
