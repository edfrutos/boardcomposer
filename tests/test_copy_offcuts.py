"""Copy the status-bar offcut count (IDE-0093)."""

from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution
from studio.main_window import MainWindow
from studio.preferences import PreferencesManager, StudioPreferences
from studio.services import StudioServices
from tests.test_inspector_board_utilization import _window
from tests.test_offcuts_status import _offcut


def test_copy_offcuts_uses_the_status_count(qapp, tmp_path):
    del qapp
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "empty-preferences.json")
    )
    services.preferences.update(StudioPreferences(language="es"))
    empty = MainWindow(services)
    action = empty._actions["copy_offcuts"]
    assert "Ctrl+Alt+Shift+R" in action.shortcut().toString()
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    clipboard.setText("keep-me")
    assert not action.isEnabled()
    empty._copy_offcuts()
    assert clipboard.text() == "keep-me"
    assert empty.statusBar().currentMessage() == empty._tr(
        "status.nothing_to_copy_offcuts"
    )

    window = _window(tmp_path)
    action = window._actions["copy_offcuts"]
    assert not action.isEnabled()
    calls: list[str] = []
    window._promote_offcuts = lambda: calls.append("promote")
    window._copy_offcuts()
    assert calls == []
    assert clipboard.text() == "keep-me"

    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=(_offcut(0), _offcut(1))),
        AssemblySolution(placements=[], offcuts=(_offcut(0),)),
    ]
    window._select_layout_solution(0)
    assert action.isEnabled()
    action.trigger()
    assert calls == []
    assert clipboard.text() == "2"
    assert window.statusBar().currentMessage() == window._tr(
        "status.offcuts_copied", n="2"
    )

    window._select_layout_solution(1)
    action.trigger()
    assert calls == []
    assert clipboard.text() == "1"

    window.services.layout.solutions = [
        AssemblySolution(placements=[], offcuts=()),
    ]
    window.services.layout.selected_solution_index = 0
    window._update_offcuts_status()
    assert not action.isEnabled()
    clipboard.setText("keep-me")
    window._copy_offcuts()
    assert calls == []
    assert clipboard.text() == "keep-me"
