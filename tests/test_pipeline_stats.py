"""Tests for candidate pipeline execution statistics."""

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.strategies import balanced_strategy


def test_pipeline_collects_execution_statistics():
    """The pipeline records generated, unique and accepted candidates."""
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=200,
            max_width_mm=100,
        )
    )
    project.add_board(Board(100, 50, 19, "A"))
    project.add_board(Board(100, 50, 19, "B"))

    pipeline = CandidatePipeline(
        project=project,
        strategy=balanced_strategy(),
    )

    solutions = pipeline.run()

    assert pipeline.stats.generated >= 1
    assert pipeline.stats.unique >= 1
    assert pipeline.stats.accepted == len(solutions)
    assert pipeline.stats.rejected == (pipeline.stats.unique - pipeline.stats.accepted)
