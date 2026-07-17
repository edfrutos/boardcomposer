"""Tests for named project templates (SCR-001 / SCR-005)."""

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_templates import (
    ProjectTemplatesManager,
    slugify_template_name,
)
from studio.welcome_screen import WelcomeScreen


def _sample_project() -> StudioProject:
    return StudioProject(
        project_id="PRJ-1",
        name="Cocina cliente",
        boards=[StudioBoard("TAB-1", 2800, 1200, "Melamina", 19, 2)],
        pieces=[
            StudioPiece("P-1", 600, 400),
            StudioPiece("P-2", 800, 300),
        ],
        placements=[StudioPlacement("P-1", 10, 20)],
    )


def test_slugify_template_name():
    assert slugify_template_name(" Cocina / Acme ") == "cocina-acme"
    assert slugify_template_name("@@@") == "plantilla"


def test_save_and_instantiate_clears_placements_by_default(tmp_path):
    manager = ProjectTemplatesManager(directory=tmp_path, autoload=False)
    manager.save_from_project("Cocina", _sample_project())

    assert len(manager.list()) == 1
    assert manager.list()[0].name == "Cocina"
    assert manager.list()[0].board_count == 1
    assert manager.list()[0].piece_count == 2

    project = manager.instantiate("Cocina")
    assert project.name == "Cocina"
    assert project.project_id != "PRJ-1"
    assert len(project.boards) == 1
    assert len(project.pieces) == 2
    assert project.placements == []


def test_save_can_include_placements(tmp_path):
    manager = ProjectTemplatesManager(directory=tmp_path, autoload=False)
    manager.save_from_project(
        "Con layout",
        _sample_project(),
        include_placements=True,
    )
    project = manager.instantiate("Con layout", include_placements=True)
    assert len(project.placements) == 1


def test_replace_same_name_updates_file(tmp_path):
    manager = ProjectTemplatesManager(directory=tmp_path, autoload=False)
    manager.save_from_project("Demo", _sample_project())
    updated = _sample_project()
    updated.pieces.append(StudioPiece("P-3", 100, 100))
    manager.save_from_project("Demo", updated)

    assert len(manager.list()) == 1
    assert manager.list()[0].piece_count == 3


def test_delete_template(tmp_path):
    manager = ProjectTemplatesManager(directory=tmp_path, autoload=False)
    manager.save_from_project("X", _sample_project())
    assert manager.delete("X") is True
    assert manager.list() == []
    assert manager.delete("X") is False


def test_welcome_has_from_template_button(qapp):
    del qapp
    screen = WelcomeScreen()
    screen.apply_language("en")
    assert screen.template_button.text() == "From template…"
