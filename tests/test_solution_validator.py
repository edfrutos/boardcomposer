from boardcomposer import AssemblySolution, BoardPlacement, ProjectConstraints
from boardcomposer.solver.solution_validator import is_valid_solution


def test_valid_solution_is_accepted():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 100, 0, 100, 50),
        ]
    )
    constraints = ProjectConstraints(max_length_mm=200, max_width_mm=50)

    assert is_valid_solution(solution, constraints) is True


def test_solution_with_overlap_is_rejected():
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 50),
            BoardPlacement("B", 50, 0, 100, 50),
        ]
    )
    constraints = ProjectConstraints(max_length_mm=200, max_width_mm=50)

    assert is_valid_solution(solution, constraints) is False


def test_solution_exceeding_length_is_rejected():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 250, 50)])
    constraints = ProjectConstraints(max_length_mm=200, max_width_mm=50)

    assert is_valid_solution(solution, constraints) is False


def test_solution_exceeding_width_is_rejected():
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 100, 75)])
    constraints = ProjectConstraints(max_length_mm=200, max_width_mm=50)

    assert is_valid_solution(solution, constraints) is False
