"""Export Timeline history for support / audit (ADR-005)."""

from __future__ import annotations

import csv
import json
from datetime import datetime
from io import StringIO

from studio.events.catalog import ALL_EVENTS, PIECE_MOVED
from studio.timeline.store import TimelineEntry, TimelineStore

_PIECE_MOVED_FIELDS: tuple[str, ...] = (
    "piece",
    "kind",
    "from_x",
    "from_y",
    "to_x",
    "to_y",
    "from_board",
    "to_board",
    "from_board_instance",
    "to_board_instance",
    "from_stock_panel_index",
    "to_stock_panel_index",
)


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
    since: datetime | None = None,
) -> tuple[TimelineEntry, ...]:
    """Return entries, optionally filtered by event, algorithm and time."""
    use_event = event_name if event_name and event_name != ALL_EVENTS else None
    if use_event or algorithm or since is not None:
        return store.filtered(use_event, algorithm=algorithm, since=since)
    return store.entries


def timeline_to_json(
    store: TimelineStore,
    *,
    event_name: str | None = None,
    algorithm: str | None = None,
    since: datetime | None = None,
    period_seconds: int | None = None,
    exported_at: datetime | None = None,
) -> str:
    """Return a JSON document with the timeline history."""
    entries = timeline_entries(
        store,
        event_name=event_name,
        algorithm=algorithm,
        since=since,
    )
    stamp = exported_at or datetime.now().astimezone()
    event_filter = event_name if event_name and event_name != ALL_EVENTS else None
    document = {
        "format": "boardcomposer.timeline",
        "version": 1,
        "exported_at": stamp.isoformat(),
        "filter": event_filter,
        "algorithm_filter": algorithm,
        "since": since.isoformat() if since is not None else None,
        "period_seconds": period_seconds,
        "count": len(entries),
        "events": [entry_to_dict(entry) for entry in entries],
    }
    return json.dumps(document, ensure_ascii=False, indent=2) + "\n"


def timeline_to_csv(
    store: TimelineStore,
    *,
    event_name: str | None = None,
    algorithm: str | None = None,
    since: datetime | None = None,
) -> str:
    """Return a CSV table with payload JSON plus key PieceMoved fields."""
    entries = timeline_entries(
        store,
        event_name=event_name,
        algorithm=algorithm,
        since=since,
    )
    buffer = StringIO()
    writer = csv.writer(buffer)
    writer.writerow(
        [
            "sequence",
            "timestamp",
            "event",
            "payload_json",
            *_PIECE_MOVED_FIELDS,
        ]
    )
    for entry in entries:
        payload = _serialize_payload(entry.payload)
        moved_columns = _piece_moved_columns(entry.event_name, payload)
        writer.writerow(
            [
                entry.sequence,
                entry.timestamp.isoformat(),
                entry.event_name,
                json.dumps(payload, ensure_ascii=False),
                *moved_columns,
            ]
        )
    return buffer.getvalue()


def _piece_moved_columns(event_name: str, payload: dict) -> list[object]:
    if event_name != PIECE_MOVED:
        return ["" for _ in _PIECE_MOVED_FIELDS]
    return [payload.get(field, "") for field in _PIECE_MOVED_FIELDS]
