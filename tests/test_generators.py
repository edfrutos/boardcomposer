from boardcomposer import Board, Project
from boardcomposer.solver.generators import generators_by_name


def test_generators_by_name():
    project = Project()
    project.add_board(Board(2000, 300, 20, "A"))

    generators = generators_by_name(["horizontal", "vertical", "free_space"])
    solutions = []

    for generator in generators:
        solutions.extend(generator(project))

    layouts = {tuple(solution.explanation.notes) for solution in solutions}

    assert ("horizontal_permutation",) in layouts
    assert ("vertical_permutation",) in layouts
    assert ("free_space",) in layouts
