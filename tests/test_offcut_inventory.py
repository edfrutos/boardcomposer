"""Promote offcuts to remnant stock (IDE-0025)."""

from boardcomposer import Board, Project, StockPanel
from boardcomposer.domain import (
    AssemblySolution,
    BoardPlacement,
    Offcut,
    PanelReference,
)
from boardcomposer.inventory.offcut_inventory import remnant_stock_from_offcuts


def _frozen_with_offcut() -> tuple[Project, AssemblySolution]:
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19, "P1", material="Melamina"))
    project.add_board(Board(400, 300, 19, "A", material="Melamina"))
    frozen = AssemblySolution(
        placements=[
            BoardPlacement(
                "A",
                0,
                0,
                400,
                300,
                panel_reference=PanelReference(0, 0),
            )
        ],
        offcuts=(
            Offcut(PanelReference(0, 0), 400, 0, 600, 500),
            Offcut(PanelReference(0, 0), 0, 300, 400, 200),
        ),
    )
    return project, frozen


def test_offcuts_become_remnant_stock_with_source_material():
    project, frozen = _frozen_with_offcut()

    remnants = remnant_stock_from_offcuts(project, frozen)

    assert [panel.id for panel in remnants] == ["P1-0-R1", "P1-0-R2"]
    assert remnants[0].length_mm == 600
    assert remnants[0].width_mm == 500
    assert remnants[0].thickness_mm == 19
    assert remnants[0].material == "Melamina"
    assert remnants[0].quantity == 1
    assert remnants[1].length_mm == 400
    assert remnants[1].width_mm == 200


def test_ids_are_stable_across_calls():
    project, frozen = _frozen_with_offcut()

    first = remnant_stock_from_offcuts(project, frozen)
    second = remnant_stock_from_offcuts(project, frozen)

    assert [panel.id for panel in first] == [panel.id for panel in second]


def test_empty_offcuts_yield_no_remnants():
    project, frozen = _frozen_with_offcut()
    empty = AssemblySolution(placements=frozen.placements)

    assert remnant_stock_from_offcuts(project, empty) == []


def test_unknown_panel_reference_is_skipped():
    project, frozen = _frozen_with_offcut()
    stray = AssemblySolution(
        placements=frozen.placements,
        offcuts=(Offcut(PanelReference(9, 0), 0, 0, 100, 100),),
    )

    assert remnant_stock_from_offcuts(project, stray) == []


def test_anonymous_stock_uses_panel_index_in_id():
    project = Project()
    project.add_stock_panel(StockPanel(1000, 500, 19))
    solution = AssemblySolution(
        placements=[],
        offcuts=(Offcut(PanelReference(0, 0), 0, 0, 200, 100),),
    )

    remnants = remnant_stock_from_offcuts(project, solution)

    assert remnants[0].id == "P1-0-R1"
