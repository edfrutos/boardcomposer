"""Timeline dock panel for Studio (ADR-005)."""

from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from studio.events.catalog import ALL_EVENTS, CATALOG
from studio.i18n import tr
from studio.timeline.store import TimelineEntry, TimelineStore


class TimelinePanel(QWidget):
    """Chronological list of Event Bus facts with optional type filter."""

    def __init__(self, store: TimelineStore, language: str = "es", parent=None) -> None:
        super().__init__(parent)
        self._store = store
        self._language = language
        self._filter_event: str | None = None

        self._filter_label = QLabel()
        self._filter = QComboBox()
        self._filter.currentIndexChanged.connect(self._on_filter_changed)
        self._clear = QPushButton()
        self._clear.clicked.connect(self._on_clear)

        controls = QHBoxLayout()
        controls.addWidget(self._filter_label)
        controls.addWidget(self._filter, stretch=1)
        controls.addWidget(self._clear)

        self._list = QListWidget()
        self._list.setUniformItemSizes(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addLayout(controls)
        layout.addWidget(self._list)

        self.retranslate(language)
        self._rebuild()
        self._store.add_listener(self._on_entry)

    def retranslate(self, language: str) -> None:
        self._language = language
        self._filter_label.setText(tr("timeline.filter", language))
        self._clear.setText(tr("timeline.clear", language))
        self._rebuild_filter_items()
        self._rebuild()

    def _rebuild_filter_items(self) -> None:
        current = self._filter.currentData()
        self._filter.blockSignals(True)
        self._filter.clear()
        self._filter.addItem(tr("timeline.filter_all", self._language), ALL_EVENTS)
        for name in CATALOG:
            label = tr(f"timeline.event.{name}", self._language)
            self._filter.addItem(label, name)
        if current is not None:
            index = self._filter.findData(current)
            self._filter.setCurrentIndex(index if index >= 0 else 0)
        self._filter.blockSignals(False)
        data = self._filter.currentData()
        self._filter_event = None if data == ALL_EVENTS else data

    def _on_filter_changed(self, _index: int) -> None:
        data = self._filter.currentData()
        self._filter_event = None if data == ALL_EVENTS else data
        self._rebuild()

    def _on_clear(self) -> None:
        self._store.clear()
        self._rebuild()

    def _on_entry(self, entry: TimelineEntry) -> None:
        if self._filter_event and entry.event_name != self._filter_event:
            return
        self._list.addItem(self._item_for(entry))
        self._list.scrollToBottom()

    def _rebuild(self) -> None:
        self._list.clear()
        for entry in self._store.filtered(self._filter_event):
            self._list.addItem(self._item_for(entry))
        if self._list.count() == 0:
            empty = QListWidgetItem(tr("timeline.empty", self._language))
            empty.setFlags(Qt.ItemFlag.NoItemFlags)
            self._list.addItem(empty)
        else:
            self._list.scrollToBottom()

    def _item_for(self, entry: TimelineEntry) -> QListWidgetItem:
        local = entry.timestamp.astimezone()
        time_text = local.strftime("%H:%M:%S")
        label = tr(f"timeline.event.{entry.event_name}", self._language)
        detail = _format_payload(entry.payload, self._language)
        text = f"{time_text}  ·  {label}"
        if detail:
            text = f"{text}  —  {detail}"
        item = QListWidgetItem(text)
        item.setData(Qt.ItemDataRole.UserRole, entry.sequence)
        return item


def _format_payload(payload: dict, language: str) -> str:
    if not payload:
        return ""
    parts: list[str] = []
    if "path" in payload:
        parts.append(str(payload["path"]))
    if "name" in payload:
        parts.append(str(payload["name"]))
    if "format" in payload:
        parts.append(str(payload["format"]))
    if "count" in payload:
        parts.append(tr("timeline.detail.count", language, n=payload["count"]))
    if "index" in payload:
        parts.append(tr("timeline.detail.index", language, n=payload["index"]))
    if "status" in payload:
        parts.append(str(payload["status"]))
    if "kind" in payload:
        parts.append(str(payload["kind"]))
    if "strategy" in payload:
        parts.append(str(payload["strategy"]))
    return ", ".join(parts)
