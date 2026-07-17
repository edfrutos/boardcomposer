"""Optional collector for placement failures (ADR-005)."""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Iterator


@dataclass(frozen=True)
class PlacementFailure:
    """One recorded attempt where a piece was not placed."""

    piece_id: str
    reason: str  # incompatible | no_fit
    stock_panel_index: int | None = None
    instance_index: int | None = None
    algorithm: str = "maxrects"


@dataclass
class PlacementFailureLog:
    """Deduplicated sample of placement failures plus aggregate counts."""

    max_unique: int = 50
    failures: list[PlacementFailure] = field(default_factory=list)
    _seen: set[tuple] = field(default_factory=set, init=False, repr=False)
    counts: dict[str, int] = field(default_factory=dict)

    def add(self, failure: PlacementFailure) -> None:
        self.counts[failure.reason] = self.counts.get(failure.reason, 0) + 1
        key = (
            failure.piece_id,
            failure.reason,
            failure.stock_panel_index,
            failure.instance_index,
            failure.algorithm,
        )
        if key in self._seen or len(self.failures) >= self.max_unique:
            return
        self._seen.add(key)
        self.failures.append(failure)

    @property
    def total(self) -> int:
        return sum(self.counts.values())


_CURRENT_LOG: ContextVar[PlacementFailureLog | None] = ContextVar(
    "boardcomposer_placement_failure_log",
    default=None,
)


def record_placement_failure(
    *,
    piece_id: str,
    reason: str,
    stock_panel_index: int | None = None,
    instance_index: int | None = None,
    algorithm: str = "maxrects",
) -> None:
    """Record a failure if a log is active in the current context."""
    log = _CURRENT_LOG.get()
    if log is None:
        return
    log.add(
        PlacementFailure(
            piece_id=piece_id,
            reason=reason,
            stock_panel_index=stock_panel_index,
            instance_index=instance_index,
            algorithm=algorithm,
        )
    )


@contextmanager
def capture_placement_failures(
    log: PlacementFailureLog | None = None,
) -> Iterator[PlacementFailureLog]:
    """Activate a failure log for the duration of a generator run."""
    active = log if log is not None else PlacementFailureLog()
    token = _CURRENT_LOG.set(active)
    try:
        yield active
    finally:
        _CURRENT_LOG.reset(token)
