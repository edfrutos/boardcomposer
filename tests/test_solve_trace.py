"""Tests for solver algorithm SolveTrace (ADR-005)."""

from boardcomposer import Board, Project
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.geometry_solver import GeometrySolver
from boardcomposer.solver.strategies import compact_first_strategy
from studio.events import EventBus
from studio.events.catalog import (
    ALGORITHM_FINISHED,
    ALGORITHM_STARTED,
    EVALUATION_FINISHED,
)
from studio.solve_trace_publisher import publish_solve_trace


def test_pipeline_records_generator_and_evaluation_trace():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    pipeline = CandidatePipeline(
        project=project,
        strategy=compact_first_strategy(),
    )
    solutions = pipeline.run()

    kinds = [event.kind for event in pipeline.trace.events]
    assert "generator_started" in kinds
    assert "generator_finished" in kinds
    assert "evaluation_started" in kinds
    assert "evaluation_finished" in kinds
    assert pipeline.trace.algorithms() == ("vertical", "free_space")
    if solutions:
        assert any(event.kind == "build_order" for event in pipeline.trace.events)


def test_geometry_solver_exposes_trace():
    project = Project()
    project.add_board(Board(500, 300, 20, "A"))

    solver = GeometrySolver(project, strategy=compact_first_strategy())
    solver.solve()

    assert solver.trace.algorithms()
    assert any(event.kind == "generator_started" for event in solver.trace.events)


def test_publish_solve_trace_maps_to_event_bus():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    pipeline = CandidatePipeline(
        project=project,
        strategy=compact_first_strategy(),
    )
    pipeline.run()

    bus = EventBus()
    seen: list[str] = []
    bus.subscribe("*", lambda name, _payload: seen.append(name))
    publish_solve_trace(bus, pipeline.trace)

    assert ALGORITHM_STARTED in seen
    assert ALGORITHM_FINISHED in seen
    assert EVALUATION_FINISHED in seen
