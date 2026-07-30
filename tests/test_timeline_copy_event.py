"""Timeline context-menu / Ctrl+C copy selected event text."""

import json

from PySide6.QtCore import QEvent, Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import QApplication

from studio.events.catalog import PROJECT_CREATED, TIMELINE_MARKED
from studio.events.event_bus import EventBus
from studio.timeline.panel import TimelinePanel
from studio.timeline.store import TimelineStore


def _panel_with_events(qapp) -> TimelinePanel:
    del qapp
    bus = EventBus()
    store = TimelineStore(bus)
    panel = TimelinePanel(store, language="es")
    bus.publish(PROJECT_CREATED, {"kind": "demo"})
    bus.publish(TIMELINE_MARKED, {"note": "checkpoint", "piece": "A"})
    # Select the latest real event (skip empty placeholder if present).
    for index in range(panel._list.count() - 1, -1, -1):
        item = panel._list.item(index)
        if item is not None and isinstance(item.data(Qt.ItemDataRole.UserRole), int):
            panel._list.setCurrentItem(item)
            break
    panel._list.setFocus()
    return panel


def test_timeline_copy_selected_line_to_clipboard(qapp):
    panel = _panel_with_events(qapp)
    messages: list[str] = []
    panel.status_requested.connect(messages.append)

    item = panel._list.currentItem()
    assert item is not None
    assert panel._copy_selected_event_line() is True

    clipboard = QApplication.clipboard()
    assert clipboard is not None
    assert clipboard.text() == item.text()
    assert messages and "portapapeles" in messages[-1].lower()


def test_timeline_copy_payload_json(qapp):
    panel = _panel_with_events(qapp)
    item = panel._list.currentItem()
    entry = panel._entry_from_item(item)
    assert entry is not None
    assert entry.event_name == TIMELINE_MARKED

    panel._copy_text_to_clipboard(
        json.dumps(entry.payload, ensure_ascii=False, indent=2)
    )
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    assert '"note": "checkpoint"' in clipboard.text()
    assert '"piece": "A"' in clipboard.text()


def test_timeline_ctrl_c_copies_selected_line(qapp):
    panel = _panel_with_events(qapp)
    item = panel._list.currentItem()
    assert item is not None

    event = QKeyEvent(
        QEvent.Type.KeyPress,
        Qt.Key.Key_C,
        Qt.KeyboardModifier.ControlModifier,
    )
    assert QApplication.sendEvent(panel._list, event)
    clipboard = QApplication.clipboard()
    assert clipboard is not None
    assert clipboard.text() == item.text()
