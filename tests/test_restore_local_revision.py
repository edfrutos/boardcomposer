"""Restore a local .bcproj revision from the diff dialog into memory."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QMessageBox

from studio.commands.add_board_command import AddBoardCommand
from studio.main_window import MainWindow
from studio.models import StudioBoard, StudioProject
from studio.preferences import PreferencesManager, StudioPreferences
from studio.project_serializer import save_project
from studio.services import StudioServices


def _window(tmp_path, path: Path, project: StudioProject) -> MainWindow:
    save_project(project, path)
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    services.projects.open_project(project, str(path))
    window = MainWindow(services)
    window.workspace.reload_project()
    window._reload_explorer()
    return window


def test_restore_local_revision_loads_ring_snapshot(qapp, tmp_path, monkeypatch):
    del qapp
    path = tmp_path / "demo.bcproj"
    original = StudioProject(
        project_id="PRJ-R",
        name="Original",
        boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
        pieces=[],
        placements=[],
    )
    window = _window(tmp_path, path, original)

    # Create a ring snapshot of "Original", then mutate disk + memory.
    save_project(
        StudioProject(
            project_id="PRJ-R",
            name="OnDisk",
            boards=[StudioBoard("B1", 1000, 500, "Demo", 19, 1)],
            pieces=[],
            placements=[],
        ),
        path,
    )
    project = window.services.projects.current_project
    assert project is not None
    project.name = "DirtyInMemory"
    window.services.projects.mark_modified()
    window.services.commands.execute(
        AddBoardCommand(
            window.services,
            StudioBoard("B2", 800, 400, "Demo", 19, 1),
        )
    )
    assert window.services.commands.can_undo()

    revisions = list(Path(path.parent / f".{path.name}.revs").glob("*.bcproj"))
    assert revisions
    snapshot = sorted(revisions, key=lambda p: p.name, reverse=True)[0]

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    window._restore_local_revision(snapshot)

    restored = window.services.projects.current_project
    assert restored is not None
    assert restored.name == "Original"
    assert window.services.projects.filename == str(path)
    assert window.services.projects.is_modified
    assert not window.services.commands.can_undo()
    assert not window.services.commands.can_redo()
    assert window._tr("status.revision_restored", name=snapshot.name) in (
        window.statusBar().currentMessage()
    )


def test_diff_dialog_restore_path_triggers_restore(qapp, tmp_path, monkeypatch):
    del qapp
    path = tmp_path / "demo.bcproj"
    project = StudioProject(
        project_id="PRJ-R2",
        name="Live",
        boards=[],
        pieces=[],
        placements=[],
    )
    window = _window(tmp_path, path, project)
    save_project(
        StudioProject(
            project_id="PRJ-R2",
            name="Newer",
            boards=[],
            pieces=[],
            placements=[],
        ),
        path,
    )
    snapshot = sorted(
        (path.parent / f".{path.name}.revs").glob("*.bcproj"),
        key=lambda p: p.name,
        reverse=True,
    )[0]

    called: list[Path] = []

    class _FakeDiffDialog:
        def __init__(self, parent, **kwargs):
            del parent, kwargs
            self.restore_path = snapshot

        def exec(self):
            return 1

        class DialogCode:
            Accepted = 1

    monkeypatch.setattr("studio.main_window.BcprojDiffDialog", _FakeDiffDialog)
    monkeypatch.setattr(
        window,
        "_restore_local_revision",
        lambda revision: called.append(Path(revision)),
    )

    window._diff_bcproj()

    assert called == [snapshot]
