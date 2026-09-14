from boardcomposer import Board, PanelReference, Project, ProjectConstraints, StockPanel
from boardcomposer.solver.candidate_pipeline import CandidatePipeline
from boardcomposer.solver.skyline.skyline import Skyline
from boardcomposer.solver.skyline_generator import generate_skyline_solution
from boardcomposer.solver.solution_validator import validate_solution
from boardcomposer.solver.strategies import balanced_strategy


def test_skyline_rejects_placement_above_max_height():
    skyline = Skyline(width_mm=1000, max_height_mm=300)

    assert skyline.place(1000, 300) is not None
    assert skyline.place(100, 50) is None


def test_skyline_uses_each_physical_panel_from_quantity():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    solution = generate_skyline_solution(project)

    assert {placement.board_id for placement in solution.placements} == {"A", "B"}
    assert {placement.panel_reference for placement in solution.placements} == {
        PanelReference(0, 0),
        PanelReference(0, 1),
    }
    assert "skyline" in solution.explanation.notes
    assert "multi_panel" in solution.explanation.notes


def test_skyline_routes_piece_to_thickness_compatible_panel():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P19"))
    project.add_stock_panel(StockPanel(1000, 500, 18, "P18"))
    project.add_board(Board(900, 400, 18, "A"))

    solution = generate_skyline_solution(project)

    assert solution.placements[0].panel_reference == PanelReference(1, 0)


def test_skyline_reports_partial_solution_when_inventory_is_insufficient():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1"))
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    solution = generate_skyline_solution(project)
    result = validate_solution(solution, project)

    assert len(solution.placements) == 1
    assert result.complete is False


def test_skyline_routes_piece_to_material_compatible_panel():
    project = Project()
    project.add_stock_panel(
        StockPanel(1000, 500, 19, "MEL", material="Melamina blanca")
    )
    project.add_stock_panel(
        StockPanel(1000, 500, 19, "CONTRA", material="Contrachapado")
    )
    project.add_board(Board(900, 400, 19, "A", material="Contrachapado"))

    solution = generate_skyline_solution(project)

    assert solution.placements[0].panel_reference == PanelReference(1, 0)


def test_skyline_tries_multiple_panel_orderings_to_reduce_waste():
    project = Project()
    project.add_stock_panel(StockPanel(2440, 1220, 19, "GRANDE"))
    project.add_stock_panel(StockPanel(700, 700, 19, "PEQUENO"))
    project.add_board(Board(600, 600, 19, "A"))

    solution = generate_skyline_solution(project)

    assert solution.placements[0].panel_reference == PanelReference(1, 0)


def test_skyline_reports_offcuts_for_consumed_panels():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    project.add_board(Board(400, 400, 19, "A"))

    solution = generate_skyline_solution(project)

    assert solution.offcuts
    assert all(
        offcut.panel_reference == PanelReference(0, 0) for offcut in solution.offcuts
    )
    assert solution.total_offcut_area_mm2 > 0


def test_skyline_drops_offcuts_smaller_than_the_reuse_threshold():
    project = Project()
    project.add_stock_panel(StockPanel(410, 410, 19, "P1"))
    project.add_board(Board(400, 400, 19, "A"))

    solution = generate_skyline_solution(project)

    assert solution.offcuts == ()


def test_skyline_reports_no_offcuts_for_an_unconsumed_panel():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 1000, 19, "P1"))
    project.add_board(Board(2000, 2000, 19, "TOO_BIG"))

    solution = generate_skyline_solution(project)

    assert solution.offcuts == ()


def test_skyline_does_not_rotate_locked_grain_on_stock_panel():
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(StockPanel(100, 250, 19, "P1", quantity=1))
    project.add_board(Board(200, 50, 19, "A", grain="locked"))

    solution = generate_skyline_solution(project)

    assert all(not item.rotated for item in solution.placements)
    assert solution.placements == []


def test_skyline_rotates_free_grain_to_fit_stock_panel():
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(StockPanel(100, 250, 19, "P1", quantity=1))
    project.add_board(Board(200, 50, 19, "A"))

    solution = generate_skyline_solution(project)

    assert solution.placements
    assert solution.placements[0].rotated is True


def test_pipeline_runs_skyline_when_multiple_panels():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    project.add_board(Board(900, 400, 19, "A"))
    project.add_board(Board(900, 400, 19, "B"))

    pipeline = CandidatePipeline(project, balanced_strategy())
    solutions = pipeline.run()

    assert pipeline.trace.algorithms() == ("maxrects", "skyline")
    assert solutions
    assert {placement.board_id for placement in solutions[0].placements} == {"A", "B"}
