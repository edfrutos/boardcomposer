from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.geometry.collision import placements_overlap
from boardcomposer.layout.kerf import (
    aabb_overlap_with_kerf,
    deflate_placement,
    inflate_project_for_kerf,
    normalize_kerf,
)
from boardcomposer.domain import BoardPlacement
from boardcomposer.solver.geometry_solver import GeometrySolver
from studio.commands import EditProjectKerfCommand
from studio.models import StudioProject
from studio.services import StudioServices


def test_normalize_kerf_clamps_and_rejects_junk():
    assert normalize_kerf(-1) == 0
    assert normalize_kerf("nope") == 0
    assert normalize_kerf(3.2) == 3.2
    assert normalize_kerf(99) == 50


def test_inflate_project_grows_pieces_and_panels():
    project = Project(
        constraints=ProjectConstraints(kerf_mm=3, max_length_mm=1000, max_width_mm=500)
    )
    project.add_stock_panel(StockPanel(1000, 500, 19, id="P1"))
    project.add_board(Board(100, 50, 19, id="A"))
    inflated = inflate_project_for_kerf(project)
    assert inflated.stock_panels[0].length_mm == 1003
    assert inflated.boards[0].length_mm == 103
    assert inflated.constraints.max_length_mm == 1003


def test_deflate_placement_restores_actual_size():
    placement = BoardPlacement("A", 0, 0, 103, 53)
    restored = deflate_placement(placement, 3)
    assert (restored.length_mm, restored.width_mm) == (100, 50)


def test_aabb_kerf_treats_flush_as_overlap_and_gap_as_ok():
    assert aabb_overlap_with_kerf(0, 0, 100, 50, 100, 0, 100, 50, 3)
    assert not aabb_overlap_with_kerf(0, 0, 100, 50, 103, 0, 100, 50, 3)


def test_placements_overlap_respects_kerf():
    left = BoardPlacement("A", 0, 0, 100, 50)
    right = BoardPlacement("B", 100, 0, 100, 50)
    assert placements_overlap(left, right) is False
    assert placements_overlap(left, right, kerf_mm=3) is True


def test_solver_leaves_kerf_gap_between_two_pieces():
    project = Project(constraints=ProjectConstraints(kerf_mm=10, allow_rotation=False))
    project.add_stock_panel(StockPanel(250, 100, 19, id="P1", quantity=1))
    project.add_board(Board(100, 80, 19, id="A"))
    project.add_board(Board(100, 80, 19, id="B"))
    solutions = GeometrySolver(project).solve()
    assert solutions
    xs = sorted(placement.x_mm for placement in solutions[0].placements)
    ys = sorted(placement.y_mm for placement in solutions[0].placements)
    assert xs[1] - xs[0] >= 110 or ys[1] - ys[0] >= 90
    for placement in solutions[0].placements:
        assert placement.length_mm == 100
        assert placement.width_mm == 80


def test_edit_project_kerf_undo():
    services = StudioServices()
    services.projects.new_project(
        StudioProject(project_id="PRJ-1", name="Kerf", kerf_mm=0)
    )
    command = EditProjectKerfCommand(services, 0, 4)
    services.commands.execute(command)
    assert services.projects.current_project.kerf_mm == 4
    services.commands.undo()
    assert services.projects.current_project.kerf_mm == 0


def test_constraints_reject_negative_kerf():
    import pytest
    from boardcomposer import ProjectConstraints

    with pytest.raises(ValueError):
        ProjectConstraints(kerf_mm=-0.1)
