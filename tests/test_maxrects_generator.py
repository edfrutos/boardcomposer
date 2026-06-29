from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_generator import generate_maxrects_solution


def test_generate_maxrects_solution():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_maxrects_solution(project)

    assert len(solution.placements) == 2
    assert solution.explanation.notes == ["maxrects"]
