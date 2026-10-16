"""Status bar shows panels consumed by the selected solution (IDE-0112)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, BoardPlacement, PanelReference
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def _mouse(event_type: QEvent.Type) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(2, 2),
        QPointF(2, 2),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_solution_panels_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_panels_label
    assert empty_label.objectName() == "statusSolutionPanels"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert empty._boards_label.objectName() == "statusPhysicalBoards"

    window = _window(tmp_path)
    label = window._solution_panels_label
    inventory = window._boards_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[]),
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0)
                ),
                BoardPlacement(
                    "B", 0, 0, 100, 50, panel_reference=PanelReference(0, 1)
                ),
            ]
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.text() == "pan. 0"
    assert not label.isHidden()
    assert "tableros" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.text() == "1/2 sol."
    assert label.text() != inventory.text()
    assert "tab." not in label.text()

    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress))
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease))
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert label.text() == "pan. 2"
    assert "2" in label.toolTip()
    assert window._solution_label.text() == "2/2 sol."
    assert calls == []
    assert "tab." not in label.text()

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A", 0, 0, 100, 50, panel_reference=PanelReference(0, 0)
                ),
                BoardPlacement(
                    "B", 0, 0, 100, 50, panel_reference=PanelReference(0, 1)
                ),
            ]
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert label.text() == "pnl 2"
    assert "boards" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert "tab." not in label.text()
