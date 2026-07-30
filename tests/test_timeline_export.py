"""Tests for Timeline history export (ADR-005)."""

import json
import csv
from io import StringIO

from studio.events import EventBus
from studio.events.catalog import PIECE_MOVED, PROJECT_CREATED, PROJECT_SAVED
from studio.timeline.export import timeline_to_csv, timeline_to_json
from studio.timeline.store import TimelineStore


def test_timeline_to_json_and_csv_include_events():
    bus = EventBus()
    store = TimelineStore(bus)
    bus.publish(PROJECT_CREATED, {"kind": "demo"})
    bus.publish(PROJECT_SAVED, {"path": "/tmp/a.bcproj"})

    document = json.loads(timeline_to_json(store))
    assert document["format"] == "boardcomposer.timeline"
    assert document["version"] == 1
    assert document["count"] == 2
    assert document["events"][0]["event"] == PROJECT_CREATED
    assert document["events"][1]["payload"]["path"] == "/tmp/a.bcproj"

    csv_text = timeline_to_csv(store)
    lines = csv_text.strip().splitlines()
    assert lines[0].startswith("sequence,timestamp,event,payload_json,piece,kind,")
    assert PROJECT_CREATED in lines[1]
    assert PROJECT_SAVED in lines[2]


def test_timeline_export_respects_event_filter():
    bus = EventBus()
    store = TimelineStore(bus)
    bus.publish(PROJECT_CREATED, {"kind": "empty"})
    bus.publish(PROJECT_SAVED, {"path": "x.bcproj"})

    document = json.loads(timeline_to_json(store, event_name=PROJECT_SAVED))
    assert document["count"] == 1
    assert document["filter"] == PROJECT_SAVED
    assert document["algorithm_filter"] is None
    assert document["events"][0]["event"] == PROJECT_SAVED

    csv_text = timeline_to_csv(store, event_name=PROJECT_CREATED)
    assert PROJECT_CREATED in csv_text
    assert PROJECT_SAVED not in csv_text


def test_timeline_export_respects_algorithm_filter():
    from studio.events.catalog import ALGORITHM_FINISHED, ALGORITHM_STARTED

    bus = EventBus()
    store = TimelineStore(bus)
    bus.publish(ALGORITHM_STARTED, {"algorithm": "maxrects"})
    bus.publish(ALGORITHM_FINISHED, {"algorithm": "skyline", "count": 1})
    bus.publish(PROJECT_CREATED, {"kind": "empty"})

    document = json.loads(timeline_to_json(store, algorithm="maxrects"))
    assert document["count"] == 1
    assert document["algorithm_filter"] == "maxrects"
    assert document["events"][0]["payload"]["algorithm"] == "maxrects"

    csv_text = timeline_to_csv(store, algorithm="skyline")
    assert "skyline" in csv_text
    assert "maxrects" not in csv_text
    assert PROJECT_CREATED not in csv_text


def test_timeline_export_respects_since_filter():
    from dataclasses import replace
    from datetime import datetime, timedelta, timezone

    bus = EventBus()
    store = TimelineStore(bus)
    bus.publish(PROJECT_CREATED, {"kind": "old"})
    bus.publish(PROJECT_SAVED, {"path": "new.bcproj"})
    old, _recent = store.entries
    past = datetime.now(timezone.utc) - timedelta(hours=2)
    store._entries[0] = replace(old, timestamp=past)

    since = datetime.now(timezone.utc) - timedelta(minutes=10)
    document = json.loads(timeline_to_json(store, since=since, period_seconds=600))
    assert document["count"] == 1
    assert document["period_seconds"] == 600
    assert document["since"] is not None
    assert document["events"][0]["event"] == PROJECT_SAVED
    assert PROJECT_CREATED not in timeline_to_csv(store, since=since)


def test_timeline_csv_exports_piece_moved_columns():
    bus = EventBus()
    store = TimelineStore(bus)
    bus.publish(
        PIECE_MOVED,
        {
            "piece": "A",
            "kind": "reassigned",
            "from_x": 10.0,
            "from_y": 20.0,
            "to_x": 30.0,
            "to_y": 40.0,
            "from_board": "P1",
            "to_board": "P2",
            "from_board_instance": 0,
            "to_board_instance": 1,
            "from_stock_panel_index": 0,
            "to_stock_panel_index": 1,
        },
    )
    bus.publish(PROJECT_SAVED, {"path": "demo.bcproj"})

    rows = list(csv.DictReader(StringIO(timeline_to_csv(store))))
    assert len(rows) == 2

    moved = rows[0]
    assert moved["event"] == PIECE_MOVED
    assert moved["piece"] == "A"
    assert moved["kind"] == "reassigned"
    assert moved["from_x"] == "10.0"
    assert moved["to_x"] == "30.0"
    assert moved["from_board"] == "P1"
    assert moved["to_board"] == "P2"
    assert moved["from_board_instance"] == "0"
    assert moved["to_board_instance"] == "1"

    saved = rows[1]
    assert saved["event"] == PROJECT_SAVED
    assert saved["piece"] == ""
    assert saved["from_x"] == ""
    assert saved["to_board"] == ""
