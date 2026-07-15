from boardcomposer import Board, Project, ProjectConstraints
from boardcomposer.solver.maxrects_generator import generate_maxrects_solution
from boardcomposer.solver.maxrects_search import (
    generate_beam_maxrects_solution,
    generate_best_maxrects_solution,
)
from boardcomposer.solver.solution_ranking import solution_ranking_key


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
    assert "maxrects" in solution.explanation.notes


def test_generate_maxrects_solution_records_selected_heuristic():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_maxrects_solution(project)

    assert "maxrects" in solution.explanation.notes
    assert any(
        name in solution.explanation.notes
        for name in [
            "best_area_fit",
            "best_short_side_fit",
            "best_long_side_fit",
            "best_bottom_left_fit",
        ]
    )


def test_generate_maxrects_solution_records_selected_ordering():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1000,
        )
    )
    project.add_board(Board(2000, 300, 20, "A"))
    project.add_board(Board(1000, 300, 20, "B"))

    solution = generate_maxrects_solution(project)

    assert any(
        name in solution.explanation.notes
        for name in ["original", "largest_area", "longest_edge"]
    )


def test_generate_maxrects_solution_can_select_beam_candidate():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1200,
            allow_rotation=True,
        )
    )

    for board in [
        Board(1800, 300, 19, "A"),
        Board(1200, 300, 19, "B"),
        Board(800, 200, 19, "C"),
        Board(700, 180, 19, "D"),
        Board(600, 250, 19, "E"),
        Board(500, 150, 19, "F"),
        Board(400, 120, 19, "G"),
    ]:
        project.add_board(board)

    solution = generate_maxrects_solution(project)

    assert len(solution.placements) == 7
    assert solution.waste_ratio <= 0.116


def test_generate_maxrects_solution_selects_best_available_candidate():
    """Beam search should outrank classic when both are available."""
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=3000,
            max_width_mm=1200,
            allow_rotation=True,
        )
    )

    for board in [
        Board(1800, 300, 19, "A"),
        Board(1200, 300, 19, "B"),
        Board(800, 200, 19, "C"),
        Board(700, 180, 19, "D"),
        Board(600, 250, 19, "E"),
        Board(500, 150, 19, "F"),
        Board(400, 120, 19, "G"),
    ]:
        project.add_board(board)

    classic = generate_best_maxrects_solution(project)
    beam = generate_beam_maxrects_solution(
        project,
        beam_width=2,
        candidate_width=None,
    )
    selected = generate_maxrects_solution(project)

    assert solution_ranking_key(selected) == max(
        solution_ranking_key(classic),
        solution_ranking_key(beam),
    )
