"""Revision backup export offers the same open/reveal dialog as other exports."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QFileDialog

from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def _window(tmp_path) -> MainWindow:
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    project = StudioProject(
        project_id="PRJ-B",
        name="Backup",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 100, 50, "Demo", 19)],
        placements=[],
    )
    path = tmp_path / "demo.bcproj"
    save_project(project, path)
    services.projects.open_project(project, str(path))
    window = MainWindow(services)
    window.update_window_title()
    return window


def test_export_revision_backup_offers_open_after(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    dest = tmp_path / "backups"
    dest.mkdir()
    offered: list[Path] = []
    monkeypatch.setattr(
        window,
        "_offer_open_exported_path",
        lambda path: offered.append(Path(path)),
    )
    monkeypatch.setattr(
        QFileDialog,
        "getExistingDirectory",
        lambda *args, **kwargs: str(dest),
    )

    window._export_revision_backup()

    assert len(offered) == 1
    folder = offered[0]
    assert folder.is_dir()
    assert folder.parent == dest
    assert (folder / "demo.bcproj").is_file()
    assert "backup" in window.statusBar().currentMessage().lower()
