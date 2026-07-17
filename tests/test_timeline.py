"""Tests for Event Bus and Timeline store (ADR-003 / ADR-005)."""

from studio.events import ALL_EVENTS, EventBus
from studio.events.catalog import PROJECT_CREATED, PROJECT_SAVED, SOLUTION_GENERATED
from studio.timeline import TimelineStore


def test_event_bus_notifies_named_and_wildcard_subscribers():
    bus = EventBus()
    named: list[tuple[str, dict]] = []
    all_events: list[tuple[str, dict]] = []

    bus.subscribe(PROJECT_CREATED, lambda n, p: named.append((n, p)))
    bus.subscribe(ALL_EVENTS, lambda n, p: all_events.append((n, p)))

    bus.publish(PROJECT_CREATED, {"kind": "empty"})
    bus.publish(PROJECT_SAVED, {"path": "/tmp/x.bcproj"})

    assert named == [(PROJECT_CREATED, {"kind": "empty"})]
    assert [name for name, _ in all_events] == [PROJECT_CREATED, PROJECT_SAVED]


def test_timeline_store_records_and_filters_events():
    bus = EventBus()
    store = TimelineStore(bus, max_entries=10)

    bus.publish(PROJECT_CREATED, {"kind": "demo"})
    bus.publish(SOLUTION_GENERATED, {"status": "ok", "count": 3})
    bus.publish(PROJECT_SAVED, {"path": "a.bcproj"})

    assert len(store.entries) == 3
    assert store.entries[0].event_name == PROJECT_CREATED
    assert [e.event_name for e in store.filtered(PROJECT_SAVED)] == [PROJECT_SAVED]


def test_timeline_store_filters_by_algorithm():
    from studio.events.catalog import ALGORITHM_FINISHED, ALGORITHM_STARTED

    bus = EventBus()
    store = TimelineStore(bus)

    bus.publish(ALGORITHM_STARTED, {"algorithm": "maxrects"})
    bus.publish(ALGORITHM_FINISHED, {"algorithm": "maxrects", "count": 2})
    bus.publish(ALGORITHM_STARTED, {"algorithm": "skyline"})
    bus.publish(PROJECT_CREATED, {"kind": "empty"})

    assert store.algorithms() == ("maxrects", "skyline")
    only_maxrects = store.filtered(algorithm="maxrects")
    assert [e.payload.get("algorithm") for e in only_maxrects] == [
        "maxrects",
        "maxrects",
    ]
    started_skyline = store.filtered(ALGORITHM_STARTED, algorithm="skyline")
    assert len(started_skyline) == 1
    assert started_skyline[0].payload["algorithm"] == "skyline"


def test_timeline_store_respects_max_entries():
    bus = EventBus()
    store = TimelineStore(bus, max_entries=2)

    for index in range(5):
        bus.publish(PROJECT_CREATED, {"n": index})

    assert len(store.entries) == 2
    assert store.entries[0].payload["n"] == 3
    assert store.entries[1].payload["n"] == 4


def test_timeline_store_clear_and_listeners():
    bus = EventBus()
    store = TimelineStore(bus)
    seen: list[str] = []
    store.add_listener(lambda entry: seen.append(entry.event_name))

    bus.publish(PROJECT_CREATED, {})
    assert seen == [PROJECT_CREATED]

    store.clear()
    assert store.entries == ()
