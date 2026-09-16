"""Estimated stock-sheet cost from catalog prices (IDE-0029)."""

import json

from boardcomposer import Board, Project, ProjectConstraints, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    PanelReference,
    SolutionExplanation,
    SolutionScore,
)
from boardcomposer.export import solution_to_json
from boardcomposer.inventory.material_cost import (
    MaterialCostEstimate,
    estimated_material_cost,
    normalize_price_map,
)
from studio.solution_highlights import solution_highlights
from studio.solution_ordering import SORT_LABELS, ordered_solution_indexes


def _project_with_panel(
    *,
    length_mm: float = 1000,
    width_mm: float = 500,
    material: str = "Melamina",
    quantity: int = 2,
) -> Project:
    project = Project(constraints=ProjectConstraints(allow_rotation=True))
    project.add_stock_panel(
        StockPanel(
            length_mm,
            width_mm,
            19,
            "P1",
            quantity=quantity,
            material=material,
        )
    )
    project.add_board(Board(400, 300, 19, "A"))
    return project


def _solution(*references: PanelReference) -> AssemblySolution:
    placements = [
        BoardPlacement(
            f"A{index}",
            0,
            0,
            400,
            300,
            panel_reference=reference,
        )
        for index, reference in enumerate(references)
    ]
    return AssemblySolution(
        placements=placements,
        score=SolutionScore(waste_score=5.0),
        explanation=SolutionExplanation(),
    )


def test_normalize_price_map_keeps_positive_casefolded_rates():
    cleaned = normalize_price_map(
        {
            " Melamina ": 25.5,
            "mdf": 0,
            "": 12,
            "Haya": "nope",
            "Roble": -3,
        }
    )
    assert cleaned == {"melamina": 25.5}


def test_estimated_material_cost_uses_consumed_panel_area():
    project = _project_with_panel()
    # One 1000×500 mm sheet = 0.5 m² × 25 €/m² = 12.50 €
    estimate = estimated_material_cost(
        _solution(PanelReference(0, 0)),
        project,
        {"melamina": 25},
    )
    assert estimate.total == 12.50
    assert estimate.priced_area_m2 == 0.5
    assert estimate.unpriced_area_m2 == 0.0
    assert estimate.missing_materials == ()
    assert estimate.has_price


def test_estimated_material_cost_counts_each_physical_instance():
    project = _project_with_panel()
    estimate = estimated_material_cost(
        _solution(PanelReference(0, 0), PanelReference(0, 1)),
        project,
        {"Melamina": 25},
    )
    assert estimate.total == 25.00
    assert estimate.priced_area_m2 == 1.0


def test_estimated_material_cost_skips_missing_panels_and_unpriced():
    project = _project_with_panel()
    project.add_stock_panel(StockPanel(800, 400, 19, "P2", quantity=1, material="MDF"))
    solution = _solution(
        PanelReference(0, 0),
        PanelReference(1, 0),
        PanelReference(9, 0),
    )
    estimate = estimated_material_cost(solution, project, {"melamina": 10})
    assert estimate.total == 5.00
    assert estimate.priced_area_m2 == 0.5
    assert estimate.unpriced_area_m2 == 0.32
    assert estimate.missing_materials == ("MDF",)
    assert estimate.has_price


def test_estimated_material_cost_without_prices_is_empty():
    project = _project_with_panel()
    estimate = estimated_material_cost(
        _solution(PanelReference(0, 0)),
        project,
        {},
    )
    assert estimate == MaterialCostEstimate(
        total=0.0,
        priced_area_m2=0.0,
        unpriced_area_m2=0.5,
        missing_materials=("Melamina",),
    )
    assert not estimate.has_price


def test_solution_to_json_adds_cost_metrics_only_with_price_map():
    project = _project_with_panel()
    solution = _solution(PanelReference(0, 0))

    bare = json.loads(solution_to_json(solution, project))
    assert "estimated_material_cost" not in bare["metrics"]

    priced = json.loads(
        solution_to_json(solution, project, material_prices={"Melamina": 25})
    )
    metrics = priced["metrics"]
    assert metrics["estimated_material_cost"] == 12.50
    assert metrics["priced_area_m2"] == 0.5
    assert metrics["unpriced_area_m2"] == 0.0
    assert metrics["missing_price_materials"] == []


def test_sort_labels_include_cost():
    keys = {key for key, _label in SORT_LABELS}
    assert keys == {
        "ranking",
        "pieces",
        "waste",
        "board_waste",
        "cost",
        "score",
    }


def test_sort_by_cost_puts_cheaper_first_and_unpriced_last():
    cheap = _solution(PanelReference(0, 0))
    pricey = _solution(PanelReference(0, 0), PanelReference(0, 1))
    unpriced = _solution(PanelReference(0, 0))
    costs = {id(cheap): 12.5, id(pricey): 25.0, id(unpriced): float("inf")}

    indexes = ordered_solution_indexes(
        [pricey, unpriced, cheap],
        sort_by="cost",
        material_cost=lambda solution: costs[id(solution)],
    )
    assert indexes == [2, 0, 1]


def test_highlights_flag_lower_cost_and_skip_when_all_unpriced():
    cheap = _solution(PanelReference(0, 0))
    pricey = _solution(PanelReference(0, 0), PanelReference(0, 1))

    highlights = solution_highlights(
        [pricey, cheap],
        material_cost=lambda solution: 25.0 if solution is pricey else 12.5,
    )
    assert "highlight.cost" in highlights[1]
    assert "highlight.cost" not in highlights.get(0, [])

    skipped = solution_highlights(
        [cheap, pricey],
        material_cost=lambda _solution: float("inf"),
    )
    assert "highlight.cost" not in skipped.get(0, [])
    assert "highlight.cost" not in skipped.get(1, [])
