"""Click the kerf label to edit the project saw kerf (IDE-0067)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_copy_selection_id import _window


def _mouse(event_type: QEvent.Type, x: float = 2, y: float = 2) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(x, y),
        QPointF(x, y),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_kerf_label_click_opens_editor(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    calls: list[str] = []
    monkeypatch.setattr(window, "_edit_project_kerf", lambda: calls.append("edit"))
    assert window._kerf_label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    tip = window._kerf_label.toolTip()
    assert "sierra" in tip.casefold()
    assert "Ctrl+Alt+K" in tip or "⌥⌘K" in tip

    assert (
        window.eventFilter(window._kerf_label, _mouse(QEvent.Type.MouseButtonPress))
        is True
    )
    assert (
        window.eventFilter(window._kerf_label, _mouse(QEvent.Type.MouseButtonRelease))
        is True
    )
    assert calls == ["edit"]
    assert window.services.projects.current_project is not None
    assert window.services.projects.current_project.kerf_mm == 0.0


def test_kerf_label_ignores_drag_and_missing_project(qapp, tmp_path, monkeypatch):
    del qapp
    window = _window(tmp_path)
    calls: list[str] = []
    monkeypatch.setattr(window, "_edit_project_kerf", lambda: calls.append("edit"))

    assert (
        window.eventFilter(window._kerf_label, _mouse(QEvent.Type.MouseButtonPress))
        is True
    )
    assert (
        window.eventFilter(window._kerf_label, _mouse(QEvent.Type.MouseMove, -10, -10))
        is False
    )
    assert (
        window.eventFilter(window._kerf_label, _mouse(QEvent.Type.MouseButtonRelease))
        is False
    )
    assert calls == []

    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    monkeypatch.setattr(empty, "_edit_project_kerf", lambda: calls.append("empty"))
    assert empty._kerf_label.isHidden()
    assert empty._kerf_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert (
        empty.eventFilter(empty._kerf_label, _mouse(QEvent.Type.MouseButtonPress))
        is False
    )
    assert calls == []
