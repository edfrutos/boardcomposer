import json

from boardcomposer.domain import AssemblySolution, Project

from .base import Presenter
from boardcomposer.solver.strategies import OptimizationStrategy


def _panel_reference_to_dict(reference) -> dict | None:
    if reference is None:
        return None
    return {
        "stock_panel_index": reference.stock_panel_index,
        "instance_index": reference.instance_index,
    }


class JsonPresenter(Presenter):
    def render(
        self,
        project: Project,
        strategy: OptimizationStrategy | None,
        solutions: list[AssemblySolution],
        top: int,
    ) -> str:
        if strategy is None:
            raise ValueError("JsonPresenter requiere una estrategia")

        return json.dumps(
            {
                "input_boards": len(project.boards),
                "stock_panels": [
                    {
                        "id": panel.id,
                        "length_mm": panel.length_mm,
                        "width_mm": panel.width_mm,
                        "thickness_mm": panel.thickness_mm,
                        "quantity": panel.quantity,
                    }
                    for panel in project.stock_panels
                ],
                "strategy": strategy.name,
                "generators": list(strategy.generator_names),
                "top": top,
                "weights": {
                    "material_utilization": strategy.weights.material_utilization,
                    "placed_boards": strategy.weights.placed_boards,
                    "compactness": strategy.weights.compactness,
                    "rotation_penalty": strategy.weights.rotation_penalty,
                },
                "best_solution": {
                    "score": solutions[0].score.total,
                    "layout": solutions[0].explanation.notes,
                    "placed_boards": len(solutions[0].placements),
                    "total_length_mm": solutions[0].total_length_mm,
                    "total_width_mm": solutions[0].total_width_mm,
                    "omitted_boards": list(solutions[0].omitted_piece_ids),
                    "offcuts_area_mm2": solutions[0].total_offcut_area_mm2,
                },
                "solutions": [
                    {
                        "placed_boards": len(solution.placements),
                        "total_length_mm": solution.total_length_mm,
                        "total_width_mm": solution.total_width_mm,
                        "score": solution.score.total,
                        "layout": solution.explanation.notes,
                        "omitted_boards": list(solution.omitted_piece_ids),
                        "placements": [
                            {
                                "board_id": placement.board_id,
                                "x_mm": placement.x_mm,
                                "y_mm": placement.y_mm,
                                "length_mm": placement.length_mm,
                                "width_mm": placement.width_mm,
                                "rotated": placement.rotated,
                                "panel_reference": _panel_reference_to_dict(
                                    placement.panel_reference
                                ),
                            }
                            for placement in solution.placements
                        ],
                        "offcuts": [
                            {
                                "panel_reference": _panel_reference_to_dict(
                                    offcut.panel_reference
                                ),
                                "x_mm": offcut.x_mm,
                                "y_mm": offcut.y_mm,
                                "length_mm": offcut.length_mm,
                                "width_mm": offcut.width_mm,
                                "area_mm2": offcut.area_mm2,
                            }
                            for offcut in solution.offcuts
                        ],
                    }
                    for solution in solutions[:top]
                ],
            },
            indent=2,
        )


def solutions_to_json(
    project: Project,
    strategy: OptimizationStrategy,
    solutions: list[AssemblySolution],
    top: int,
) -> str:
    return JsonPresenter().render(project, strategy, solutions, top)
