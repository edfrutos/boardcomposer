"""In-memory timeline of Studio events (ADR-005)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Callable

from studio.events.catalog import ALL_EVENTS
from studio.events.event_bus import EventBus


@dataclass(frozen=True)
class TimelineEntry:
    """One fact recorded on the timeline."""

    sequence: int
    timestamp: datetime
    event_name: str
    payload: dict


Listener = Callable[[TimelineEntry], None]


@dataclass
class TimelineStore:
    """Consumes the Event Bus and keeps a chronological event log."""

    bus: EventBus
    max_entries: int = 500
    _entries: list[TimelineEntry] = field(default_factory=list, init=False, repr=False)
    _listeners: list[Listener] = field(default_factory=list, init=False, repr=False)
    _sequence: int = field(default=0, init=False, repr=False)

    def __post_init__(self) -> None:
        self.bus.subscribe(ALL_EVENTS, self._on_event)

    @property
    def entries(self) -> tuple[TimelineEntry, ...]:
        return tuple(self._entries)

    def add_listener(self, listener: Listener) -> None:
        self._listeners.append(listener)

    def remove_listener(self, listener: Listener) -> None:
        if listener in self._listeners:
            self._listeners.remove(listener)

    def clear(self) -> None:
        self._entries.clear()

    def algorithms(self) -> tuple[str, ...]:
        """Return distinct algorithm names seen in entry payloads."""
        names: list[str] = []
        seen: set[str] = set()
        for entry in self._entries:
            value = entry.payload.get("algorithm")
            if isinstance(value, str) and value and value not in seen:
                seen.add(value)
                names.append(value)
        return tuple(names)

    def filtered(
        self,
        event_name: str | None = None,
        *,
        algorithm: str | None = None,
    ) -> tuple[TimelineEntry, ...]:
        """Return entries matching optional event-type and algorithm filters."""
        result: list[TimelineEntry] = []
        for entry in self._entries:
            if event_name and event_name != ALL_EVENTS:
                if entry.event_name != event_name:
                    continue
            if algorithm:
                value = entry.payload.get("algorithm")
                if value != algorithm:
                    continue
            result.append(entry)
        return tuple(result)

    def _on_event(self, event_name: str, payload: dict) -> None:
        self._sequence += 1
        entry = TimelineEntry(
            sequence=self._sequence,
            timestamp=datetime.now(timezone.utc),
            event_name=event_name,
            payload=dict(payload),
        )
        self._entries.append(entry)
        overflow = len(self._entries) - self.max_entries
        if overflow > 0:
            del self._entries[:overflow]

        for listener in list(self._listeners):
            listener(entry)
