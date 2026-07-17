"""Chronological record of solver algorithm phases (ADR-005)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class TraceEvent:
    """One fact recorded while the candidate pipeline runs."""

    kind: str
    payload: dict[str, object] = field(default_factory=dict)


@dataclass
class SolveTrace:
    """In-memory log of generator/evaluation phases for one solve."""

    events: list[TraceEvent] = field(default_factory=list)

    def record(self, kind: str, **payload: object) -> None:
        self.events.append(TraceEvent(kind=kind, payload=dict(payload)))

    def clear(self) -> None:
        self.events.clear()

    def algorithms(self) -> tuple[str, ...]:
        """Return generator names that started during this solve."""
        names: list[str] = []
        for event in self.events:
            if event.kind != "generator_started":
                continue
            name = event.payload.get("algorithm")
            if isinstance(name, str):
                names.append(name)
        return tuple(names)
