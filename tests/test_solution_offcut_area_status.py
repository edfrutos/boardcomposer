"""Status bar shows offcut area of the selected solution (IDE-0130)."""

from dataclasses import replace

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
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


def test_solution_offcut_area_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_offcut_area_label
    assert empty_label.objectName() == "statusSolutionOffcutArea"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path)
    label = window._solution_offcut_area_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=()),
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 200, 100),),
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.text() == "retár. 0 mm²"
    assert not label.isHidden()
    assert window._offcuts_label.isHidden()
    assert "área de retales" in label.toolTip().casefold()
    assert "clic" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    assert window._solution_label.text() == "1/2 sol."

    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress))
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease))
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    assert label.text() == "retár. 20000 mm²"
    assert "20000 mm²" in label.toolTip()
    assert window._offcuts_label.text() == "1 ret."
    assert window._solution_label.text() == "2/2 sol."
    assert calls == []

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert label.text() == "retár. 200 cm²"
    assert "200 cm²" in label.toolTip()

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 200, 100),),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        replace(window.services.preferences.current, language="en", units="mm")
    )
    window._retranslate_ui()
    assert label.text() == "offar. 20000 mm²"
    assert "offcut area" in label.toolTip().casefold()
    assert "click" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
