from studio.commands import RenameProjectCommand
from studio.explorer_actions import explorer_context_actions
from studio.models import StudioProject
from studio.services import StudioServices


def test_explorer_project_root_offers_rename():
    assert explorer_context_actions("project:root") == ("rename",)


def test_rename_project_redo_and_undo():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(
            project_id="PRJ-1",
            name="Viejo",
            boards=[],
            pieces=[],
            placements=[],
        )
    )
    command = RenameProjectCommand(services, "Viejo", "Nuevo")

    command.redo()
    project = services.projects.current_project
    assert project is not None
    assert project.name == "Nuevo"

    command.undo()
    assert project.name == "Viejo"
