"""Tests for stable solution ranking."""

from boardcomposer import AssemblySolution, BoardPlacement, SolutionScore
from boardcomposer.solver.solution_ranking import solution_ranking_key


def make_solution(
    placements: list[BoardPlacement],
    score: float,
) -> AssemblySolution:
    """Create a solution with a controlled total score."""
    return AssemblySolution(
        placements=placements,
        score=SolutionScore(
            waste_score=score,
        ),
    )


def test_higher_score_is_ranked_first():
    """The total score remains the primary ranking criterion."""
    lower = make_solution(
        [BoardPlacement("A", 0, 0, 100, 50)],
        score=50,
    )
    higher = make_solution(
        [BoardPlacement("A", 0, 0, 100, 50)],
        score=60,
    )

    ranked = sorted(
        [lower, higher],
        key=solution_ranking_key,
        reverse=True,
    )

    assert ranked[0] is higher


def test_lower_waste_breaks_equal_score_tie():
    """Less internal waste wins when scores are equal."""
    compact = make_solution(
        [
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ],
        score=50,
    )
    wasteful = make_solution(
        [
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 200, 0, 100, 50),
        ],
        score=50,
    )

    ranked = sorted(
        [wasteful, compact],
        key=solution_ranking_key,
        reverse=True,
    )

    assert ranked[0] is compact


def test_fewer_rotations_break_equal_geometry_tie():
    """Fewer rotated placements win when geometry and score are equal."""
    normal = make_solution(
        [BoardPlacement("A", 0, 0, 100, 50, rotated=False)],
        score=50,
    )
    rotated = make_solution(
        [BoardPlacement("A", 0, 0, 100, 50, rotated=True)],
        score=50,
    )

    ranked = sorted(
        [rotated, normal],
        key=solution_ranking_key,
        reverse=True,
    )

    assert ranked[0] is normal
