"""Timeline list keyboard shortcuts drive placement replay."""

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from boardcomposer.domain import AssemblySolution, BoardPlacement
from studio.events.event_bus import EventBus
from studio.timeline.panel import TimelinePanel
from studio.timeline.store import TimelineStore


def _solution(count: int = 3) -> AssemblySolution:
    placements = [
        BoardPlacement(f"P-{index}", float(index * 10), 0.0, 100.0, 50.0)
        for index in range(count)
    ]
    return AssemblySolution(placements=placements)


def _panel(qapp) -> TimelinePanel:
    del qapp
    store = TimelineStore(EventBus())
    panel = TimelinePanel(store, language="es")
    panel.set_replay_solution(_solution())
    panel._list.setFocus()
    return panel


def _press(panel: TimelinePanel, key: Qt.Key) -> None:
    event = QKeyEvent(QEvent.Type.KeyPress, key, Qt.KeyboardModifier.NoModifier)
    assert QApplication.sendEvent(panel._list, event)


def test_timeline_replay_shortcuts_step_and_reset(qapp):
    panel = _panel(qapp)
    assert panel._replay.step == 3

    _press(panel, Qt.Key.Key_Home)
    assert panel._replay.step == 0

    _press(panel, Qt.Key.Key_Right)
    assert panel._replay.step == 1

    _press(panel, Qt.Key.Key_Right)
    assert panel._replay.step == 2

    _press(panel, Qt.Key.Key_Left)
    assert panel._replay.step == 1


def test_timeline_replay_shortcut_space_toggles_play(qapp):
    panel = _panel(qapp)
    panel._on_replay_reset()
    assert not panel._replay.playing

    _press(panel, Qt.Key.Key_Space)
    assert panel._replay.playing

    _press(panel, Qt.Key.Key_Space)
    assert not panel._replay.playing


def test_timeline_replay_shortcuts_ignored_without_solution(qapp):
    del qapp
    panel = TimelinePanel(TimelineStore(EventBus()), language="es")
    panel._list.setFocus()
    _press(panel, Qt.Key.Key_Right)
    assert panel._replay.step == 0
    assert not panel._replay.available
