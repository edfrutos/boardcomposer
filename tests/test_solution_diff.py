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


def test_compare_solutions_summary_translates_to_english():
    reference = _solution([BoardPlacement("A", 0, 0, 10, 10)], score=2.0)
    candidate = _solution([BoardPlacement("A", 5, 0, 10, 10)], score=8.0)

    diff = compare_solutions(
        reference,
        candidate,
        reference_index=0,
        candidate_index=1,
        language="en",
    )

    text = "\n".join(diff.summary_lines())
    assert "Differences of #2" in text
    assert "Score" in text
    assert "better here" in text or "better in reference" in text


def test_format_diff_unavailable_translates():
    from studio.solution_diff import format_diff_unavailable

    lines = format_diff_unavailable("diff.need_two", "en")
    assert lines[0] == "Differences"
    assert "At least 2 solutions" in lines[2]
    assert "Ctrl+Shift+D" in lines[2]


def test_compare_solutions_identical_content_is_flagged():
    placement = BoardPlacement("A", 0, 0, 10, 10)
    left = _solution([placement], score=3.0)
    right = _solution([BoardPlacement("A", 0, 0, 10, 10)], score=3.0)

    diff = compare_solutions(left, right, reference_index=0, candidate_index=1)

    assert diff.identical
    assert not diff.metrics
    assert not diff.placements


def test_compare_solutions_at_step_reports_partial_divergence():
    from studio.solution_diff import (
        compare_solutions_at_step,
        truncate_solution_to_step,
    )

    reference = _solution(
        [
            BoardPlacement("A", 0, 0, 10, 10),
            BoardPlacement("B", 20, 0, 10, 10),
        ]
    )
    candidate = _solution(
        [
            BoardPlacement("A", 0, 0, 10, 10),
            BoardPlacement("B", 30, 0, 10, 10),
        ]
    )

    empty = compare_solutions_at_step(
        reference,
        candidate,
        0,
        reference_index=0,
        candidate_index=1,
    )
    assert "paso 0/" in empty[0]
    assert "Sin piezas" in empty[2]

    matched = compare_solutions_at_step(
        reference,
        candidate,
        1,
        reference_index=0,
        candidate_index=1,
    )
    assert "coinciden" in matched[2]

    diverged = compare_solutions_at_step(
        reference,
        candidate,
        2,
        reference_index=0,
        candidate_index=1,
    )
    text = "\n".join(diverged)
    assert "B:" in text
    assert "paso 2/" in diverged[0]

    truncated = truncate_solution_to_step(candidate, 1)
    assert len(truncated.placements) == 1
    assert truncated.placements[0].board_id == "A"
