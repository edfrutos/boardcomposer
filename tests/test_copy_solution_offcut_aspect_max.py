"""Copy the status-bar maximum offcut aspect ratio (IDE-0245)."""

from dataclasses import replace

import pytest
from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
from studio.keyboard_shortcuts import STUDIO_SHORTCUTS
from studio.main_window import MainWindow
from tests.test_inspector_board_utilization import _window

ACTION = "copy_solution_offcut_aspect_max"
NOTHING = "status.nothing_to_copy_solution_offcut_aspect_max"


@pytest.fixture
def clipboard(qapp):
    del qapp
    board = QApplication.clipboard()
    assert board is not None
    board.setText("keep-me")
    return board


def _select(window: MainWindow, *sizes: tuple[float, float]) -> None:
    window.services.layout.solutions = [
        AssemblySolution(
            placements=[],
            offcuts=tuple(
                Offcut(PanelReference(0, 0), 400, 0, length, width)
                for length, width in sizes
            ),
        )
    ]
    window.services.layout.selected_solution_index = 0
    window._update_solution_status()


def test_copy_offcut_aspect_max_is_menu_only(qapp, tmp_path):
    del qapp
    window = _window(tmp_path)
    action = window._actions[ACTION]
    assert action in window._menus["edit"].actions()
    assert action.shortcuts() == []
    assert ACTION not in {binding.action_key for binding in STUDIO_SHORTCUTS}

    _select(window, (100, 10))
    assert action.statusTip() == window._tr(f"tip.{ACTION}")
    assert "Ctrl" not in window._tr(f"tip.{ACTION}")


def test_copy_offcut_aspect_max_copies_the_formatted_value(clipboard, tmp_path):
    window = _window(tmp_path)
    action = window._actions[ACTION]
    calls: list[str] = []
    window._step_layout_solution = lambda _delta: calls.append("step")
    _select(window, (10, 10), (100, 10), (50, 40), (200, 100))
    zoom = window.workspace.zoom

    assert window._solution_offcut_aspect_max_label.text() == "xrel. 10.00"
    assert action.isEnabled()
    action.trigger()
    assert clipboard.text() == "10.00"
    assert window.statusBar().currentMessage() == window._tr(
        "status.solution_offcut_aspect_max_copied", value="10.00"
    )
    assert calls == []
    assert window.services.layout.selected_solution_index == 0
    assert window.workspace.zoom == zoom


def test_copy_offcut_aspect_max_is_disabled_when_the_label_is_hidden(
    clipboard, tmp_path
):
    window = _window(tmp_path)
    action = window._actions[ACTION]
    assert not action.isEnabled()

    _select(window, (100, 40))
    assert action.isEnabled()

    _select(window)
    assert window._solution_offcut_aspect_max_label.isHidden()
    assert not action.isEnabled()
    assert action.statusTip() == window._tr(NOTHING)
    window._copy_solution_offcut_aspect_max()
    assert clipboard.text() == "keep-me"
    assert window.statusBar().currentMessage() == window._tr(NOTHING)

    _select(window, (100, 40))
    window.services.layout.selected_solution_index = 9
    window._update_solution_status()
    assert not action.isEnabled()
    window._copy_solution_offcut_aspect_max()
    assert clipboard.text() == "keep-me"


def test_copy_offcut_aspect_max_ignores_units_and_language(clipboard, tmp_path):
    window = _window(tmp_path)
    action = window._actions[ACTION]
    _select(window, (100, 40))
    window.services.preferences.update(
        replace(window.services.preferences.current, units="cm", language="en")
    )
    window._retranslate_ui()

    assert window._solution_offcut_aspect_max_label.text() == "mxas 2.50"
    assert action.text() == "Copy maximum offcut aspect ratio of the solution"
    assert action.isEnabled()
    assert action.statusTip() == window._tr(f"tip.{ACTION}")
    action.trigger()
    assert clipboard.text() == "2.50"
