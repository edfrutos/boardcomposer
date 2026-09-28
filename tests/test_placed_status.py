"""Status bar shows placed pieces over the inventory total (IDE-0060)."""

from studio.main_window import MainWindow
from studio.models import StudioPiece, StudioPlacement, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices


def _window(tmp_path, language: str) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language=language))
    return MainWindow(services)


def test_placed_status_counts_inventory_not_stray_placements(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, "es")
    assert window._placed_label.text() == "0/0"

    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        pieces=[
            StudioPiece("P1", 400, 300),
            StudioPiece("P2", 200, 100),
        ],
        placements=[
            StudioPlacement("P1", 0, 0),
            StudioPlacement("AJENA", 10, 10),
        ],
    )
    window.services.projects.open_project(project, None)
    window.update_window_title()
    assert window._placed_label.text() == "1/2"
    assert "colocadas" in window._placed_label.toolTip().casefold()
    assert "1 de 2" in window._placed_label.toolTip()


def test_placed_status_follows_language(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, "en")
    project = StudioProject(
        project_id="PRJ-1",
        name="Shop",
        pieces=[StudioPiece("P1", 100, 50)],
    )
    window.services.projects.open_project(project, None)
    window._retranslate_ui()
    assert window._placed_label.text() == "0/1"
    assert "pieces placed" in window._placed_label.toolTip().casefold()
