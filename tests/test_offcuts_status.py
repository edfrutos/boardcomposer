"""Status bar shows offcuts of the selected solution (IDE-0092)."""

from PySide6.QtCore import QEvent, QPointF, Qt
from PySide6.QtGui import QMouseEvent

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
from tests.test_inspector_board_utilization import _window


def _offcut(instance: int) -> Offcut:
    return Offcut(PanelReference(0, instance), 10, 0, 100, 50)


def _mouse(event_type: QEvent.Type) -> QMouseEvent:
    return QMouseEvent(
        event_type,
        QPointF(2, 2),
        QPointF(2, 2),
        Qt.MouseButton.LeftButton,
        Qt.MouseButton.LeftButton,
        Qt.KeyboardModifier.NoModifier,
    )


def test_offcuts_status_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._offcuts_label
    assert label.objectName() == "statusOffcuts"
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=()),
    ]
    window.services.layout.selected_solution_index = 0
    window._update_offcuts_status()
    assert label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=(_offcut(0), _offcut(1))),
        AssemblySolution(placements=[], offcuts=(_offcut(0),)),
    ]
    window.services.layout.selected_solution_index = 0
    window._select_layout_solution(0)
    assert label.text() == "2 ret."
    assert not label.isHidden()
    assert "retales" in label.toolTip().casefold()
    assert "2" in label.toolTip()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    calls: list[str] = []
    window._promote_offcuts = lambda: calls.append("promote")
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress))
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease))
    assert calls == []

    window._select_layout_solution(1)
    assert label.text() == "1 ret."
    assert calls == []

    window.services.preferences.update(
        window.services.preferences.current.__class__(language="en")
    )
    window._retranslate_ui()
    assert label.text() == "1 ret."
    assert "offcuts" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
