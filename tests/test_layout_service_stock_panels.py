from boardcomposer import AssemblySolution, BoardPlacement, PanelReference

from studio.models import StudioBoard, StudioPiece, StudioProject
from studio.services import StudioServices


def test_layout_service_maps_studio_boards_to_core_stock_panels():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Multipanel",
            boards=[
                StudioBoard("P19", 1000, 500, "Melamina", 19, 2),
                StudioBoard("P18", 800, 400, "MDF", 18, 1),
            ],
            pieces=[StudioPiece("A", 900, 400, "Melamina", 19)],
        )
    )

    core_project = services.layout.to_core_project()

    assert core_project is not None
    assert [panel.id for panel in core_project.stock_panels] == ["P19", "P18"]
    assert [panel.quantity for panel in core_project.stock_panels] == [2, 1]
    assert core_project.boards[0].thickness_mm == 19
    assert [panel.material for panel in core_project.stock_panels] == [
        "Melamina",
        "MDF",
    ]
    assert core_project.boards[0].material == "Melamina"


def test_layout_service_applies_physical_panel_assignment_to_studio():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Multipanel",
            boards=[
                StudioBoard("P19", 1000, 500, "Melamina", 19),
                StudioBoard("P18", 800, 400, "MDF", 18),
            ],
            pieces=[StudioPiece("A", 700, 300, "MDF", 18)],
        )
    )
    services.layout.solutions = [
        AssemblySolution(
            placements=[
                BoardPlacement(
                    "A",
                    10,
                    20,
                    700,
                    300,
                    panel_reference=PanelReference(1, 0),
                )
            ]
        )
    ]

    applied = services.layout.apply_last_solution_to_current_project()

    assert applied is True
    placement = services.projects.current_project.placements[0]
    assert placement.board_id == "P18"
    assert placement.board_instance == 0
    assert placement.stock_panel_index == 1


def test_layout_service_returns_partial_solution_when_a_piece_has_wrong_material():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Materiales",
            boards=[StudioBoard("P1", 1000, 500, "Melamina blanca", 19)],
            pieces=[
                StudioPiece("A", 400, 300, "Melamina blanca", 19),
                StudioPiece("B", 400, 300, "Contrachapado", 19),
            ],
        )
    )

    solution = services.layout.solve_current_project()

    assert solution is not None
    assert solution.omitted_piece_ids == ("B",)


def test_layout_service_reports_a_fully_omitted_partial_solution_when_nothing_fits():
    """When no piece fits anywhere, Studio still gets a (fully partial)
    solution back instead of nothing, so it can show a useful diagnosis
    rather than a bare 'no solution' message."""
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Sin solución",
            boards=[StudioBoard("P1", 100, 100, "Melamina", 19)],
            pieces=[StudioPiece("A", 900, 900, "Melamina", 19)],
        )
    )

    solution = services.layout.solve_current_project()

    assert solution is not None
    assert solution.omitted_piece_ids == ("A",)
    assert services.layout.stats.generated > 0


def test_layout_service_reports_waste_across_consumed_panels():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Multipanel",
            boards=[StudioBoard("P1", 1000, 500, "Melamina", 19, 2)],
            pieces=[
                StudioPiece("A", 900, 400, "Melamina", 19),
                StudioPiece("B", 900, 400, "Melamina", 19),
            ],
        )
    )

    solution = services.layout.solve_current_project()

    assert solution is not None
    assert services.layout.board_waste_ratio(solution) == 0.28
