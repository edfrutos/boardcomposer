"""Remember last successful revision-backup destination folder."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def _window(tmp_path, *, backup_dir: Path | None = None) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    prefs = StudioPreferences(language="es")
    if backup_dir is not None:
        prefs = StudioPreferences(
            language="es", last_backup_directory=str(backup_dir)
        )
    services.preferences.update(prefs)
    project = StudioProject(
        project_id="PRJ-B",
        name="Backup",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    path = tmp_path / "project" / "demo.bcproj"
    path.parent.mkdir(parents=True, exist_ok=True)
    save_project(project, path)
    services.projects.open_project(project, str(path))
    window = MainWindow(services)
    window.update_window_title()
    return window


def test_suggested_backup_directory_prefers_existing(qapp, tmp_path):
    del qapp
    remembered = tmp_path / "backups"
    remembered.mkdir()
    window = _window(tmp_path, backup_dir=remembered)

    suggested = window._suggested_backup_directory(tmp_path / "project" / "demo.bcproj")

    assert suggested == str(remembered)


def test_suggested_backup_directory_falls_back_to_project_parent(qapp, tmp_path):
    del qapp
    window = _window(tmp_path, backup_dir=tmp_path / "gone")
    project = tmp_path / "project" / "demo.bcproj"

    suggested = window._suggested_backup_directory(project)

    assert suggested == str(project.parent.resolve())


def test_export_revision_backup_remembers_destination(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    dest = tmp_path / "backups"
    dest.mkdir()
    monkeypatch.setattr(window, "_offer_open_exported_path", lambda path: None)
    monkeypatch.setattr(
        QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: str(dest),
    )

    window._export_revision_backup()

    remembered = window.services.preferences.current.last_backup_directory
    assert remembered == str(dest.resolve())
    reloaded = PreferencesManager(tmp_path / "preferences.json").current
    assert reloaded.last_backup_directory == str(dest.resolve())
