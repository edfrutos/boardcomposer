"""Tests for Studio project preview thumbnails (SCR-001)."""

from PySide6.QtCore import QSize

from studio.models import StudioBoard, StudioPiece, StudioPlacement, StudioProject
from studio.project_serializer import save_project
from studio.project_thumbnail import (
    project_file_thumbnail,
    studio_project_to_svg,
    studio_to_assembly_solution,
)
from studio.welcome_screen import WelcomeScreen


def _sample_project() -> StudioProject:
    return StudioProject(
        "demo",
        "Demo",
        boards=[StudioBoard("P1", 1000, 500, "Demo", 19, 1)],
        pieces=[StudioPiece("A", 400, 300, "Demo", 19)],
        placements=[StudioPlacement("A", 10, 20, False, 0, "P1", 0, 0)],
    )


def test_studio_project_to_svg_renders_placed_pieces():
    svg = studio_project_to_svg(_sample_project())

    assert svg is not None
    assert "P1" in svg
    assert 'width="400"' in svg
    assert ">A</text>" in svg


def test_studio_project_to_svg_draws_empty_boards():
    project = StudioProject(
        "empty",
        "Empty",
        boards=[StudioBoard("P1", 800, 400, "Demo", 19, 2)],
    )

    svg = studio_project_to_svg(project)

    assert svg is not None
    assert "P1 ×2" in svg
    assert 'width="800"' in svg or "800" in svg


def test_studio_project_to_svg_returns_none_for_blank_project():
    assert studio_project_to_svg(StudioProject("blank", "Blank")) is None


def test_studio_to_assembly_solution_swaps_dims_when_rotated():
    project = StudioProject(
        "rot",
        "Rot",
        boards=[StudioBoard("P1", 1000, 500)],
        pieces=[StudioPiece("A", 400, 200)],
        placements=[StudioPlacement("A", 0, 0, True, 90, "P1", 0, 0)],
    )

    solution = studio_to_assembly_solution(project)

    assert len(solution.placements) == 1
    assert solution.placements[0].length_mm == 200
    assert solution.placements[0].width_mm == 400
    assert solution.placements[0].rotated is True


def test_project_file_thumbnail_produces_pixmap(qapp, tmp_path):
    del qapp
    path = tmp_path / "demo.bcproj"
    save_project(_sample_project(), path)

    pixmap = project_file_thumbnail(path, box=QSize(120, 72))

    assert pixmap is not None
    assert not pixmap.isNull()
    assert pixmap.width() > 0
    assert pixmap.height() > 0


def test_project_file_thumbnail_returns_none_for_corrupt_file(qapp, tmp_path):
    del qapp
    path = tmp_path / "broken.bcproj"
    path.write_text("{not-json", encoding="utf-8")

    assert project_file_thumbnail(path) is None


def test_welcome_screen_shows_thumbnail_icon(qapp, tmp_path):
    del qapp
    path = tmp_path / "cocina.bcproj"
    save_project(_sample_project(), path)

    screen = WelcomeScreen()
    screen.set_recent_files([str(path)])

    item = screen.recent_list.item(0)
    assert item is not None
    assert "cocina.bcproj" in item.text()
    assert not item.icon().isNull()
