"""Restore-latest local revision menu action and enablement."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from studio.keyboard_shortcuts import STUDIO_SHORTCUTS
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def _window(tmp_path, *, with_file: bool = False) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-R",
        name="Live",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[],
        placements=[],
    )
    if with_file:
        path = tmp_path / "demo.bcproj"
        save_project(project, path)
        services.projects.open_project(project, str(path))
    else:
        services.projects.new_project(project)
    window = MainWindow(services)
    window.update_window_title()
    return window


def test_restore_local_revision_shortcut_registered():
    assert any(
        b.action_key == "restore_local_revision" and b.sequence == "Ctrl+Alt+Y"
        for b in STUDIO_SHORTCUTS
    )


def test_restore_action_disabled_without_ring(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, with_file=False)
    action = window._actions["restore_local_revision"]
    assert not action.isEnabled()
    assert "guarda" in action.statusTip().lower()


def test_restore_action_enabled_with_ring(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, with_file=True)
    path = Path(window.services.projects.filename)
    # Second save creates a ring snapshot of the first file.
    save_project(
        StudioProject(
            project_id="PRJ-R",
            name="Newer",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        ),
        path,
    )
    window.update_window_title()
    action = window._actions["restore_local_revision"]
    assert action.isEnabled()
    tip = action.statusTip()
    assert tip
    assert "Y" in tip or "revisión" in tip.lower() or "revision" in tip.lower()


def test_restore_latest_action_triggers_restore(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path, with_file=True)
    path = Path(window.services.projects.filename)
    save_project(
        StudioProject(
            project_id="PRJ-R",
            name="Newer",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        ),
        path,
    )
    window.update_window_title()
    called: list[Path] = []
    monkeypatch.setattr(
        window,
        "_restore_local_revision",
        lambda revision: called.append(Path(revision)),
    )
    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    window._actions["restore_local_revision"].trigger()

    assert len(called) == 1
    assert called[0].parent.name.endswith(".bcproj.revs")
