"""Status bar shows unplaced inventory pieces (IDE-0079)."""

from dataclasses import replace

from PySide6.QtCore import Qt

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


def test_omitted_status_hidden_without_project_or_when_complete(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, "es")
    label = window._omitted_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        pieces=[
            StudioPiece("P1", 400, 300),
            StudioPiece("P2", 200, 100),
        ],
        placements=[StudioPlacement("P1", 0, 0), StudioPlacement("P2", 10, 10)],
    )
    window.services.projects.open_project(project, None)
    window.update_window_title()
    assert label.isHidden()
    assert window._placed_label.text() == "2/2"


def test_omitted_status_counts_unplaced_inventory(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, "es")
    project = StudioProject(
        project_id="PRJ-1",
        name="Taller",
        pieces=[
            StudioPiece("P1", 400, 300),
            StudioPiece("P2", 200, 100),
            StudioPiece("P3", 150, 80),
        ],
        placements=[
            StudioPlacement("P1", 0, 0),
            StudioPlacement("AJENA", 10, 10),
        ],
    )
    window.services.projects.open_project(project, None)
    window.update_window_title()
    label = window._omitted_label
    assert label.text() == "2 om."
    assert not label.isHidden()
    assert "omitidas" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._placed_label.text() == "1/3"

    project.pieces.append(StudioPiece("P4", 80, 40))
    window.update_window_title()
    assert label.text() == "3 om."

    window.services.preferences.update(
        replace(window.services.preferences.current, language="en")
    )
    window._retranslate_ui()
    assert label.text() == "3 om."
    assert "omitted" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
