"""Export Timeline history for support / audit (ADR-005)."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from io import StringIO

from studio.events.catalog import ALL_EVENTS
from studio.timeline.store import TimelineEntry, TimelineStore


def _serialize_payload(payload: dict) -> dict:
    """Convert payload values to JSON-friendly scalars."""
    result: dict[str, object] = {}
    for key, value in payload.items():
        if isinstance(value, (str, int, float, bool)) or value is None:
            result[key] = value
        elif isinstance(value, (list, tuple)):
            result[key] = [
                item
                if isinstance(item, (str, int, float, bool)) or item is None
                else str(item)
                for item in value
            ]
        else:
            result[key] = str(value)
    return result


def entry_to_dict(entry: TimelineEntry) -> dict:
    """Serialize one timeline entry."""
    return {
        "sequence": entry.sequence,
        "timestamp": entry.timestamp.isoformat(),
        "event": entry.event_name,
        "payload": _serialize_payload(entry.payload),
    }


def timeline_entries(
    store: TimelineStore,
    *,
    event_name: str | None = None,
    algorithm: str | None = None,
) -> tuple[TimelineEntry, ...]:
    """Return entries, optionally filtered by event type and algorithm."""
    use_event = event_name if event_name and event_name != ALL_EVENTS else None
    if use_event or algorithm:
        return store.filtered(use_event, algorithm=algorithm)
    return store.entries


def timeline_to_json(
    store: TimelineStore,
    *,
    event_name: str | None = None,
    algorithm: str | None = None,
    exported_at: datetime | None = None,
) -> str:
    """Return a JSON document with the timeline history."""
    entries = timeline_entries(
        store,
        event_name=event_name,
        algorithm=algorithm,
    )
    stamp = exported_at or datetime.now().astimezone()
    event_filter = event_name if event_name and event_name != ALL_EVENTS else None
    document = {
        "format": "boardcomposer.timeline",
        "version": 1,
        "exported_at": stamp.isoformat(),
        "filter": event_filter,
        "algorithm_filter": algorithm,
        "count": len(entries),
        "events": [entry_to_dict(entry) for entry in entries],
    }
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def timeline_to_csv(
    store: TimelineStore,
    *,
    event_name: str | None = None,
    algorithm: str | None = None,
) -> str:
    """Return a CSV table with sequence, timestamp, event and payload JSON."""
    entries = timeline_entries(
        store,
        event_name=event_name,
        algorithm=algorithm,
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["sequence", "timestamp", "event", "payload_json"])
    for entry in entries:
        writer.writerow(
            [
                entry.sequence,
                entry.timestamp.isoformat(),
                entry.event_name,
                json.dumps(_serialize_payload(entry.payload), ensure_ascii=False),
            ]
        )
    return buffer.getvalue()
