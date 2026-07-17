"""Export an `AssemblySolution` as a structured JSON document."""

from __future__ import annotations

import json

from boardcomposer.domain import AssemblySolution, Project


def _panel_reference_to_dict(reference) -> dict | None:
    if reference is None:
        return None
    return {
        "stock_panel_index": reference.stock_panel_index,
        "instance_index": reference.instance_index,
    }


def solution_to_dict(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    strategy_name: str | None = None,
    solution_index: int | None = None,
) -> dict:
    """Return a JSON-serializable dict for one solution."""
    payload: dict = {
        "solution_index": solution_index,
        "strategy": strategy_name,
        "complete": solution.is_complete,
        "score": solution.score.total,
        "metrics": {
            "placed_pieces": len(solution.placements),
            "omitted_pieces": len(solution.omitted_piece_ids),
            "total_length_mm": solution.total_length_mm,
            "total_width_mm": solution.total_width_mm,
            "waste_ratio": solution.waste_ratio,
            "used_area_mm2": solution.used_area_mm2,
            "offcut_area_mm2": solution.total_offcut_area_mm2,
            "panels_used": len(solution.panel_references),
        },
        "notes": list(solution.explanation.notes),
        "strengths": list(solution.explanation.strengths),
        "weaknesses": list(solution.explanation.weaknesses),
        "omitted_piece_ids": list(solution.omitted_piece_ids),
        "placements": [
            {
                "piece_id": placement.board_id,
                "x_mm": placement.x_mm,
                "y_mm": placement.y_mm,
                "length_mm": placement.length_mm,
                "width_mm": placement.width_mm,
                "rotated": placement.rotated,
                "panel_reference": _panel_reference_to_dict(placement.panel_reference),
            }
            for placement in solution.placements
        ],
        "offcuts": [
            {
                "panel_reference": _panel_reference_to_dict(offcut.panel_reference),
                "x_mm": offcut.x_mm,
                "y_mm": offcut.y_mm,
                "length_mm": offcut.length_mm,
                "width_mm": offcut.width_mm,
                "area_mm2": offcut.area_mm2,
            }
            for offcut in solution.offcuts
        ],
    }

    if project is not None:
        payload["stock_panels"] = [
            {
                "id": panel.id,
                "length_mm": panel.length_mm,
                "width_mm": panel.width_mm,
                "thickness_mm": panel.thickness_mm,
                "quantity": panel.quantity,
                "material": panel.material,
            }
            for panel in project.stock_panels
        ]
        if solution.panel_references:
            payload["metrics"]["panel_waste_ratio"] = solution.panel_waste_ratio(
                project
            )

    return payload


def solution_to_json(
    solution: AssemblySolution,
    project: Project | None = None,
    *,
    strategy_name: str | None = None,
    solution_index: int | None = None,
) -> str:
    """Serialize one solution to indented JSON text."""
    return (
        json.dumps(
            solution_to_dict(
                solution,
                project,
                strategy_name=strategy_name,
                solution_index=solution_index,
            ),
            indent=2,
            ensure_ascii=False,
        )
        + "\n"
    )
