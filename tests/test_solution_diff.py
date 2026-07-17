"""Tests for SCR-003 solution differences panel helpers."""

from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from studio.solution_diff import compare_solutions


def _solution(
    placements: list[BoardPlacement],
    *,
    score: float = 1.0,
    omitted: tuple[str, ...] = (),
) -> AssemblySolution:
    return AssemblySolution(
        placements=placements,
        score=SolutionScore(waste_score=score),
        explanation=SolutionExplanation(),
        omitted_piece_ids=omitted,
    )


def test_compare_solutions_marks_identical_when_same_index():
    solution = _solution([BoardPlacement("A", 0, 0, 10, 10)], score=5)

    diff = compare_solutions(
        solution,
        solution,
        reference_index=0,
        candidate_index=0,
    )

    assert diff.identical
    assert "idéntica" in diff.summary_lines()[0]


def test_compare_solutions_reports_metric_and_placement_changes():
    reference = _solution(
        [BoardPlacement("A", 0, 0, 10, 10), BoardPlacement("B", 20, 0, 10, 10)],
        score=2.0,
    )
    candidate = _solution(
        [
            BoardPlacement("A", 5, 0, 10, 10),
            BoardPlacement(
                "C",
                0,
                0,
                10,
                10,
                panel_reference=PanelReference(0, 0),
            ),
        ],
        score=8.0,
        omitted=("B",),
    )

    diff = compare_solutions(
        reference,
        candidate,
        reference_index=0,
        candidate_index=1,
        board_waste_reference=0.4,
        board_waste_candidate=0.2,
    )

    assert not diff.identical
    metric_labels = {metric.label for metric in diff.metrics}
    assert "Puntuación" in metric_labels
    assert "Material libre" in metric_labels
    assert "Piezas omitidas" in metric_labels

    kinds = {change.kind: change.piece_id for change in diff.placements}
    assert kinds["moved"] == "A"
    assert kinds["only_reference"] == "B"
    assert kinds["only_candidate"] == "C"

    text = "\n".join(diff.summary_lines())
    assert "Diferencias de #2" in text
    assert "A:" in text


def test_compare_solutions_identical_content_is_flagged():
    placement = BoardPlacement("A", 0, 0, 10, 10)
    left = _solution([placement], score=3.0)
    right = _solution([BoardPlacement("A", 0, 0, 10, 10)], score=3.0)

    diff = compare_solutions(left, right, reference_index=0, candidate_index=1)

    assert diff.identical
    assert not diff.metrics
    assert not diff.placements
