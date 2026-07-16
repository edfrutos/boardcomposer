from boardcomposer import (
    AssemblySolution,
    Board,
    BoardPlacement,
    PanelReference,
    Project,
    ProjectConstraints,
    StockPanel,
)
from boardcomposer.solver.solution_validator import validate_solution
from boardcomposer.solver.validation_result import ValidationReason


def test_same_coordinates_on_different_physical_panels_do_not_overlap():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1", quantity=2))
    project.add_board(Board(100, 100, 19, "A"))
    project.add_board(Board(100, 100, 19, "B"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement("A", 0, 0, 100, 100, panel_reference=PanelReference(0, 0)),
            BoardPlacement("B", 0, 0, 100, 100, panel_reference=PanelReference(0, 1)),
        ]
    )

    result = validate_solution(solution, project)

    assert result.valid is True
    assert result.complete is True


def test_stock_panel_project_rejects_unassigned_placement():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1"))
    project.add_board(Board(50, 50, 19, "A"))
    solution = AssemblySolution(placements=[BoardPlacement("A", 0, 0, 50, 50)])

    result = validate_solution(solution, project)

    assert ValidationReason.UNASSIGNED_STOCK_PANEL in result.reasons


def test_stock_panel_project_rejects_unknown_panel_reference():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1"))
    project.add_board(Board(50, 50, 19, "A"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                50,
                50,
                panel_reference=PanelReference(0, 1),
            )
        ]
    )

    result = validate_solution(solution, project)

    assert ValidationReason.UNKNOWN_STOCK_PANEL in result.reasons


def test_stock_panel_project_rejects_placement_outside_its_panel():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1"))
    project.add_board(Board(50, 50, 19, "A"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                60,
                0,
                50,
                50,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )

    result = validate_solution(solution, project)

    assert ValidationReason.EXCEEDS_STOCK_PANEL in result.reasons


def test_stock_panel_project_rejects_thickness_mismatch():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1"))
    project.add_board(Board(50, 50, 18, "A"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                50,
                50,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )

    result = validate_solution(solution, project)

    assert ValidationReason.PANEL_THICKNESS_MISMATCH in result.reasons


def test_stock_panel_project_rejects_material_mismatch():
    project = Project()
    project.add_stock_panel(StockPanel(100, 100, 19, "P1", material="Melamina blanca"))
    project.add_board(Board(50, 50, 19, "A", material="Contrachapado"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                50,
                50,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )

    result = validate_solution(solution, project)

    assert ValidationReason.PANEL_MATERIAL_MISMATCH in result.reasons


def test_stock_panel_project_accepts_case_and_whitespace_insensitive_material():
    project = Project()
    project.add_stock_panel(
        StockPanel(100, 100, 19, "P1", material="Melamina Blanca")
    )
    project.add_board(Board(50, 50, 19, "A", material="  melamina blanca  "))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                50,
                50,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )

    result = validate_solution(solution, project)

    assert ValidationReason.PANEL_MATERIAL_MISMATCH not in result.reasons


def test_stock_panel_dimensions_replace_legacy_global_size_constraints():
    project = Project(constraints=ProjectConstraints(max_length_mm=50, max_width_mm=50))
    project.add_stock_panel(StockPanel(100, 100, 19, "P1"))
    project.add_board(Board(100, 100, 19, "A"))
    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                100,
                100,
                panel_reference=PanelReference(0, 0),
            )
        ]
    )

    result = validate_solution(solution, project)

    assert result.valid is True
    assert ValidationReason.EXCEEDS_CONSTRAINTS not in result.reasons
