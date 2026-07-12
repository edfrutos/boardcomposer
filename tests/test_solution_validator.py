from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    Project,
    ProjectConstraints,
)
from boardcomposer.solver.solution_validator import is_valid_solution


def make_project() -> Project:
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=200,
            max_width_mm=100,
        )
    )
    project.add_board(Board(100, 50, 19, "A"))
    project.add_board(Board(100, 50, 19, "B"))
    return project


def test_valid_complete_solution_is_accepted():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ]
    )

    assert is_valid_solution(solution, make_project()) is True


def test_incomplete_solution_is_rejected():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
        ]
    )

    assert is_valid_solution(solution, make_project()) is False


def test_solution_with_duplicate_piece_is_rejected():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("A", 100, 0, 100, 50),
        ]
    )

    assert is_valid_solution(solution, make_project()) is False


def test_solution_with_unknown_piece_is_rejected():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("X", 100, 0, 100, 50),
        ]
    )

    assert is_valid_solution(solution, make_project()) is False


def test_solution_with_overlap_is_rejected():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 50, 0, 100, 50),
        ]
    )

    assert is_valid_solution(solution, make_project()) is False


def test_solution_outside_constraints_is_rejected():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 150, 0, 100, 50),
        ]
    )

    assert is_valid_solution(solution, make_project()) is False
