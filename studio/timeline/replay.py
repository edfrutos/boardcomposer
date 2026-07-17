"""Step-through replay of a solution's placements (ADR-005)."""

from __future__ import annotations

from dataclasses import dataclass, field

from boardcomposer.domain import AssemblySolution


@dataclass
class SolutionReplay:
    """Reveal placements one by one without mutating the project.

    ``step`` is the number of placements currently revealed
    (0 = none, ``total`` = full solution).
    """

    solution: AssemblySolution | None = None
    step: int = 0
    _playing: bool = field(default=False, init=False, repr=False)

    @property
    def total(self) -> int:
        if self.solution is None:
            return 0
        return len(self.solution.placements)

    @property
    def available(self) -> bool:
        return self.total > 0

    @property
    def playing(self) -> bool:
        return self._playing

    @property
    def algorithm(self) -> str | None:
        if self.solution is None or not self.solution.explanation.notes:
            return None
        return self.solution.explanation.notes[0]

    @property
    def current_piece_id(self) -> str | None:
        if self.solution is None or self.step <= 0:
            return None
        index = min(self.step, self.total) - 1
        return self.solution.placements[index].board_id

    def load(self, solution: AssemblySolution | None) -> None:
        self.stop()
        self.solution = solution
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
