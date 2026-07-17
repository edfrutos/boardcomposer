"""Publish a SolveTrace onto the Studio Event Bus (ADR-003 / ADR-005)."""

from __future__ import annotations

from boardcomposer.solver.solve_trace import SolveTrace
from studio.events import catalog as events
from studio.events.event_bus import EventBus


def publish_solve_trace(bus: EventBus, trace: SolveTrace) -> None:
    """Map pipeline trace events to catalog Event Bus facts."""
    for event in trace.events:
        if event.kind == "generator_started":
            bus.publish(
                events.ALGORITHM_STARTED,
                {"algorithm": event.payload.get("algorithm")},
            )
        elif event.kind == "generator_finished":
            payload = {
                "algorithm": event.payload.get("algorithm"),
                "count": event.payload.get("count", 0),
            }
            if "duration_ms" in event.payload:
                payload["duration_ms"] = event.payload["duration_ms"]
            bus.publish(events.ALGORITHM_FINISHED, payload)
        elif event.kind == "evaluation_finished":
            payload = {
                "accepted": event.payload.get("accepted", 0),
                "rejected": event.payload.get("rejected", 0),
            }
            if "duration_ms" in event.payload:
                payload["duration_ms"] = event.payload["duration_ms"]
            bus.publish(events.EVALUATION_FINISHED, payload)
        elif event.kind == "placement_failures_summary":
            bus.publish(
                events.PLACEMENT_FAILURES_SUMMARY,
                {
                    "total": event.payload.get("total", 0),
                    "incompatible": event.payload.get("incompatible", 0),
                    "no_fit": event.payload.get("no_fit", 0),
                    "unique": event.payload.get("unique", 0),
                },
            )
        elif event.kind == "placement_failed":
            bus.publish(
                events.PLACEMENT_FAILED,
                dict(event.payload),
            )
