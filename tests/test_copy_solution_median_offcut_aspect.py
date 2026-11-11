"""Copy the status-bar median-area offcut aspect ratio (IDE-0224)."""

from dataclasses import replace

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window


def test_copy_solution_median_offcut_aspect_uses_the_formatted_ratio(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_solution_median_offcut_aspect"]
    shortcut = action.shortcut().toString()
    assert "Ctrl+Alt+Shift+" in shortcut
    assert "," in shortcut or "Comma" in shortcut
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_solution_median_offcut_aspect()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_solution_median_offcut_aspect"
    )

    window = _window(tmp_path)
    action = window._actions["copy_solution_median_offcut_aspect"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    window._copy_solution_median_offcut_aspect()
    assert calls == []
    assert clipboard.text() == "keep-me"

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
                Offcut(PanelReference(0, 0), 400, 0, 100, 100),
                Offcut(PanelReference(0, 0), 400, 0, 200, 50),
            ),
        ),
        AssemblySolution(
            placements=[],
            offcuts=(Offcut(PanelReference(0, 0), 400, 0, 50, 200),),
        ),
    ]
    window._select_layout_solution(0)
    zoom = window.workspace.zoom
    assert window._solution_median_offcut_aspect_label.isHidden()
    assert not action.isEnabled()
    window._copy_solution_median_offcut_aspect()
    assert calls == []
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(
        "status.nothing_to_copy_solution_median_offcut_aspect"
    )

    window._select_layout_solution(1)
    assert window._solution_median_offcut_aspect_label.text() == "reln. 2.50"
    assert window._solution_largest_offcut_aspect_label.text() == "relr. 2.00"
    assert window._solution_smallest_offcut_aspect_label.text() == "relm. 1.00"
    assert window._solution_median_offcut_size_label.text() == "mdnd. 100 x 40 mm"
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "2.50"
    assert "reln." not in clipboard.text()
    assert clipboard.text() != "2.00"
    assert clipboard.text() != "1.00"
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_median_offcut_aspect_copied", value="2.50"
    )
    assert window.services.layout.selected_solution_index == 1
    assert window.workspace.zoom == zoom

    window._select_layout_solution(2)
    assert window._solution_median_offcut_aspect_label.text() == "reln. 1.00"
    assert window._solution_largest_offcut_aspect_label.text() == "relr. 4.00"
    assert window._solution_smallest_offcut_aspect_label.text() == "relm. 1.00"
    action.trigger()
    assert clipboard.text() == "1.00"
    assert "reln." not in clipboard.text()
    assert calls == []

    window._select_layout_solution(3)
    assert window._solution_median_offcut_aspect_label.text() == "reln. 4.00"
    assert window._solution_median_offcut_size_label.text() == "mdnd. 50 x 200 mm"
    action.trigger()
    assert clipboard.text() == "4.00"
    assert calls == []

    window._select_layout_solution(1)
    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm")
    )
    window._retranslate_ui()
    assert window._solution_median_offcut_aspect_label.text() == "reln. 2.50"
    assert window._solution_median_offcut_size_label.text() == "mdnd. 10 x 4 cm"
    action.trigger()
    assert clipboard.text() == "2.50"
    assert calls == []

    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_solution_median_offcut_aspect()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=(
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
    assert window._solution_median_offcut_aspect_label.text() == "aspm 2.50"
    assert window._solution_largest_offcut_aspect_label.text() == "aspr 2.00"
    assert window._solution_smallest_offcut_aspect_label.text() == "asps 1.00"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "2.50"
    assert "aspm" not in clipboard.text()
    assert calls == []
