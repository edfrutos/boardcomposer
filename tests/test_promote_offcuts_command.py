from boardcomposer.domain import AssemblySolution, Offcut, PanelReference
from studio.commands import PromoteOffcutsCommand
from studio.models import StudioBoard, StudioProject
from studio.offcut_inventory import remnant_studio_boards
from studio.services import StudioServices


def _services() -> StudioServices:
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Retales",
            boards=[StudioBoard("P1", 1000, 500, "Melamina", 19, 1)],
        )
    )
    return services


def test_promote_offcuts_redo_undo_and_idempotent():
    from boardcomposer import Project, StockPanel

    services = _services()
    project = services.projects.current_project
    assert project is not None
    core = Project()
    core.add_stock_panel(StockPanel(1000, 500, 19, "P1", material="Melamina"))
    solution = AssemblySolution(
        placements=[],
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 500),),
    )
    boards = remnant_studio_boards(core, solution, {"P1"})
    command = PromoteOffcutsCommand(services, boards)

    command.redo()
    assert [board.board_id for board in project.boards] == ["P1", "P1-0-R1"]
    remnant = project.boards[1]
    assert remnant.remnant is True
    assert remnant.length_mm == 600
    assert remnant.material == "Melamina"

    command.undo()
    assert [board.board_id for board in project.boards] == ["P1"]

    command.redo()
    again = remnant_studio_boards(
        core, solution, {board.board_id for board in project.boards}
    )
    assert again == []
