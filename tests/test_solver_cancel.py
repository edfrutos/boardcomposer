"""Tests for cooperative solver cancellation."""

from boardcomposer import Board, Project
from boardcomposer.solver.cancel import (
    CancellationToken,
    CancelledError,
    check_cancelled,
)
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.strategies import compact_first_strategy


def test_check_cancelled_noop_without_token():
    check_cancelled(None)


def test_cancellation_token_raises():
    token = CancellationToken()
    assert not token.is_cancelled
    token.cancel()
    assert token.is_cancelled
    try:
        token.raise_if_cancelled()
    except CancelledError:
        pass
    else:
        raise AssertionError("expected CancelledError")


def test_pipeline_stops_when_token_already_cancelled():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    token = CancellationToken()
    token.cancel()

    pipeline = CandidatePipeline(
        project=project,
        strategy=compact_first_strategy(),
        cancel=token,
    )
    solutions = pipeline.run()

    assert solutions == []
    assert pipeline.stats.cancelled is True


def test_pipeline_cancels_between_generators(monkeypatch):
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    token = CancellationToken()
    calls = {"n": 0}

    def fake_generators_by_name(names):
        def gen_a(_project):
            calls["n"] += 1
            token.cancel()
            return []

        def gen_b(_project):
            calls["n"] += 1
            return []

        return [gen_a, gen_b]

    monkeypatch.setattr(
        "boardcomposer.solver.candidate_pipeline.generators_by_name",
        fake_generators_by_name,
    )

    pipeline = CandidatePipeline(
        project=project,
        strategy=compact_first_strategy(),
        cancel=token,
    )
    solutions = pipeline.run()

    assert solutions == []
    assert pipeline.stats.cancelled is True
    assert calls["n"] == 1


def test_geometry_solver_propagates_cancel():
    project = Project()
    project.add_board(Board(500, 300, 20, "A"))

    token = CancellationToken()
    token.cancel()

    solver = GeometrySolver(
        project,
        strategy=compact_first_strategy(),
        cancel=token,
    )
    assert solver.solve() == []
    assert solver.stats.cancelled is True
