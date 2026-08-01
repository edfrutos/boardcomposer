"""Clear undo/redo when opening or replacing a project."""

from __future__ import annotations

from studio.commands.add_board_command import AddBoardCommand
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.recent_files import RecentFilesManager
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json"),
        recent_files=RecentFilesManager(path=tmp_path / "recent.json"),
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="One",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        )
    )
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    window.services.commands.execute(
        AddBoardCommand(
            window.services,
            StudioBoard("B2", 800, 400, "Demo", 19, 1),
        )
    )
    window.update_undo_redo()
    assert window.services.commands.can_undo()
    return window


def test_load_empty_project_clears_undo(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)

    window._load_empty_project(name="Fresh")

    assert not window.services.commands.can_undo()
    assert not window.services.commands.can_redo()
    assert not window._actions["undo"].isEnabled()


def test_load_demo_project_clears_undo(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)

    window._load_demo_project()

    assert not window.services.commands.can_undo()
    assert not window._actions["undo"].isEnabled()


def test_open_project_clears_undo(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    path = tmp_path / "other.bcproj"
    save_project(
        StudioProject(
            project_id="PRJ-2",
            name="Other",
            boards=[],
            pieces=[],
            placements=[],
        ),
        path,
    )
    monkeypatch.setattr(
        window,
        "_confirm_discard_unsaved_changes",
        lambda: True,
    )
    monkeypatch.setattr(
        "studio.main_window.QFileDialog.getOpenFileName",
        lambda *args, **kwargs: (str(path), ""),
    )

    window._open_project()

    assert window.services.projects.current_project is not None
    assert window.services.projects.current_project.name == "Other"
    assert not window.services.commands.can_undo()
    assert not window._actions["undo"].isEnabled()


def test_open_recent_project_clears_undo(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    path = tmp_path / "recent.bcproj"
    save_project(
        StudioProject(
            project_id="PRJ-3",
            name="Recent",
            boards=[],
            pieces=[],
            placements=[],
        ),
        path,
    )
    monkeypatch.setattr(
        window,
        "_confirm_discard_unsaved_changes",
        lambda: True,
    )

    window._open_recent_project(str(path))

    assert window.services.projects.current_project.name == "Recent"
    assert not window.services.commands.can_undo()
