"""Tests for Timeline history export (ADR-005)."""

import json

from studio.events import EventBus
from studio.events.catalog import PROJECT_CREATED, PROJECT_SAVED
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
    assert lines[0] == "sequence,timestamp,event,payload_json"
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
