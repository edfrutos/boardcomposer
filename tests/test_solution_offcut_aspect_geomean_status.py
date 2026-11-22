"""Status bar shows geometric mean of offcut aspect ratios (IDE-0241)."""

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


def test_solution_offcut_aspect_geomean_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_offcut_aspect_geomean_label
    assert empty_label.objectName() == "statusSolutionOffcutAspectGeomean"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path)
    label = window._solution_offcut_aspect_geomean_label
    assert label.text() == ""
    assert label.isHidden()
    assert label.toolTip() == ""
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=()),
        AssemblySolution(
            placements=[],
            offcuts=(
                Offcut(PanelReference(0, 0), 400, 0, 50, 50),
                Offcut(PanelReference(0, 0), 400, 0, 100, 40),
                Offcut(PanelReference(0, 0), 400, 0, 200, 100),
            ),
        ),
        AssemblySolution(
            placements=[],
            offcuts=(
                Offcut(PanelReference(0, 0), 400, 0, 10, 10),
                Offcut(PanelReference(0, 0), 400, 0, 100, 10),
                Offcut(PanelReference(0, 0), 400, 0, 50, 40),
                Offcut(PanelReference(0, 0), 400, 0, 200, 100),
            ),
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.isHidden()
    assert window._solution_label.text() == "1/3 sol."
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor

    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress)) is False
    assert window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease)) is False
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom

    window._select_layout_solution(1)
    # aspects 1.00, 2.50, 2.00 → geometric_mean 1.71
    assert label.text() == "grel. 1.71"
    assert not label.isHidden()
    assert window._solution_offcut_aspect_average_label.text() == "relp. 1.83"
    assert window._solution_offcut_aspect_median_label.text() == "mrel. 2.00"
    assert window._solution_offcut_aspect_stddev_label.text() == "drel. 0.62"
    assert window._solution_offcut_aspect_span_label.text() == "arel. 1.50"
    assert label.text() != window._solution_offcut_aspect_average_label.text()
    assert label.text() != window._solution_offcut_aspect_median_label.text()
    assert label.text() != window._solution_offcut_aspect_stddev_label.text()
    assert label.text() != window._solution_offcut_aspect_span_label.text()
    assert "mm" not in label.text()
    assert "geométrica" in label.toolTip().casefold()
    assert "clic" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonPress))
    window.eventFilter(label, _mouse(QEvent.Type.MouseButtonRelease))
    assert calls == []
    assert window.services.layout.selected_solution_index == 1
    assert window.workspace.zoom == zoom

    window._select_layout_solution(2)
    # aspects 1.00, 10.00, 1.25, 2.00 → geometric_mean 2.24
    assert label.text() == "grel. 2.24"
    assert window._solution_offcut_aspect_average_label.text() == "relp. 3.56"
    assert window._solution_offcut_aspect_median_label.text() == "mrel. 1.25"
    assert window._solution_offcut_aspect_stddev_label.text() == "drel. 3.73"
    assert label.text() != window._solution_offcut_aspect_average_label.text()
    assert label.text() != window._solution_offcut_aspect_median_label.text()
    assert label.text() != window._solution_offcut_aspect_stddev_label.text()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 50, 50),),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    assert label.text() == "grel. 1.00"
    assert window._solution_offcut_aspect_average_label.text() == "relp. 1.00"
    assert window._solution_offcut_aspect_stddev_label.text() == "drel. 0.00"

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert label.text() == "grel. 1.00"
    assert "1.00" in label.toolTip()

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(
                Offcut(PanelReference(0, 0), 400, 0, 10, 10),
                Offcut(PanelReference(0, 0), 400, 0, 100, 10),
                Offcut(PanelReference(0, 0), 400, 0, 50, 40),
                Offcut(PanelReference(0, 0), 400, 0, 200, 100),
            ),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    window.services.preferences.update(
        replace(window.services.preferences.current, language="en", units="mm")
    )
    window._retranslate_ui()
    assert label.text() == "gmas 2.24"
    assert window._solution_offcut_aspect_average_label.text() == "asav 3.56"
    assert window._solution_offcut_aspect_median_label.text() == "mdas 1.25"
    assert window._solution_offcut_aspect_stddev_label.text() == "sdas 3.73"
    assert "geometric" in label.toolTip().casefold()
    assert "click" not in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert "mm" not in label.text()
