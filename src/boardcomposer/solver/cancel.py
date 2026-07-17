"""Cooperative cancellation for long-running solver pipelines."""

from __future__ import annotations

from dataclasses import dataclass, field
from threading import Event


class CancelledError(Exception):
    """Raised when a cooperative cancel token is triggered mid-run."""


@dataclass
class CancellationToken:
    """Flag for cooperative cancellation across threads.

    Writers call `cancel()` from the UI thread; the solver polls
    `is_cancelled` between generators / candidates.
    """

    _event: Event = field(default_factory=Event, init=False, repr=False)

    def cancel(self) -> None:
        self._event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    def raise_if_cancelled(self) -> None:
        if self._event.is_set():
            raise CancelledError("Cálculo cancelado por el usuario")


def check_cancelled(token: CancellationToken | None) -> None:
    """No-op helper when `token` is None."""
    if token is not None:
        token.raise_if_cancelled()
