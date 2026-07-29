"""Tests for shared export panel layout helpers."""

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
)
from boardcomposer.export.common import (
    PANEL_GAP_MM,
    canvas_size_mm,
    panel_offsets,
)


def _two_panel_project_and_solution() -> tuple[Project, AssemblySolution]:
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", quantity=2))
    project.add_board(Board(400, 300, 19, "A"))
    project.add_board(Board(400, 300, 19, "B"))

    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            ),
            BoardPlacement(
                "B",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 1),
            ),
        ]
    )
    return project, solution


def test_panel_offsets_empty_without_project():
    _, solution = _two_panel_project_and_solution()
    assert panel_offsets(solution, None) == {}


def test_panel_offsets_lays_panels_left_to_right_with_gap():
    project, solution = _two_panel_project_and_solution()
    offsets = panel_offsets(solution, project)

    first = PanelReference(0, 0)
    second = PanelReference(0, 1)
    assert offsets[first] == 0.0
    assert offsets[second] == 1000.0 + PANEL_GAP_MM


def test_canvas_size_mm_uses_offsets_when_project_present():
    project, solution = _two_panel_project_and_solution()
    offsets = panel_offsets(solution, project)

    width, height = canvas_size_mm(solution, project, offsets)
    assert width == 1000.0 + PANEL_GAP_MM + 1000.0
    assert height == 500.0


def test_canvas_size_mm_falls_back_to_solution_totals():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
    )
    width, height = canvas_size_mm(solution, None, {})
    assert width == solution.total_length_mm
    assert height == solution.total_width_mm
    assert width == 100.0
    assert height == 50.0
