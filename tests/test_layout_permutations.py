from boardcomposer import Board, Project
from boardcomposer.solver.layout_generator import generate_horizontal_permutations


def test_generate_horizontal_permutations():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solutions = generate_horizontal_permutations(project)

    assert len(solutions) == 2
    assert {s.placements[0].board_id for s in solutions} == {"A", "B"}
