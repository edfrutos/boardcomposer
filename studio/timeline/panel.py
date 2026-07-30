"""Timeline dock panel for Studio (ADR-005)."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone

from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from boardcomposer.domain import AssemblySolution
from boardcomposer.solver.solve_trace import SolveTrace
from studio.events.catalog import ALL_EVENTS, CATALOG, PIECE_MOVED, TIMELINE_MARKED
from studio.i18n import tr
from studio.timeline.phase_replay import SolvePhaseReplay
from studio.timeline.replay import SolutionReplay
from studio.timeline.store import TimelineEntry, TimelineStore

_PLAY_INTERVAL_MS = 450
_ALL_ALGORITHMS = "__all_algorithms__"
_MODE_PLACEMENTS = "placements"
_MODE_PHASES = "phases"
_PERIOD_OPTIONS: tuple[tuple[int | None, str], ...] = (
    (None, "timeline.filter_period_all"),
    (60, "timeline.filter_period_1m"),
    (300, "timeline.filter_period_5m"),
    (900, "timeline.filter_period_15m"),
    (3600, "timeline.filter_period_1h"),
)


class TimelinePanel(QWidget):
    """Chronological event list plus placement replay controls."""

    replay_step_changed = Signal(object, int)
    """Emitted as ``(solution | None, reveal_count)`` when the replay step changes."""

    phase_step_changed = Signal(object, int)
    """Emitted as ``(TraceEvent | None, step)`` when the phase replay step changes."""

    entry_selected = Signal(object)
    """Emitted as ``TimelineEntry`` when the user clicks an event in the list."""

    export_requested = Signal()
    """Ask the main window to run the Timeline history export dialog."""
    filters_changed = Signal()
    """Notify parent UI that filter-dependent actions should refresh."""

    def __init__(self, store: TimelineStore, language: str = "es", parent=None) -> None:
        super().__init__(parent)
        self._store = store
        self._language = language
        self._filter_event: str | None = None
        self._filter_algorithm: str | None = None
        self._filter_period_seconds: int | None = None
        self._replay_mode = _MODE_PLACEMENTS
        self._replay = SolutionReplay()
        self._phase_replay = SolvePhaseReplay()

        self._filter_label = QLabel()
        self._filter = QComboBox()
        self._filter.currentIndexChanged.connect(self._on_filter_changed)
        self._algo_label = QLabel()
        self._algo_filter = QComboBox()
        self._algo_filter.currentIndexChanged.connect(self._on_algo_filter_changed)
        self._period_label = QLabel()
        self._period_filter = QComboBox()
        self._period_filter.currentIndexChanged.connect(self._on_period_changed)
        self._clear = QPushButton()
        self._clear.clicked.connect(self._on_clear)
        self._mark = QPushButton()
        self._mark.clicked.connect(self._on_mark_clicked)
        self._export = QPushButton()
        self._export.clicked.connect(self._on_export_clicked)
        self._piece_moves = QPushButton()
        self._piece_moves.setCheckable(True)
        self._piece_moves.clicked.connect(self._on_piece_moves_clicked)

        filters = QHBoxLayout()
        filters.addWidget(self._filter_label)
        filters.addWidget(self._filter, stretch=1)
        filters.addWidget(self._algo_label)
        filters.addWidget(self._algo_filter, stretch=1)
        filters.addWidget(self._period_label)
        filters.addWidget(self._period_filter, stretch=1)

        actions = QHBoxLayout()
        actions.addStretch(1)
        actions.addWidget(self._piece_moves)
        actions.addWidget(self._mark)
        actions.addWidget(self._export)
        actions.addWidget(self._clear)

        self._mode_label = QLabel()
        self._mode = QComboBox()
        self._mode.currentIndexChanged.connect(self._on_mode_changed)
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
        replay_row.addWidget(self._mode_label)
        replay_row.addWidget(self._mode)
        replay_row.addWidget(self._replay_label, stretch=1)
        replay_row.addWidget(self._replay_reset)
        replay_row.addWidget(self._replay_back)
        replay_row.addWidget(self._replay_forward)
        replay_row.addWidget(self._replay_play)

        self._list = QListWidget()
        self._list.setUniformItemSizes(True)
        self._list.itemClicked.connect(self._on_item_clicked)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.addLayout(filters)
        layout.addLayout(actions)
        layout.addLayout(replay_row)
        layout.addWidget(self._list)

        self._play_timer = QTimer(self)
        self._play_timer.setInterval(_PLAY_INTERVAL_MS)
        self._play_timer.timeout.connect(self._on_play_tick)

        self.retranslate(language)
        self._rebuild()
        self._update_replay_controls()
        self._sync_event_actions()
        self._store.add_listener(self._on_entry)
        self._store.add_changed_listener(self._sync_event_actions)

    def retranslate(self, language: str) -> None:
        self._language = language
        self._filter_label.setText(tr("timeline.filter", language))
        self._algo_label.setText(tr("timeline.filter_algorithm", language))
        self._period_label.setText(tr("timeline.filter_period", language))
        self._mode_label.setText(tr("timeline.replay_mode", language))
        self._clear.setText(tr("timeline.clear", language))
        self._mark.setText(tr("timeline.mark", language))
        self._export.setText(tr("timeline.export", language))
        self._piece_moves.setText(tr("timeline.filter_piece_moves", language))
        self._sync_event_actions()
        self._replay_reset.setText(tr("timeline.replay_reset", language))
        self._replay_back.setText(tr("timeline.replay_back", language))
        self._replay_forward.setText(tr("timeline.replay_forward", language))
        self._rebuild_filter_items()
        self._rebuild_algorithm_items()
        self._rebuild_period_items()
        self._rebuild_mode_items()
        self._rebuild()
        self._update_replay_controls()

    def set_replay_solution(self, solution: AssemblySolution | None) -> None:
        """Bind the selected layout solution for placement walkthrough."""
        self._replay.load(solution)
        self._play_timer.stop()
        self._update_replay_controls()

    def set_phase_trace(self, trace: SolveTrace | None) -> None:
        """Bind the last solve trace for algorithm-phase walkthrough."""
        self._phase_replay.load(trace)
        self._play_timer.stop()
        self._update_replay_controls()

    def _rebuild_mode_items(self) -> None:
        current = self._replay_mode
        self._mode.blockSignals(True)
        self._mode.clear()
        self._mode.addItem(
            tr("timeline.replay_mode_placements", self._language),
            _MODE_PLACEMENTS,
        )
        self._mode.addItem(
            tr("timeline.replay_mode_phases", self._language),
            _MODE_PHASES,
        )
        index = self._mode.findData(current)
        self._mode.setCurrentIndex(index if index >= 0 else 0)
        self._mode.blockSignals(False)
        data = self._mode.currentData()
        self._replay_mode = data if isinstance(data, str) else _MODE_PLACEMENTS

    def _on_mode_changed(self, _index: int) -> None:
        data = self._mode.currentData()
        self._replay_mode = data if isinstance(data, str) else _MODE_PLACEMENTS
        self._play_timer.stop()
        self._replay.stop()
        self._phase_replay.stop()
        self._update_replay_controls()
        if self._replay_mode == _MODE_PHASES:
            self.phase_step_changed.emit(
                self._phase_replay.current,
                self._phase_replay.step,
            )
        else:
            self.replay_step_changed.emit(self._replay.solution, self._replay.step)

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

    def _rebuild_algorithm_items(self) -> None:
        current = self._filter_algorithm
        self._algo_filter.blockSignals(True)
        self._algo_filter.clear()
        self._algo_filter.addItem(
            tr("timeline.filter_algorithm_all", self._language),
            _ALL_ALGORITHMS,
        )
        for name in self._store.algorithms():
            self._algo_filter.addItem(name, name)
        if current:
            index = self._algo_filter.findData(current)
            self._algo_filter.setCurrentIndex(index if index >= 0 else 0)
        self._algo_filter.blockSignals(False)
        data = self._algo_filter.currentData()
        self._filter_algorithm = None if data == _ALL_ALGORITHMS else data

    def _rebuild_period_items(self) -> None:
        current = self._filter_period_seconds
        self._period_filter.blockSignals(True)
        self._period_filter.clear()
        for seconds, key in _PERIOD_OPTIONS:
            self._period_filter.addItem(tr(key, self._language), seconds)
        if current is not None:
            index = self._period_filter.findData(current)
            self._period_filter.setCurrentIndex(index if index >= 0 else 0)
        self._period_filter.blockSignals(False)
        data = self._period_filter.currentData()
        self._filter_period_seconds = data if isinstance(data, int) else None

    def _filter_since(self) -> datetime | None:
        if self._filter_period_seconds is None:
            return None
        return datetime.now(timezone.utc) - timedelta(
            seconds=self._filter_period_seconds
        )

    def _on_filter_changed(self, _index: int) -> None:
        data = self._filter.currentData()
        self._filter_event = None if data == ALL_EVENTS else data
        self._rebuild()
        self._sync_event_actions()
        self.filters_changed.emit()

    def _on_algo_filter_changed(self, _index: int) -> None:
        data = self._algo_filter.currentData()
        self._filter_algorithm = None if data == _ALL_ALGORITHMS else data
        self._rebuild()
        self._sync_event_actions()
        self.filters_changed.emit()

    def _on_period_changed(self, _index: int) -> None:
        data = self._period_filter.currentData()
        self._filter_period_seconds = data if isinstance(data, int) else None
        self._rebuild()
        self._sync_event_actions()
        self.filters_changed.emit()

    def _on_clear(self) -> None:
        self._store.clear()
        self._rebuild_algorithm_items()
        self._rebuild()

    def _on_export_clicked(self) -> None:
        self.export_requested.emit()

    def _on_piece_moves_clicked(self) -> None:
        target = ALL_EVENTS if self._filter_event == PIECE_MOVED else PIECE_MOVED
        index = self._filter.findData(target)
        if index >= 0:
            self._filter.setCurrentIndex(index)

    def _sync_event_actions(self) -> None:
        """Enable Export/Clear only when the Timeline has events."""
        has_visible_events = bool(
            self._store.filtered(
                self._filter_event,
                algorithm=self._filter_algorithm,
                since=self._filter_since(),
            )
        )
        self._export.setEnabled(has_visible_events)
        export_tip = tr(
            "tip.export_timeline"
            if has_visible_events
            else "status.timeline_export_empty",
            self._language,
        )
        self._export.setToolTip(export_tip)
        self._export.setStatusTip(export_tip)

        has_any_events = bool(self._store.entries)
        self._clear.setEnabled(has_any_events)
        clear_tip = tr(
            "tip.timeline_clear" if has_any_events else "status.timeline_clear_empty",
            self._language,
        )
        self._clear.setToolTip(clear_tip)
        self._clear.setStatusTip(clear_tip)
        self._piece_moves.setChecked(self._filter_event == PIECE_MOVED)
        self._piece_moves.setToolTip(tr("timeline.filter_piece_moves", self._language))
        self._piece_moves.setStatusTip(
            tr("timeline.filter_piece_moves", self._language)
        )

    def _on_mark_clicked(self) -> None:
        note, ok = QInputDialog.getText(
            self,
            tr("timeline.mark_dialog_title", self._language),
            tr("timeline.mark_dialog_label", self._language),
        )
        if not ok:
            return
        text = note.strip()
        if not text:
            return
        payload: dict[str, object] = {"note": text}
        if self._replay.available:
            payload["step"] = self._replay.step
            if self._replay.algorithm:
                payload["algorithm"] = self._replay.algorithm
            piece = self._replay.current_piece_id
            if piece:
                payload["piece"] = piece
        self._store.bus.publish(TIMELINE_MARKED, payload)

    def current_filter_event(self) -> str | None:
        """Return the active event filter, or None for all events."""
        return self._filter_event

    def current_filter_algorithm(self) -> str | None:
        """Return the active algorithm filter, or None for all algorithms."""
        return self._filter_algorithm

    def current_filter_since(self) -> datetime | None:
        """Return the lower time bound for the active period filter."""
        return self._filter_since()

    def current_filter_period_seconds(self) -> int | None:
        """Return the active period length in seconds, or None for all time."""
        return self._filter_period_seconds

    @property
    def phase_replay_total(self) -> int:
        """Number of solver phases available for algorithm-level replay."""
        return self._phase_replay.total

    def _on_item_clicked(self, item: QListWidgetItem) -> None:
        sequence = item.data(Qt.ItemDataRole.UserRole)
        if not isinstance(sequence, int):
            return
        entry = self._store.entry_by_sequence(sequence)
        if entry is None:
            return
        self.entry_selected.emit(entry)

    def _matches_filters(self, entry: TimelineEntry) -> bool:
        if self._filter_event and entry.event_name != self._filter_event:
            return False
        if self._filter_algorithm:
            if entry.payload.get("algorithm") != self._filter_algorithm:
                return False
        since = self._filter_since()
        if since is not None and entry.timestamp < since:
            return False
        return True

    def _on_entry(self, entry: TimelineEntry) -> None:
        if entry.payload.get("algorithm") and (
            self._algo_filter.findData(entry.payload["algorithm"]) < 0
        ):
            self._rebuild_algorithm_items()
        if not self._matches_filters(entry):
            return
        self._list.addItem(self._item_for(entry))
        self._list.scrollToBottom()

    def _rebuild(self) -> None:
        self._list.clear()
        for entry in self._store.filtered(
            self._filter_event,
            algorithm=self._filter_algorithm,
            since=self._filter_since(),
        ):
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
        if self._replay_mode == _MODE_PHASES:
            step = self._phase_replay.reset()
            self._emit_phase(step)
            return
        step = self._replay.reset()
        self._emit_replay(step)

    def _on_replay_back(self) -> None:
        if self._replay_mode == _MODE_PHASES:
            step = self._phase_replay.step_back()
            self._emit_phase(step)
            return
        step = self._replay.step_back()
        self._emit_replay(step)

    def _on_replay_forward(self) -> None:
        if self._replay_mode == _MODE_PHASES:
            step = self._phase_replay.step_forward()
            self._emit_phase(step)
            return
        step = self._replay.step_forward()
        self._emit_replay(step)

    def _on_replay_play(self) -> None:
        active = (
            self._phase_replay if self._replay_mode == _MODE_PHASES else self._replay
        )
        if active.playing:
            active.stop()
            self._play_timer.stop()
            self._update_replay_controls()
            return
        active.start()
        if self._replay_mode == _MODE_PHASES:
            self._emit_phase(self._phase_replay.step)
        else:
            self._emit_replay(self._replay.step)
        if active.playing:
            self._play_timer.start()
        self._update_replay_controls()

    def _on_play_tick(self) -> None:
        active = (
            self._phase_replay if self._replay_mode == _MODE_PHASES else self._replay
        )
        if not active.playing:
            self._play_timer.stop()
            self._update_replay_controls()
            return
        if self._replay_mode == _MODE_PHASES:
            step = self._phase_replay.step_forward()
            self._emit_phase(step)
        else:
            step = self._replay.step_forward()
            self._emit_replay(step)
        if not active.playing:
            self._play_timer.stop()

    def _emit_replay(self, step: int) -> None:
        self._update_replay_controls()
        self.replay_step_changed.emit(self._replay.solution, step)

    def _emit_phase(self, step: int) -> None:
        self._update_replay_controls()
        self.phase_step_changed.emit(self._phase_replay.current, step)

    def _update_replay_controls(self) -> None:
        if self._replay_mode == _MODE_PHASES:
            self._update_phase_controls()
            return
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

    def _update_phase_controls(self) -> None:
        available = self._phase_replay.available
        self._replay_reset.setEnabled(available)
        self._replay_back.setEnabled(available and self._phase_replay.step > 0)
        self._replay_forward.setEnabled(
            available and self._phase_replay.step < self._phase_replay.total
        )
        self._replay_play.setEnabled(available)
        play_key = (
            "timeline.replay_pause"
            if self._phase_replay.playing
            else "timeline.replay_play"
        )
        self._replay_play.setText(tr(play_key, self._language))
        if not available:
            self._replay_label.setText(tr("timeline.phase_none", self._language))
            return
        event = self._phase_replay.current
        if event is None:
            self._replay_label.setText(
                tr(
                    "timeline.phase_progress_idle",
                    self._language,
                    current=0,
                    total=self._phase_replay.total,
                )
            )
            return
        algorithm = event.payload.get("algorithm")
        kind_label = tr(f"timeline.phase.{event.kind}", self._language)
        if isinstance(algorithm, str) and algorithm:
            self._replay_label.setText(
                tr(
                    "timeline.phase_progress_algo",
                    self._language,
                    kind=kind_label,
                    algorithm=algorithm,
                    current=self._phase_replay.step,
                    total=self._phase_replay.total,
                )
            )
        else:
            self._replay_label.setText(
                tr(
                    "timeline.phase_progress",
                    self._language,
                    kind=kind_label,
                    current=self._phase_replay.step,
                    total=self._phase_replay.total,
                )
            )


def _format_payload(payload: dict, language: str) -> str:
    if not payload:
        return ""
    parts: list[str] = []
    piece_move = _format_piece_move_payload(payload)
    if piece_move:
        parts.append(piece_move)
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
    if "step" in payload and "index" not in payload:
        parts.append(tr("timeline.detail.step", language, n=payload["step"]))
    if "status" in payload:
        parts.append(str(payload["status"]))
    if "kind" in payload and not piece_move:
        parts.append(str(payload["kind"]))
    if "strategy" in payload:
        parts.append(str(payload["strategy"]))
    if "algorithm" in payload:
        parts.append(str(payload["algorithm"]))
    if "piece" in payload and not piece_move:
        parts.append(str(payload["piece"]))
    if "note" in payload:
        parts.append(str(payload["note"]))
    if "reason" in payload:
        reason = str(payload["reason"])
        parts.append(tr(f"timeline.reason.{reason}", language))
    if "duration_ms" in payload:
        parts.append(
            tr("timeline.detail.duration_ms", language, n=payload["duration_ms"])
        )
    if "total" in payload and "count" not in payload:
        parts.append(tr("timeline.detail.total", language, n=payload["total"]))
    if "no_fit" in payload:
        parts.append(tr("timeline.detail.no_fit", language, n=payload["no_fit"]))
    if "incompatible" in payload:
        parts.append(
            tr("timeline.detail.incompatible", language, n=payload["incompatible"])
        )
    if "accepted" in payload:
        parts.append(tr("timeline.detail.accepted", language, n=payload["accepted"]))
    if "rejected" in payload:
        parts.append(tr("timeline.detail.rejected", language, n=payload["rejected"]))
    return ", ".join(parts)


def _format_piece_move_payload(payload: dict) -> str:
    required = {"piece", "from_x", "from_y", "to_x", "to_y"}
    if not required.issubset(payload):
        return ""

    piece = str(payload["piece"])
    from_xy = f"({float(payload['from_x']):g},{float(payload['from_y']):g})"
    to_xy = f"({float(payload['to_x']):g},{float(payload['to_y']):g})"

    from_board = payload.get("from_board")
    to_board = payload.get("to_board")
    from_instance = payload.get("from_board_instance")
    to_instance = payload.get("to_board_instance")

    panel_changed = (
        from_board != to_board
        or from_instance != to_instance
        or payload.get("from_stock_panel_index") != payload.get("to_stock_panel_index")
    )

    if panel_changed:
        from_panel = (
            f"{from_board or '-'}#{from_instance if from_instance is not None else 0}"
        )
        to_panel = f"{to_board or '-'}#{to_instance if to_instance is not None else 0}"
        return f"{piece}: {from_panel}→{to_panel}, {from_xy}→{to_xy}"

    return f"{piece}: {from_xy}→{to_xy}"
