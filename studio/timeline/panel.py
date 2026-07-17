"""Timeline dock panel for Studio (ADR-005)."""

from __future__ import annotations

from PySide6.QtCore import Qt, QTimer, Signal
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

from boardcomposer.domain import AssemblySolution
from studio.events.catalog import ALL_EVENTS, CATALOG
from studio.i18n import tr
from studio.timeline.replay import SolutionReplay
from studio.timeline.store import TimelineEntry, TimelineStore

_PLAY_INTERVAL_MS = 450


class TimelinePanel(QWidget):
    """Chronological event list plus placement replay controls."""

    replay_step_changed = Signal(object, int)
    """Emitted as ``(solution | None, reveal_count)`` when the replay step changes."""

    def __init__(self, store: TimelineStore, language: str = "es", parent=None) -> None:
        super().__init__(parent)
        self._store = store
        self._language = language
        self._filter_event: str | None = None
        self._replay = SolutionReplay()

        self._filter_label = QLabel()
        self._filter = QComboBox()
        self._filter.currentIndexChanged.connect(self._on_filter_changed)
        self._clear = QPushButton()
        self._clear.clicked.connect(self._on_clear)

        controls = QHBoxLayout()
        controls.addWidget(self._filter_label)
        controls.addWidget(self._filter, stretch=1)
        controls.addWidget(self._clear)

        self._replay_label = QLabel()
        self._replay_reset = QPushButton()
        self._replay_back = QPushButton()
        self._replay_forward = QPushButton()
        self._replay_play = QPushButton()
        self._replay_reset.clicked.connect(self._on_replay_reset)
        self._replay_back.clicked.connect(self._on_replay_back)
        self._replay_forward.clicked.connect(self._on_replay_forward)
        self._replay_play.clicked.connect(self._on_replay_play)

        replay_row = QHBoxLayout()
        replay_row.addWidget(self._replay_label)
        replay_row.addStretch(1)
        replay_row.addWidget(self._replay_reset)
        replay_row.addWidget(self._replay_back)
        replay_row.addWidget(self._replay_forward)
        replay_row.addWidget(self._replay_play)

        self._list = QListWidget()
        self._list.setUniformItemSizes(True)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addLayout(controls)
        layout.addLayout(replay_row)
        layout.addWidget(self._list)

        self._play_timer = QTimer(self)
        self._play_timer.setInterval(_PLAY_INTERVAL_MS)
        self._play_timer.timeout.connect(self._on_play_tick)

        self.retranslate(language)
        self._rebuild()
        self._update_replay_controls()
        self._store.add_listener(self._on_entry)

    def retranslate(self, language: str) -> None:
        self._language = language
        self._filter_label.setText(tr("timeline.filter", language))
        self._clear.setText(tr("timeline.clear", language))
        self._replay_reset.setText(tr("timeline.replay_reset", language))
        self._replay_back.setText(tr("timeline.replay_back", language))
        self._replay_forward.setText(tr("timeline.replay_forward", language))
        self._rebuild_filter_items()
        self._rebuild()
        self._update_replay_controls()

    def set_replay_solution(self, solution: AssemblySolution | None) -> None:
        """Bind the selected layout solution for placement walkthrough."""
        self._replay.load(solution)
        self._play_timer.stop()
        self._update_replay_controls()

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

    def _on_replay_reset(self) -> None:
        step = self._replay.reset()
        self._emit_replay(step)

    def _on_replay_back(self) -> None:
        step = self._replay.step_back()
        self._emit_replay(step)

    def _on_replay_forward(self) -> None:
        step = self._replay.step_forward()
        self._emit_replay(step)

    def _on_replay_play(self) -> None:
        if self._replay.playing:
            self._replay.stop()
            self._play_timer.stop()
            self._update_replay_controls()
            return
        self._replay.start()
        self._emit_replay(self._replay.step)
        if self._replay.playing:
            self._play_timer.start()
        self._update_replay_controls()

    def _on_play_tick(self) -> None:
        if not self._replay.playing:
            self._play_timer.stop()
            self._update_replay_controls()
            return
        step = self._replay.step_forward()
        self._emit_replay(step)
        if not self._replay.playing:
            self._play_timer.stop()

    def _emit_replay(self, step: int) -> None:
        self._update_replay_controls()
        self.replay_step_changed.emit(self._replay.solution, step)

    def _update_replay_controls(self) -> None:
        available = self._replay.available
        self._replay_reset.setEnabled(available)
        self._replay_back.setEnabled(available and self._replay.step > 0)
        self._replay_forward.setEnabled(
            available and self._replay.step < self._replay.total
        )
        self._replay_play.setEnabled(available)
        play_key = (
            "timeline.replay_pause" if self._replay.playing else "timeline.replay_play"
        )
        self._replay_play.setText(tr(play_key, self._language))
        if available:
            algorithm = self._replay.algorithm or tr(
                "timeline.replay_algorithm_unknown",
                self._language,
            )
            piece = self._replay.current_piece_id
            if piece:
                self._replay_label.setText(
                    tr(
                        "timeline.replay_progress_algo_piece",
                        self._language,
                        algorithm=algorithm,
                        piece=piece,
                        current=self._replay.step,
                        total=self._replay.total,
                    )
                )
            else:
                self._replay_label.setText(
                    tr(
                        "timeline.replay_progress_algo",
                        self._language,
                        algorithm=algorithm,
                        current=self._replay.step,
                        total=self._replay.total,
                    )
                )
        else:
            self._replay_label.setText(tr("timeline.replay_none", self._language))


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
    if "algorithm" in payload:
        parts.append(str(payload["algorithm"]))
    if "accepted" in payload:
        parts.append(tr("timeline.detail.accepted", language, n=payload["accepted"]))
    if "rejected" in payload:
        parts.append(tr("timeline.detail.rejected", language, n=payload["rejected"]))
    return ", ".join(parts)
