"""Status bar shows the mean-area offcut's aspect ratio (IDE-0226)."""

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


def test_solution_mean_offcut_aspect_follows_the_selected_solution(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    empty_label = empty._solution_mean_offcut_aspect_label
    assert empty_label.objectName() == "statusSolutionMeanOffcutAspect"
    assert empty_label.isHidden()
    assert empty_label.cursor().shape() == Qt.CursorShape.ArrowCursor

    window = _window(tmp_path)
    label = window._solution_mean_offcut_aspect_label
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
                Offcut(PanelReference(0, 0), 400, 0, 40, 40),
                Offcut(PanelReference(0, 0), 400, 0, 50, 50),
                Offcut(PanelReference(0, 0), 400, 0, 100, 40),
                Offcut(PanelReference(0, 0), 400, 0, 200, 100),
            ),
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert label.isHidden()
    assert window._solution_mean_offcut_size_label.isHidden()
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
    assert label.text() == "rela. 2.50"
    assert not label.isHidden()
    assert window._solution_largest_offcut_aspect_label.text() == "relr. 2.00"
    assert window._solution_smallest_offcut_aspect_label.text() == "relm. 1.00"
    assert window._solution_median_offcut_aspect_label.text() == "reln. 2.50"
    assert window._solution_mean_offcut_size_label.text() == "mdds. 100 x 40 mm"
    assert label.text() != window._solution_largest_offcut_aspect_label.text()
    assert label.text() != window._solution_smallest_offcut_aspect_label.text()
    assert label.text() != window._solution_median_offcut_aspect_label.text()
    assert label.text() != window._solution_mean_offcut_size_label.text()
    assert "mm" not in label.text()
    assert "relación" in label.toolTip().casefold()
    assert "clic" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    assert calls == []
    assert window.services.layout.selected_solution_index == 1
    assert window.workspace.zoom == zoom

    window._select_layout_solution(2)
    assert label.text() == "rela. 2.50"
    assert window._solution_median_offcut_aspect_label.text() == "reln. 1.00"
    assert window._solution_largest_offcut_aspect_label.text() == "relr. 2.00"
    assert window._solution_smallest_offcut_aspect_label.text() == "relm. 1.00"
    assert window._solution_mean_offcut_size_label.text() == "mdds. 100 x 40 mm"
    assert window._solution_median_offcut_size_label.text() == "mdnd. 50 x 50 mm"
    assert label.text() != window._solution_median_offcut_aspect_label.text()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(
                Offcut(PanelReference(0, 0), 400, 0, 100, 10),
                Offcut(PanelReference(0, 0), 400, 0, 30, 100),
            ),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    assert label.text() == "rela. 3.33"
    assert window._solution_mean_offcut_size_label.text() == "mdds. 30 x 100 mm"
    assert window._solution_largest_offcut_aspect_label.text() == "relr. 3.33"
    assert window._solution_smallest_offcut_aspect_label.text() == "relm. 10.00"
    assert window._solution_median_offcut_aspect_label.text() == "reln. 10.00"
    assert label.text() != window._solution_median_offcut_aspect_label.text()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 50, 50),),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()
    assert label.text() == "rela. 1.00"
    assert window._solution_mean_offcut_size_label.text() == "mdds. 50 x 50 mm"

    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert label.text() == "rela. 1.00"
    assert "1.00" in label.toolTip()
    assert window._solution_mean_offcut_size_label.text() == "mdds. 5 x 5 cm"

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert label.isHidden()
    assert label.cursor().shape() == Qt.CursorShape.ArrowCursor
    assert window._solution_label.isHidden()

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(
                Offcut(PanelReference(0, 0), 400, 0, 40, 40),
                Offcut(PanelReference(0, 0), 400, 0, 50, 50),
                Offcut(PanelReference(0, 0), 400, 0, 100, 40),
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
    assert label.text() == "aspa 2.50"
    assert window._solution_median_offcut_aspect_label.text() == "aspm 1.00"
    assert window._solution_largest_offcut_aspect_label.text() == "aspr 2.00"
    assert window._solution_smallest_offcut_aspect_label.text() == "asps 1.00"
    assert window._solution_mean_offcut_size_label.text() == "avgd 100 x 40 mm"
    assert "aspect ratio" in label.toolTip().casefold()
    assert "click" in label.toolTip().casefold()
    assert label.cursor().shape() == Qt.CursorShape.PointingHandCursor
    assert "mm" not in label.text()
