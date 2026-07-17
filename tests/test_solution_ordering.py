"""Tests for SCR-003 sort/filter helpers."""

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    SolutionExplanation,
    SolutionScore,
)
from studio.solution_ordering import SORT_LABELS, ordered_solution_indexes


def _solution(
    placements: list[BoardPlacement],
    *,
    score: float,
    omitted: tuple[str, ...] = (),
) -> AssemblySolution:
    return AssemblySolution(
        placements=placements,
        score=SolutionScore(waste_score=score),
        explanation=SolutionExplanation(),
        omitted_piece_ids=omitted,
    )


def _packed(*ids: str) -> list[BoardPlacement]:
    """Place pieces side by side with no internal gaps."""
    return [
        BoardPlacement(piece_id, index * 10, 0, 10, 10)
        for index, piece_id in enumerate(ids)
    ]


def _sparse(*ids: str) -> list[BoardPlacement]:
    """Place pieces far apart so the bounding box wastes a lot of area."""
    return [
        BoardPlacement(piece_id, index * 100, 0, 10, 10)
        for index, piece_id in enumerate(ids)
    ]


def test_ranking_preserves_pipeline_order():
    solutions = [
        _solution(_packed("A"), score=1.0),
        _solution(_packed("A", "B", "C"), score=9.0),
        _solution(_packed("A", "B"), score=5.0),
    ]

    assert ordered_solution_indexes(solutions) == [0, 1, 2]


def test_sort_by_pieces_puts_the_fullest_solution_first():
    solutions = [
        _solution(_packed("A"), score=1.0),
        _solution(_packed("A", "B", "C"), score=9.0),
        _solution(_packed("A", "B"), score=5.0),
    ]

    assert ordered_solution_indexes(solutions, sort_by="pieces") == [1, 2, 0]


def test_sort_by_waste_puts_the_least_wasteful_first():
    solutions = [
        _solution(_sparse("A", "B"), score=1.0),
        _solution(_packed("A", "B"), score=9.0),
        _solution(_sparse("A", "B", "C"), score=5.0),
    ]

    assert ordered_solution_indexes(solutions, sort_by="waste") == [1, 0, 2]
    assert solutions[1].waste_ratio < solutions[0].waste_ratio
    assert solutions[0].waste_ratio < solutions[2].waste_ratio


def test_sort_by_score_puts_the_highest_score_first():
    solutions = [
        _solution(_packed("A"), score=1.0),
        _solution(_packed("A", "B", "C"), score=9.0),
        _solution(_packed("A", "B"), score=5.0),
    ]

    assert ordered_solution_indexes(solutions, sort_by="score") == [1, 2, 0]


def test_complete_only_filters_partial_solutions():
    solutions = [
        _solution(_packed("A"), score=1.0, omitted=("X",)),
        _solution(_packed("A", "B", "C"), score=9.0),
        _solution(_packed("A", "B"), score=5.0, omitted=("Y",)),
    ]

    assert ordered_solution_indexes(solutions, complete_only=True) == [1]
    assert ordered_solution_indexes(solutions, sort_by="score", complete_only=True) == [
        1
    ]


def test_sort_by_board_waste_uses_the_provided_callback():
    solutions = [
        _solution(_packed("A"), score=1.0),
        _solution(_packed("A", "B", "C"), score=9.0),
    ]
    board_waste = {id(solutions[0]): 0.8, id(solutions[1]): 0.2}

    indexes = ordered_solution_indexes(
        solutions,
        sort_by="board_waste",
        board_waste=lambda s: board_waste[id(s)],
    )

    assert indexes == [1, 0]


def test_unknown_sort_key_falls_back_to_ranking():
    solutions = [_solution(_packed("A"), score=1.0)]

    assert ordered_solution_indexes(solutions, sort_by="nope") == [0]


def test_sort_labels_cover_every_supported_key():
    keys = {key for key, _label in SORT_LABELS}
    assert keys == {"ranking", "pieces", "waste", "board_waste", "score"}
