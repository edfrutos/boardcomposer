"""Tests for the modal solve progress dialog (thread-safe completion)."""

from __future__ import annotations

import time

from boardcomposer.solver.pipeline_stats import PipelineStats
from studio.solve_worker import run_solve_with_progress


class _FakeLayoutService:
    def __init__(self, *, delay_s: float = 0.05, fail: bool = False) -> None:
        self.stats = PipelineStats()
        self._delay_s = delay_s
        self._fail = fail
        self.calls = 0

    def solve_current_project(self, cancel=None):
        del cancel
        self.calls += 1
        time.sleep(self._delay_s)
        if self._fail:
            raise RuntimeError("boom")
        return None


def test_run_solve_with_progress_completes_without_hanging(qapp):
    """Regression: finishing on the worker thread used to leave the dialog hung."""
    del qapp
    from PySide6.QtWidgets import QWidget

    parent = QWidget()
    parent.show()
    layout = _FakeLayoutService(delay_s=0.05)

    solution = run_solve_with_progress(
        parent=parent,
        layout_service=layout,
        label="Working…",
        title="Solve",
        cancel_text="Cancel",
    )

    assert solution is None
    assert layout.calls == 1
    parent.close()


def test_run_solve_with_progress_surfaces_worker_errors(qapp):
    del qapp
    from PySide6.QtWidgets import QWidget

    parent = QWidget()
    parent.show()
    layout = _FakeLayoutService(fail=True)

    try:
        run_solve_with_progress(
            parent=parent,
            layout_service=layout,
            label="Working…",
            title="Solve",
            cancel_text="Cancel",
        )
    except RuntimeError as exc:
        assert "boom" in str(exc)
    else:
        raise AssertionError("expected RuntimeError")
    finally:
        parent.close()
