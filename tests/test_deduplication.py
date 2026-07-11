from boardcomposer import AssemblySolution, BoardPlacement
from boardcomposer.solver.deduplication import deduplicate_solutions


def test_deduplicate_solutions_removes_exact_duplicates():
    solution_a = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])
    solution_b = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 50)])

    unique = deduplicate_solutions([solution_a, solution_b])

    assert len(unique) == 1


def test_deduplicate_solutions_ignores_global_translation():
    solution_a = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 80, 50),
        ]
    )
    solution_b = AssemblySolution(
        placements=[
            BoardPlacement("A", 20, 30, 100, 50),
            BoardPlacement("B", 120, 30, 80, 50),
        ]
    )

    unique = deduplicate_solutions([solution_a, solution_b])

    assert len(unique) == 1


def test_deduplicate_solutions_uses_position_tolerance():
    solution_a = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 80, 50),
        ]
    )
    solution_b = AssemblySolution(
        placements=[
            BoardPlacement("A", 0.4, 0.4, 100, 50),
            BoardPlacement("B", 100.4, 0.4, 80, 50),
        ]
    )

    unique = deduplicate_solutions([solution_a, solution_b])

    assert len(unique) == 1


def test_deduplicate_solutions_keeps_different_geometry():
    solution_a = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 80, 50),
        ]
    )
    solution_b = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 0, 50, 80, 50),
        ]
    )

    unique = deduplicate_solutions([solution_a, solution_b])

    assert len(unique) == 2
