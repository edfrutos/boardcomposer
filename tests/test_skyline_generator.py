from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.skyline_generator import generate_skyline_solution


def test_generate_skyline_solution():
    project = Project(
        constraints=ProjectConstraints(
            max_width_mm=3000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_skyline_solution(project)

    assert len(solution.placements) == 2
    assert solution.explanation.notes == ["skyline"]
