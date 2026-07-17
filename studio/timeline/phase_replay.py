"""Step-through replay of solver SolveTrace phases (ADR-005)."""

from __future__ import annotations

from dataclasses import dataclass, field

from boardcomposer.solver.solve_trace import SolveTrace, TraceEvent

# Phases shown in algorithm-level walkthrough (skip empty bookkeeping).
_PHASE_KINDS = frozenset(
    {
        "generator_started",
        "generator_finished",
        "placement_failures_summary",
        "placement_failed",
        "evaluation_started",
        "evaluation_finished",
        "build_order",
        "cancelled",
    }
)


@dataclass
class SolvePhaseReplay:
    """Walk SolveTrace events without mutating the project.

    ``step`` is 1-based index into ``phases`` (0 = before the first phase).
    """

    phases: tuple[TraceEvent, ...] = ()
    step: int = 0
    _playing: bool = field(default=False, init=False, repr=False)

    @property
    def total(self) -> int:
        return len(self.phases)

    @property
    def available(self) -> bool:
        return self.total > 0

    @property
    def playing(self) -> bool:
        return self._playing

    @property
    def current(self) -> TraceEvent | None:
        if self.step <= 0 or self.step > self.total:
            return None
        return self.phases[self.step - 1]

    def load(self, trace: SolveTrace | None) -> None:
        self.stop()
        if trace is None:
            self.phases = ()
        else:
            self.phases = tuple(
                event for event in trace.events if event.kind in _PHASE_KINDS
            )
        self.step = self.total

    def reset(self) -> int:
        self.stop()
        self.step = 0
        return self.step

    def finish(self) -> int:
        self.stop()
        self.step = self.total
        return self.step

    def step_forward(self) -> int:
        if self.step < self.total:
            self.step += 1
        if self.step >= self.total:
            self.stop()
        return self.step

    def step_back(self) -> int:
        self.stop()
        if self.step > 0:
            self.step -= 1
        return self.step

    def start(self) -> None:
        if not self.available:
            return
        if self.step >= self.total:
            self.step = 0
        self._playing = True

    def stop(self) -> None:
        self._playing = False
