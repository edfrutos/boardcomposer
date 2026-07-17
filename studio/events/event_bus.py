"""Event bus for BoardComposer Studio."""

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Callable, DefaultDict

from studio.events.catalog import ALL_EVENTS

EventHandler = Callable[[str, dict], None]


@dataclass
class EventBus:
    """Simple synchronous event bus (ADR-003).

    Handlers subscribed to ``ALL_EVENTS`` ("*") receive every publication.
    """

    _subscribers: DefaultDict[str, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list)
    )

    def subscribe(self, event_name: str, handler: EventHandler) -> None:
        self._subscribers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: EventHandler) -> None:
        if handler in self._subscribers[event_name]:
            self._subscribers[event_name].remove(handler)

    def publish(self, event_name: str, payload: dict | None = None) -> None:
        event_payload = payload or {}

        for handler in list(self._subscribers[event_name]):
            handler(event_name, event_payload)

        if event_name != ALL_EVENTS:
            for handler in list(self._subscribers[ALL_EVENTS]):
                handler(event_name, event_payload)
