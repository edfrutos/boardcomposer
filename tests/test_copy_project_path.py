"""Copy the saved .bcproj path (IDE-0061)."""

from PySide6.QtWidgets import QApplication

from studio.models import StudioProject
from studio.project_serializer import save_project
from tests.test_copy_selection_id import _window


def test_copy_project_path_shortcut_and_clipboard(qapp, tmp_path):
    del qapp
    path = tmp_path / "taller.bcproj"
    project = StudioProject(project_id="PRJ-1", name="Taller")
    save_project(project, path)
    window = _window(tmp_path)
    assert "Ctrl+Alt+Shift+C" in (
        window._actions["copy_project_path"].shortcut().toString()
    )
    assert not window._actions["copy_project_path"].isEnabled()

    window.services.projects.open_project(project, str(path))
    window.update_window_title()
    action = window._actions["copy_project_path"]
    assert action.isEnabled()
    tip = action.statusTip()
    assert "⌥⇧⌘C" in tip or "Ctrl+Alt+Shift+C" in tip

    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.clear()
    action.trigger()
    assert clipboard.text() == str(path)
    assert window.statusBar().currentMessage() == window._tr(
        "status.project_path_copied"
    )


def test_copy_project_path_without_file_keeps_clipboard(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    window.services.projects.new_project(
        StudioProject(project_id="PRJ-1", name="Nuevo")
    )
    window.update_window_title()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not window._actions["copy_project_path"].isEnabled()
    window._copy_project_path()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.project_path_unavailable"
    )
