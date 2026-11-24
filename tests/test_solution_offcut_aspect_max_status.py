"""Status bar shows the maximum offcut aspect ratio (IDE-0244)."""

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


def _solution(*sizes: tuple[float, float]) -> AssemblySolution:
    return AssemblySolution(
        placements=[],
        offcuts=tuple(
            Offcut(PanelReference(0, 0), 400, 0, length, width)
            for length, width in sizes
        ),
    )


def _select(window: MainWindow, *sizes: tuple[float, float]) -> None:
    window.services.layout.solutions = [_solution(*sizes)]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()


def test_offcut_aspect_max_is_hidden_without_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    label = MainWindow(services)._solution_offcut_aspect_max_label
    assert label.objectName() == "statusSolutionOffcutAspectMax"
    assert label.isHidden()
    assert label.text() == ""
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor


def test_offcut_aspect_max_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._solution_offcut_aspect_max_label
    assert label.isHidden()
    window.services.layout.solutions = [
        _solution(),
        _solution((50, 50), (100, 40), (200, 100)),
        _solution((10, 10), (100, 10), (50, 40), (200, 100)),
    ]

    window._select_layout_solution(0)
    assert label.isHidden()
    assert window._solution_label.text() == "1/3 sol."

    window._select_layout_solution(1)
    # aspects 1.00, 2.50, 2.00
    assert label.text() == "xrel. 2.50"
    assert not label.isHidden()
    assert "máxima" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()

    window._select_layout_solution(2)
    # aspects 1.00, 10.00, 1.25, 2.00; the largest-area offcut is 2.00
    assert label.text() == "xrel. 10.00"
    assert window._solution_largest_offcut_aspect_label.text() == "relr. 2.00"
    assert window._solution_offcut_aspect_span_label.text() == "arel. 9.00"
    assert window._solution_offcut_aspect_average_label.text() == "relp. 3.56"
    assert window._solution_offcut_aspect_geomean_label.text() == "grel. 2.24"

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.text() == ""
    assert label.toolTip() == ""


def test_offcut_aspect_max_ignores_orientation(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._solution_offcut_aspect_max_label

    _select(window, (50, 50))
    assert label.text() == "xrel. 1.00"

    _select(window, (10, 40), (40, 20))
    assert label.text() == "xrel. 4.00"


def test_offcut_aspect_max_label_is_not_clickable(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._solution_offcut_aspect_max_label
    _select(window, (100, 40))
    zoom = window.workspace.zoom
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")

    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom


def test_offcut_aspect_max_ignores_units_and_translates(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    label = window._solution_offcut_aspect_max_label
    _select(window, (100, 10), (200, 100))

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert label.text() == "xrel. 10.00"

    window.services.preferences.update(
        replace(window.services.preferences.current, language="en")
    )
    window._retranslate_ui()
    assert label.text() == "mxas 10.00"
    assert "maximum" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
