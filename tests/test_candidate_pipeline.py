from boardcomposer import Board, Project, StockPanel
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.strategies import (
    compact_first_strategy,
    material_first_strategy,
)


def test_candidate_pipeline_returns_ranked_solutions():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    pipeline = CandidatePipeline(
        project=project,
        strategy=compact_first_strategy(),
    )

    solutions = pipeline.run()

    assert len(solutions) > 0
    assert solutions[0].score.total >= solutions[-1].score.total


def test_candidate_pipeline_keeps_offcuts_with_a_single_physical_panel():
    """Regression: with exactly one physical panel, the pipeline used to
    rebuild each candidate solution from scratch (just to force-assign the
    implicit panel reference), silently losing any offcut/omitted-piece
    information a generator like MaxRects had already attached."""
    project = Project()
    project.add_stock_panel(StockPanel(1200, 800, 19, "TAB-A"))
    project.add_board(Board(400, 400, 19, "P-1"))

    pipeline = CandidatePipeline(
        project=project,
        strategy=material_first_strategy(),
    )

    solutions = pipeline.run()

    assert solutions
    assert solutions[0].offcuts
