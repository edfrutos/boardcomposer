from studio.commands import EditProjectMetadataCommand
from studio.models import StudioProject
from studio.preferences import PreferencesManager
from studio.services import StudioServices


def test_edit_project_metadata_redo_and_undo(tmp_path):
    services = StudioServices(
        preferences=PreferencesManager(tmp_path / "preferences.json")
    )
    services.projects.new_project(
        StudioProject(project_id="PRJ-1", name="Cocina", client="A")
    )
    command = EditProjectMetadataCommand(
        services,
        old_client="A",
        old_reference="",
        old_notes="",
        new_client="Nordik",
        new_reference="PED-1",
        new_notes="Urgente",
    )
    services.commands.execute(command)
    project = services.projects.current_project
    assert project is not None
    assert project.client == "Nordik"
    assert project.reference == "PED-1"
    assert project.notes == "Urgente"

    services.commands.undo()
    assert project.client == "A"
    assert project.reference == ""
    assert project.notes == ""
