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
            bus.publish(
                events.ALGORITHM_FINISHED,
                {
                    "algorithm": event.payload.get("algorithm"),
                    "count": event.payload.get("count", 0),
                },
            )
        elif event.kind == "evaluation_finished":
            bus.publish(
                events.EVALUATION_FINISHED,
                {
                    "accepted": event.payload.get("accepted", 0),
                    "rejected": event.payload.get("rejected", 0),
                },
            )
