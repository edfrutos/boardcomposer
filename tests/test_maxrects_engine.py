"""Test the iter_maxrects_candidates function."""

from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_engine import iter_maxrects_candidates
from boardcomposer.solver.maxrects.orderings import MAXRECTS_BOARD_ORDERINGS
from boardcomposer.solver.maxrects.strategies import MAXRECTS_HEURISTICS


def _project() -> Project:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))
    return project


def test_iter_maxrects_candidates_uses_classic_candidates_by_default():
    """Test that the iter_maxrects_candidates uses the classic candidates by default."""
    candidates = list(iter_maxrects_candidates(_project()))

    assert candidates
    assert all("maxrects" in candidate.explanation.notes for candidate in candidates)


def test_iter_maxrects_candidates_can_use_beam():
    """Test that the iter_maxrects_candidates use the beam search algorithm."""
    candidates = list(
        iter_maxrects_candidates(
            _project(),
            beam_width=2,
        )
    )

    assert len(candidates) == (len(MAXRECTS_HEURISTICS) * len(MAXRECTS_BOARD_ORDERINGS))
    assert all("beam" in candidate.explanation.notes for candidate in candidates)
