from boardcomposer import AssemblySolution, BoardPlacement, SolutionScore
from studio.solution_highlights import solution_highlights


def test_solution_highlights_is_empty_for_a_single_solution():
    solutions = [AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])]

    assert solution_highlights(solutions) == {}


def test_solution_highlights_flags_best_and_worst_solution():
    better = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ],
        score=SolutionScore(waste_score=90),
    )
    worse = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        score=SolutionScore(waste_score=10),
    )

    highlights = solution_highlights([better, worse])

    assert "highlight.pieces" in highlights[0]
    assert "highlight.score" in highlights[0]
    assert 1 not in highlights or "highlight.pieces" not in highlights[1]
