"""Copy the status-bar zoom (IDE-0091)."""

from PySide6.QtWidgets import QApplication

from tests.test_zoom_limit_enablement import _window


def test_copy_zoom_matches_the_label_and_does_not_reset(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions["copy_zoom"]
    assert "Ctrl+Alt+Shift+Z" in action.shortcut().toString()
    assert action.isEnabled()
    label = window._zoom_label.text()
    assert label.endswith("%")
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    calls: list[str] = []
    window._zoom_100 = lambda: calls.append("reset")
    zoom_before = window.workspace.zoom
    action.trigger()
    assert calls == []
    assert clipboard.text() == label
    assert window.workspace.zoom == zoom_before
    assert window.statusBar().currentMessage() == window._tr(
        "status.zoom_copied", n=label
    )

    window.workspace._camera.zoom = 1.0
    window.workspace._apply_camera()
    assert window._zoom_label.text() == "100%"
    action.trigger()
    assert calls == []
    assert clipboard.text() == "100%"
    assert window.workspace.zoom == 1.0

    window.workspace.zoom_in()
    assert window._zoom_label.text() != "100%"
    action.trigger()
    assert calls == []
    assert clipboard.text() == window._zoom_label.text()
    assert window.workspace.zoom != 1.0
