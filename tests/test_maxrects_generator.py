from boardcomposer import (
    Board,
    PanelReference,
    Project,
    ProjectConstraints,
    StockPanel,
)
from boardcomposer.solver.maxrects_generator import generate_maxrects_solution
from boardcomposer.solver.maxrects_search import (
    generate_beam_maxrects_solution,
    generate_best_maxrects_solution,
)
from boardcomposer.solver.solution_ranking import solution_ranking_key
from boardcomposer.solver.solution_validator import validate_solution


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


def test_maxrects_uses_stock_panel_dimensions():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=5000,
            max_width_mm=5000,
        )
    )
    project.add_stock_panel(
        StockPanel(
            length_mm=1000,
            width_mm=500,
            thickness_mm=19,
            id="P1",
        )
    )
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    solution = generate_maxrects_solution(project)

    assert len(solution.placements) == 1
    assert solution.total_length_mm <= 1000
    assert solution.total_width_mm <= 500


def test_maxrects_keeps_constraints_fallback_without_stock_panels():
    project = Project(
        constraints=ProjectConstraints(
            max_length_mm=2000,
            max_width_mm=500,
        )
    )
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    solution = generate_maxrects_solution(project)

    assert len(solution.placements) == 2


def test_maxrects_uses_each_physical_panel_from_quantity():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    solution = generate_maxrects_solution(project)

    assert {placement.board_id for placement in solution.placements} == {"A", "B"}
    assert {placement.panel_reference for placement in solution.placements} == {
        PanelReference(0, 0),
        PanelReference(0, 1),
    }


def test_maxrects_routes_piece_to_thickness_compatible_panel():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P19"))
    project.add_stock_panel(StockPanel(1000, 500, 18, "P18"))
    project.add_board(Board(900, 400, 18, "A"))

    solution = generate_maxrects_solution(project)

    assert solution.placements[0].panel_reference == PanelReference(1, 0)


def test_maxrects_reports_partial_solution_when_inventory_is_insufficient():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    solution = generate_maxrects_solution(project)
    result = validate_solution(solution, project)

    assert len(solution.placements) == 1
    assert result.complete is False


def test_maxrects_routes_piece_to_material_compatible_panel():
    project = Project()
    project.add_stock_panel(
        StockPanel(1000, 500, 19, "MEL", material="Melamina blanca")
    )
    project.add_stock_panel(
        StockPanel(1000, 500, 19, "CONTRA", material="Contrachapado")
    )
    project.add_board(Board(900, 400, 19, "A", material="Contrachapado"))

    solution = generate_maxrects_solution(project)

    assert solution.placements[0].panel_reference == PanelReference(1, 0)


def test_maxrects_tries_multiple_panel_orderings_to_reduce_waste():
    """A piece that fits both panels should end up on the smaller one when
    that leaves less waste, provided the search explores panel orderings."""
    project = Project()
    project.add_stock_panel(StockPanel(2440, 1220, 19, "GRANDE"))
    project.add_stock_panel(StockPanel(700, 700, 19, "PEQUENO"))
    project.add_board(Board(600, 600, 19, "A"))

    solution = generate_maxrects_solution(project)

    assert solution.placements[0].panel_reference == PanelReference(1, 0)


def test_maxrects_reports_offcuts_for_consumed_panels():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    project.add_board(Board(400, 400, 19, "A"))

    solution = generate_maxrects_solution(project)

    assert solution.offcuts
    assert all(
        offcut.panel_reference == PanelReference(0, 0) for offcut in solution.offcuts
    )
    assert solution.total_offcut_area_mm2 > 0


def test_maxrects_drops_offcuts_smaller_than_the_reuse_threshold():
    project = Project()
    project.add_stock_panel(StockPanel(410, 410, 19, "P1"))
    project.add_board(Board(400, 400, 19, "A"))

    solution = generate_maxrects_solution(project)

    assert solution.offcuts == ()


def test_maxrects_reports_no_offcuts_for_an_unconsumed_panel():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    project.add_board(Board(2000, 2000, 19, "TOO_BIG"))

    solution = generate_maxrects_solution(project)

    assert solution.offcuts == ()
