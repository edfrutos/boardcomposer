"""Tests for CSV and JSON solution exporters (SCR-007)."""

import csv
import io
import json

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.export import solution_to_csv, solution_to_json


def _solution() -> tuple[Project, AssemblySolution]:
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(1000, 500, 19, "P1", quantity=1, material="Melamina")
    )
    project.add_board(Board(400, 300, 19, "A"))

    solution = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                10,
                20,
                400,
                300,
                rotated=True,
                panel_reference=PanelReference(0, 0),
            )
        ],
        score=SolutionScore(waste_score=7.5),
        explanation=SolutionExplanation(notes=["test"], strengths=["compacta"]),
        omitted_piece_ids=("B",),
        offcuts=(Offcut(PanelReference(0, 0), 400, 0, 600, 300),),
    )
    return project, solution


def test_solution_to_json_includes_placements_and_metrics():
    project, solution = _solution()

    payload = json.loads(
        solution_to_json(
            solution,
            project,
            strategy_name="material",
            solution_index=0,
        )
    )

    assert payload["strategy"] == "material"
    assert payload["complete"] is False
    assert payload["omitted_piece_ids"] == ["B"]
    assert payload["placements"][0]["piece_id"] == "A"
    assert payload["placements"][0]["rotated"] is True
    assert payload["stock_panels"][0]["id"] == "P1"
    assert payload["metrics"]["placed_pieces"] == 1
    assert "panel_waste_ratio" in payload["metrics"]


def test_solution_to_json_works_without_project():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    payload = json.loads(solution_to_json(solution))

    assert "stock_panels" not in payload
    assert payload["placements"][0]["piece_id"] == "A"


def test_solution_to_csv_lists_placements():
    _project, solution = _solution()

    text = solution_to_csv(solution)
    rows = list(csv.DictReader(io.StringIO(text)))

    assert rows[0]["piece_id"] == "A"
    assert rows[0]["x_mm"] == "10"
    assert rows[0]["rotated"] == "true"
    assert rows[0]["stock_panel_index"] == "0"
    assert rows[0]["instance_index"] == "0"


def test_solution_to_csv_handles_missing_panel_reference():
    solution = AssemblySolution(
        placements=[BoardPlacement("A", 0, 0, 100, 50)],
        explanation=SolutionExplanation(),
    )

    rows = list(csv.DictReader(io.StringIO(solution_to_csv(solution))))

    assert rows[0]["stock_panel_index"] == ""
    assert rows[0]["instance_index"] == ""
