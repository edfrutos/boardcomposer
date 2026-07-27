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


def test_solution_highlights_includes_board_free_length_width():
    compact = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        score=SolutionScore(waste_score=50),
    )
    sprawling = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 400, 300)],
        score=SolutionScore(waste_score=50),
    )

    def board_waste(solution: AssemblySolution) -> float:
        # Lower free-board ratio wins; compact layout is denser on stock.
        return 0.2 if solution.total_length_mm <= 100 else 0.8

    highlights = solution_highlights(
        [compact, sprawling],
        board_waste=board_waste,
    )

    assert "highlight.length" in highlights[0]
    assert "highlight.width" in highlights[0]
    assert "highlight.board_free" in highlights[0]
    assert "highlight.length" not in highlights.get(1, [])
    assert "highlight.width" not in highlights.get(1, [])
    assert "highlight.board_free" not in highlights.get(1, [])
